import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def read_data(file_path):
    return pd.read_csv(file_path)

def add_time(df):
    df['time_sec'] = df.index  
    return df

def find_best_effort(df, window_size=5):
    power_series = df['PowerOriginal'] 
    rolling_means = power_series.rolling(window=window_size).mean()
    return rolling_means.max()

def create_df_pc(df, durations):
    daten = [
        {'Zeit in Sekunden': d, 'Leistung in Watt': find_best_effort(df, d)} 
        for d in durations
    ]
    return pd.DataFrame(daten).dropna()

def create_plot_pc(df_pc):
    ax = df_pc.plot(x='Zeit in Sekunden', y='Leistung in Watt', marker='o', grid=True)
    ax.set_title('Power-Curve (Leistungskurve)', fontsize=14, fontweight='bold')
    ax.figure.savefig('screenshot.png')
    plt.show()



if __name__ == "__main__":
    print("Starte die Auswertung in einer einzelnen Datei...\n")

    
    df = add_time(read_data("data/activities/activity.csv"))

    
    df_pc = create_df_pc(df, [1, 5, 60, 300, 1200])
    create_plot_pc(df_pc)

    
    print("\n--- Berechnete Power-Curve Werte ---")
    print(df_pc.to_string(index=False))
    print("-" * 36 + "\n")
    
    print("Auswertung erfolgreich! Bild 'screenshot.png' wurde im Hauptordner erstellt.")

