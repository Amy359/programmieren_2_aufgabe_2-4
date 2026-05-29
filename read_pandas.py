import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# --- 1. DATEN EINLESEN ---
def read_my_activity():
    # Daten ganz normal einlesen
    df = pd.read_csv("data/activities/activity.csv")
    
    # Fehlerhafte/leere Werte mit 0 füllen
    df["PowerOriginal"] = df["PowerOriginal"].fillna(0)
    df["HeartRate"] = df["HeartRate"].fillna(0)
    
    # Eigene Zeitachse erstellen, da Duration manchmal Probleme macht
    df["Zeit_Sekunden"] = range(len(df))
    return df


# --- 2. PLOT & ZONEN ---
def make_power_hr_plot(df):
    # Einfacher Subplot mit zwei Achsen
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Leistung auf der linken Seite (Blau)
    fig.add_trace(
        go.Scatter(
            x=df["Zeit_Sekunden"], 
            y=df["PowerOriginal"], 
            name="Leistung (Watt)",
            line=dict(color="blue")
        ),
        secondary_y=False
    )
    
    # Herzfrequenz auf der rechten Seite (Rot)
    fig.add_trace(
        go.Scatter(
            x=df["Zeit_Sekunden"], 
            y=df["HeartRate"], 
            name="Herzfrequenz (bpm)",
            line=dict(color="red")
        ),
        secondary_y=True
    )
    
    # Achsen ganz normal beschriften
    fig.update_layout(title_text="Verlauf von Leistung und Herzfrequenz")
    fig.update_xaxes(title_text="Zeit in Sekunden")
    fig.update_yaxes(title_text="Leistung (Watt)", secondary_y=False)
    fig.update_yaxes(title_text="Herzfrequenz (bpm)", secondary_y=True)
    
    return fig


def add_hr_zones(df, max_hr):
    # Klassische Funktion zur Zonen-Zuweisung
    def check_zone(puls):
        if puls == 0:
            return "Keine Daten"
        elif puls < max_hr * 0.6:
            return "Zone 1 (Regeneration)"
        elif puls < max_hr * 0.7:
            return "Zone 2 (Grundlage 1)"
        elif puls < max_hr * 0.8:
            return "Zone 3 (Grundlage 2)"
        elif puls < max_hr * 0.9:
            return "Zone 4 (Entwicklung)"
        else:
            return "Zone 5 (Spitze)"
        
    df['Zone'] = df['HeartRate'].apply(check_zone)
    return df


# --- 3. HAUPTPROGRAMM ---
if __name__ == "__main__":
    st.title("Dashboard für die Leistungsanalyse")
    
    # Daten laden
    activity_df = read_my_activity()
    
    # Mittelwert und Maximalwert berechnen
    mittelwert_leistung = activity_df['PowerOriginal'].mean()
    maximalwert_leistung = activity_df['PowerOriginal'].max()
    
    # KPIs nebeneinander anzeigen
    col1, col2 = st.columns(2)
    col1.metric("Mittelwert der Leistung", f"{mittelwert_leistung:.1f} W")
    col2.metric("Maximalwert der Leistung", f"{maximalwert_leistung:.1f} W")
    
    st.write("---")
    
    max_hr = st.number_input("Eingabe maximale Herzfrequenz (HFmax):", min_value=140, max_value=220, value=190, step=1)
    
    # Zonen berechnen und dem Dataframe hinzufügen
    activity_df = add_hr_zones(activity_df, max_hr)
    
    # Interaktiven Plot anzeigen
    fig = make_power_hr_plot(activity_df)
    st.plotly_chart(fig)
    
    st.write("---")
    st.subheader("Auswertung der einzelnen Zonen")
    
    zonen_liste = [
        "Zone 1 (Regeneration)", 
        "Zone 2 (Grundlage 1)", 
        "Zone 3 (Grundlage 2)", 
        "Zone 4 (Entwicklung)", 
        "Zone 5 (Spitze)"
    ]
    
    # Liste für die Tabellendaten erstellen
    tabellen_daten = []
    
    for zone in zonen_liste:
        zone_daten = activity_df[activity_df['Zone'] == zone]
        anzahl_sekunden = len(zone_daten)
        zeit_in_minuten = anzahl_sekunden / 60
        
        if anzahl_sekunden > 0:
            durchschnitt_leistung_zone = zone_daten['PowerOriginal'].mean()
        else:
            durchschnitt_leistung_zone = 0
            
        # Daten als Dictionary an die Liste anhängen
        tabellen_daten.append({
            "Leistungszone": zone,
            "Zeit (Minuten)": round(zeit_in_minuten, 2),
            "Ø Leistung (Watt)": round(durchschnitt_leistung_zone, 1)
        })
    
    # DataFrame aus der Liste erstellen
    summary_df = pd.DataFrame(tabellen_daten)
    
    # Tabelle formatiert in Streamlit ausgeben
    st.dataframe(summary_df, use_container_width=True, hide_index=True)