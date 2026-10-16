



# ==============================================================================================================================
# IMPORTIEREN DER NÖTIGEN PAKETE
# ==============================================================================================================================

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


# ==============================================================================================================================
# HINTERGRUNDFARBE DER APP
# ==============================================================================================================================
Window.clearcolor = (0.1, 0.12, 0.15, 1)
# background_color = (0.72, 0.72, 0.72, 1)  # Farbe für Task-active

# ==============================================================================================================================
# RUNDE BUTTONS ERSTELLEN
# ==============================================================================================================================

# 1. Die originale __init__-Methode von Kivy sichern
original_init = Button.__init__

# 2. Neue __init__ mit plattformunabhängigen dp-Radien
def custom_init(self, **kwargs):
    original_init(self, **kwargs)
    
    # Wir starten die Schablone VOR dem Zeichnen des Buttons
    with self.canvas.before:
        StencilPush()
        self.stencil_before = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        StencilUse()
        
    # Wir schließen die Schablone NACH dem Zeichnen des Buttons wieder
    with self.canvas.after:
        StencilUnUse()
        # WICHTIG: Hier muss auch dp(30) stehen, damit die Maske deckungsgleich ist!
        self.stencil_after = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        StencilPop()
        
    # Die Maske muss mitwandern, wenn sich die Position oder Größe ändert
    self.bind(pos=update_stencil, size=update_stencil)

# 3. Hilfsfunktion, damit die runden Ecken bei Größenänderungen exakt mitgehen
def update_stencil(instance, *args):
    instance.stencil_before.pos = instance.pos
    instance.stencil_before.size = instance.size
    instance.stencil_before.radius = [dp(15)] # Aktualisiert den Radius in dp
    
    instance.stencil_after.pos = instance.pos
    instance.stencil_after.size = instance.size
    instance.stencil_after.radius = [dp(15)]  # Aktualisiert den Radius in dp

# 4. Die originale Kivy-Button Klasse global überschreiben
Button.__init__ = custom_init

# ==============================================================================================================================
# BESONDDERE PULSE BUTTONS
# ==============================================================================================================================

class FertigPulseButton(Button):
    # Kivy-Eigenschaft für das pulsierende Basis-Grün
    puls_farbe = ListProperty([0.12, 0.53, 0.22, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.3, 0.1)
        
        self.text = "Fertig"
        self.font_size = 40
        self.bold = True
        
        # Kivy-Standard-Hintergrund komplett deaktivieren
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        # 1. Textur für den weichen Verlauf erstellen
        # Ein vertikaler Streifen mit 2 Pixeln Höhe: Unten unsichtbar, oben weiß schimmernd
        self.glanz_textur = Texture.create(size=(1, 2), colorfmt='rgba')
        # Pixel-Daten im Hex-Format: 
        # Unten (0% Deckkraft): \xff\xff\xff\x00 | Oben (30% Deckkraft): \xff\xff\xff\x4c
        # Jetzt kommt das Weiß nach oben, da Kivy die Textur von unten nach oben liest
        pixel_daten = b'\xff\xff\xff\x4c' + b'\xff\xff\xff\x00'
        self.glanz_textur.blit_buffer(pixel_daten, colorfmt='rgba', bufferfmt='ubyte')

        with self.canvas.before:
            # 1. Der Haupt-Button (Basis-Grün, das pulsiert)
            self.bg_color = Color(rgba=self.puls_farbe)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            
            # 2. Der Lichtreflex (Nutzt die Verlaufstextur)
            Color(1, 1, 1, 1) # Volles Weiß, die Transparenz regelt die Textur
            self.reflex_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16], texture=self.glanz_textur)

        # Bindings für Größenänderungen und Bewegung
        self.bind(pos=self.grafik_aktualisieren, size=self.grafik_aktualisieren)
        self.bind(puls_farbe=self.farbe_anpassen)
        
        # Starte das Pulsieren des Hintergrunds
        self.animation_starten()

    def grafik_aktualisieren(self, *args):
        # Haupt-Button anpassen
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        # NEU: Der Ecken-Radius des Haupt-Buttons wächst dynamisch mit der Höhe mit!
        self.bg_rect.radius = [self.height * 0.25]
        
        # Lichtreflex berechnen: Sitzt harmonisch im oberen Bereich des Buttons
        eingerueckt_x = self.x + 4
        eingerueckt_y = self.y + (self.height * 0.35)
        breite_reflex = self.width - 8
        hoehe_reflex = self.height * 0.60
        
        self.reflex_rect.pos = (eingerueckt_x, eingerueckt_y)
        self.reflex_rect.size = (breite_reflex, hoehe_reflex)
        # NEU: Der Ecken-Radius des Lichtreflexes passt sich ebenfalls dynamisch an!
        self.reflex_rect.radius = [self.height * 0.20]


    def farbe_anpassen(self, instance, value):
        # Übergibt den animierten Farbwert an den Canvas-Hintergrund
        self.bg_color.rgba = value

    def animation_starten(self):
        # Weiches Pulsieren des Grüns über die Grafikkarte
        to_light = Animation(puls_farbe=[0.18, 0.68, 0.28, 1], duration=0.5, t='in_out_quad')
        to_dark = Animation(puls_farbe=[0.12, 0.53, 0.22, 1], duration=0.5, t='in_out_quad')
        
        puls_loop = to_light + to_dark
        puls_loop.repeat = True
        puls_loop.start(self)

class BuyPulseButton(Button):
    # Kivy-Eigenschaft für das pulsierende Basis-Grün
    puls_farbe = ListProperty([0.12, 0.53, 0.22, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Aktiviert die prozentuale Anpassung: 30% Breite (0.3), 10% Höhe (0.1)
        self.size_hint = (0.3, 0.1)
        
        # Festgelegter Premium-Preis für deinen Münz-Shop
        self.text = "€ 3,99"
        self.font_size = 28
        self.bold = True
        
        # Kivy-Standard-Hintergrund komplett deaktivieren
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        # 1. Textur für den weichen Verlauf erstellen
        self.glanz_textur = Texture.create(size=(1, 2), colorfmt='rgba')
        pixel_daten = b'\xff\xff\xff\x4c' + b'\xff\xff\xff\x00'
        self.glanz_textur.blit_buffer(pixel_daten, colorfmt='rgba', bufferfmt='ubyte')

        with self.canvas.before:
            # 1. Der Haupt-Button (Basis-Grün, das pulsiert)
            self.bg_color = Color(rgba=self.puls_farbe)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            
            # 2. Der Lichtreflex (Nutzt die Verlaufstextur)
            Color(1, 1, 1, 1)
            self.reflex_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12], texture=self.glanz_textur)

        # Bindings für Größenänderungen und Bewegung
        self.bind(pos=self.grafik_aktualisieren, size=self.grafik_aktualisieren)
        self.bind(puls_farbe=self.farbe_anpassen)
        
        # Starte das Pulsieren des Hintergrunds
        self.animation_starten()

    def grafik_aktualisieren(self, *args):
        # Haupt-Button anpassen
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_rect.radius = [self.height * 0.25]
        
        # Lichtreflex berechnen: Sitzt harmonisch im oberen Bereich des Buttons
        eingerueckt_x = self.x + 4
        eingerueckt_y = self.y + (self.height * 0.35)
        breite_reflex = self.width - 8
        hoehe_reflex = self.height * 0.60
        
        self.reflex_rect.pos = (eingerueckt_x, eingerueckt_y)
        self.reflex_rect.size = (breite_reflex, hoehe_reflex)
        self.reflex_rect.radius = [self.height * 0.20]

    def farbe_anpassen(self, instance, value):
        self.bg_color.rgba = value

    def animation_starten(self):
        to_light = Animation(puls_farbe=[0.18, 0.68, 0.28, 1], duration=0.5, t='in_out_quad')
        to_dark = Animation(puls_farbe=[0.12, 0.53, 0.22, 1], duration=0.5, t='in_out_quad')
        
        puls_loop = to_light + to_dark
        puls_loop.repeat = True
        puls_loop.start(self)

class WeiterPulseButton(Button):
    # Kivy-Eigenschaft für das pulsierende Basis-Grün
    puls_farbe = ListProperty([0.12, 0.53, 0.22, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Aktiviert die prozentuale Anpassung: 30% Breite (0.3), 10% Höhe (0.1)
        self.size_hint = (0.3, 0.1)
        
        self.text = "Weiter"
        self.font_size = 28
        self.bold = True
        
        # Kivy-Standard-Hintergrund komplett deaktivieren
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        # 1. Textur für den weichen Verlauf erstellen
        self.glanz_textur = Texture.create(size=(1, 2), colorfmt='rgba')
        # Weiß kommt nach oben, da Kivy die Textur von unten nach oben liest
        pixel_daten = b'\xff\xff\xff\x4c' + b'\xff\xff\xff\x00'
        self.glanz_textur.blit_buffer(pixel_daten, colorfmt='rgba', bufferfmt='ubyte')

        with self.canvas.before:
            # 1. Der Haupt-Button (Basis-Grün, das pulsiert)
            self.bg_color = Color(rgba=self.puls_farbe)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            
            # 2. Der Lichtreflex (Nutzt die Verlaufstextur)
            Color(1, 1, 1, 1) # Volles Weiß, die Transparenz regelt die Textur
            self.reflex_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[16], texture=self.glanz_textur)

        # Bindings für Größenänderungen und Bewegung
        self.bind(pos=self.grafik_aktualisieren, size=self.grafik_aktualisieren)
        self.bind(puls_farbe=self.farbe_anpassen)
        
        # Starte das Pulsieren des Hintergrunds
        self.animation_starten()

    def grafik_aktualisieren(self, *args):
        # Haupt-Button anpassen
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        # Der Ecken-Radius wächst oder schrumpft jetzt dynamisch mit der Button-Höhe mit!
        self.bg_rect.radius = [self.height * 0.25]
        
        # Lichtreflex berechnen: Sitzt harmonisch im oberen Bereich des Buttons
        eingerueckt_x = self.x + 4
        eingerueckt_y = self.y + (self.height * 0.35)
        breite_reflex = self.width - 8
        hoehe_reflex = self.height * 0.60
        
        self.reflex_rect.pos = (eingerueckt_x, eingerueckt_y)
        self.reflex_rect.size = (breite_reflex, hoehe_reflex)
        self.reflex_rect.radius = [self.height * 0.20]

    def farbe_anpassen(self, instance, value):
        # Übergibt den animierten Farbwert an den Canvas-Hintergrund
        self.bg_color.rgba = value

    def animation_starten(self):
        # Weiches Pulsieren des Grüns über die Grafikkarte
        to_light = Animation(puls_farbe=[0.18, 0.68, 0.28, 1], duration=0.5, t='in_out_quad')
        to_dark = Animation(puls_farbe=[0.12, 0.53, 0.22, 1], duration=0.5, t='in_out_quad')
        
        puls_loop = to_light + to_dark
        puls_loop.repeat = True
        puls_loop.start(self)

class WidgetButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Wir schalten die eckigen Kivy-Standardbilder ab,
        # damit sie nicht unter unserem abgerundeten Button hervorgucken
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0) # Macht den alten Hintergrund unsichtbar

        # Wir zeichnen den Button komplett eigenständig und sauber im canvas.before
        with self.canvas.before:
            # Das ist die normale, dunkelblaue/graue Kivy-Standardfarbe des Buttons
            # (Ändere die Werte, falls dein Button eine andere Farbe haben soll)
            self.bg_color = Color(0.12, 0.16, 0.22, 1) 
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        # Den weißen Rand zeichnen wir in canvas.after, damit er sauber oben liegt
        with self.canvas.after:
            self.border_color = Color(1, 1, 1, 1) # Weißer Rand
            self.custom_border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(15)),
                width=dp(2)
            )

        # Das hier sorgt für die visuelle Reaktion, wenn man den Button drückt
        self.bind(state=self._update_pressed_color)
        # Und das hier hält das Layout synchron
        self.bind(pos=self._update_layout, size=self._update_layout)

    def _update_pressed_color(self, instance, value):
        # Wenn gedrückt, wird der Button etwas heller/bläulicher (wie der Kivy-Standard)
        if value == 'down':
            self.bg_color.rgba = (0.18, 0.24, 0.35, 1)
        else:
            self.bg_color.rgba = (0.12, 0.16, 0.22, 1)

    def _update_layout(self, *args):
        # Diese Funktion zieht die Grafiken NUR auf die Größe, die das Layout vorgibt!
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        self.custom_border.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(15)
        )

