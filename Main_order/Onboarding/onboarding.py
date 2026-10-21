

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



# ==============================================================================================================================
# ERSTELLEN DER EINFÜHRUNGSSCREENS
# ==============================================================================================================================

# ERSTELLEN DES ERSTEN SCREENS: (Erklährung?)
class einführung_to_ltc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Erstellen der Objekte:
        welcome_label = Label(
            text="Willkommen bei LTC!",
            font_name="Roboto-Bold",
            font_size=80,
            size_hint=(1.0, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        learn1_label = Label(
            text="Lerne mit verschiedensten Technologien zu programmieren und",
            font_size=40,
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        learn2_label = Label(
            text="werde ein professioneller Entwickler! Meistere eine Lektion",
            font_size=40,
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        learn3_label = Label(
            text="nach der anderen und codiere deine eigenen Projekte!",
            font_size=40,
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        
        weiter_button = WeiterPulseButton( #type:ignore
            text="Weiter",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )

        # Binden des Buttons Funktion:
        weiter_button.bind(on_press=self.weiter_schalten)
        
        # Adden der Objekte:
        layout.add_widget(welcome_label)
        layout.add_widget(learn1_label)
        layout.add_widget(learn2_label)
        layout.add_widget(learn3_label)
        layout.add_widget(weiter_button)

        # Ausführen:
        self.add_widget(layout)

    def weiter_schalten(self, instance):
        self.manager.current = 'einführung2'

# ERSTELLEN DES ZWEITEN SCREENS: (Warum?)
class einführung_warum_ltc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        # Erstellen der Objekte:
        warum_coden_label = Label(
            text="Warum möchtest du coden lernen?",
            font_size=80,
            font_name="Roboto-Bold",
            size_hint=(0.5, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        wahl1_button = Button(
            text="Ein Projekt umsetzen",
            font_size=30,
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.35, 'center_y': 0.6}
        )
        wahl1_button.bind(on_press=lambda instance: self.motivation_speichern("Ein Projekt umsetzen"))

        wahl2_button = Button(
            text="Karriere voranbringen",
            font_size=30,
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.65, 'center_y': 0.6}
        )
        wahl2_button.bind(on_press=lambda instance: self.motivation_speichern("Karriere voranbringen"))

        wahl3_button = Button(
            text="Fähigkeiten verbessern",
            font_size=30,
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.35, 'center_y': 0.3}
        )
        wahl3_button.bind(on_press=lambda instance: self.motivation_speichern("Faehigkeiten verbessern"))

        wahl4_button = Button(
            text="Aus Spaß",
            font_size=30,
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.65, 'center_y': 0.3}
        )
        wahl4_button.bind(on_press=lambda instance: self.motivation_speichern("Aus Spass"))

        # Adden der Objekte:
        layout.add_widget(warum_coden_label)
        layout.add_widget(wahl1_button)
        layout.add_widget(wahl2_button)
        layout.add_widget(wahl3_button)
        layout.add_widget(wahl4_button)

        # Ausführen:
        self.add_widget(layout)

    def motivation_speichern(self, auswahl_text):
        app_ordner = App.get_running_app().user_data_dir
        datei_pfad = os.path.join(app_ordner, "motivation.txt")
        
        with open(datei_pfad, "w", encoding="utf-8") as datei:
            datei.write(f"Auswahl: {auswahl_text}\n")
        print(f"Sicher gespeichert unter: {datei_pfad}")

        self.manager.current = 'einführung3'

# Werbung für LTC dasein
class einführung_was_erreichen_ltc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title_label = Label(
            text="Was kannst du nach LTC?",
            font_size=60,
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        e1 = Label(
            text="Wenn du mit LTC durch bist, bist du in",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        e2 = Label(
            text="der Lage, selbst Software zu schreiben, zu warten",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        e3 = Label(
            text="und zu veröffentlichen. Du musst nichts mehr lernen.",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )

        e4 = Label(
            text="Du bekommst dein nötiges Wissen komplett durch LTC!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )

        weiter_button = WeiterPulseButton( #type:ignore
            text="Weiter",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            on_press=self.weiter_function
        )

        # Adden der Objekte:
        layout.add_widget(title_label)
        layout.add_widget(e1)
        layout.add_widget(e2)
        layout.add_widget(e3)
        layout.add_widget(e4)
        layout.add_widget(weiter_button)

        self.add_widget(layout)

    def weiter_function(self, instance):
        self.manager.current = 'einführung4'

class einführung_wie_viel_zeit_ltc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Wähle dein tägliches Ziel:",
            font_name='Roboto-Bold',
            font_size=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            on_press=self.weiter
        )

        option1 = Button(
            text="Locker",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            on_press=self.weiter
        )

        option2 = Button(
            text="Normal",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_press=self.weiter
        )

        option3 = Button(
            text="Intensiv",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            on_press=self.weiter
        )

       
        layout.add_widget(title)
        layout.add_widget(option1)
        layout.add_widget(option2)
        layout.add_widget(option3)
        self.add_widget(layout)

    def weiter(self, instance):
        self.manager.current = 'einführung5'

# ERSTELLEN DES DRITTEN SCREENS (Pfad?)
class einführung_pfad_ltc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        waehle_deinen_pfad = Label(
            text="Wähle deinen Pfad:",
            font_size=80,
            font_name="Roboto-Bold",
            size_hint=(0.5, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        grafik_python = Image(
            source="LTCPythonLogo.png",
            size_hint=(0.09, 0.09),
            pos_hint={'center_x': 0.23, 'center_y': 0.6}
        )
        
        grafik_html = Image(
            source="LTCHTMLLogo.png",
            size_hint=(0.09, 0.09),
            pos_hint={'center_x': 0.23, 'center_y': 0.45}
        )
        
        grafik_css = Image(
            source="LTCCSSLogo.png",
            size_hint=(0.09, 0.09),
            pos_hint={'center_x': 0.29, 'center_y': 0.45}
        )

        grafik_js = Image(
            source="LTCJavaScriptLogo.png",
             size_hint=(0.09, 0.09),
            pos_hint={'center_x': 0.35, 'center_y': 0.45}
        )
        
        # Auswahl und Co.:
        python_developer_pfad = Button(
            text="Python-Entwickler",
            font_size=40,
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        python_developer_pfad.bind(on_press=lambda instance: self.pfad_speichern("Python Developer"))
        
        web_developer_pfad = Button(
            text="Web-Entwickler",
            font_size=40,
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        web_developer_pfad.bind(on_press=lambda instance: self.pfad_speichern("Web Developer"))

        # Adden der Objekte:
        layout.add_widget(waehle_deinen_pfad)
        layout.add_widget(python_developer_pfad)
        layout.add_widget(web_developer_pfad)
        #layout.add_widget(grafik_python)
        #layout.add_widget(grafik_html)
        #layout.add_widget(grafik_css)
        #layout.add_widget(grafik_js)
        
        # Ausführen:
        self.add_widget(layout)

    def pfad_speichern(self, pfad_text):
        app_ordner = App.get_running_app().user_data_dir
        datei_pfad = os.path.join(app_ordner, "pfad.txt")
        
        with open(datei_pfad, "w", encoding="utf-8") as datei:
            datei.write(f"Pfad: {pfad_text}\n")
        print(f"Pfad sicher gespeichert unter: {datei_pfad}")

        if "Python" in pfad_text:
            self.manager.current = 'python_dashboard'
        elif "Web" in pfad_text:
            self.manager.current = 'web_dashboard'


