# Sakai-Aufgabe: Objektorientierung (10pkt)

Diese Streamlit-App visualisiert medizinische Nutzerdaten und EKG-Signale basierend auf einer objektorientierten Struktur mit den Klassen `Person` und `EKG_Test`.

---

## 🛠️ Setup & Start (PDM)

Führe diese Befehle nacheinander im Terminal aus, um das Projekt einzurichten und zu starten:

```bash
# 1. PDM global installieren (falls nötig)
pip install pdm

# 2. In deinen lokalen Projektordner wechseln
cd <PROJEKT_ORDNER_NAME>

# 3. Virtuelle Umgebung und Abhängigkeiten installieren
pdm install

# 4. Streamlit-App starten
pdm run streamlit run main.py