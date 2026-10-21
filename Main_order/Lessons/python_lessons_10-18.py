
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
# PYTHON LEKTION 10: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion10_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Kommentare #",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Damit unser Code auch nach Monaten noch gut lesbar ist,",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="kommentieren wir ihn mit #. Das ist für die Wartung wichtig!",
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
        self.manager.current = 'python_l10_s2'

class PythonLektion10_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Nach jedem # kommt der dazugehörige Code.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Danach lassen wir eine Zeile frei und es kommt",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="ein weiteres # und wieder Code usw.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir ein kleines Beispiel an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="# Erstellen von Number:\nnumber = 5", # \n macht den Zeilenumbruch!
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
        self.manager.current = 'python_l10_s3'

class PythonLektion10_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Wodurch wird Code wartbar?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Kommentare #",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="3-5 Leerzeilen",
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
                    abschluss = self.manager.get_screen('python_l10_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l10_s4'

class PythonLektion10_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was ist richtig?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Nichts davon",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Code, #, Leerzeile, Code, # ...",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="#, Code, Leerzeile, #, Code ...",
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
                    abschluss = self.manager.get_screen('python_l10_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l10_s5'

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

class PythonLektion10_Screen5(Screen):
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
            text="# Die Aktualisierung:\ndata = 5.78",        # Der Quiz-Code zweizeilig untereinander
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
            text="Falsche Art.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Kein Fehler.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Unklare Syntax.",
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
                    abschluss = self.manager.get_screen('python_l10_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l10_s6'

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

class PythonLektion10_Screen6(Screen):
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(10) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'






# =============================================================================================================================
# PYTHON LEKTION 11: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion11_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Bedingungen - Teil 1",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Professionelle Apps müssen oft Entscheidungen treffen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Dazu benötigen sie Bedingungen (if-Anweisungen).",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne etwas Neues!",
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
        self.manager.current = 'python_l11_s2'

class PythonLektion11_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Ein If wird nur dann ausgeführt, wenn die enthaltene",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Bedingung stimmt, also True ist. Ansonsten wird der Code",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="im If-Block übersprungen. Nur bei True wird es ausgeführt!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir einen If-Block an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="wert = True\nif wert:\n    print('Thats True!')", # \n macht den Zeilenumbruch!
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
        self.manager.current = 'python_l11_s3'

class PythonLektion11_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Die Bedingung muss ... sein.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="False",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="True",
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
                    abschluss = self.manager.get_screen('python_l11_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l11_s4'

class PythonLektion11_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Ein Wert ist bei if (variable): immer:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="True",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Nicht vollständig.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="False",
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
                    abschluss = self.manager.get_screen('python_l11_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l11_s5'

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

class PythonLektion11_Screen5(Screen):
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
            text="name = 'Jessica'\nif Jessica:\n    print('Whats the matter?')",        # Der Quiz-Code zweizeilig untereinander
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
            text="Kein richtiges if-Statement.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Beim if muss der Variablenname stehen",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="print - Kein Befehl, ein DRUCKER",
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
                    abschluss = self.manager.get_screen('python_l11_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l11_s6'

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

class PythonLektion11_Screen6(Screen):
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(11) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'







# =============================================================================================================================
# PYTHON LEKTION 12: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion12_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Bedingungen - Teil 2",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Um mit einem if zu überprüfen, ob zwei Werte gleich sind,",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="verwenden wir den sogenannten Gleichheitsoperator!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne über den Operator!",
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
        self.manager.current = 'python_l12_s2'

class PythonLektion12_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Mit == können wir in einem if prüfen, ob zwei Werte",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="den gleichen Inhalt besitzen. Wenn das Ergebnis",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="also True ist, wird der if-Block ausgeführt.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir den Gleichheitsoperator im Einsatz an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="wert_1 = 5\nwert_2 = 5\nif wert_1 == wert_2:\n    print('Gleicher Inhalt!')", # \n macht den Zeilenumbruch!
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
        self.manager.current = 'python_l12_s3'

class PythonLektion12_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Der ==-Operator prüft, ob ...",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Zwei Werte ungleich sind.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="Zwei Werte gleich sind.",
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
                    abschluss = self.manager.get_screen('python_l12_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l12_s4'

class PythonLektion12_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was muss die Bedingung ergeben, damit der Code ausgeführt wird?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="True",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Nicht vollständig.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="False",
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
                    abschluss = self.manager.get_screen('python_l12_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l12_s5'

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

class PythonLektion12_Screen5(Screen):
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
            text="person_1 = 'Jessica'\nperson_2 = 'Marko'\nif person_1:\n    print('Done')",        # Der Quiz-Code zweizeilig untereinander
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
            text="Es stimmt doch.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Kein Gleichheitsoperator",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Falscher Befehl.",
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
                    abschluss = self.manager.get_screen('python_l12_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l12_s6'

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

class PythonLektion12_Screen6(Screen):
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(12) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'







# =============================================================================================================================
# PYTHON LEKTION 13: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion13_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Bedingungen - Teil 3",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Um mit einem if zu überprüfen, ob zwei Werte",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="ungleich (verschieden) sind, verwenden wir !=.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne über !=!",
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
        self.manager.current = 'python_l13_s2'

class PythonLektion13_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Mit !=, dem Ungleichheitsoperator, können wir prüfen",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="ob zwei Werte unterschiedlich sind. Ist das Ergebnis True,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="wird der If-Block ausgeführt, sonst wird er übersprungen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir den Ungleichheitsoperator an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="data_base_1 = 85\ndata_base_2 = 55\nif data_base_1 != data_base_2:\n    print('Ungleich!')", # \n macht den Zeilenumbruch!
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
        self.manager.current = 'python_l13_s3'

class PythonLektion13_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Was prüft der !=-Operator?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Zwei Werte ungleich sind.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Zwei Werte gleich sind.",
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
                    abschluss = self.manager.get_screen('python_l13_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l13_s4'

class PythonLektion13_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was sind ==, !=?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Rechnungen",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Gleichungen",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Operatoren",
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
                    abschluss = self.manager.get_screen('python_l13_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l13_s5'

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

class PythonLektion13_Screen5(Screen):
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
            text="glas_1 = 'Coffee'\nglas_2 = 'Beer'\nif glas_1 != glas_2:\n    print('Unterschiedliches')\n    print('Getränk!')",        # Der Quiz-Code zweizeilig untereinander
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
            text="Das ist korrekt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)
        
        self.option2 = Button(
            text="Syntaxfehler.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Ungültige Syntax.",
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
                    abschluss = self.manager.get_screen('python_l13_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l13_s6'

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

class PythonLektion13_Screen6(Screen):
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
            text="Starkes Wissen bei den Operatoren!",
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(13) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'






# =============================================================================================================================
# PYTHON LEKTION 14: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion14_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Bedingungen - Teil 4",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Um mit einem if, falls er nicht zutrifft noch bevor der",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="If-Block endet, noch einmal etwas zu überprüfen nutzen wir...",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Erfahre es...",
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
        self.manager.current = 'python_l14_s2'

class PythonLektion14_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="den klassischen elif-Befehl. Er wird unten nach if angehängt.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Es ist, als würde man sagen: Ist if False, versuche es noch mit elif.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Wir können so viele elif-Blöcke schreiben, wie wir wollen. Python prüft",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="jeden elif-Block nacheinander. Sieh es dir an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="our_text = 'Die Coderin'\nif our_text == 'Der Coder':\n    print('Der Coder?')\nelif our_text == 'Die Coderin':\n    print('Die Coderin?')", # \n macht den Zeilenumbruch!
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
        self.manager.current = 'python_l14_s3'

class PythonLektion14_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="elif kann es geben...",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Maximal 3",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="So viele, wie wir wollen.",
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
                    abschluss = self.manager.get_screen('python_l14_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l14_s4'

class PythonLektion14_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was prüft Python zuerst?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Alles",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Zuerst das elif, danach das if.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Zuerst das if, danach das elif.",
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
                    abschluss = self.manager.get_screen('python_l14_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l14_s5'

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

class PythonLektion14_Screen5(Screen):
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
            text="student_1 = 'Anna'\nstudent_2 = 'Alice'\nif student_1 !=:\n    print('The live is not long.')\nelif student_2 == 'Dia':\n    print('I think the sky is red.')",        # Der Quiz-Code zweizeilig untereinander
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
            text="Ungültige Logik bei elif.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Ungültige Logik bei if.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="NameError",
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
                    abschluss = self.manager.get_screen('python_l14_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l14_s6'

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

class PythonLektion14_Screen6(Screen):
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
            text="Gute Leistung, Herr Programmierer!",
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
        fertig_button = FertigPulseButton(  #type:ignore
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(14) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'






# =============================================================================================================================
# PYTHON LEKTION 15: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion15_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Bedingungen - Teil 5",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Was, wenn wir bei einem if-Block etwas Besonderes tun wollen,",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="das nur passiert, wenn alle Bedingungen False sind?",
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
        self.manager.current = 'python_l15_s2'

class PythonLektion15_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Wenn if und alle elif-Bedingungen False sind,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="verwenden wir else als Ausweichmöglichkeit.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="else wird nur ausgeführt, wenn alles davor False ist.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="else steht immer ganz unten! Schau:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="entry = input('Gib etwas ein: ')\nif entry == 'hi':\n    print('Hallo!')\nelif entry == 'moin':\n    print('Hi Deutscher! :)')\nelse:\n    print('Was?!')", # \n macht den Zeilenumbruch!
            lexer=Python3Lexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l15_s3'

class PythonLektion15_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Wo steht else immer?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Unten angehängt.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Wo wir wollen.",
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
                    abschluss = self.manager.get_screen('python_l15_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l15_s4'

class PythonLektion15_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Welche Reihenfolge gilt beim If-Statement?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="if, elif, else",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="if, else, elif",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="elif, if, else",
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
                    abschluss = self.manager.get_screen('python_l15_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l15_s5'

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

class PythonLektion15_Screen5(Screen):
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
            text="name = input('Wie heißt du? ')\nif name != 'Elon Musk':\n    print('Glaubwürdig!')\nelse:\n    print('Hmm...')",        # Der Quiz-Code zweizeilig untereinander
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
            text="Das ist korrekt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)
        
        self.option2 = Button(
            text="Oben.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Ich frage mal GPT...",
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
                    abschluss = self.manager.get_screen('python_l15_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l15_s6'

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
    
class PythonLektion15_Screen6(Screen):
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
            text="Du schlägst dich echt gut muss man sagen...",
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
        fertig_button = FertigPulseButton(  #type:ignore
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(15) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'






# =============================================================================================================================
# PYTHON LEKTION 16: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion16_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Die Konsole - Teil 1",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Was ist eigentlich die Konsole?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Die Konsole ist das wichtigste Tool überhaupt!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne es zu nutzen!",
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
        self.manager.current = 'python_l16_s2'

class PythonLektion16_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Im Terminal (einer App unter Windows) können wir Befehle eingeben",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="die dann vom Computer durchgeführt werden. Aber die Konsole",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="kann mehr: Auch unsere Python-Programme werden dort ausgeführt,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="und alle print()-Ausgaben werden dort angezeigt. Schau dir einen Befehl an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="python --version", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l16_s3'

class PythonLektion16_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Was ist die Shell?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Ein Shellyfish.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="Eine Eingabe für Befehle oder eine Programmausgabe.",
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
                    abschluss = self.manager.get_screen('python_l16_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l16_s4'

class PythonLektion16_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Worüber werden unsere Programme ausgeführt?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Über das Terminal.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Über irgendeine App",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Über den Browser.",
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
                    abschluss = self.manager.get_screen('python_l16_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l16_s5'

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

class PythonLektion16_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde die richtige Aussage!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="# JIPPI kein Buggy-Code heute!",        # Der Quiz-Code zweizeilig untereinander
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
            text="Das Terminal ist wichtig.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Das Terminal ist sehr wichtig.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Das Terminal ist bewundernswert.",
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
                    abschluss = self.manager.get_screen('python_l16_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l16_s6'

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

class PythonLektion16_Screen6(Screen):
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
            text="Du hast das wichtigste Tool eines Devs drauf!",
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
        fertig_button = FertigPulseButton(  #type:ignore
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(16) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'






# =============================================================================================================================
# PYTHON LEKTION 17: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion17_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Die Konsole - Teil 2",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Wie dir vielleicht schon aufgefallen ist, hat dieses",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Tool verschiedene Namen - und wo brauche ich es als Dev?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Erfahre den Nutzen.",
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
        self.manager.current = 'python_l17_s2'

class PythonLektion17_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Das Terminal, auch Konsole oder Shell genannt, ist fast",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="überall, bei allen Entwickler-Tools eingebaut. Also Sachen wie:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Programmier-Editoren, im Betriebssystem oder auch im Internet.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Dort ist es meistens ein Bereich oder eine eigene App.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l17_s3'

class PythonLektion17_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Worin ist das Terminal eingebaut?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Bereich/App",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Subsystem",
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
                    abschluss = self.manager.get_screen('python_l17_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l17_s4'

class PythonLektion17_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Nutzen Devs die Konsole?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Nein.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Ja.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="Alle heiligen Zeilen.",
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
                    abschluss = self.manager.get_screen('python_l17_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l17_s5'

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

class PythonLektion17_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Finde die richtige Aussage!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="# Code ist jetzt mal unrelevant.",        # Der Quiz-Code zweizeilig untereinander
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
            text="Die Konsole nennt man auch Dev-Tools.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Anwendungsbereich? Lies weiter.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Das Terminal ist in fast jedem OS.",
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
                    abschluss = self.manager.get_screen('python_l17_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'python_l17_s6'

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

class PythonLektion17_Screen6(Screen):
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
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(17) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.manager.current = 'python_dashboard_2'






# =============================================================================================================================
# PYTHON LEKTION 18: DIE LERN SCREENS
# =============================================================================================================================

class PythonLektion18_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Die Konsole - Teil 3",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Zeit für etwas Praxis! Zeit das Terminal zu nutzen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Schalte deinen Computer ein, und warte mal. (Du brauchst Windows)",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Starten wir durch!",
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
        self.manager.current = 'python_l18_s2'

class PythonLektion18_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Jetzt, wo du deinen Windows-Computer eingeschaltet hast, werden",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="wir das Terminal (Konsole, Shell) auf dem Betriebssystem Windows",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="öffnen, um ein paar Befehle in die Tasten zu hauen! Bereit?",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Pass gut auf und befolge die Anweisungen genau. Viel Spaß!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l18_s3'

class PythonLektion18_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Also, öffnen wir das Terminal, indem du zuerst die Windows-Taste",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="drückst, und anschließend in das Eingabefeld eingibst: 'Terminal'",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Starte die angezeigte Terminal-App, indem du auf 'Öffnen' klickst.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Nun hast du ein mächtiges, schwarzes Terminal-Fenster vor dir!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l18_s4'

class PythonLektion18_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Am Anfang des Eingabefeldes siehst du z. B. deinen Benutzernamen unter Windows.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Du möchtest hier nun sicher einen Befehl eingeben, damit du die Möglichkeiten siehst, oder?",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Um uns z. B. alle Ordner unter Windows anzeigen zu lassen, gib den unten stehenden Befehl ein:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Nun listet dir das Terminal alle auf. Cool, oder?",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="ls", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l18_s5'

class PythonLektion18_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Am Ende deiner Auflistung siehst du wieder das vertraute Eingabefeld.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Möchtest du alle aktuellen Hintergrundprozesse anzeigen?",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Dann gib wieder den unten stehenden Befehl ein.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Hinweis: Diese Sprache nennen wir PowerShell!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="get-process", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l18_s6'

class PythonLektion18_Screen6(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Du hast nun das Terminal erfolgreich geöffnet, und auch bereits",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="deine ersten Befehle ausgeführt. Gut gemacht! Das schafft nicht jeder.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Du kannst jetzt stolz das Terminal über das X rechts oben schließen und den",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Computer herunterfahren. Genieße deinen wohlverdienten Feierabend!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="", # \n macht den Zeilenumbruch!
            lexer=PowerShellLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),               # Höhe angepasst für 2 Zeilen
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
        self.manager.current = 'python_l18_s7'

class PythonLektion18_Screen7(Screen):
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
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        
        self.coins_anzeige_label = Label(
            text="",
            font_size=45,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )

        grafik = Image(
            source='LTC_Maskottchen.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        # Der finale Fertig-Button
        fertig_button = FertigPulseButton(  #type:ignore
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
        layout.add_widget(self.coins_anzeige_label)
        layout.add_widget(grafik)

        # Startet bei 0 und nimmt die Punkte der Quiz-Screens auf
        self.lektions_xp = 0
        self.lektions_coins = 0

        # Ausführen:
        self.add_widget(layout)
    
    # *args hinzugefügt für stabile Kivy-Event-Verarbeitung
    def on_pre_enter(self, *args):
        self.lektions_coins = 50
        self.lektions_xp = 150
        self.xp_anzeige_label.text = f"Wegen Praxislektion hast du {self.lektions_xp} XP verdient!"
        self.coins_anzeige_label.text = f"Wegen Praxislektion hast du {self.lektions_coins} Münzen verdient!"
        
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

        gesamte_xp = aktuelle_xp + 150 # Ausnahme wegen Praxis.
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

        gesamte_coins = aktuelle_coins + 50 # Ausnahmnsweise 50 wegen Praxis.
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # Zurück zum Dashboard leiten
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        python_dashboard.lektion_erfolgreich(18) # Bei Screen L2_S6 hier eine 2, bei L3_S6 eine 3 eintragen!

        self.lektions_xp = 0
        self.lektions_coins = 0
        self.manager.current = 'python_dashboard_2'




