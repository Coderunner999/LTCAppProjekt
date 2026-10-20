import os
from datetime import datetime
from kivy.app import App

# Temporäre App-Klasse für den Pfad
class LTC(App):
    pass

app_ordner = LTC().user_data_dir
keys_datei = os.path.join(app_ordner, "keys.txt")
heute_str = datetime.now().strftime("%Y-%m-%d")

# Hier legen wir fest, wie viele Schlüssel du zum Testen haben willst:
TEST_SCHLUESSEL = 3

print("--- LTC SCHLUESSEL REPARATUR ---")

try:
    # Wir überschreiben die Datei einfach direkt mit gültigen Daten!
    with open(keys_datei, "w", encoding="utf-8") as w:
        w.write(f"{heute_str},{TEST_SCHLUESSEL}")
    
    print("ERFOLG: Die Datei wurde neu geschrieben!")
    print(f"Pfad: {keys_datei}")
    print(f"Inhalt der Datei ist jetzt: {heute_str},{TEST_SCHLUESSEL}")
    print("Starte jetzt deine ltcapp.py neu.")

except Exception as e:
    print("FEHLER: Die Datei konnte nicht beschrieben werden.")
