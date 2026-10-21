
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.codeinput import CodeInput
from pygments.lexers import Python3Lexer
from pygments.lexers.html import HtmlLexer
from pygments.styles import get_style_by_name
from kivy.metrics import sp
from kivy.clock import Clock
from pygments.lexers.shell import PowerShellLexer
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics import StencilPush, StencilUse, StencilUnUse, StencilPop, RoundedRectangle, Color
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivy.graphics.texture import Texture
from kivy.graphics import Line
import webbrowser
from kivy.core.audio import SoundLoader





# =============================================================================================================================
# PYTHON LEKTION 1: DIE LERN-SCREENS
# =============================================================================================================================

class PythonLektion1_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Willkommen in Python!",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Python ist eine der beliebtesten Programmiersprachen weltweit.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Mit ihr können wir Apps, Spiele, Roboter usw. programmieren.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Beginnen wir mit VARIABLEN.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        self.fehler_gemacht = False

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l1_s2'

class PythonLektion1_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Deine originalen Erklärungen
        erklährung_label1 = Label(
            text="Variablen kennst du aus der Mathematik. Dort sind sie",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Platzhalter für Zahlen. Ähnlich ist es auch in Python.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Mit Variablen können wir beliebige Dinge im Code speichern,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="um später im Code darauf zuzugreifen. Hier ein Beispiel:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="number = 14\ngreet = 'Hallo'", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.48}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.fehler_gemacht = False

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l1_s3'

class PythonLektion1_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Code erstellt eine Variable namens schedule",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        frage2 = Label(
            text="und weist ihr den Wert 3 zu?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        self.option1 = Button(
            text="3 = schedule",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="schedule = 3",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(frage2)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.sound_wrong = SoundLoader.load('false_answer.mp3')
        self.sound_wrong.play()
        self.fehler_gemacht = True  # Korrigiert: Fehler wird registriert

    def antwort_richtig(self, instance):
        # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
        if instance.background_color != [0.25, 0.55, 0.95, 1]:
            self.option1.background_color = (1, 1, 1, 1)
            if hasattr(self, 'option3'):
                self.option3.background_color = (1, 1, 1, 1)
            
            # Button wird beim 1. Klick marineblau gefärbt
            instance.background_color = (0.25, 0.55, 0.95, 1)
            self.sound_true = SoundLoader.load('true_answer.mp3')
            self.sound_true.play()
            
            # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
            if not self.fehler_gemacht:
                abschluss = self.manager.get_screen('python_l1_s6')
                abschluss.lektions_xp += 10
                
            return  # Auf den zweiten Klick warten

        # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
        instance.background_color = (1, 1, 1, 1)
        self.manager.current = 'python_l1_s4'

class PythonLektion1_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Welche Variable ist richtig programmiert?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="data = 2",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="data = 2-",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Keine Antwort ist richtig.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.sound_true = SoundLoader.load('true_answer.mp3')
                self.sound_true.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l1_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l1_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

class PythonLektion1_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="a = 6,7\nb = 'hi, guys'",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Der Fehler liegt bei b (Komma im Text).",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Der Fehler liegt bei a (Komma statt Punkt bei Zahlen).",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Beide Zeilen sind absolut fehlerfrei.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False

        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
           # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
           if instance.background_color != [0.25, 0.55, 0.95, 1]:
               self.option1.background_color = (1, 1, 1, 1)
               if hasattr(self, 'option3'):
                   self.option3.background_color = (1, 1, 1, 1)
               
               # Button wird beim 1. Klick marineblau gefärbt
               instance.background_color = (0.25, 0.55, 0.95, 1)
               self.sound_true = SoundLoader.load('true_answer.mp3')
               self.sound_true.play()
               
               # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
               if not self.fehler_gemacht:
                   abschluss = self.manager.get_screen('python_l1_s6')
                   abschluss.lektions_xp += 10
                   
               return  # Auf den zweiten Klick warten
   
           # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
           instance.background_color = (1, 1, 1, 1)
           self.manager.current = 'python_l1_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.sound_false = SoundLoader.load('false_answer.mp3')
        self.sound_false.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.sound_false.play()
        self.fehler_gemacht = True

class PythonLektion1_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du bist deinen Zielen einen Schritt näher!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        
        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( # type: ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(1) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'






# =============================================================================================================================
# PYTHON LEKTION 2: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion2_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Variablen verändern",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Schon gewusst? Wir können Variablen ganz einfach verändern!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Diesen Vorgang nennen wir auch Aktualisieren.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Starten wir gleich rein!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        self.fehler_gemacht = False
        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l2_s2'

class PythonLektion2_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Da Variablen Platzhalter für Daten sind (wie eine Box)",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="können wir auch ihren Inhalt wie bei einer Box wieder ändern.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Wir tun dies ganz einfach, indem wir die Variable erneut",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="definieren (erstellen) und ihr einen NEUEN Wert zuweisen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="number = 1\nnumber = 3", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.48}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.fehler_gemacht = False
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l2_s3'

class PythonLektion2_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Wodurch aktualisieren wir Variablen?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Erneute definieren",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Löschen des Codes",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.sound_false = SoundLoader.load('false_answer.mp3')
        self.sound_false.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.sound_true = SoundLoader.load('true_answer.mp3')
                self.sound_true.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l2_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l2_s4'

class PythonLektion2_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Kann man eine Variable wieder ändern?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Nur teilweise",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Ja, das geht",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="Nein, das ist unmöglich!",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.sound_true = SoundLoader.load('true_answer.mp3')
                self.sound_true.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l2_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l2_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True
    
class PythonLektion2_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="status = 'offline'\nstatus = online",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Das ist nicht möglich",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Um online fehlen die ''",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Bill Gates war am Werk...",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
                # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
                if instance.background_color != [0.25, 0.55, 0.95, 1]:
                    self.option1.background_color = (1, 1, 1, 1)
                    if hasattr(self, 'option3'):
                        self.option3.background_color = (1, 1, 1, 1)
                    
                    # Button wird beim 1. Klick marineblau gefärbt
                    instance.background_color = (0.25, 0.55, 0.95, 1)
                    self.true_answer = SoundLoader.load('true_answer.mp3')
                    self.true_answer.play()
                    
                    # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                    if not self.fehler_gemacht:
                        abschluss = self.manager.get_screen('python_l2_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'python_l2_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion2_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du bist deinen Zielen einen Schritt näher!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( # type: ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(2) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'






# =============================================================================================================================
# PYTHON LEKTION 3: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion3_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Rechnen mit Variablen",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Wir können nicht nur Zahlen speichern, sondern",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="wir können auch ganze Rechnungen mit Variablen aufstellen!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Schauen wir es uns mal an!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l3_s2'

class PythonLektion3_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Da wir (Dezimal-) Zahlen in Variablen speichern können,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="können wir selbstverständlich auch mit diesen Zahlen rechnen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Dazu definieren wir mindestens zwei Variablen mit jeweils zwei Zahlen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Anschließend berechnet eine dritte Variable das Ergebnis der anderen Variablen!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="num_1 = 15\nnum_2 = 17\nsolution = num_1 + num_2", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.48}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l3_s3'

class PythonLektion3_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Das Ergebnis bekommen wir mit...",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Zufällige Generierung.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="Eine dritte Variable (solution).",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
                # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
                if instance.background_color != [0.25, 0.55, 0.95, 1]:
                    self.option1.background_color = (1, 1, 1, 1)
                    if hasattr(self, 'option3'):
                        self.option3.background_color = (1, 1, 1, 1)
                    
                    # Button wird beim 1. Klick marineblau gefärbt
                    instance.background_color = (0.25, 0.55, 0.95, 1)
                    self.true_answer = SoundLoader.load('true_answer.mp3')
                    self.true_answer.play()
                    
                    # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                    if not self.fehler_gemacht:
                        abschluss = self.manager.get_screen('python_l3_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'python_l3_s4'

class PythonLektion3_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Ist es möglich 5 Zahlen zu addieren?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Das ist unmöglich.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Nur 2 Zahlen möglich",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Ja, das geht",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
                # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
                if instance.background_color != [0.25, 0.55, 0.95, 1]:
                    self.option1.background_color = (1, 1, 1, 1)
                    if hasattr(self, 'option3'):
                        self.option3.background_color = (1, 1, 1, 1)
                    
                    # Button wird beim 1. Klick marineblau gefärbt
                    instance.background_color = (0.25, 0.55, 0.95, 1)
                    self.true_answer = SoundLoader.load('true_answer.mp3')
                    self.true_answer.play()

                    
                    # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                    if not self.fehler_gemacht:
                        abschluss = self.manager.get_screen('python_l3_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'python_l3_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion3_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="user = 130\ninstalls = 160\ntotal = user + installs",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Kein Fehler.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)
        
        self.option2 = Button(
            text="Frag den Professor",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Das funktioniert so nicht.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l3_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l3_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion3_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du bist deinen Zielen einen Schritt näher!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( # type: ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(3) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'







# =============================================================================================================================
# PYTHON LEKTION 4: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion4_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Texte ausgeben",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Damit wir die Ergebnisse unserer Programme sehen können,",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="muss unser Programm Text am Bildschirm anzeigen!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lernen wir den Befehl kennen!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l4_s2'

class PythonLektion4_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Wir haben bereits gelernt, Texte und Zahlen zu speichern usw.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Wir wissen aber noch nicht, wie wir Texte auf dem Bildschirm anzeigen!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Dazu verwenden wir den sogenannten print()-Befehl.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="In den Klammern steht der Text, den wir anzeigen wollen! Schau:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="print('Hello World!')", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.48}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l4_s3'

class PythonLektion4_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Befehl zeigt Texte an?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="print()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="text()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l4_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l4_s4'

class PythonLektion4_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Welcher Code zeigt 'Developer' an?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="print(Developer)",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="println('Developer')",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="print('Developer')",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
                # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
                if instance.background_color != [0.25, 0.55, 0.95, 1]:
                    self.option1.background_color = (1, 1, 1, 1)
                    if hasattr(self, 'option3'):
                        self.option3.background_color = (1, 1, 1, 1)
                    
                    # Button wird beim 1. Klick marineblau gefärbt
                    instance.background_color = (0.25, 0.55, 0.95, 1)
                    self.true_answer = SoundLoader.load('true_answer.mp3')
                    self.true_answer.play()
                    
                    # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                    if not self.fehler_gemacht:
                        abschluss = self.manager.get_screen('python_l4_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'python_l4_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion4_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="print('3..')\nPrint('2...')\nprint('1...')",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Der Code ist fehlerfrei.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Das zweite print() ist falsch!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="DA FEHLT EIN PUNKT!!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l4_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l4_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion4_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du bist deinen Zielen einen Schritt näher!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( #type: ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(4) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'






# =============================================================================================================================
# PYTHON LEKTION 5: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion5_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Variablen in print()",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Wir wissen bereits, wie wir fertige Texte anzeigen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Was ist, wenn wir Variablen (ihren Inhalt) anzeigen wollen?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lass es uns lernen!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l5_s2'

class PythonLektion5_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Wir haben mit print() die Macht Texte anzuzeigen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Um aber den Inhalt von Variablen anzuzeigen, lassen wir einfach die",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="zwei Anführungszeichen weg, und schreiben nur den Variablennamen!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir den korrekten Code dazu an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="name = 'Karl'\nprint(name)", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.48}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l5_s3'

class PythonLektion5_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Beim Anzeigen von Variablen lassen wir die ... weg:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Klammern",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="Anführungszeichen",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l5_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l5_s4'

class PythonLektion5_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Welcher Code zeigt die Variable info an?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="print(INFO)",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="println(info)",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="print(info)",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l5_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l5_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion5_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="alter = 16\nprint(alter)",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.5, 0.12),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Das ist kein Python-Code!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Der Code ist alt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Der Code ist fehlerfrei.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
                # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
                if instance.background_color != [0.25, 0.55, 0.95, 1]:
                    self.option1.background_color = (1, 1, 1, 1)
                    if hasattr(self, 'option3'):
                        self.option3.background_color = (1, 1, 1, 1)
                    
                    # Button wird beim 1. Klick marineblau gefärbt
                    instance.background_color = (0.25, 0.55, 0.95, 1)
                    self.true_answer = SoundLoader.load('true_answer.mp3')
                    self.true_answer.play()
                    
                    # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                    if not self.fehler_gemacht:
                        abschluss = self.manager.get_screen('python_l5_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'python_l5_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True
    
class PythonLektion5_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du kannst perfekt Texte anzeigen, super!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( #type: ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(5) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'






# =============================================================================================================================
# PYTHON LEKTION 6: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion6_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Datentypen",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Du hast bereits gesehen, dass es verschiedene Werte gibt:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Zahlen und Texte. Aber was genau ist das, und wie funktioniert es?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Tüfteln wir los!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l6_s2'

class PythonLektion6_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Es gibt verschiedene sogenannte Typen von Daten in Python.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Wir nennen sie Datentypen, auf Englisch Data Types. Sie sind so aufgebaut:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="String = Text, Integer = ganze Zahl, Float = Dezimalzahl, Boolean = Richtig/Falsch",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir die Typen mit Code an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="name = 'Selcia' # Ein String\ndata = True # Ein Boolean\nnumber = 67 # Ein Integer\nex_n = 12.5 # Ein Float", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.4}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l6_s3'

class PythonLektion6_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Die Werte True und False gehören zu einem...",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Boolean",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Float",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l6_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l6_s4'

class PythonLektion6_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Welcher Code ist ein String?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="active_user = 'Finn'",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="normal = True",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="string_3000 = 0.003",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l6_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l6_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion6_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="name = Todd\nprint(name)",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Todd ist kein Typ, und kein Wert!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)
        
        self.option2 = Button(
            text="SyntaxError",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Man darf es nicht printen.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l6_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l6_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion6_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Die Datentypen gehören dir! Stark!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
            
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0
    
        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
                
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")
    
        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0
    
        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
                
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
                
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(6) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!
    
        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'







# =============================================================================================================================
# PYTHON LEKTION 7: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion7_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Typen umwandeln - Teil 1",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Wir kennen bereits String, Float, Integer, Boolean.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Aber wie wandelt man Strings in Integer um usw?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne es heute!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l7_s2'

class PythonLektion7_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Es gibt dazu 4 Befehle: str(), float(), int(), bool()",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Das Wort am Anfang sagt uns, zu welchem Typ der Wert umgewandelt werden soll.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Der Wert in den Klammern ist das, was umgewandelt werden soll!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir ein Beispiel aus der Praxis an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="text = '5' # Unser Wert.\n# Umwandeln in Ganze Zahl durch:\nzahl = int(text)\nprint(zahl) # 5", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.4}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l7_s3'

class PythonLektion7_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Dieser Befehl wandelt den Wert in den Klammern in eine Dezimalzahl um:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="float()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="int()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l7_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l7_s4'

class PythonLektion7_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Wo ist der umzuwandelnde Wert?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="In den Klammern.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="In den Klammern.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="Gibt es nicht.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l7_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l7_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion7_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="name_text = 'Sepp'\nname_status = bool(name_text)",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Ein String lässt sich nicht in einen Boolean umwandeln!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Kein Fehler, es ergibt True.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Da fehlt noch Depp!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l7_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l7_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion7_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du bist deinen Zielen einen Schritt näher!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(7) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'








# =============================================================================================================================
# PYTHON LEKTION 8: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion8_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Typen umwandeln - Teil 2",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Wir wissen, wie wir einfache Typen umwandeln. Gut.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Können wir das auch alles in einer einzigen Zeile tun?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Erhalte wertvolles Wissen!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l8_s2'

class PythonLektion8_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Wir können in 2 Zeilen Code Typen umwandeln.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Um später bei großen Apps Zeilen zu sparen, lass es uns",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="in einer einzigen brillanten Zeile tun!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir echten Code aus der Praxis an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="number = 4.5\nprint(bool(number))\n# Ein Befehl IM anderen drin!", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.4}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l8_s3'

class PythonLektion8_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Was muss bei Projekten minimiert werden?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Code Zeilen",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Code Kommentare",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l8_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l8_s4'

class PythonLektion8_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Das ist die kurze Art:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="print(str(data))",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="a = str(a_old)",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Es gibt keine kurze Art!",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l8_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l8_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion8_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="name = 'Coder3000'\nprint(bool(name))",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Ein String lässt sich nicht in einen Boolean umwandeln!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Kein Fehler, es ergibt False.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Kein Fehler, es ergibt True.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l8_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l8_s6' 

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion8_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Du bist deinen Zielen einen Schritt näher!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(8) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'







# =============================================================================================================================
# PYTHON LEKTION 9: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion9_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Eingaben in Python",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Wie machen wir unsere Programme interaktiv und",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="lassen den Nutzer Text eingeben?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne es!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        layout.add_widget(welcome_label)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l9_s2'

class PythonLektion9_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Text-Eingaben erstellen wir mit input().",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Um die Nutzereingabe zu speichern, schreiben wir alles",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="in eine Variable. Das können wir später verwenden!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Nachher wollen wir die Nutzereingabe wieder ausgeben.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="entry = input()\nprint(entry) # Eingabe nochmal anzeigen", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Höhe angepasst für 2 Zeilen
            pos_hint={'center_x': 0.5, 'center_y': 0.4}, # Perfekt zentriert im Bereich
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        weiter_button = Button(
            text="Weiter",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        weiter_button.bind(on_press=self.weiter)

        # Objekte hinzufügen
        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt) # Das kombinierte Widget hinzufügen

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'python_l9_s3'

class PythonLektion9_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Dieser Befehl ermöglicht Eingaben:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="input()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="entry()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l9_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l9_s4'

class PythonLektion9_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Wie speichern wir Eingaben?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Mit einem Befehl",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="In einer Variable",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="In entry()",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l9_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l9_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion9_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde den Fehler im Code!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="input() = entry\nprint(input())",        # Der Quiz-Code zweizeilig untereinander
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),               # Exakt die gleichen Maße wie auf Screen 2
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, # Perfekt zentriert an derselben Stelle
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        # Deine originalen Optionen (Abstände für die Buttons)
        self.option1 = Button(
            text="Ein Skript-Kiddie!",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Das ist korrekt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Befehl/Variable vertauscht.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        # Adden der Objekte:
        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)    # Das identische Editor-Widget
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)
        
        self.fehler_gemacht = False
        
        # Ausführen:
        self.add_widget(layout)
    
    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()
                
                # Korrigiert: 10 XP dazurechnen, wenn direkt beim 1. Mal richtig geklickt wurde
                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('python_l9_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l9_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class PythonLektion9_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erfolg_label1 = Label(
            text="Lektion abgeschlossen!",
            font_size=80,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        motivation = Label(
            text="Super, den ersten Abschnitt hast du fertig!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_anzeige_label = Label(
            text="",
            font_size=45,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        # Adden der Objekte:
        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"
        
    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        # ---------------------------------------------------------------------------------------------------------------------
        # XP SPEICHERN (Dein Original-Code)
        # ---------------------------------------------------------------------------------------------------------------------
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_xp = int(datei.read().strip())
                except:
                    aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        with open(xp_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_xp))
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # ---------------------------------------------------------------------------------------------------------------------
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix)
        # ---------------------------------------------------------------------------------------------------------------------
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10 # Unabhängig von Fehlern immer +10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard')
        python_dashboard.lektion_erfolgreich(9) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard'

