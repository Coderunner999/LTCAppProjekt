
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
# WEB LEKTION 1: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion1_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Willkommen im Web!",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Starte mit HTML, um deine eigenen Websites zu bauen!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Absolviere Lektionen und baue echte Kenntnisse auf!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Starten wir rein!",
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
        self.manager.current = 'web_l1_s2'

class WebLektion1_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Um in HTML zu coden, verwenden wir sogenannte Tags.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Dabei gibt es öffnende und schließende Tags wie <html> und </html>.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Der Code unserer Websites startet immer mit dem HTML-Tag.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir das Grundgerüst einer HTML-Website an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="<html>\n    Restlicher HTML Code...\n    Mehr Zeilen...\n</html>", # \n macht den Zeilenumbruch!
            lexer=HtmlLexer(),
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
        self.manager.current = 'web_l1_s3'

class WebLektion1_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Das ist ein schließender Tag:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<html>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="</button>",
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
                    abschluss = self.manager.get_screen('web_l1_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l1_s4'

class WebLektion1_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was ist ein Tag in HTML?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Eine Befehlsgruppe, die etwas darstellt.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Eine Art Befehl wie in JavaScript.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Ein Tag hat 24 Stunden.",
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
                        abschluss = self.manager.get_screen('web_l1_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'web_l1_s5'

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

class WebLektion1_Screen5(Screen):
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
            text="</html>\n<html>",        # Der Quiz-Code zweizeilig untereinander
            lexer=HtmlLexer(),
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
            text="Das HTML-Tag existiert nicht.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Die Tags sind verwechselt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Das ist ungültige Syntax.",
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
                    abschluss = self.manager.get_screen('web_l1_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l1_s6'

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

class WebLektion1_Screen6(Screen):
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
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix - JETZT AUCH FÜR WEB!)
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
            
        # ---------------------------------------------------------------------------------------------------------------------
        # WEB FORTSCHRITT AKTUALISIEREN & WECHSELN
        # ---------------------------------------------------------------------------------------------------------------------
        web_dashboard = self.manager.get_screen('web_dashboard') # Holt das korrekte Web-Dashboard
        web_dashboard.lektion_erfolgreich(1) # Übergibt die 1, da es Web-Lektion 1 ist

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard' # Wechselt zum Web-Dashboard






# =============================================================================================================================
# WEB LEKTION 2: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion2_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Überschriften",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Es gibt einen Tag, mit dem wir natürlich innerhalb",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="des HTML-Tags Überschriften erstellen können.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Starten wir rein!",
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
        self.manager.current = 'web_l2_s2'

class WebLektion2_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Um eine Überschrift zu erstellen, nutzen wir den H1, H2,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="H3-, H4-, H5- oder H6-Tag. H6 ist die kleinste Überschrift,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="und H1 ist die größte. Die anderen sind Zwischengrößen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Lass uns 3 Überschriften untereinander erstellen:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="<html>\n    <h1>Headline big</h1>\n    <h3>Headline middle</h3>\n    <h6>Headline small</h6>\n</html>", # \n macht den Zeilenumbruch!
            lexer=HtmlLexer(),
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
        self.manager.current = 'web_l2_s3'

class WebLektion2_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Was ist die größte Überschrift?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<h2>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="<h1>",
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
                    abschluss = self.manager.get_screen('web_l2_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l2_s4'

class WebLektion2_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was ist die kleinste Überschrift in HTML?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<h1>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="<h6>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="<h9>",
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
                        abschluss = self.manager.get_screen('web_l2_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'web_l2_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

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

class WebLektion2_Screen5(Screen):
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
            text="<html>\n    <h1>Breaking News<h1>\n</html>",        # Der Quiz-Code zweizeilig untereinander
            lexer=HtmlLexer(),
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
            text="Kein Fehler.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Der H1-Tag existiert nicht, nur H6.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)
        
        self.option3 = Button(
            text="Tag ist nicht richtig geschlossen.",
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
                    abschluss = self.manager.get_screen('web_l2_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l2_s6'

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

class WebLektion2_Screen6(Screen):
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
            text="Starke Überschriften hast du drauf!",
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
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix - JETZT AUCH FÜR WEB!)
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
            
        # ---------------------------------------------------------------------------------------------------------------------
        # WEB FORTSCHRITT AKTUALISIEREN & WECHSELN
        # ---------------------------------------------------------------------------------------------------------------------
        web_dashboard = self.manager.get_screen('web_dashboard') # Holt das korrekte Web-Dashboard
        web_dashboard.lektion_erfolgreich(2) # Übergibt die 1, da es Web-Lektion 1 ist

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard' # Wechselt zum Web-Dashboard






# =============================================================================================================================
# WEB LEKTION 3: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion3_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Paragraphen",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        

        erklährung_label1 = Label(
            text="Lerne über die besonders gebräuchlichen Paragraphen",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="in der Web-Technologie HTML!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Starten wir!",
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
        self.manager.current = 'web_l3_s2'

class WebLektion3_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        erklährung_label1 = Label(
            text="Was ist ein Paragraph in HTML? Ein Paragraph ist nichts",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="anderes als ein weiterer Tag, mit dem wir Text anzeigen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Der Paragraph verwendet dazu den P-Tag. Du denkst dir schon, wie",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="man ihn erstellt, oder? Schau mal:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        #  BEIDE VARIABLEN IN EINEM EINZIGEN, ZWEIZEILIGEN CODE-EDITOR
        code_source_gesamt = CodeInput(
            text="<html>\n    <h1>Paragraph is under me</h1>\n    <p>ICH BIN DER TEXT!!!</p>\n</html>", # \n macht den Zeilenumbruch!
            lexer=HtmlLexer(),
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
        self.manager.current = 'web_l3_s3'

class WebLektion3_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Tag erstellt einen Text?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<h1>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="<p>",
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
                    abschluss = self.manager.get_screen('web_l3_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l3_s4'

class WebLektion3_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was ist ein Paragraph eigentlich?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Text im Web",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Para im Web",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Ein schlechter Tag.",
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
                        abschluss = self.manager.get_screen('web_l3_s6')
                        abschluss.lektions_xp += 10
                        
                    return  # Auf den zweiten Klick warten
        
                # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
                instance.background_color = (1, 1, 1, 1)
                self.manager.current = 'web_l3_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

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

class WebLektion3_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # 1. Die Frage
        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        #  GENAU DER SELBE CODE-EDITOR WIE AUF SCREEN 2
        code_source_gesamt = CodeInput(
            text="<html>\n    <h1>Welcome to my Website!<h1>\n</html>",        # Der Quiz-Code zweizeilig untereinander
            lexer=HtmlLexer(),
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
            text="Hier fehlt nichts.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Ein Paragraph (P-Tag)",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)
        
        self.option3 = Button(
            text="Ein Text (T-Tag)",
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
                    abschluss = self.manager.get_screen('web_l3_s6')
                    abschluss.lektions_xp += 10
                    
                return  # Auf den zweiten Klick warten
    
            # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l3_s6'

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

class WebLektion3_Screen6(Screen):
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
            text="Der Paragraph ist ein starker Text!",
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
        # NEU: MÜNZEN IM HINTERGRUND SPEICHERN (10 Münzen fix - JETZT AUCH FÜR WEB!)
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
            
        # ---------------------------------------------------------------------------------------------------------------------
        # WEB FORTSCHRITT AKTUALISIEREN & WECHSELN
        # ---------------------------------------------------------------------------------------------------------------------
        web_dashboard = self.manager.get_screen('web_dashboard') # Holt das korrekte Web-Dashboard
        web_dashboard.lektion_erfolgreich(3) # Übergibt die 1, da es Web-Lektion 1 ist

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard' # Wechselt zum Web-Dashboard






# =============================================================================================================================
# WEB LEKTION 4: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion4_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Bilder",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        erklährung_label1 = Label(
            text="Mit HTML können wir nicht nur Texte anzeigen,",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="sondern auch Bilder in unsere Website einfügen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne den Bild-Tag kennen!",
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

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l4_s2'

class WebLektion4_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erklährung_label1 = Label(
            text="Um ein Bild einzufügen, verwenden wir den IMG-Tag.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        erklährung_label2 = Label(
            text="Die Bilddatei wird mit dem src-Attribut angegeben.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Das alt-Attribut beschreibt das Bild für Besucher.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir ein Beispiel an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <img src='bild.jpg' alt='Ein schönes Bild'>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
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

        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt)

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l4_s3'

class WebLektion4_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Tag fügt ein Bild ein?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<p>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="<img>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l4_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l4_s4'

class WebLektion4_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Mit welchem Attribut wird die Bilddatei angegeben?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="src",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="href",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="title",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l4_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l4_s5'

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

class WebLektion4_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <img bild.jpg alt='Bild'>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        self.option1 = Button(
            text="Das Bild ist zu groß.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Das src-Attribut fehlt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="Das HTML-Tag existiert nicht.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l4_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l4_s6'

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

class WebLektion4_Screen6(Screen):
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
            text="Du kannst jetzt Bilder in HTML einfügen!",
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

        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        self.lektions_xp = 0
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"

    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir

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

        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))

        web_dashboard = self.manager.get_screen('web_dashboard')
        web_dashboard.lektion_erfolgreich(4)

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'





# =============================================================================================================================
# WEB LEKTION 5: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion5_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Der Body-Tag",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        erklährung_label1 = Label(
            text="Der Body-Tag enthält den sichtbaren Inhalt",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="unserer HTML-Website.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne, wie man ihn verwendet!",
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

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l5_s2'

class WebLektion5_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erklährung_label1 = Label(
            text="Der Body-Tag steht innerhalb des HTML-Tags.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        erklährung_label2 = Label(
            text="Alles, was Besucher auf der Website sehen,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="kommt normalerweise in den Body-Bereich.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Hier ist ein einfaches Beispiel:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <body>\n        <h1>Meine Website</h1>\n        <p>Willkommen!</p>\n    </body>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
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

        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt)

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l5_s3'

class WebLektion5_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Tag enthält den sichtbaren Inhalt?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<head>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="<body>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l5_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l5_s4'

class WebLektion5_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was gehört in den Body-Bereich?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Überschriften und Texte",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Nur der HTML-Name",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Nur Kommentare",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l5_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l5_s5'

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

class WebLektion5_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <body>\n        <h1>Willkommen!</h1>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        self.option1 = Button(
            text="Der Body-Tag wird nicht geschlossen.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Der h1-Tag existiert nicht.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="HTML darf keinen Body enthalten.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l5_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l5_s6'

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

class WebLektion5_Screen6(Screen):
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
            text="Du kannst jetzt den Body-Tag verwenden!",
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

        fertig_button = FertigPulseButton(  #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        self.lektions_xp = 0
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"

    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir

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

        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))

        web_dashboard = self.manager.get_screen('web_dashboard')
        web_dashboard.lektion_erfolgreich(5)

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'






# =============================================================================================================================
# WEB LEKTION 6: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion6_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Der Head-Tag",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        erklährung_label1 = Label(
            text="Der Head-Tag enthält wichtige Informationen",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="über unsere HTML-Website.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne, wie man ihn verwendet!",
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

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l6_s2'

class WebLektion6_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erklährung_label1 = Label(
            text="Der Head-Tag steht innerhalb des HTML-Tags.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        erklährung_label2 = Label(
            text="Dort speichern wir Informationen für den Browser.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Diese Informationen sieht man meistens nicht direkt.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Hier ist ein einfaches Beispiel:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <head>\n        <title>Meine Website</title>\n    </head>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
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

        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt)

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l6_s3'

class WebLektion6_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welche Informationen stehen im Head-Tag?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Informationen für den Browser",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Nur sichtbare Überschriften",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l6_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l6_s4'

class WebLektion6_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Welcher Tag legt den Titel der Website fest?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<title>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="<h1>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="<name>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l6_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l6_s5'

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

class WebLektion6_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <head>\n        <title>Meine Website</title>\n    <body>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        self.option1 = Button(
            text="Der Head-Bereich wird nicht geschlossen.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Der Title-Tag ist falsch.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="HTML darf keinen Head-Bereich enthalten.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l6_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l6_s6'

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

class WebLektion6_Screen6(Screen):
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
            text="Du kannst jetzt den Head-Tag verwenden!",
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

        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        self.lektions_xp = 0
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"

    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir

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

        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))

        web_dashboard = self.manager.get_screen('web_dashboard')
        web_dashboard.lektion_erfolgreich(6)

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'







# =============================================================================================================================
# WEB LEKTION 7: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion7_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Links mit dem A-Tag",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        erklährung_label1 = Label(
            text="Mit Links können wir andere Websites",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="oder andere Seiten unseres Projekts öffnen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne den A-Tag kennen!",
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

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l7_s2'

class WebLektion7_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erklährung_label1 = Label(
            text="Der A-Tag erstellt einen anklickbaren Link.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        erklährung_label2 = Label(
            text="In href schreiben wir das Ziel des Links.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Der Text zwischen den A-Tags ist anklickbar.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Schau dir ein Beispiel an:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <a href='https://www.example.com'>\n        Website öffnen\n    </a>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
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

        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt)

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l7_s3'

class WebLektion7_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Tag erstellt einen Link?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<link>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="<a>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l7_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l7_s4'

class WebLektion7_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Wo steht das Ziel des Links?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="In href",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="In src",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="In alt",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l7_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l7_s5'

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

class WebLektion7_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <a href='https://www.example.com'>\n        Website öffnen\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        self.option1 = Button(
            text="Die Website ist nicht erreichbar.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="href darf nicht verwendet werden.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Der A-Tag wird nicht geschlossen.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                self.option2.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l7_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l7_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

class WebLektion7_Screen6(Screen):
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
            text="Du kannst jetzt Links mit dem A-Tag erstellen!",
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

        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        self.lektions_xp = 0
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"

    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir

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

        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))

        web_dashboard = self.manager.get_screen('web_dashboard')
        web_dashboard.lektion_erfolgreich(7)

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'






# =============================================================================================================================
# WEB LEKTION 8: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion8_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Ungeordnete Listen",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        erklährung_label1 = Label(
            text="Mit HTML können wir mehrere Dinge",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="übersichtlich untereinander anzeigen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Dafür verwenden wir den UL-Tag!",
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

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l8_s2'

class WebLektion8_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erklährung_label1 = Label(
            text="Der UL-Tag steht für eine ungeordnete Liste.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        erklährung_label2 = Label(
            text="Er fasst mehrere Listeneinträge zusammen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Die Liste wird normalerweise mit Punkten angezeigt.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Hier ist ein einfaches Beispiel:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <ul>\n        <li>HTML lernen</li>\n        <li>Websites bauen</li>\n    </ul>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
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

        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt)

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l8_s3'

class WebLektion8_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Tag erstellt eine ungeordnete Liste?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<ul>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="<list>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l8_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l8_s4'

class WebLektion8_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was zeigt der UL-Tag an?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Eine ungeordnete Liste",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Ein einzelnes Bild",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Eine Überschrift",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l8_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l8_s5'

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

class WebLektion8_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <ul>\n        <li>HTML lernen</li>\n        <li>Websites bauen</li>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        self.option1 = Button(
            text="Der UL-Tag wird nicht geschlossen.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Eine Liste darf keine Texte enthalten.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Der UL-Tag existiert nicht.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l8_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l8_s6'

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

class WebLektion8_Screen6(Screen):
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
            text="Du kannst jetzt ungeordnete Listen erstellen!",
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

        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        self.lektions_xp = 0
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"

    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir

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

        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))

        web_dashboard = self.manager.get_screen('web_dashboard')
        web_dashboard.lektion_erfolgreich(8)

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'







# =============================================================================================================================
# WEB LEKTION 9: DIE LERN SCREENS
# =============================================================================================================================

class WebLektion9_Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        welcome_label = Label(
            text="Listeneinträge mit LI",
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        erklährung_label1 = Label(
            text="Mit dem UL-Tag erstellen wir eine ungeordnete Liste.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Die einzelnen Einträge erstellen wir mit dem LI-Tag.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne, wie man Listeneinträge erstellt!",
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

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l9_s2'

class WebLektion9_Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        erklährung_label1 = Label(
            text="Der LI-Tag steht für einen einzelnen Listeneintrag.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        erklährung_label2 = Label(
            text="Jeder Eintrag kommt zwischen einen öffnenden",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="und einen schließenden LI-Tag.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Hier ist ein einfaches Beispiel:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <ul>\n        <li>HTML lernen</li>\n        <li>Websites bauen</li>\n        <li>Code schreiben</li>\n    </ul>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
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

        layout.add_widget(weiter_button)
        layout.add_widget(erklährung_label1)
        layout.add_widget(erklährung_label2)
        layout.add_widget(erklährung_label3)
        layout.add_widget(erklährung_label4)
        layout.add_widget(code_source_gesamt)

        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'web_l9_s3'

class WebLektion9_Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage1 = Label(
            text="Welcher Tag erstellt einen einzelnen Listeneintrag?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="<ul>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="<li>",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage1)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.false_answer = SoundLoader.load('false_answer.mp3')
        self.false_answer.play()
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l9_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l9_s4'

class WebLektion9_Screen4(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was steht normalerweise im LI-Tag?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        self.option1 = Button(
            text="Der Text eines Listeneintrags",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Nur der Titel der Website",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Eine Bilddatei",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l9_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l9_s5'

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

class WebLektion9_Screen5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Was fehlt in diesem Code?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        code_source_gesamt = CodeInput(
            text="<html>\n    <ul>\n        <li>HTML lernen\n        <li>Websites bauen</li>\n    </ul>\n</html>",
            lexer=HtmlLexer(),
            style=get_style_by_name('monokai'),
            font_size=32,
            size_hint=(0.6, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            readonly=True,
            use_bubble=True,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )

        self.option1 = Button(
            text="Der UL-Tag fehlt.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)

        self.option2 = Button(
            text="Der erste LI-Tag wird nicht geschlossen.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        self.option3 = Button(
            text="Der LI-Tag darf keinen Text enthalten.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.08}
        )
        self.option3.bind(on_press=self.antwort_falsch_option3)

        layout.add_widget(frage)
        layout.add_widget(code_source_gesamt)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        layout.add_widget(self.option3)

        self.fehler_gemacht = False
        self.add_widget(layout)

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                self.option3.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)
                self.true_answer = SoundLoader.load('true_answer.mp3')
                self.true_answer.play()

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l9_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l9_s6'

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

class WebLektion9_Screen6(Screen):
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
            text="Du kannst jetzt Listeneinträge erstellen!",
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

        fertig_button = FertigPulseButton( #type:ignore
            text="Fertig",
            font_size=40,
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        fertig_button.bind(on_press=self.lektion_beenden)

        layout.add_widget(erfolg_label1)
        layout.add_widget(fertig_button)
        layout.add_widget(motivation)
        layout.add_widget(self.xp_anzeige_label)
        layout.add_widget(grafik)

        self.lektions_xp = 0
        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.xp_anzeige_label.text = f"Du hast {self.lektions_xp} XP verdient!"

    def lektion_beenden(self, instance):
        app_ordner = App.get_running_app().user_data_dir

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

        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try:
                    aktuelle_coins = int(datei.read().strip())
                except:
                    aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        with open(coins_datei, "w", encoding="utf-8") as datei:
            datei.write(str(gesamte_coins))

        web_dashboard = self.manager.get_screen('web_dashboard')
        web_dashboard.lektion_erfolgreich(9)

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'

