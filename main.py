import streamlit as st
from PIL import Image

from person import Person
from ekgdata import EKG_Test

# -------------------------
# PERSONEN LADEN
# -------------------------

persons = Person.load_person_data()
person_names = Person.get_person_list(persons)

col1, col2 = st.columns(2)

with col1:
    st.write("# EKG APP")
    st.write("## Versuchsperson auswählen")

    current_user_name = st.selectbox(
        "Versuchsperson",
        options=person_names,
        key="current_user"
    )

    current_user = Person.find_person_data_by_name(current_user_name)

    st.write(f"Die Person heißt: {current_user.get_full_name()}")
    st.write(f"Alter: {current_user.calc_age()} Jahre")
    st.write(f"Max HF: {current_user.hr_max} BPM")

with col2:
    if current_user:
        image = current_user.get_image()
        if image:
            st.image(image, caption=current_user.get_full_name())
        else:
            st.warning("Kein Bild gefunden.")

# -------------------------
# EKG TEST AUSWÄHLEN
# -------------------------

st.write("---")
st.write("## EKG-Test auswählen")

if len(current_user.ekg_tests) == 0:
    st.warning("Diese Person hat keine EKG-Tests.")
else:
    # Liste der Test-IDs
    test_ids = [test["id"] for test in current_user.ekg_tests]

    selected_test_id = st.selectbox(
        "EKG-Test auswählen",
        options=test_ids,
        key="ekg_test"
    )

    # EKG-Test laden
    ekg = EKG_Test.load_by_id(selected_test_id)

    st.write(f"### EKG-Test ID: {ekg.id}")
    st.write(f"Datum: {ekg.date}")

    # Peaks finden + HR berechnen
    ekg.find_peaks()
    hr = ekg.estimate_hr()

    st.write(f"**Herzfrequenz:** {hr:.2f} BPM")

    # Plot anzeigen
    st.write("### EKG-Plot")
    ekg.plot_time_series()

