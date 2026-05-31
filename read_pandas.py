import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# --- 1. DATEN LADEN ---
def read_my_activity():
    # Erstellt Testdaten, falls die CSV nicht existiert (für eine lauffähige Demo)
    try:
        df = pd.read_csv("data/activities/activity.csv")
    except FileNotFoundError:
        import numpy as np
        df = pd.DataFrame({
            "PowerOriginal": np.random.randint(100, 300, 600),
            "HeartRate": np.random.randint(110, 185, 600)
        })
        
    df["PowerOriginal"] = df["PowerOriginal"].fillna(0)
    df["HeartRate"] = df["HeartRate"].fillna(0)
    df["Zeit_Sekunden"] = range(len(df))
    return df

# --- MAIN APP ---
st.title("Dashboard für die Leistungsanalyse")
df = read_my_activity()

# KPIs anzeigen
col1, col2 = st.columns(2)
col1.metric("Mittelwert der Leistung", f"{df['PowerOriginal'].mean():.1f} W")
col2.metric("Maximalwert der Leistung", f"{df['PowerOriginal'].max():.1f} W")

st.write("---")
max_hr = st.number_input("Eingabe maximale Herzfrequenz (HFmax):", min_value=140, max_value=220, value=190, step=1)

# Zonen-Konfiguration (Name: (Maximaler Prozentwert, Farbe))
ZONEN = {
    "Zone 1 (Regeneration)": (0.60, "gray"),
    "Zone 2 (Grundlage 1)":   (0.70, "green"),
    "Zone 3 (Grundlage 2)":   (0.80, "yellow"),
    "Zone 4 (Entwicklung)":   (0.90, "orange"),
    "Zone 5 (Spitze)":        (1.00, "red")
}

# --- 2. PLOT ERSTELLEN ---
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Leistung (Blau, linke Achse)
fig.add_trace(go.Scatter(x=df["Zeit_Sekunden"], y=df["PowerOriginal"], name="Leistung (Watt)", line=dict(color="#1f77b4", width=1.5)), secondary_y=False)

# Herzfrequenz (Anthrazit, rechte Achse)
fig.add_trace(go.Scatter(x=df["Zeit_Sekunden"], y=df["HeartRate"], name="Herzfrequenz (bpm)", line=dict(color="#2c3e50", width=2.5)), secondary_y=True)

# Farbige Hintergrundbänder einzeichnen & Daten für die Tabelle sammeln
tabellen_daten = []
lower_bpm = 0

for name, (pct, color) in ZONEN.items():
    upper_bpm = max_hr * pct
    
    # Hintergrundband hinzufügen
    fig.add_hrect(y0=lower_bpm, y1=upper_bpm, fillcolor=color, opacity=0.40, layer="below", line_width=0, secondary_y=True)
    
    # Daten für diese Zone filtern und auswerten
    zone_filter = (df["HeartRate"] >= lower_bpm) & (df["HeartRate"] < upper_bpm) if name != "Zone 5 (Spitze)" else (df["HeartRate"] >= lower_bpm)
    zone_df = df[zone_filter]
    
    tabellen_daten.append({
        "Leistungszone": name,
        "Zeit (Minuten)": round(len(zone_df) / 60, 2),
        "Ø Leistung (Watt)": round(zone_df["PowerOriginal"].mean(), 1) if not zone_df.empty else 0.0
    })
    
    lower_bpm = upper_bpm

# Plot-Layout einstellen
fig.update_layout(
    title_text="Verlauf von Leistung und Herzfrequenz mit Zonen-Hintergrund",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified"
)
fig.update_xaxes(title_text="Zeit in Sekunden")
fig.update_yaxes(title_text="Leistung (Watt)", secondary_y=False)
fig.update_yaxes(title_text="Herzfrequenz (bpm)", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# --- 3. AUSWERTUNGSTABELLE MIT FARBEN ---
st.write("---")
st.subheader("Auswertung der einzelnen Zonen")

# Basis-DataFrame erstellen
df_tabelle = pd.DataFrame(tabellen_daten)

# Funktion, die jeder Zeile die Farbe basierend auf der 'Leistungszone' zuweist
def style_zonen(row):
    zone_name = row["Leistungszone"]
    # Farbe aus dem ZONEN-Diktat holen (Standard ist transparent, falls nicht gefunden)
    farbe = ZONEN.get(zone_name, (None, "transparent"))[1]
    
    # Textfarbe anpassen für bessere Lesbarkeit (Gelb braucht dunklen Text, der Rest hellen)
    text_farbe = "black" if farbe in ["yellow", "transparent"] else "white"
    
    return [f"background-color: {farbe}; color: {text_farbe}; font-weight: bold;"] * len(row)

# Styling anwenden
styled_df = df_tabelle.style.apply(style_zonen, axis=1)

# Gestylte Tabelle in Streamlit anzeigen
st.dataframe(styled_df, use_container_width=True, hide_index=True)