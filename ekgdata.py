import json
import pandas as pd
import plotly.express as px

class EKG_Test:
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.result_link = ekg_dict["result_link"]

        # CSV laden
        self.df = pd.read_csv(
            self.result_link,
            sep="\t",
            header=None,
            names=["Messwerte in mV", "Zeit in ms"]
        )

        # Auf 5000 Werte begrenzen
        self.df = self.df.iloc[:5000]

        self.peaks = None
        self.heart_rate = None

    @classmethod
    def load_by_id(cls, test_id, json_path="data/person_db.json"):
        with open(json_path, "r") as file:
            person_data = json.load(file)

        for person in person_data:
            if "ekg_tests" in person:
                for ekg_dict in person["ekg_tests"]:
                    if ekg_dict.get("id") == test_id:
                        print(f"Test mit ID {test_id} gefunden!")
                        return cls(ekg_dict)

        raise ValueError(f"EKG-Test mit ID {test_id} wurde nicht gefunden.")

    # ---------------------------------------------------------
    # PEAK-ERKENNUNG
    # ---------------------------------------------------------
    def find_peaks(self):
        df = self.df.copy()

        window_ms = 150          # kleinere Fenstergröße = bessere Peak-Position
        refractory_ms = 250      # kein Peak schneller als 250 ms
        amplitude_threshold = 350  # Option A: feste Schwelle

        df["is_peak"] = False

        t_min = df["Zeit in ms"].min()
        t_max = df["Zeit in ms"].max()

        peaks = []
        last_peak_time = None

        t = t_min
        while t < t_max:
            block = df[(df["Zeit in ms"] >= t) & (df["Zeit in ms"] < t + window_ms)]

            if len(block) > 0:
                block_max = block["Messwerte in mV"].max()

                if block_max > amplitude_threshold:
                    idx = block["Messwerte in mV"].idxmax()
                    peak_time = df.loc[idx, "Zeit in ms"]

                    if last_peak_time is None or (peak_time - last_peak_time) > refractory_ms:
                        peaks.append(idx)
                        last_peak_time = peak_time

            t += window_ms

        df.loc[:, "is_peak"] = False
        df.loc[peaks, "is_peak"] = True

        self.df = df
        self.peaks = df[df["is_peak"]]

        print(f"{len(self.peaks)} Peaks > {amplitude_threshold} mV gefunden.")

    # ---------------------------------------------------------
    # HERZFREQUENZ
    # ---------------------------------------------------------
    def estimate_hr(self):
        if self.peaks is None or len(self.peaks) < 2:
            print("Zu wenige Peaks – bitte zuerst find_peaks() ausführen.")
            self.heart_rate = None
            return None

        df = self.df

        anzahl_peaks = df["is_peak"].sum()

        dt_ms = df["Zeit in ms"].iloc[-1] - df["Zeit in ms"].iloc[0]
        dt_min = dt_ms / 60000

        self.heart_rate = anzahl_peaks / dt_min
        print(f"Geschätzte Herzfrequenz: {self.heart_rate:.2f} BPM")

        return self.heart_rate

    # ---------------------------------------------------------
    # STREAMLIT-PLOT
    # ---------------------------------------------------------
    def plot_time_series(self, n_points=2000):
        df_plot = self.df.iloc[:n_points]

        fig = px.line(
            df_plot,
            x="Zeit in ms",
            y="Messwerte in mV",
            title=f"EKG-Test ID: {self.id}"
        )

        if self.peaks is not None and not self.peaks.empty:
            t_min = df_plot["Zeit in ms"].min()
            t_max = df_plot["Zeit in ms"].max()

            visible_peaks = self.peaks[
                (self.peaks["Zeit in ms"] >= t_min) &
                (self.peaks["Zeit in ms"] <= t_max)
            ]

            fig.add_scatter(
                x=visible_peaks["Zeit in ms"],
                y=visible_peaks["Messwerte in mV"],
                mode="markers",
                name="Peaks",
                marker=dict(color="red", size=12, symbol="x")
            )

        # WICHTIG: Streamlit statt fig.show()
        import streamlit as st
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    print("--- Modul-Test gestartet ---")

    try:
        ekg = EKG_Test.load_by_id(test_id=1, json_path="data/person_db.json")

        ekg.find_peaks()
        ekg.estimate_hr()
        ekg.plot_time_series()

    except Exception as e:
        print(f"Fehler im Ablauf: {e}")