class CodeInput(CodeInput):
    def __init__(self, **kwargs):
        # Wir erzwingen hier in der Klasse direkt, dass size_hint_y immer None ist!
        kwargs['size_hint_y'] = None
        super().__init__(**kwargs)
        
        # 1. Kivy-Standardhintergrund komplett abschalten
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0) # 100% transparent innen

        # 2. Dein gewünschtes Padding für den Abstand zum Rand
        self.padding = [dp(15), dp(15), dp(15), dp(15)]

        # 3. Schablone (Stencil) für den Text-Anschnitt im canvas.before
        with self.canvas.before:
            StencilPush()
            self.stencil = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            StencilUse()

        # 4. Der weiße, 2dp dicke Rahmen im canvas.after
        with self.canvas.after:
            StencilUnUse()
            StencilPop()

            Color(1, 1, 1, 1) # Weißer Rand
            self.custom_border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(15)),
                width=dp(2) # 2dp Dicke
            )

        # 5. Automatische Event-Bindungen für Layout und Textänderungen
        self.bind(pos=self._update_layout, size=self._update_layout)
        self.bind(minimum_height=self._adjust_height)
        
        # Einmalige Initialisierung der Höhe beim Start
        self.height = self.minimum_height

    def _adjust_height(self, instance, value):
        # Setzt die Höhe des Widgets atomar auf den exakt benötigten Textplatz
        self.height = value

    def _update_layout(self, *args):
        # Hält die Grafik-Elemente synchron mit der berechneten Größe
        self.stencil.pos = self.pos
        self.stencil.size = self.size

        self.custom_border.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(15)
        )

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
        
        weiter_button = WeiterPulseButton(
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

        weiter_button = WeiterPulseButton(
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
           
# =============================================================================================================================
# UNIVERSELLER AMPEL-BUTTON
# =============================================================================================================================

class FarbigerLektionsButton(Button):
    def __init__(self, lektions_id, status="gesperrt", **kwargs):
        super().__init__(**kwargs)
        # Feste Groesse fuer ein rundes/quadratisches Aussehen im Dashboard
        self.size_hint = (None, None)
        self.size = (140, 140)
        
        self.lektions_id = lektions_id
        self.status = status
        
        self.text = str(lektions_id)
        self.font_size = 40
        self.font_name = "Roboto-Bold"
        
        self.farbe_aktualisieren(status)

    def farbe_aktualisieren(self, neuer_status):
        self.status = neuer_status
        
        # WICHTIG: Stoppt JEDE laufende Kivy-Animation auf diesem Button,
        # bevor wir eine neue Farbe zuweisen! Das verhindert das Dreifach-Blinken.
        Animation.cancel_all(self)

        if neuer_status == "erledigt":
            #self.background_color = (0.2, 0.8, 0.2, 1) # Gruen
            self.background_color = (0.25, 0.55, 0.95, 1)

        elif neuer_status == "aktiv":
            #self.background_color = (1, 0.7, 0, 1)     # Gelb
            self.background_color = (0.85, 0.92, 0.98, 1)

            # Puls-Animation starten
            to_dark = Animation(background_color=(0.4, 0.4, 0.4, 1), duration=1.5, t='in_out_quad')
            to_light = Animation(background_color=(0.85, 0.92, 0.98, 1), duration=1.5, t='in_out_quad')
            
            puls_loop = to_dark + to_light
            puls_loop.repeat = True
            puls_loop.start(self)

        else:
            self.background_color = (0.4, 0.4, 0.4, 1) # Grau

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
            text="Variablen kennst du aus der Mathematik, dort sind sie",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Platzhalter für Zahlen. Ähnlich ist es auch in Python.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Mit Variablen können wir belibige Dinge im Code speichern",
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
            text="Welcher Code erstellt eine Variable namens schedule,",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        frage2 = Label(
            text="und weißt ihr den Wert 3 zu?",
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
        self.fehler_gemacht = True  # Korrigiert: Fehler wird registriert

    def antwort_richtig(self, instance):
        # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
        if instance.background_color != [0.25, 0.55, 0.95, 1]:
            self.option1.background_color = (1, 1, 1, 1)
            if hasattr(self, 'option3'):
                self.option3.background_color = (1, 1, 1, 1)
            
            # Button wird beim 1. Klick marineblau gefärbt
            instance.background_color = (0.25, 0.55, 0.95, 1)
            
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
            text="Keine ist richtig.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Diesen Vorgang nennen wir auch AKTUALISIEREN",
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
            text="Durch was aktualisieren wir Variablen?",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="können wir selbstverständlicherweise auch mit diesen Zahlen rechnen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Dazu definieren wir mindestens 2 Variablen, mit jeweils 2 Zahlen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Anschließend rechnet eine dritte Variable das Ergebnis der andren aus!",
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
            text="Zufälliger generierung.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="Ein dritten (solution) Variable.",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
                # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
                if instance.background_color != [0.25, 0.55, 0.95, 1]:
                    self.option1.background_color = (1, 1, 1, 1)
                    if hasattr(self, 'option3'):
                        self.option3.background_color = (1, 1, 1, 1)
                    
                    # Button wird beim 1. Klick marineblau gefärbt
                    instance.background_color = (0.25, 0.55, 0.95, 1)
                    
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Wir haben bereits gelernt Texte und Zahlen zu speichern usw.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Wir wissen aber noch nicht wie wir Texte am Screen anzeigen!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Dazu verwenden wir den sogenannten print() Befehl.",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Was ist wenn wir aber Variablen (ihren Inhalt) anzeigen wollen?",
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
            text="Beim anzeigen von Variablen lassen wir die ... weg:",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Der Code ist nicht Python!",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Du hast bereits gesehen das es verschiedene Werte gibt:",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="Zahlen, und Texte. Aber was ist das genau und wie läuft es?",
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
            text="String = Text, Integer = Ganze Zahl, Float = Dezi.Zahl, Boolean = Richtig/Falsch",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Das Wort (Abteil) am Anfang sagt uns zu was es werden soll.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Der Wert in den Klammern ist das WAS umgewandelt werden soll!",
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
            text="Dieser Befehl wandelt den Wert in den Klammern zu einer Dezimalzahl um:",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
            text="Wo ist der zu umwandelde Wert?",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Kein String zu Boolean!",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Wir wissen wie wir einfache Typen umwandeln, gut.",
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
            text="in einer einzigen brillianten Zeile tun!",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Kein String zu Boolean!",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Um die Nutzereingabe zu speichern schreiben wir alles",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="in eine Variable. Das können wir später verwenden!",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="nacher wollen wir die Nutzereingabe wieder printen.",
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
            text="Dieser Befhl erstellt Eingaben:",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Ein Script Kiddie!",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Super, ersten Abschnitt hast du fertig!",
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
        fertig_button = FertigPulseButton(
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
            text="Kommentieren wir in mit #. Das ist für die Wartung wichtig!",
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
            text="Nach jeden # kommt der dazugehörige Code.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Danach lassen wir eine Zeile frei, und es kommt",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="ein weiterer # und wieder Code, usw.",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Dazu benötigen sie Bedingungen (If Statement)",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )

        erklährung_label3 = Label(
            text="Lerne neues!",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Mit == können wir in einem if prüfen ob zwei Werte",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="den gleischen Inhalt besitzen. Wenn das stimmt, das",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Ergebnis also True ist, wird der if-Block ausgeführt.",
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
            text="Der Operator == prüft ob ...",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
            text="Was die Bedingung ergeben, damit es ausgeführt wird?",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Um mit einem if zu überprüfen ob zwei Werte",
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
            text="on zwei Werte unterschiedlich sind. Ist das Ergebnis True,",
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
            text="Was prüft der != Operator?",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
            text="SyntaxFehler.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="den klassichen elif-Befehl. Er wird unten nach if angehängt.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Es ist als würde man sagen: Ist if False, versuche noch elif.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Wir können so viele elif schreiben wir wir wollen, Python probiert",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="jeden elif-Block nacheinander aus. Sieh's dir an:",
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
            text="Soviele wie wir wollen",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
            text="Den elif, dann erst if.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_falsch_option2)

        self.option3 = Button(
            text="Den if, dass erst elif.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Was wenn wir bei einem if-Block etwas besonderes tun wollen",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label2 = Label(
            text="was nur passiert wenn alle Bedingungen False sind?",
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
            text="Um eine Ausweichmöglichkeit, wenn der if und alle elifs",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="False sind, zu programmieren, verwenden wir else.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Else wird nur ausgeführt wenn alles davor komplett False ist.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Der Else ist immer komplett unten angehängt! Schau:",
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
            text="Wo ist der else immer?",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Die Konsole ist das wichtigste Tool denn je!",
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
            text="Im Terminal (App auf Windows) können wir Befehle eingeben",
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
            text="und alle print() werden dort angezeigt. Schau dir einen Befehl an:",
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
            text="Eine Befehlseingabe/Programmausgabe",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Die Terminal ist wichtig.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Wie dir viellciht schon aufgefallen ist, hat dieses",
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
            text="Das Terminal, Konsole, oder auch Shell genannt, ist fast",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="überall, bei allen Entwickler-Tools eingebaut. Also Sachen wie:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Programmier-Editoren, im Betriebsystem, oder auch im Internet.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Dort ist es meistens ein Bereich, oder eine ganze eigene App.",
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
            text="Als was ist das Terminal eingebaut?",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Die Konsole nennt man auch: Dev-Tools.",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.option1.bind(on_press=self.antwort_falsch_option1)
        
        self.option2 = Button(
            text="Anwedungsbereich? Lesen.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="Jetzt wo du deinen Windows-Computer eingeschaltet hast, werden",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="wir das Terminal (Konsole, Shell) auf dem Betriebsystem Windows",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="öffnen, um ein paar Befehle in die Tasten zu hauen! Bereit?",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Pass gut auf, und befolge den Anweisungen genau, viel Spaß!",
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
            text="Am Anfang des Eingabefeldes siehst du z.b deinen Benutzernamen auf Windows.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        erklährung_label2 = Label(
            text="Du möchtest hier nun sicher einen Befehl eingeben, damit du die Macht siehst nicht?",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Um uns z.b alle Ordner auf Windows anzeigen zu lassen, gib den unteren Befehl ein:",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        erklährung_label4 = Label(
            text="Nun werden sie dir alle vom Terminal aufgelistet, cool oder?",
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
            text="Dann gib den wieder den unteren Befehl ein.",
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
            text="deine ersten befehle durchgeführt. Gut gemacht! Das schafft nicht jeder.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Du kannst jetzt stolz, das Terminal rechts oben, durch das X schließen, und den",
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
        fertig_button = FertigPulseButton(
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
            text="Starte mit HTML um deine eigenen Websites zu bauen!",
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
            text="Dabei gibt es öffnende Tags, und schließende Tags wie: <html>, </html>",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
            text="Eine Befehlsgruppe die etwas darstellt.",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_richtig)

        self.option2 = Button(
            text="Eine Art Befehl, wie in Javascript.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Ein HTML-Tag existiert nicht.",
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Du bist deinen Zielen einen schritt näher!",
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
        fertig_button = FertigPulseButton(
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
            text="H3, H4, H5, oder H6 Tag. H6 ist die kleinste Überschrift,",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Und H1 ist die allergrößte. Die anderen sind Zwischengrößen.",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
            text="anderes, als ein weiterer Tag mit dem wir Text anzeigen.",
            font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        erklährung_label3 = Label(
            text="Der Paragraph verwendet dazu den P-Tag. Du denkst dir schon wie",
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            # 1. Klick-Prüfung: Ist der Button noch nicht im edlen Marineblau?
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                if hasattr(self, 'option3'):
                    self.option3.background_color = (1, 1, 1, 1)
                
                # Button wird beim 1. Klick marineblau gefärbt
                instance.background_color = (0.25, 0.55, 0.95, 1)
                
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
            text="Ein Paragraph ist eigentlich ein?",
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
        self.fehler_gemacht = True

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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
        fertig_button = FertigPulseButton(
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)

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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l4_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l4_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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
            text="Der HTML-Tag existiert nicht.",
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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l4_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l4_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

        fertig_button = FertigPulseButton(
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)

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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l5_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l5_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l5_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l5_s6'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

        fertig_button = FertigPulseButton(
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)

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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l6_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l6_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l6_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l6_s6'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

        fertig_button = FertigPulseButton(
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)

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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l7_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l7_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l7_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l7_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
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

        fertig_button = FertigPulseButton(
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option2.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)

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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l8_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l8_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l8_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l8_s6'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

        fertig_button = FertigPulseButton(
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
        self.fehler_gemacht = True

    def antwort_richtig(self, instance):
            if instance.background_color != [0.25, 0.55, 0.95, 1]:
                self.option1.background_color = (1, 1, 1, 1)
                instance.background_color = (0.25, 0.55, 0.95, 1)

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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l9_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l9_s5'

    def antwort_falsch_option2(self, instance):
        self.option2.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

                if not self.fehler_gemacht:
                    abschluss = self.manager.get_screen('web_l9_s6')
                    abschluss.lektions_xp += 10

                return

            instance.background_color = (1, 1, 1, 1)
            self.manager.current = 'web_l9_s6'

    def antwort_falsch_option1(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)
        self.fehler_gemacht = True

    def antwort_falsch_option3(self, instance):
        self.option3.background_color = (0.9, 0.3, 0.3, 1)
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

        fertig_button = FertigPulseButton(
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

# =============================================================================================================================
# ERSTELLEN DER SCREENS FÜR DIE MENÜLEISTE
# =============================================================================================================================

class AITutor_Screen_Web(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        start_chat = Button(
            text="Starte den AI Coding Tutor",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=lambda x: webbrowser.open("https://ltctutor-mobile.netlify.app")
        )
        self.layout.add_widget(start_chat)
        ad_label = Label(
           text="Frage, Lerne, und Übe mit dem AI Coding Tutor!",
           font_size='14sp',
           pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(ad_label)

        headline_label = Label(
            text="AI Coding Tutor",
            font_size='24sp',
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.layout.add_widget(headline_label)
        ai_grafik = Image(
            source='AI_Image.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.layout.add_widget(ai_grafik)
        
        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
                
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                        
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
                
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
                
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
                
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )
                
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)

        self.layout.add_widget(card_menu)
        self.layout.add_widget(lernen_button_menu)
        self.layout.add_widget(ai_tutor_button_menu)
        self.layout.add_widget(profil_button_menu)
        self.layout.add_widget(üben_button_menu)

        self.add_widget(self.layout)

    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen_web'

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'web_dashboard'

    def trainingfunc(self, instance):
        self.manager.current = 'training_web'

class AITutor_Screen_Python_2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        start_chat = Button(
            text="Starte den AI Coding Tutor",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=lambda x: webbrowser.open("https://ltctutor-mobile.netlify.app")
        )
        self.layout.add_widget(start_chat)
        ad_label = Label(
            text="Frage, Lerne, und Übe mit dem AI Coding Tutor!",
            font_size='14sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(ad_label)
        
        headline_label = Label(
            text="AI Coding Tutor",
            font_size='24sp',
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.layout.add_widget(headline_label)
        ai_grafik = Image(
            source='AI_Image.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.layout.add_widget(ai_grafik)


        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
                
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                        
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
                
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
                
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
                
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )
                
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)

        self.layout.add_widget(card_menu)
        self.layout.add_widget(lernen_button_menu)
        self.layout.add_widget(ai_tutor_button_menu)
        self.layout.add_widget(profil_button_menu)
        self.layout.add_widget(üben_button_menu)

        self.add_widget(self.layout)

    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen_2'

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'python_dashboard_2'

    def trainingfunc(self, instance):
        self.manager.current = 'training_python_2'

class AITutor_Screen_Python(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        start_chat = Button(
            text="Starte den AI Coding Tutor",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=lambda x: webbrowser.open("https://ltctutor-mobile.netlify.app")
        )
        self.layout.add_widget(start_chat)
        ad_label = Label(
            text="Frage, Lerne, und Übe mit dem AI Coding Tutor!",
            font_size='14sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(ad_label)
        
        headline_label = Label(
            text="AI Coding Tutor",
            font_size='24sp',
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.layout.add_widget(headline_label)
        ai_grafik = Image(
            source='AI_Image.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.layout.add_widget(ai_grafik)

        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
                
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                        
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
                
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
                
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
                
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )
                
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)

        self.layout.add_widget(card_menu)
        self.layout.add_widget(lernen_button_menu)
        self.layout.add_widget(ai_tutor_button_menu)
        self.layout.add_widget(profil_button_menu)
        self.layout.add_widget(üben_button_menu)

        self.add_widget(self.layout)

    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen'

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'python_dashboard'

    def trainingfunc(self, instance):
        self.manager.current = 'training_python'

class Profil_Screen_Python(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Erstellen der Objekte:
        learner = Label(
            text="Deine Fortschritte:",
            font_size=80,
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        
        xp_card = Button(
            text="",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_label = Label(
            text="XP: Laden...",
            font_size=50,
            font_name='Roboto-Bold',
            color=(0.3, 0.6, 0.9, 1), # Ein schönes Mimo-Blau
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        
        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
        
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)



        reset_button = Button(
            text="Reset",
            font_size=40,
            size_hint=(0.15, 0.08),
            pos_hint={'center_x': 0.9, 'y': 0.9}, # Schon an deiner neuen Position!
            background_color=(0.9, 0.3, 0.3, 1) # Macht den Button roetlich
        )
        reset_button.bind(on_press=self.fortschritt_zuruecksetzen)
        

        # Adden der Objekte:
        layout.add_widget(card_menu)
        layout.add_widget(lernen_button_menu)
        layout.add_widget(profil_button_menu)
        layout.add_widget(learner)
        layout.add_widget(xp_card)
        layout.add_widget(self.xp_label)
        layout.add_widget(reset_button)
        layout.add_widget(üben_button_menu)
        layout.add_widget(ai_tutor_button_menu)

        # Ausführen:
        self.add_widget(layout)

    def on_enter(self, *args):
        app = App.get_running_app()
        xp_datei = os.path.join(app.user_data_dir, "xp.txt")
        gesamt_xp = 0
        
        # Prüfen, ob die Datei existiert und XP auslesen
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    gesamt_xp = int(datei.read().strip())
                except:
                    gesamt_xp = 0 # Falls die Datei leer oder fehlerhaft ist
                    
        # Label-Text live updaten
        self.xp_label.text = f"XP: {gesamt_xp}"

    def zu_profil_wechseln(self, instance):
        pass

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'python_dashboard'
    
    def fortschritt_zuruecksetzen(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        motivation_datei = os.path.join(app_ordner, "motivation.txt")
        pfad_datei = os.path.join(app_ordner, "pfad.txt")
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        xp_datei = os.path.join(app_ordner, "xp.txt")
        coins_datei = os.path.join(app_ordner, "coins.txt")
        
        if os.path.exists(motivation_datei):
            os.remove(motivation_datei)
        if os.path.exists(pfad_datei):
            os.remove(pfad_datei)
        if os.path.exists(fortschritt_datei):
            os.remove(fortschritt_datei)
        if os.path.exists(xp_datei):
            os.remove(xp_datei)
        if os.path.exists(coins_datei):
            os.remove(coins_datei)

        
        python_dashboard = self.manager.get_screen('python_dashboard')
        for nummer, btn in python_dashboard.alle_buttons.items():
            if nummer == 1:
                btn.farbe_aktualisieren("aktiv")
            else:
                btn.farbe_aktualisieren("gesperrt") 

        print("Fortschritt und XP erfolgreich gelöscht!")
        self.manager.current = 'einführung1'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_python'

    def trainingfunc(self, instance):
        self.manager.current = 'training_python'

class Profil_Screen_Python_2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Erstellen der Objekte:
        learner = Label(
            text="Deine Fortschritte:",
            font_size=80,
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        
        xp_card = Button(
            text="",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_label = Label(
            text="XP: Laden...",
            font_size=50,
            font_name='Roboto-Bold',
            color=(0.3, 0.6, 0.9, 1), # Ein schönes Mimo-Blau
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        
        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
        
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )

        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)



        reset_button = Button(
            text="Reset",
            font_size=40,
            size_hint=(0.15, 0.08),
            pos_hint={'center_x': 0.9, 'y': 0.9}, # Schon an deiner neuen Position!
            background_color=(0.9, 0.3, 0.3, 1) # Macht den Button roetlich
        )
        reset_button.bind(on_press=self.fortschritt_zuruecksetzen)
        

        # Adden der Objekte:
        layout.add_widget(card_menu)
        layout.add_widget(lernen_button_menu)
        layout.add_widget(profil_button_menu)
        layout.add_widget(learner)
        layout.add_widget(xp_card)
        layout.add_widget(self.xp_label)
        layout.add_widget(reset_button)
        layout.add_widget(üben_button_menu)
        layout.add_widget(ai_tutor_button_menu)

        # Ausführen:
        self.add_widget(layout)

    def on_enter(self, *args):
        app = App.get_running_app()
        xp_datei = os.path.join(app.user_data_dir, "xp.txt")
        gesamt_xp = 0
        
        # Prüfen, ob die Datei existiert und XP auslesen
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    gesamt_xp = int(datei.read().strip())
                except:
                    gesamt_xp = 0 # Falls die Datei leer oder fehlerhaft ist
                    
        # Label-Text live updaten
        self.xp_label.text = f"XP: {gesamt_xp}"

    def zu_profil_wechseln(self, instance):
        pass

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'python_dashboard_2'
    
    def fortschritt_zuruecksetzen(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        motivation_datei = os.path.join(app_ordner, "motivation.txt")
        pfad_datei = os.path.join(app_ordner, "pfad.txt")
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        xp_datei = os.path.join(app_ordner, "xp.txt")
        coins_datei = os.path.join(app_ordner, "coins.txt")
        
        if os.path.exists(motivation_datei):
            os.remove(motivation_datei)
        if os.path.exists(pfad_datei):
            os.remove(pfad_datei)
        if os.path.exists(fortschritt_datei):
            os.remove(fortschritt_datei)
        if os.path.exists(xp_datei):
            os.remove(xp_datei)
        if os.path.exists(coins_datei):
            os.remove(coins_datei)

        
        python_dashboard = self.manager.get_screen('python_dashboard_2')
        for nummer, btn in python_dashboard.alle_buttons.items():
            if nummer == 1:
                btn.farbe_aktualisieren("aktiv")
            else:
                btn.farbe_aktualisieren("gesperrt") 

        print("Fortschritt und XP erfolgreich gelöscht!")
        self.manager.current = 'einführung1'

    def trainingfunc(self, instance):
        self.manager.current = 'training_python_2'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_python_2'

class Profil_Screen_Web(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Erstellen der Objekte:
        learner = Label(
            text="Deine Fortschritte:",
            font_size=80,
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )

        xp_card = Button(
            text="",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.xp_label = Label(
            text="XP: Laden...",
            font_size=50,
            font_name='Roboto-Bold',
            color=(0.3, 0.6, 0.9, 1), # Ein schönes Mimo-Blau
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
        
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )

        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)

        reset_button = Button(
            text="Reset",
            font_size=40,
            size_hint=(0.15, 0.08),
            pos_hint={'center_x': 0.9, 'y': 0.9}, # Schon an deiner neuen Position!
            background_color=(0.9, 0.3, 0.3, 1) # Macht den Button roetlich
        )
        reset_button.bind(on_press=self.fortschritt_zuruecksetzen)


        # Adden der Objekte:
        layout.add_widget(card_menu)
        layout.add_widget(lernen_button_menu)
        layout.add_widget(profil_button_menu)
        layout.add_widget(learner)
        layout.add_widget(xp_card)
        layout.add_widget(self.xp_label)
        layout.add_widget(reset_button)
        layout.add_widget(üben_button_menu)
        layout.add_widget(ai_tutor_button_menu)

        # Ausführen:
        self.add_widget(layout)

    def on_enter(self, *args):
        app = App.get_running_app()
        xp_datei = os.path.join(app.user_data_dir, "xp.txt")
        gesamt_xp = 0
        
        # Prüfen, ob die Datei existiert und XP auslesen
        if os.path.exists(xp_datei):
            with open(xp_datei, "r", encoding="utf-8") as datei:
                try:
                    gesamt_xp = int(datei.read().strip())
                except:
                    gesamt_xp = 0 # Falls die Datei leer oder fehlerhaft ist
                    
        # Label-Text live updaten
        self.xp_label.text = f"XP: {gesamt_xp}"

    def zu_profil_wechseln(self, instance):
        pass

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'web_dashboard' # Hier springt er zum Web-Dashboard!
    
    def fortschritt_zuruecksetzen(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        
        motivation_datei = os.path.join(app_ordner, "motivation.txt")
        pfad_datei = os.path.join(app_ordner, "pfad.txt")
        fortschritt_datei = os.path.join(app_ordner, "web_fortschritt.txt") # Ändert web_fortschritt
        xp_datei = os.path.join(app_ordner, "xp.txt")
        coins_datei = os.path.join(app_ordner, "coins.txt")
        
        if os.path.exists(motivation_datei):
            os.remove(motivation_datei)
        if os.path.exists(pfad_datei):
            os.remove(pfad_datei)
        if os.path.exists(fortschritt_datei):
            os.remove(fortschritt_datei)
        if os.path.exists(xp_datei):
            os.remove(xp_datei)
        if os.path.exists(coins_datei):
            os.remove(coins_datei)

        # Setzt die Web-Dashboard-Buttons zurück
        web_dashboard = self.manager.get_screen('web_dashboard')
        for nummer, btn in web_dashboard.alle_buttons.items():
            if nummer == 1:
                btn.farbe_aktualisieren("aktiv")
            else:
                btn.farbe_aktualisieren("gesperrt") 

        print("Fortschritt und XP erfolgreich gelöscht!")
        self.manager.current = 'einführung1'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_web'

    def trainingfunc(self, instance):
        self.manager.current = 'training_web'

class Training_Screen_Python(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Starte mit dem Training!",
            font_name='Roboto-Bold',
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
                
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc,
            background_color = (0.72, 0.72, 0.72, 1)
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)
        
        bald_verfügbar = Label(
            text="Training ist bald verfügbar!",
            font_size='24sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )



        layout.add_widget(title)
        layout.add_widget(card_menu)
        layout.add_widget(lernen_button_menu)
        layout.add_widget(profil_button_menu)
        layout.add_widget(üben_button_menu)
        layout.add_widget(bald_verfügbar)
        layout.add_widget(ai_tutor_button_menu)
        self.add_widget(layout)

    def trainingfunc(self, instance):
        self.manager.current = 'training_python'


    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen'

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'python_dashboard'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_python'

class Training_Screen_Python_2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Starte mit dem Training!",
            font_name='Roboto-Bold',
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        
        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
                        
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
        
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc,
            background_color = (0.72, 0.72, 0.72, 1)
        )

        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)
        
        bald_verfügbar = Label(
            text="Training ist bald verfügbar!",
            font_size='24sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        

        layout.add_widget(title)
        layout.add_widget(card_menu)
        layout.add_widget(lernen_button_menu)
        layout.add_widget(profil_button_menu)
        layout.add_widget(üben_button_menu)
        layout.add_widget(bald_verfügbar)
        layout.add_widget(ai_tutor_button_menu)
        self.add_widget(layout)

    def trainingfunc(self, instance):
        self.manager.current = 'training_python_2'

    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen_2'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_python_2'

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'python_dashboard_2'

class Training_Screen_Web(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Starte mit dem Training!",
            font_name='Roboto-Bold',
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
                
        # Menüleiste:
        card_menu = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
                                
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05}
        )
               
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
       
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
       
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
       
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc,
            background_color = (0.72, 0.72, 0.72, 1)
        )

        lernen_button_menu.bind(on_press=self.zu_lernen_wechseln)

        bald_verfügbar = Label(
            text="Training ist bald verfügbar!",
            font_size='24sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
                

        layout.add_widget(title)
        layout.add_widget(card_menu)
        layout.add_widget(lernen_button_menu)
        layout.add_widget(profil_button_menu)
        layout.add_widget(üben_button_menu)
        layout.add_widget(ai_tutor_button_menu)
        layout.add_widget(bald_verfügbar)
        self.add_widget(layout)

    def trainingfunc(self, instance):
        self.manager.current = 'training_web'

    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen_web'

    def zu_lernen_wechseln(self, instance):
        self.manager.current = 'web_dashboard'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_web'
        
# =============================================================================================================================
# ERSTELLEN DER DASHBOARDS DER PFADE
# =============================================================================================================================

# ERSTELLEN DES PYTHON DEVELOPER DASHBOARDS
class PythonDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = FloatLayout()
        self.alle_buttons = {}

        # Erstellen der Objekte:
        title_label = Label(
            text="Python-Entwickler - 1. Abschnitt",
            font_size='27sp',
            font_name="Roboto-Bold",
            size_hint=(1.0, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        
        self.coins_display_button = Button(
            text="0 Münzen",
            font_size=36,
            font_name="Roboto-Bold",
            size_hint=(0.18, 0.07),
            pos_hint={'center_x': 0.1, 'center_y': 0.95},
            background_normal='',
            background_color=(1, 0.75, 0, 1),      # Ein schönes Mimo-Goldgelb
            disabled_color=(1, 1, 1, 1),
            on_press=self.ltcstorefunction
        )

        kurs_wechsel_btn = Button(
            text="Mehr Kurse",
            font_size=32,
            font_name="Roboto-Bold",
            size_hint=(0.18, 0.07), # Kompakte Breite für die Ecke
            pos_hint={'center_x': 0.9, 'center_y': 0.95}, # Exakt an der alten Reset-Position!
            background_color=(0.3, 0.6, 0.9, 1) # Ein schickes, einladendes Blau
        )
        kurs_wechsel_btn.bind(on_press=self.zu_kurse_wechseln)
        
        card_menu_unten = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )

        card_menu_oben = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.95}
        )

        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)  # Helles Aschgrau



        )
        
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )

        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )


        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )

        üben_button_menu.bind(on_press=self.trainingfunc)
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)


        next_abschnitt_button = Button(
            text="Nächster Abschnitt",
            size_hint=(0.4, 0.1),
            font_name='Roboto-Bold',
            font_size=36,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            on_press=self.next_abschnitt_function
        )

        info_dev_button = Button(
            text="INFO",
            font_name='Roboto-Bold',
            font_size=36,
            size_hint=(0.18, 0.07),
            on_press=self.infofunction,
            pos_hint={'center_x': 0.9, 'center_y': 0.2}
        )
        
        # Fortschritt aus Datei laden
        app_ordner = App.get_running_app().user_data_dir
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        aktueller_fortschritt = 1
        
        if os.path.exists(fortschritt_datei):
            with open(fortschritt_datei, "r", encoding="utf-8") as datei:
                try:
                    aktueller_fortschritt = int(datei.read().strip())
                except:
                    aktueller_fortschritt = 1

        # Neue Definition der Lektionen (ID, center_x, center_y)
        lektionen_liste = [
            (1, 0.35, 0.7),   # Lektion 1: Start oben in der Mitte
            (2, 0.5, 0.7),  # Lektion 2: Links versetzt
            (3, 0.65, 0.7),  # Lektion 3: Rechts versetzt
            (4, 0.35, 0.6),   # Lektion 4: Wieder in der Mitte
            (5, 0.5, 0.6),  # Lektion 5: Links versetzt
            (6, 0.65, 0.6),
            (7, 0.35, 0.5),   # NEU: Reihe 3 (unten)
            (8, 0.5, 0.5),  
            (9, 0.65, 0.5) 
        ]
        
        # Dynamisches Erstellen und Adden der Ampel-Buttons:
        for nummer, x, y in lektionen_liste:
            if nummer < aktueller_fortschritt:
                start_status = "erledigt"
            elif nummer == aktueller_fortschritt:
                start_status = "aktiv"
            else:
                start_status = "gesperrt"
            
            btn = FarbigerLektionsButton(lektions_id=nummer, status=start_status, pos_hint={'center_x': x, 'center_y': y})
            btn.bind(on_press=self.lektion_geklickt)
            
            self.alle_buttons[nummer] = btn
            self.layout.add_widget(btn)
        
        # Adden der Objekte:
        self.layout.add_widget(title_label)
        self.layout.add_widget(card_menu_oben)
        self.layout.add_widget(card_menu_unten)
        self.layout.add_widget(lernen_button_menu)
        self.layout.add_widget(profil_button_menu)
        self.layout.add_widget(self.coins_display_button)
        self.layout.add_widget(kurs_wechsel_btn)
        self.layout.add_widget(next_abschnitt_button)
        self.layout.add_widget(info_dev_button)
        self.layout.add_widget(üben_button_menu)
        self.layout.add_widget(ai_tutor_button_menu)
        
        # Ausführen:
        self.add_widget(self.layout)

    def on_enter(self, *args):
        # 1. Münzen aktualisieren
        app_ordner = App.get_running_app().user_data_dir
        coins_datei = os.path.join(app_ordner, "coins.txt")
        münzen = 0
        if os.path.exists(coins_datei):
            try:
                with open(coins_datei, "r", encoding="utf-8") as d:
                    münzen = int(d.read().strip())
            except:
                pass
        self.coins_display_button.text = f"{münzen} Münzen"
        
        # 2. Buttons live aktualisieren
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        aktueller_fortschritt = 1
        if os.path.exists(fortschritt_datei):
            try:
                with open(fortschritt_datei, "r", encoding="utf-8") as d:
                    aktueller_fortschritt = int(d.read().strip())
            except:
                pass

        for nummer, btn in self.alle_buttons.items():
            if nummer < aktueller_fortschritt:
                btn.farbe_aktualisieren("erledigt")
            elif nummer == aktueller_fortschritt:
                btn.farbe_aktualisieren("aktiv")
            else:
                btn.farbe_aktualisieren("gesperrt")

        
    def lektion_geklickt(self, instance_des_buttons):
        nummer = instance_des_buttons.lektions_id
        status = instance_des_buttons.status

       # erledigt und gesperrt
        if status == "gesperrt": # if status == "erledigt" or...
            return
        elif status == "erledigt":
            # hier kommt jetzt die neuen widgets:
            self.widget1 = WidgetButton(
                text="",
                size_hint=(0.6, 0.3),
                background_color=(0.21, 0.26, 0.39, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
                       
            self.widget2 = Button(
                text="Zurück",
                size_hint=(0.3, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                on_press=self.back
            )
                                   
            self.widget3 = Label(
                text="Bereits erledigt!",
                font_name="Roboto-Bold",
                font_size='24sp',
                pos_hint={'center_y': 0.5, 'center_y': 0.6}
            )
                       
            self.layout.add_widget(self.widget1)
            self.layout.add_widget(self.widget2)
            self.layout.add_widget(self.widget3)
            return

        
            
        #  Ab hier wird der Code überwacht
        try:
            if nummer == 1:
                self.manager.current = 'python_l1_s1'
            elif nummer == 2:
                self.manager.current = 'python_l2_s1'
            elif nummer == 3:
                self.manager.current = 'python_l3_s1'
            elif nummer == 4:
                self.manager.current = 'python_l4_s1'
            elif nummer == 5:
                self.manager.current = 'python_l5_s1'
            elif nummer == 6:
                self.manager.current = 'python_l6_s1'
            elif nummer == 7:
                self.manager.current = 'python_l7_s1'
            elif nummer == 8:
                self.manager.current = 'python_l8_s1'
            elif nummer == 9:
                self.manager.current = 'python_l9_s1'
            else:
                pass
        except:
            # Wenn der ScreenManager den Namen nicht findet, fängt das except den Fehler ab
            pass


    def lektion_erfolgreich(self, beendete_nummer):
        # 1. Berechne die nächste Lektionsnummer
        naechste_nummer = beendete_nummer + 1
        
        # 2. WICHTIG: Schreibe den neuen Fortschritt SOFORT in die Datei!
        # Ohne diese Zeilen liest on_enter gleich wieder den alten Zustand aus!
        app_ordner = App.get_running_app().user_data_dir
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        with open(fortschritt_datei, "w", encoding="utf-8") as datei:
            datei.write(str(naechste_nummer))
            
        print(f"Fortschritt in Datei aktualisiert! Nächste Lektion: {naechste_nummer}")

        # 3. Aktualisiere die Buttons im aktuellen Speicher (falls nötig)
        if beendete_nummer in self.alle_buttons:
            self.alle_buttons[beendete_nummer].farbe_aktualisieren("erledigt")
        if naechste_nummer in self.alle_buttons:
            self.alle_buttons[naechste_nummer].farbe_aktualisieren("aktiv")


    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen'
        
    def zu_kurse_wechseln(self, instance):
        self.manager.current = 'kurse_screen'

    def ltcstorefunction(self, instance):
        self.manager.current = 'ltc_store_python'

    def next_abschnitt_function(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        abschnitt_datei = os.path.join(app_ordner, "python_abschnitt.txt")
        
        # Speichere Abschnitt 2 ab
        with open(abschnitt_datei, "w", encoding="utf-8") as datei:
            datei.write("2")
            
        # Wechsel zum zweiten Dashboard
        self.manager.current = 'python_dashboard_2'

    def infofunction(self, instance):
        self.manager.current = 'Info_Screen_python1'

    def trainingfunc(self, instance):
        self.manager.current = 'training_python'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_python'

    def back(self, instance):
        self.layout.remove_widget(self.widget1)
        self.layout.remove_widget(self.widget2)
        self.layout.remove_widget(self.widget3)

class PythonDashboard2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.alle_buttons = {}

        # UI-Elemente initialisieren
        title_label = Label(
            text="Python-Entwickler - 2. Abschnitt",
            font_size='27sp',
            font_name="Roboto-Bold",
            size_hint=(1.0, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        
        self.coins_display_button = Button(
            text="0 Münzen",
            font_size=36,
            font_name="Roboto-Bold",
            size_hint=(0.18, 0.07),
            pos_hint={'center_x': 0.1, 'center_y': 0.95},
            background_normal='',
            background_color=(1, 0.75, 0, 1),
            disabled_color=(1, 1, 1, 1),
            on_press=self.ltcstorefunction
        )
        
        kurs_wechsel_btn = Button(
            text="Mehr Kurse",
            font_size=32,
            font_name="Roboto-Bold",
            size_hint=(0.18, 0.07),
            pos_hint={'center_x': 0.9, 'center_y': 0.95},
            background_color=(0.3, 0.6, 0.9, 1),
            on_press=self.zu_kurse_wechseln
        )
        
        card_menu_oben = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.95}
        )
        
        card_menu_unten = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
        
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
        
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )

        üben_button_menu.bind(on_press=self.trainingfunc)
        profil_button_menu.bind(on_press=self.zu_profil_wechseln)
        
        prev_abschnitt_button = Button(
            text="Zurück",
            size_hint=(0.18, 0.07),
            font_name='Roboto-Bold',
            font_size=36,
            pos_hint={'center_x': 0.1, 'center_y': 0.2},
            on_press=self.prev_abschnitt_function
        )

        info_dev_button = Button(
            text="INFO",
            font_name='Roboto-Bold',
            font_size=36,
            size_hint=(0.18, 0.07),
            on_press=self.infofunction,
            pos_hint={'center_x': 0.9, 'center_y': 0.2}
        )


        next_abschnitt_button = Button(
            text="Abs. 3 kommt bald!",
            size_hint=(0.4, 0.1),
            font_name='Roboto-Bold',
            font_size=36,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
        )

        # Lektionen 10 bis 18 generieren
        lektionen_liste = [
            (10, 0.35, 0.7), (11, 0.5, 0.7), (12, 0.65, 0.7),
            (13, 0.35, 0.6), (14, 0.5, 0.6), (15, 0.65, 0.6),
            (16, 0.35, 0.5), (17, 0.5, 0.5), (18, 0.65, 0.5) 
        ]
        
        app_ordner = App.get_running_app().user_data_dir
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        aktueller_fortschritt = 10
        
        if os.path.exists(fortschritt_datei):
            try:
                with open(fortschritt_datei, "r", encoding="utf-8") as d:
                    aktueller_fortschritt = max(10, int(d.read().strip()))
            except:
                pass

        for nummer, x, y in lektionen_liste:
            if nummer < aktueller_fortschritt:
                status = "erledigt"
            elif nummer == aktueller_fortschritt:
                status = "aktiv"
            else:
                status = "gesperrt"
                
            btn = FarbigerLektionsButton(
                lektions_id=nummer,
                status=status,
                pos_hint={'center_x': x, 'center_y': y}
            )
            btn.bind(on_press=self.lektion_geklickt)
            self.alle_buttons[nummer] = btn
            self.layout.add_widget(btn)
        
        # Widgets zum Layout hinzufügen
        self.layout.add_widget(title_label)
        self.layout.add_widget(card_menu_oben)
        self.layout.add_widget(card_menu_unten)
        self.layout.add_widget(lernen_button_menu)
        self.layout.add_widget(profil_button_menu)
        self.layout.add_widget(self.coins_display_button)
        self.layout.add_widget(kurs_wechsel_btn)
        self.layout.add_widget(prev_abschnitt_button)
        self.layout.add_widget(info_dev_button)
        self.layout.add_widget(üben_button_menu)
        self.layout.add_widget(next_abschnitt_button)
        self.layout.add_widget(ai_tutor_button_menu)
        self.add_widget(self.layout)

    def on_enter(self, *args):
        # 1. Münzen aktualisieren
        app_ordner = App.get_running_app().user_data_dir
        coins_datei = os.path.join(app_ordner, "coins.txt")
        münzen = 0
        if os.path.exists(coins_datei):
            try:
                with open(coins_datei, "r", encoding="utf-8") as d:
                    münzen = int(d.read().strip())
            except:
                pass
        self.coins_display_button.text = f"{münzen} Münzen"
        
        # 2. Buttons live an den echten Fortschritt anpassen
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        aktueller_fortschritt = 1
        if os.path.exists(fortschritt_datei):
            try:
                with open(fortschritt_datei, "r", encoding="utf-8") as d:
                    aktueller_fortschritt = int(d.read().strip())
            except:
                pass

        for nummer, btn in self.alle_buttons.items():
            if nummer < aktueller_fortschritt:
                btn.farbe_aktualisieren("erledigt")
            elif nummer == aktueller_fortschritt:
                btn.farbe_aktualisieren("aktiv")
            else:
                btn.farbe_aktualisieren("gesperrt")
     
    def lektion_geklickt(self, instance_des_buttons):
        nummer = instance_des_buttons.lektions_id
        status = instance_des_buttons.status
        
        # erledigt und gesperrt
        if status == "gesperrt": # if status == "erledigt" or...
            return
        elif status == "erledigt":
            # hier kommt jetzt die neuen widgets:
            self.widget1 = WidgetButton(
                text="",
                size_hint=(0.6, 0.3),
                background_color=(0.21, 0.26, 0.39, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
                        
            self.widget2 = Button(
                text="Zurück",
                size_hint=(0.3, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                on_press=self.back
            )
                                    
            self.widget3 = Label(
                text="Bereits erledigt!",
                font_name="Roboto-Bold",
                font_size='24sp',
                pos_hint={'center_y': 0.5, 'center_y': 0.6}
            )
                        
            self.layout.add_widget(self.widget1)
            self.layout.add_widget(self.widget2)
            self.layout.add_widget(self.widget3)
            return
            
        try:
            if nummer == 10:
                self.manager.current = 'python_l10_s1'
            elif nummer == 11:
                self.manager.current = 'python_l11_s1'
            elif nummer == 12:
                self.manager.current = 'python_l12_s1'
            elif nummer == 13:
                self.manager.current = 'python_l13_s1'
            elif nummer == 14:
                self.manager.current = 'python_l14_s1'
            elif nummer == 15:
                self.manager.current = 'python_l15_s1'
            elif nummer == 16:
                self.manager.current = 'python_l16_s1'
            elif nummer == 17:
                self.manager.current = 'python_l17_s1'
            elif nummer == 18:
                self.manager.current = 'python_l18_s1'
            else:
                pass
        except:
            pass

    def lektion_erfolgreich(self, beendete_nummer):
        naechste = beendete_nummer + 1
        app_ordner = App.get_running_app().user_data_dir
        fortschritt_datei = os.path.join(app_ordner, "python_fortschritt.txt")
        
        with open(fortschritt_datei, "w", encoding="utf-8") as d:
            d.write(str(naechste))
            
        if beendete_nummer in self.alle_buttons:
            self.alle_buttons[beendete_nummer].farbe_aktualisieren("erledigt")
        if naechste in self.alle_buttons:
            self.alle_buttons[naechste].farbe_aktualisieren("aktiv")

    def prev_abschnitt_function(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        abschnitt_datei = os.path.join(app_ordner, "python_abschnitt.txt")
        
        with open(abschnitt_datei, "w", encoding="utf-8") as d:
            d.write("1")
            
        self.manager.current = 'python_dashboard'

    def zu_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen_2'
        
    def zu_kurse_wechseln(self, instance):
        self.manager.current = 'kurse_screen'
        
    def ltcstorefunction(self, instance):
        self.manager.current = 'ltc_store_python'

    def infofunction(self, instance):
        self.manager.current = 'Info_Screen_python2'

    def trainingfunc(self, instance):
        self.manager.current = 'training_python_2'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_python_2'

    def back(self, instance):
        self.layout.remove_widget(self.widget1)
        self.layout.remove_widget(self.widget2)
        self.layout.remove_widget(self.widget3)

# ERSTELLEN DES WEB DEVELOPER DASHBOARDS
class WebDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = FloatLayout()
        self.alle_buttons = {}
        
        # Erstellen der Objekte:
        title_label = Label(
            text="Web-Entwickler - 1. Abschnitt",
            font_size='27sp',
            font_name="Roboto-Bold",
            size_hint=(1.0, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        
        kurs_wechsel_btn = Button(
            text="Mehr Kurse",
            font_size=32,
            font_name="Roboto-Bold",
            size_hint=(0.18, 0.07), # Kompakte Breite für die Ecke
            pos_hint={'center_x': 0.9, 'center_y': 0.95}, # Exakt an der alten Reset-Position!
            background_color=(0.3, 0.6, 0.9, 1) # Ein schickes, einladendes Blau
        )

        kurs_wechsel_btn.bind(on_press=self.zu_kurse_wechseln)

        self.coins_display_button = Button(
            text="0 Münzen",
            font_size=36,
            font_name="Roboto-Bold",
            size_hint=(0.18, 0.07),
            pos_hint={'center_x': 0.1, 'center_y': 0.95},
            background_normal='',
            background_color=(1, 0.75, 0, 1),      # Ein schönes Mimo-Goldgelb
            disabled_color=(1, 1, 1, 1),
            on_press=self.ltcstorefunction
        )
       

        card_menu_oben = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.95}
        )
        
        # 2. MENÜLEISTE FÜR WEB
        card_menu_unten = Button(
            text="",
            size_hint=(1.0, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
        
        lernen_button_menu = Button(
            text="Lernen",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.125, 'center_y': 0.05},
            background_color = (0.72, 0.72, 0.72, 1)
        )
                
        ai_tutor_button_menu = Button(
            text="AI Tutor",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.625, 'center_y': 0.05},
            on_press=self.zu_ai_wechseln
        )
        
        profil_button_menu = Button(
            text="Profil",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.875, 'center_y': 0.05}
        )
        
        
        üben_button_menu = Button(
            text="Training",
            font_name='Roboto-Bold',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.375, 'center_y': 0.05},
            on_press=self.trainingfunc
        )

        üben_button_menu.bind(on_press=self.trainingfunc)
        profil_button_menu.bind(on_press=self.zu_web_profil_wechseln)

        info_dev_button = Button(
            text="INFO",
            font_name='Roboto-Bold',
            font_size=36,
            size_hint=(0.18, 0.07),
            on_press=self.infofunction,
            pos_hint={'center_x': 0.9, 'center_y': 0.2}
        )

        next_abschnitt_button = Button(
            text="Abs. 2 kommt bald!",
            size_hint=(0.4, 0.1),
            font_name='Roboto-Bold',
            font_size=36,
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
        )

        # Fortschritt aus Datei laden
        app_ordner = App.get_running_app().user_data_dir
        fortschritt_datei = os.path.join(app_ordner, "web_fortschritt.txt")
        aktueller_fortschritt = 1
        
        if os.path.exists(fortschritt_datei):
            with open(fortschritt_datei, "r", encoding="utf-8") as datei:
                try:
                    aktueller_fortschritt = int(datei.read().strip())
                except:
                    aktueller_fortschritt = 1

        # Neue Definition der Lektionen (ID, center_x, center_y)
        lektionen_liste = [
            (1, 0.35, 0.7),
            (2, 0.5, 0.7),
            (3, 0.65, 0.7),
            (4, 0.35, 0.6),
            (5, 0.5, 0.6),
            (6, 0.65, 0.6),
            (7, 0.35, 0.5),   # NEU
            (8, 0.5, 0.5),  
            (9, 0.65, 0.5)    
        ]

        
        # Dynamisches Erstellen und Adden der Ampel-Buttons:
        for nummer, x, y in lektionen_liste:
            if nummer < aktueller_fortschritt:
                start_status = "erledigt"
            elif nummer == aktueller_fortschritt:
                start_status = "aktiv"
            else:
                start_status = "gesperrt"
            
            btn = FarbigerLektionsButton(lektions_id=nummer, status=start_status, pos_hint={'center_x': x, 'center_y': y})
            btn.bind(on_press=self.lektion_geklickt)
            
            self.alle_buttons[nummer] = btn
            self.layout.add_widget(btn)
        
        # Adden der Objekte:
        self.layout.add_widget(title_label)
        self.layout.add_widget(card_menu_oben)
        self.layout.add_widget(card_menu_unten)
        self.layout.add_widget(lernen_button_menu)
        self.layout.add_widget(profil_button_menu)
        self.layout.add_widget(self.coins_display_button)
        self.layout.add_widget(info_dev_button)
        self.layout.add_widget(kurs_wechsel_btn)
        self.layout.add_widget(üben_button_menu)
        self.layout.add_widget(next_abschnitt_button)
        self.layout.add_widget(ai_tutor_button_menu)
        
        # Ausführen:
        self.add_widget(self.layout)
    
    def lektion_geklickt(self, instance_des_buttons):
        nummer = instance_des_buttons.lektions_id
        status = instance_des_buttons.status
        
        # erledigt und gesperrt
        if status == "gesperrt": # if status == "erledigt" or...
            return
        elif status == "erledigt":
            # hier kommt jetzt die neuen widgets:
            self.widget1 = WidgetButton(
                text="",
                size_hint=(0.6, 0.3),
                background_color=(0.21, 0.26, 0.39, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
                
            self.widget2 = Button(
                text="Zurück",
                size_hint=(0.3, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                on_press=self.back
            )
                            
            self.widget3 = Label(
                text="Bereits erledigt!",
                font_name="Roboto-Bold",
                font_size='24sp',
                pos_hint={'center_y': 0.5, 'center_y': 0.6}
            )
                
            self.layout.add_widget(self.widget1)
            self.layout.add_widget(self.widget2)
            self.layout.add_widget(self.widget3)
            return

        try:    
            if nummer == 1:
                self.manager.current = 'web_l1_s1'
            elif nummer == 2:
                self.manager.current = 'web_l2_s1'
            elif nummer == 3:
                self.manager.current = 'web_l3_s1'
            elif nummer == 4:
                self.manager.current = 'web_l4_s1'
            elif nummer == 5:
                self.manager.current = 'web_l5_s1'
            elif nummer == 6:
                self.manager.current = 'web_l6_s1'
            elif nummer == 7:
                self.manager.current = 'web_l7_s1'
            elif nummer == 8:
                self.manager.current = 'web_l8_s1'
            elif nummer == 9:
                self.manager.current = 'web_l9_s1'
            else:
                print(f"Web Lektion {nummer} wird bald freigeschaltet!")
                pass
        except:
            pass

    def lektion_erfolgreich(self, beendete_nummer):
        # 1. Berechne die nächste Lektionsnummer
        naechste_nummer = beendete_nummer + 1
        
        # 2. WICHTIG: Schreibe den neuen Fortschritt SOFORT in die Datei!
        # Ohne diese Zeilen liest on_enter gleich wieder den alten Zustand aus!
        app_ordner = App.get_running_app().user_data_dir
        fortschritt_datei = os.path.join(app_ordner, "web_fortschritt.txt")
        with open(fortschritt_datei, "w", encoding="utf-8") as datei:
            datei.write(str(naechste_nummer))
            
        print(f"Fortschritt in Datei aktualisiert! Nächste Lektion: {naechste_nummer}")

        # 3. Aktualisiere die Buttons im aktuellen Speicher (falls nötig)
        if beendete_nummer in self.alle_buttons:
            self.alle_buttons[beendete_nummer].farbe_aktualisieren("erledigt")
        if naechste_nummer in self.alle_buttons:
            self.alle_buttons[naechste_nummer].farbe_aktualisieren("aktiv")


    def on_enter(self, *args):
        # Aktualisiert die Münzen live, wenn man das Web-Dashboard betritt
        app_ordner = App.get_running_app().user_data_dir
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktueller_münzstand = 0
        if os.path.exists(coins_datei):
            with open(coins_datei, "r", encoding="utf-8") as datei:
                try: aktueller_münzstand = int(datei.read().strip())
                except: aktueller_münzstand = 0
        self.coins_display_button.text = f"{aktueller_münzstand} Münzen"

    def zu_lernen_wechseln(self, instance):
        pass # Wir sind schon auf dem Web-Dashboard

    def zu_web_profil_wechseln(self, instance):
        self.manager.current = 'profil_screen_web' # Neuer Name!

    def zu_kurse_wechseln(self, instance):
        self.manager.current = 'kurse_screen'

    def ltcstorefunction(self, instance):
        self.manager.current = 'ltc_store_web'

    def infofunction(self, instance):
        self.manager.current = 'Info_Screen_web1'

    def zu_ai_wechseln(self, instance):
        self.manager.current = 'ai_tutor_web'

    def trainingfunc(self, instance):
        self.manager.current = 'training_web'

    def back(self, instance):
        self.layout.remove_widget(self.widget1)
        self.layout.remove_widget(self.widget2)
        self.layout.remove_widget(self.widget3)

# ERSTELLEN DES KURSEWECHSELN SCREENS:
class Kurse_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        titel = Label(
            text="Bereit, mehr zu lernen?",
            font_size=70,
            font_name="Roboto-Bold",
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        add_label = Label(
            text="Entdecke unsere großen Karrierepfade und werde ein",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            font_size=40
        )

        add_label2 = Label(
            text="professioneller Entwickler. Lerne deine eigenen Projekte",
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_size=40
        )

        add_label3 = Label(
            text="in der Praxis aufzubauen, bis zur Veröffentlichung.",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            font_size=40
        )

        # Python-Auswahlbutton
        python_btn = Button(
            text="Python-Entwickler",
            font_size=40,
            font_name="Roboto-Bold",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            #background_color=(0.2, 0.6, 0.2, 1) # Ein schönes Erfolg-Grün
        )
        python_btn.bind(on_press=self.waehle_python)

        # Web-Dev-Auswahlbutton
        web_btn = Button(
            text="Web-Entwickler",
            font_size=40,
            font_name="Roboto-Bold",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            #background_color=(0.2, 0.5, 0.8, 1) # Ein schickes Web-Blau
        )
        web_btn.bind(on_press=self.waehle_web)

        layout.add_widget(titel)
        layout.add_widget(python_btn)
        layout.add_widget(web_btn)
        layout.add_widget(add_label)
        layout.add_widget(add_label2)
        layout.add_widget(add_label3)

        # Ausführen:
        self.add_widget(layout)

    def waehle_python(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        pfad_datei = os.path.join(app_ordner, "pfad.txt")
        
        # Schreibt "Python Developer" rein, ohne XP oder Münzen anzurühren!
        with open(pfad_datei, "w", encoding="utf-8") as datei:
            datei.write("Python Developer")
            
        self.manager.current = 'python_dashboard'

    def waehle_web(self, instance):
        app_ordner = App.get_running_app().user_data_dir
        pfad_datei = os.path.join(app_ordner, "pfad.txt")
        
        # Schreibt "Web Developer" rein
        with open(pfad_datei, "w", encoding="utf-8") as datei:
            datei.write("Web Developer")
            
        self.manager.current = 'web_dashboard'

# ERSTELLEN DES LTC STORE SCREENS:
class LTC_Store_Python_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Adden der Objekte:
        title_label = Label(
            text="LTC Store",
            size_hint=(1.0, 0.2),
            font_size=80,
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        add_label = Label(
            text="Du hast Münzen, weißt aber nicht was du damit tun sollst?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        add_label2 = Label(
            text="Kein Problem! Kauf dir coole Extras und Möglichkeiten!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        exit_button = Button(
            text="Zurück",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.exit_function
        )

        no_items_now = Label(
            text="Keine Items derzeit. Schau später wieder vorbei!",
            font_size=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name='Roboto-Bold'
                )
        
        # Adden der Objekte zum Layout:
        layout.add_widget(title_label)
        layout.add_widget(add_label)
        layout.add_widget(add_label2)
        layout.add_widget(exit_button)
        layout.add_widget(no_items_now)

        # Ausführen:
        self.add_widget(layout)

    def exit_function(self, instance):
        self.manager.current = 'python_dashboard'

class LTC_Store_Web_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Adden der Objekte:
        title_label = Label(
            text="LTC Store",
            size_hint=(1.0, 0.2),
            font_size=80,
            font_name='Roboto-Bold',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        add_label = Label(
            text="Du hast Münzen, weißt aber nicht was du damit tun sollst?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        add_label2 = Label(
            text="Kein Problem! Kauf dir coole Extras und Möglichkeiten!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )

        exit_button = Button(
            text="Zurück",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.exit_function
        )

        no_items_now = Label(
            text="Keine Items derzeit. Schau später wieder vorbei!",
            font_size=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name='Roboto-Bold'
        )

        # Adden der Objekte zum Layout:
        layout.add_widget(title_label)
        layout.add_widget(add_label)
        layout.add_widget(add_label2)
        layout.add_widget(exit_button)
        layout.add_widget(no_items_now)

        # Ausführen:
        self.add_widget(layout)

    def exit_function(self, instance):
        self.manager.current = 'web_dashboard'

# Erstellen des Info-Button-Screens für die dashbaords:
class Info_Python1_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Ein paar Worte an dich",
            font_name='Roboto-Bold',
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        back = Button(
            text="Zurück",
            font_name='Roboto-Bold',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.backfunction
        )

        e1 = Label(
            text="Willkommen bei meiner App!",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            font_size='12sp'
        )

        e2 = Label(
            text="Dieses Projekt wurde von mir als Solo-Entwickler komplett alleine aufgebaut.",
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_size='12sp'
        )

        e3 = Label(
            text="Ich arbeite kontinuierlich an Verbesserungen und veröffentliche regelmäßig neue Updates.",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            font_size='12sp'
        )

        e4 = Label(
            text="Um die App weiterzuentwickeln, bin ich auf deine Unterstützung angewiesen.",
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_size='12sp'
        )

        e5 = Label(
            text="Bitte nimm dir kurz Zeit für eine ehrliche Rezension im Play Store.",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            font_size='12sp'
        )

        e6 = Label(
            text="Jede einzelne Bewertung hilft mir als Einzelkämpfer unglaublich weiter!",
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            font_size='12sp'
        )
        
        layout.add_widget(title)
        layout.add_widget(e1)
        layout.add_widget(e2)
        layout.add_widget(e3)
        layout.add_widget(e4)
        layout.add_widget(e5)
        layout.add_widget(e6)
        layout.add_widget(back)
        self.add_widget(layout)

    def backfunction(self, instance):
        self.manager.current = 'python_dashboard'

class Info_Python2_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Ein paar Worte an dich",
            font_name='Roboto-Bold',
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
       
        back = Button(
            text="Zurück",
            font_name='Roboto-Bold',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.backfunction
        )

        e1 = Label(
            text="Willkommen bei meiner App!",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            font_size='12sp'
        )
       
        e2 = Label(
            text="Dieses Projekt wurde von mir als Solo-Entwickler komplett alleine aufgebaut.",
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_size='12sp'
        )
       
        e3 = Label(
            text="Ich arbeite kontinuierlich an Verbesserungen und veröffentliche regelmäßig neue Updates.",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            font_size='12sp'
        )
       
        e4 = Label(
            text="Um die App weiterzuentwickeln, bin ich auf deine Unterstützung angewiesen.",
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_size='12sp'
        )
       
        e5 = Label(
            text="Bitte nimm dir kurz Zeit für eine ehrliche Rezension im Play Store.",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            font_size='12sp'
        )
       
        e6 = Label(
            text="Jede einzelne Bewertung hilft mir als Einzelkämpfer unglaublich weiter!",
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            font_size='12sp'
        )
               
        layout.add_widget(title)
        layout.add_widget(e1)
        layout.add_widget(e2)
        layout.add_widget(e3)
        layout.add_widget(e4)
        layout.add_widget(e5)
        layout.add_widget(e6)
        layout.add_widget(back)
        self.add_widget(layout)

    def backfunction(self, instance):
        self.manager.current = 'python_dashboard_2'

class Info_Web1_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Label(
            text="Ein paar Worte an dich",
            font_name='Roboto-Bold',
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )

        back = Button(
            text="Zurück",
            font_name='Roboto-Bold',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.backfunction
        )
        
        e1 = Label(
            text="Willkommen bei meiner App!",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            font_size='12sp'
        )
        
        e2 = Label(
            text="Dieses Projekt wurde von mir als Solo-Entwickler komplett alleine aufgebaut.",
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_size='12sp'
        )
        
        e3 = Label(
            text="Ich arbeite kontinuierlich an Verbesserungen und veröffentliche regelmäßig neue Updates.",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            font_size='12sp'
        )
        
        e4 = Label(
            text="Um die App weiterzuentwickeln, bin ich auf deine Unterstützung angewiesen.",
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_size='12sp'
        )
        
        e5 = Label(
            text="Bitte nimm dir kurz Zeit für eine ehrliche Rezension im Play Store.",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            font_size='12sp'
        )
        
        e6 = Label(
            text="Jede einzelne Bewertung hilft mir als Einzelkämpfer unglaublich weiter!",
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            font_size='12sp'
        )
                
        layout.add_widget(title)
        layout.add_widget(e1)
        layout.add_widget(e2)
        layout.add_widget(e3)
        layout.add_widget(e4)
        layout.add_widget(e5)
        layout.add_widget(e6)
        layout.add_widget(back)
        self.add_widget(layout)

    def backfunction(self, instance):
        self.manager.current = 'web_dashboard'

# =============================================================================================================================
# ERSTELLEN DER HAUPTKLASSE
# =============================================================================================================================

class LTC(App):
    def build(self):
        sm = ScreenManager()
        sm.transition = NoTransition()
        sm.add_widget(einführung_to_ltc(name='einführung1'))
        sm.add_widget(einführung_warum_ltc(name='einführung2'))
        sm.add_widget(einführung_was_erreichen_ltc(name='einführung3'))
        sm.add_widget(einführung_wie_viel_zeit_ltc(name='einführung4'))
        sm.add_widget(einführung_pfad_ltc(name='einführung5'))
        sm.add_widget(PythonDashboard(name='python_dashboard'))
        sm.add_widget(WebDashboard(name='web_dashboard'))
        sm.add_widget(PythonLektion1_Screen1(name='python_l1_s1'))
        sm.add_widget(PythonLektion1_Screen2(name='python_l1_s2'))
        sm.add_widget(PythonLektion1_Screen3(name='python_l1_s3'))
        sm.add_widget(PythonLektion1_Screen4(name='python_l1_s4'))
        sm.add_widget(PythonLektion1_Screen5(name='python_l1_s5'))
        sm.add_widget(PythonLektion1_Screen6(name='python_l1_s6'))
        sm.add_widget(PythonLektion2_Screen1(name='python_l2_s1'))
        sm.add_widget(PythonLektion2_Screen2(name='python_l2_s2'))
        sm.add_widget(PythonLektion2_Screen3(name='python_l2_s3'))
        sm.add_widget(PythonLektion2_Screen4(name='python_l2_s4'))
        sm.add_widget(PythonLektion2_Screen5(name='python_l2_s5'))
        sm.add_widget(PythonLektion2_Screen6(name='python_l2_s6'))
        sm.add_widget(PythonLektion3_Screen1(name='python_l3_s1'))
        sm.add_widget(PythonLektion3_Screen2(name='python_l3_s2'))
        sm.add_widget(PythonLektion3_Screen3(name='python_l3_s3'))
        sm.add_widget(PythonLektion3_Screen4(name='python_l3_s4'))
        sm.add_widget(PythonLektion3_Screen5(name='python_l3_s5'))
        sm.add_widget(PythonLektion3_Screen6(name='python_l3_s6'))
        sm.add_widget(Profil_Screen_Python(name='profil_screen'))
        sm.add_widget(Profil_Screen_Web(name='profil_screen_web'))
        sm.add_widget(PythonLektion4_Screen1(name='python_l4_s1'))
        sm.add_widget(PythonLektion4_Screen2(name='python_l4_s2'))
        sm.add_widget(PythonLektion4_Screen3(name='python_l4_s3'))
        sm.add_widget(PythonLektion4_Screen4(name='python_l4_s4'))
        sm.add_widget(PythonLektion4_Screen5(name='python_l4_s5'))
        sm.add_widget(PythonLektion4_Screen6(name='python_l4_s6'))
        sm.add_widget(PythonLektion5_Screen1(name='python_l5_s1'))
        sm.add_widget(PythonLektion5_Screen2(name='python_l5_s2'))
        sm.add_widget(PythonLektion5_Screen3(name='python_l5_s3'))
        sm.add_widget(PythonLektion5_Screen4(name='python_l5_s4'))
        sm.add_widget(PythonLektion5_Screen5(name='python_l5_s5'))
        sm.add_widget(PythonLektion5_Screen6(name='python_l5_s6'))
        sm.add_widget(PythonLektion6_Screen1(name='python_l6_s1'))
        sm.add_widget(PythonLektion6_Screen2(name='python_l6_s2'))
        sm.add_widget(PythonLektion6_Screen3(name='python_l6_s3'))
        sm.add_widget(PythonLektion6_Screen4(name='python_l6_s4'))
        sm.add_widget(PythonLektion6_Screen5(name='python_l6_s5'))
        sm.add_widget(PythonLektion6_Screen6(name='python_l6_s6'))
        sm.add_widget(Kurse_Screen(name='kurse_screen'))
        sm.add_widget(WebLektion1_Screen1(name='web_l1_s1'))
        sm.add_widget(WebLektion1_Screen2(name='web_l1_s2'))
        sm.add_widget(WebLektion1_Screen3(name='web_l1_s3'))
        sm.add_widget(WebLektion1_Screen4(name='web_l1_s4'))
        sm.add_widget(WebLektion1_Screen5(name='web_l1_s5'))
        sm.add_widget(WebLektion1_Screen6(name='web_l1_s6'))
        sm.add_widget(LTC_Store_Python_Screen(name='ltc_store_python'))
        sm.add_widget(LTC_Store_Web_Screen(name='ltc_store_web'))
        sm.add_widget(PythonLektion7_Screen1(name='python_l7_s1'))
        sm.add_widget(PythonLektion7_Screen2(name='python_l7_s2'))
        sm.add_widget(PythonLektion7_Screen3(name='python_l7_s3'))
        sm.add_widget(PythonLektion7_Screen4(name='python_l7_s4'))
        sm.add_widget(PythonLektion7_Screen5(name='python_l7_s5'))
        sm.add_widget(PythonLektion7_Screen6(name='python_l7_s6'))
        sm.add_widget(PythonLektion8_Screen1(name='python_l8_s1'))
        sm.add_widget(PythonLektion8_Screen2(name='python_l8_s2'))
        sm.add_widget(PythonLektion8_Screen3(name='python_l8_s3'))
        sm.add_widget(PythonLektion8_Screen4(name='python_l8_s4'))
        sm.add_widget(PythonLektion8_Screen5(name='python_l8_s5'))
        sm.add_widget(PythonLektion8_Screen6(name='python_l8_s6'))
        sm.add_widget(PythonLektion9_Screen1(name='python_l9_s1'))
        sm.add_widget(PythonLektion9_Screen2(name='python_l9_s2'))
        sm.add_widget(PythonLektion9_Screen3(name='python_l9_s3'))
        sm.add_widget(PythonLektion9_Screen4(name='python_l9_s4'))
        sm.add_widget(PythonLektion9_Screen5(name='python_l9_s5'))
        sm.add_widget(PythonLektion9_Screen6(name='python_l9_s6'))
        sm.add_widget(PythonDashboard2(name='python_dashboard_2'))
        sm.add_widget(PythonLektion10_Screen1(name='python_l10_s1'))
        sm.add_widget(PythonLektion10_Screen2(name='python_l10_s2'))
        sm.add_widget(PythonLektion10_Screen3(name='python_l10_s3'))
        sm.add_widget(PythonLektion10_Screen4(name='python_l10_s4'))
        sm.add_widget(PythonLektion10_Screen5(name='python_l10_s5'))
        sm.add_widget(PythonLektion10_Screen6(name='python_l10_s6'))
        sm.add_widget(PythonLektion11_Screen1(name='python_l11_s1'))
        sm.add_widget(PythonLektion11_Screen2(name='python_l11_s2'))
        sm.add_widget(PythonLektion11_Screen3(name='python_l11_s3'))
        sm.add_widget(PythonLektion11_Screen4(name='python_l11_s4'))
        sm.add_widget(PythonLektion11_Screen5(name='python_l11_s5'))
        sm.add_widget(PythonLektion11_Screen6(name='python_l11_s6'))
        sm.add_widget(PythonLektion12_Screen1(name='python_l12_s1'))
        sm.add_widget(PythonLektion12_Screen2(name='python_l12_s2'))
        sm.add_widget(PythonLektion12_Screen3(name='python_l12_s3'))
        sm.add_widget(PythonLektion12_Screen4(name='python_l12_s4'))
        sm.add_widget(PythonLektion12_Screen5(name='python_l12_s5'))
        sm.add_widget(PythonLektion12_Screen6(name='python_l12_s6'))
        sm.add_widget(PythonLektion13_Screen1(name='python_l13_s1'))
        sm.add_widget(PythonLektion13_Screen2(name='python_l13_s2'))
        sm.add_widget(PythonLektion13_Screen3(name='python_l13_s3'))
        sm.add_widget(PythonLektion13_Screen4(name='python_l13_s4'))
        sm.add_widget(PythonLektion13_Screen5(name='python_l13_s5'))
        sm.add_widget(PythonLektion13_Screen6(name='python_l13_s6'))
        sm.add_widget(Profil_Screen_Python_2(name='profil_screen_2'))
        sm.add_widget(PythonLektion14_Screen1(name='python_l14_s1'))
        sm.add_widget(PythonLektion14_Screen2(name='python_l14_s2'))
        sm.add_widget(PythonLektion14_Screen3(name='python_l14_s3'))
        sm.add_widget(PythonLektion14_Screen4(name='python_l14_s4'))
        sm.add_widget(PythonLektion14_Screen5(name='python_l14_s5'))
        sm.add_widget(PythonLektion14_Screen6(name='python_l14_s6'))
        sm.add_widget(PythonLektion15_Screen1(name='python_l15_s1'))
        sm.add_widget(PythonLektion15_Screen2(name='python_l15_s2'))
        sm.add_widget(PythonLektion15_Screen3(name='python_l15_s3'))
        sm.add_widget(PythonLektion15_Screen4(name='python_l15_s4'))
        sm.add_widget(PythonLektion15_Screen5(name='python_l15_s5'))
        sm.add_widget(PythonLektion15_Screen6(name='python_l15_s6'))
        sm.add_widget(PythonLektion16_Screen1(name='python_l16_s1'))
        sm.add_widget(PythonLektion16_Screen2(name='python_l16_s2'))
        sm.add_widget(PythonLektion16_Screen3(name='python_l16_s3'))
        sm.add_widget(PythonLektion16_Screen4(name='python_l16_s4'))
        sm.add_widget(PythonLektion16_Screen5(name='python_l16_s5'))
        sm.add_widget(PythonLektion16_Screen6(name='python_l16_s6'))
        sm.add_widget(PythonLektion17_Screen1(name='python_l17_s1'))
        sm.add_widget(PythonLektion17_Screen2(name='python_l17_s2'))
        sm.add_widget(PythonLektion17_Screen3(name='python_l17_s3'))
        sm.add_widget(PythonLektion17_Screen4(name='python_l17_s4'))
        sm.add_widget(PythonLektion17_Screen5(name='python_l17_s5'))
        sm.add_widget(PythonLektion17_Screen6(name='python_l17_s6'))
        sm.add_widget(PythonLektion18_Screen1(name='python_l18_s1'))
        sm.add_widget(PythonLektion18_Screen2(name='python_l18_s2'))
        sm.add_widget(PythonLektion18_Screen3(name='python_l18_s3'))
        sm.add_widget(PythonLektion18_Screen4(name='python_l18_s4'))
        sm.add_widget(PythonLektion18_Screen5(name='python_l18_s5'))
        sm.add_widget(PythonLektion18_Screen6(name='python_l18_s6'))
        sm.add_widget(PythonLektion18_Screen7(name='python_l18_s7'))
        sm.add_widget(Info_Python1_Screen(name='Info_Screen_python1'))
        sm.add_widget(Info_Python2_Screen(name='Info_Screen_python2'))
        sm.add_widget(Info_Web1_Screen(name='Info_Screen_web1'))
        sm.add_widget(Training_Screen_Python(name='training_python'))
        sm.add_widget(Training_Screen_Python_2(name='training_python_2'))
        sm.add_widget(Training_Screen_Web(name='training_web'))
        sm.add_widget(WebLektion2_Screen1(name='web_l2_s1'))
        sm.add_widget(WebLektion2_Screen2(name='web_l2_s2'))
        sm.add_widget(WebLektion2_Screen3(name='web_l2_s3'))
        sm.add_widget(WebLektion2_Screen4(name='web_l2_s4'))
        sm.add_widget(WebLektion2_Screen5(name='web_l2_s5'))
        sm.add_widget(WebLektion2_Screen6(name='web_l2_s6'))
        sm.add_widget(WebLektion3_Screen1(name='web_l3_s1'))
        sm.add_widget(WebLektion3_Screen2(name='web_l3_s2'))
        sm.add_widget(WebLektion3_Screen3(name='web_l3_s3'))
        sm.add_widget(WebLektion3_Screen4(name='web_l3_s4'))
        sm.add_widget(WebLektion3_Screen5(name='web_l3_s5'))
        sm.add_widget(WebLektion3_Screen6(name='web_l3_s6'))
        sm.add_widget(WebLektion4_Screen1(name='web_l4_s1'))
        sm.add_widget(WebLektion4_Screen2(name='web_l4_s2'))
        sm.add_widget(WebLektion4_Screen3(name='web_l4_s3'))
        sm.add_widget(WebLektion4_Screen4(name='web_l4_s4'))
        sm.add_widget(WebLektion4_Screen5(name='web_l4_s5'))
        sm.add_widget(WebLektion4_Screen6(name='web_l4_s6'))
        sm.add_widget(WebLektion5_Screen1(name='web_l5_s1'))
        sm.add_widget(WebLektion5_Screen2(name='web_l5_s2'))
        sm.add_widget(WebLektion5_Screen3(name='web_l5_s3'))
        sm.add_widget(WebLektion5_Screen4(name='web_l5_s4'))
        sm.add_widget(WebLektion5_Screen5(name='web_l5_s5'))
        sm.add_widget(WebLektion5_Screen6(name='web_l5_s6'))
        sm.add_widget(WebLektion6_Screen1(name='web_l6_s1'))
        sm.add_widget(WebLektion6_Screen2(name='web_l6_s2'))
        sm.add_widget(WebLektion6_Screen3(name='web_l6_s3'))
        sm.add_widget(WebLektion6_Screen4(name='web_l6_s4'))
        sm.add_widget(WebLektion6_Screen5(name='web_l6_s5'))
        sm.add_widget(WebLektion6_Screen6(name='web_l6_s6'))
        sm.add_widget(WebLektion7_Screen1(name='web_l7_s1'))
        sm.add_widget(WebLektion7_Screen2(name='web_l7_s2'))
        sm.add_widget(WebLektion7_Screen3(name='web_l7_s3'))
        sm.add_widget(WebLektion7_Screen4(name='web_l7_s4'))
        sm.add_widget(WebLektion7_Screen5(name='web_l7_s5'))
        sm.add_widget(WebLektion7_Screen6(name='web_l7_s6'))
        sm.add_widget(WebLektion8_Screen1(name='web_l8_s1'))
        sm.add_widget(WebLektion8_Screen2(name='web_l8_s2'))
        sm.add_widget(WebLektion8_Screen3(name='web_l8_s3'))
        sm.add_widget(WebLektion8_Screen4(name='web_l8_s4'))
        sm.add_widget(WebLektion8_Screen5(name='web_l8_s5'))
        sm.add_widget(WebLektion8_Screen6(name='web_l8_s6'))
        sm.add_widget(WebLektion9_Screen1(name='web_l9_s1'))
        sm.add_widget(WebLektion9_Screen2(name='web_l9_s2'))
        sm.add_widget(WebLektion9_Screen3(name='web_l9_s3'))
        sm.add_widget(WebLektion9_Screen4(name='web_l9_s4'))
        sm.add_widget(WebLektion9_Screen5(name='web_l9_s5'))
        sm.add_widget(WebLektion9_Screen6(name='web_l9_s6'))
        sm.add_widget(AITutor_Screen_Python(name='ai_tutor_python'))
        sm.add_widget(AITutor_Screen_Web(name='ai_tutor_web'))
        sm.add_widget(AITutor_Screen_Python_2(name='ai_tutor_python_2'))

        # Pfade für Auto-Skip definieren
        pfad_datei = os.path.join(self.user_data_dir, "pfad.txt")
        abschnitt_datei = os.path.join(self.user_data_dir, "python_abschnitt.txt")
        
        target_screen = 'einführung1'
        
        if os.path.exists(pfad_datei):
            try:
                with open(pfad_datei, "r", encoding="utf-8") as d:
                    pfad = d.read()
                
                if "Python" in pfad:
                    target_screen = 'python_dashboard'
                    
                    # Überprüfung des gespeicherten Python-Abschnitts
                    if os.path.exists(abschnitt_datei):
                        with open(abschnitt_datei, "r", encoding="utf-8") as a_d:
                            if a_d.read().strip() == "2":
                                target_screen = 'python_dashboard_2'
                                
                elif "Web" in pfad:
                    target_screen = 'web_dashboard'
            except:
                pass

        sm.current = target_screen
            
        return sm
    
if __name__ == '__main__':
    LTC().run()

