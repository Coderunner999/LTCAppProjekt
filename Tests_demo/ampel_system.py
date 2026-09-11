
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class FarbigerLektionsButton(Button):
    def __init__(self, lektions_id, status="gesperrt", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (140, 140) # Quadratisch
        
        self.lektions_id = lektions_id
        self.status = status
        
        # Text auf dem Button ist einfach die Nummer der Lektion
        self.text = str(lektions_id)
        self.font_size = 40
        
        # Farbe beim Erstellen direkt setzen
        self.farbe_aktualisieren(status)

    def farbe_aktualisieren(self, neuer_status):
        self.status = neuer_status
        if neuer_status == "erledigt":
            self.background_color = (0.2, 0.8, 0.2, 1) # Grün
        elif neuer_status == "aktiv":
            self.background_color = (1, 0.7, 0, 1)     # Gelb / Orange
        else:
            self.background_color = (0.4, 0.4, 0.4, 1) # Grau


class PythonDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        self.alle_buttons = {}
        
        # Konfiguration: (Lektionsnummer, X-Position, Y-Position)
        lektionen_liste = [
            (1, 0.5, 0.7),
            (2, 0.5, 0.5),
            (3, 0.5, 0.3)
        ]
        
        # Zum Testen starten wir wieder mit Lektion 1 als aktiv
        aktueller_fortschritt = 1
        
        for nummer, x, y in lektionen_liste:
            # Status ermitteln
            start_status = "erledigt" if nummer < aktueller_fortschritt else ("aktiv" if nummer == aktueller_fortschritt else "gesperrt")
            
            # Button erstellen
            btn = FarbigerLektionsButton(lektions_id=nummer, status=start_status, pos_hint={'center_x': x, 'center_y': y})
            btn.bind(on_press=self.lektion_geklickt)
            
            self.alle_buttons[nummer] = btn
            layout.add_widget(btn)
            
        self.add_widget(layout)

    def lektion_geklickt(self, instance_des_buttons):
        nummer = instance_des_buttons.lektions_id
        status = instance_des_buttons.status
        
        # NEU: Wenn der Button grün (erledigt) ist, sperren wir den Klick!
        if status == "erledigt":
            print(f"Lektion {nummer} ist bereits erledigt und kann nicht mehr geklickt werden!")
            return
            
        # Wenn der Button grau (gesperrt) ist, blockieren wir ebenfalls
        if status == "gesperrt":
            print(f"Lektion {nummer} ist grau und gesperrt!")
            return
            
        # Nur wenn der Status "aktiv" (gelb) ist, geht es weiter:
        print(f"Spiele Lektion {nummer}...")
        
        # Wenn erfolgreich beendet (Simulation):
        self.lektion_erfolgreich(nummer)


    def lektion_erfolgreich(self, beendete_nummer):
        # 1. Geklickten Button grün machen
        self.alle_buttons[beendete_nummer].farbe_aktualisieren("erledigt")
        
        # 2. Nächsten Button gelb machen
        naechste_nummer = beendete_nummer + 1
        if naechste_nummer in self.alle_buttons:
            self.alle_buttons[naechste_nummer].farbe_aktualisieren("aktiv")


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PythonDashboard(name='python_dashboard'))
        return sm

if __name__ == '__main__':
    MainApp().run()
