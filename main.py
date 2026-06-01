import streamlit as st
import read_data as read_data 
from PIL import Image

person_dict = read_data.load_person_data()
person_names = read_data.get_person_list(person_dict)

import streamlit as st

col1, col2 = st.columns(2)


# --- 1. FUNKTIONEN DEFINIEREN (Ganz nach oben) ---

def find_person_data_by_name(suchstring):
    """ Eine Funktion, der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurückgibt """
    
    person_data = person_dict
    
    if suchstring == "None" or not suchstring:
        return {}

    two_names = suchstring.split(", ")
    nachname = two_names[0]
    vorname = two_names[1]

    for eintrag in person_data:
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            return eintrag
            
    return {}


# --- 2. UI UND LOGIK (Darunter) ---
with col1:
    st.write("# EKG APP")
    st.write("## Versuchsperson auswählen")

    current_user = st.selectbox('Versuchsperson', options=person_names, key="current_user")
    st.write(f"Die Person heißt: {current_user}")

   


# --- 3. BILD DYNAMISCH LADEN (Jetzt kennt Python die Funktion!) ---
with col2:
    if current_user:
        aktuelle_person_daten = find_person_data_by_name(current_user)
        
        if aktuelle_person_daten and "picture_path" in aktuelle_person_daten:
            dateipfad = aktuelle_person_daten["picture_path"]
            
            try:
                image = Image.open(dateipfad)
                st.image(image, caption=st.session_state.current_user)
            except FileNotFoundError:
                st.warning(f"Datei '{dateipfad}' existiert nicht im Ordner.")
        else:
            st.warning(f"Kein Bildpfad in den Daten für {current_user} hinterlegt.")

with col1: 
    st.write(f"Der Pfad ist: {dateipfad}")






# main.py

# Hier importierst du dein Modul mit dem exakten Dateinamen (ohne .py)
import advanced_powercurve as apc

if __name__ == "__main__":
    # 1. Daten einlesen (Sicherstellen, dass der Pfad stimmt)
    df = apc.read_data("data/activity.csv") 
    
    # 2. Zeitspalte hinzufügen
    df = apc.add_time(df)
    
    # 3. Power-Curve berechnen
    intervalle = [1, 5, 60, 300, 1200]
    df_pc = apc.create_df_pc(df, intervalle)
    
    # 4. DAS HIER ERSETZT DEN FEHLERHAFTEN STREAMLIT-CODE:
    # Anstatt st.image() rufen wir jetzt einfach unsere Plot-Funktion auf
    apc.create_plot_pc(df_pc)
    
    print("Auswertung erfolgreich! Bild 'screenshot.png' wurde erstellt.")