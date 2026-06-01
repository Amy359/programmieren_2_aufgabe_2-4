import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def read_data(file_path):
    """Liest die CSV-Datei mit den Aktivitätsdaten ein."""
    return pd.read_csv(file_path)

def add_time(df):
    """Nutzt den Pandas-Index als fortlaufende Sekundenanzahl."""
    df['time_sec'] = df.index  
    return df

def find_best_effort(df, window_size=5):
    power_series = df['PowerOriginal'] 
    rolling_means = power_series.rolling(window=window_size).mean()
    return rolling_means.max()

def create_df_pc(df, durations):
    """Erstellt das Power-Curve DataFrame per List Comprehension."""
    daten = [
        {'Zeit in Sekunden': d, 'Leistung in Watt': find_best_effort(df, d)} 
        for d in durations
    ]
    return pd.DataFrame(daten).dropna()

def create_plot_pc(df_pc):
    """Plottet die Leistungskurve, speichert sie und zeigt sie an."""
    ax = df_pc.plot(x='Zeit in Sekunden', y='Leistung in Watt', marker='o', grid=True, figsize=(10, 6))
    ax.set_title('Power-Curve (Leistungskurve)', fontsize=14, fontweight='bold')
    ax.figure.savefig('screenshot.png', dpi=150)
    plt.show()



if __name__ == "__main__":
    print("Starte die Auswertung in einer einzelnen Datei...")
    
    # 1. HIER GGF. DEN UTEN DATEINAMEN REINSCHREIBEN (z. B. activity_1.csv)
    # Ich habe den Pfad laut deinem Screenshot auf den Ordner "activities" angepasst!
    df = read_data("data/activities/activity.csv")
    
    # 2. Zeitspalte hinzufügen
    df = add_time(df)
    
    # 3. Power-Curve für die Intervalle berechnen
    intervalle = [1, 5, 60, 300, 1200]
    df_pc = create_df_pc(df, intervalle)
    
    # 4. Plot anzeigen und screenshot.png generieren
    create_plot_pc(df_pc)
    
    print("Auswertung erfolgreich! Bild 'screenshot.png' wurde im Hauptordner erstellt.")

