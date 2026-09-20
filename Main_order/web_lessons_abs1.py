
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.graphics import Color, Line
import os
from kivy.uix.floatlayout import FloatLayout
from pygments.lexers.html import HtmlLexer
from pygments.styles import get_style_by_name
from kivy.properties import ListProperty
from kivy.graphics.texture import Texture
from kivy.animation import Animation


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

class RoundedCodeInput(CodeInput):
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
        code_source_gesamt = RoundedCodeInput(
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
        code_source_gesamt = RoundedCodeInput(
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
            source='AbzeichenLTCnew.png',
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
        # 1. IMPORTS DIREKT IN DER FUNKTION (Verhindert Namensraum-Fehler auf Android)
        import os
        from kivy.app import App
        from kivy.utils import platform

        # 2. ABSOLUT SICHERE PFAD-ERMITTLUNG
        try:
            if platform == 'android':
                from android.storage import app_storage_details # type: ignore
                app_ordner = app_storage_details().files_dir
            else:
                app_ordner = os.path.dirname(os.path.abspath(__file__))
            
            if not app_ordner:
                app_ordner = App.get_running_app().user_data_dir
        except Exception as e:
            print(f"Pfad-Fehler abgefangen: {e}")
            app_ordner = "."

        # 3. XP SPEICHERN MIT CRASH-SCHUTZ
        xp_datei = os.path.join(app_ordner, "xp.txt")
        aktuelle_xp = 0
        if os.path.exists(xp_datei):
            try:
                with open(xp_datei, "r", encoding="utf-8") as datei:
                    inhalt = datei.read().strip()
                    # Prüft, ob die Datei leer ist, um ValueError zu verhindern
                    aktuelle_xp = int(inhalt) if inhalt else 0
            except Exception as e:
                print(f"Fehler beim XP-Lesen: {e}")
                aktuelle_xp = 0

        gesamte_xp = aktuelle_xp + self.lektions_xp
        try:
            with open(xp_datei, "w", encoding="utf-8") as datei:
                datei.write(str(gesamte_xp))
        except Exception as e:
            print(f"Fehler beim XP-Schreiben: {e}")
            
        print(f"XP erfolgreich aktualisiert! Gesamt: {gesamte_xp} XP")

        # 4. MÜNZEN SPEICHERN MIT CRASH-SCHUTZ
        coins_datei = os.path.join(app_ordner, "coins.txt")
        aktuelle_coins = 0
        if os.path.exists(coins_datei):
            try:
                with open(coins_datei, "r", encoding="utf-8") as datei:
                    inhalt = datei.read().strip()
                    aktuelle_coins = int(inhalt) if inhalt else 0
            except Exception as e:
                print(f"Fehler beim Münzen-Lesen: {e}")
                aktuelle_coins = 0

        gesamte_coins = aktuelle_coins + 10
        try:
            with open(coins_datei, "w", encoding="utf-8") as datei:
                datei.write(str(gesamte_coins))
        except Exception as e:
            print(f"Fehler beim Münzen-Schreiben: {e}")
            
        print(f"Münzen erfolgreich im Hintergrund aktualisiert! Gesamt: {gesamte_coins}")
            
        # 5. DASHBOARD AKTUALISIEREN & WECHSELN MIT ABSICHERUNG
        try:
            web_dashboard = self.manager.get_screen('web_dashboard')
            web_dashboard.lektion_erfolgreich(1)
        except Exception as e:
            print(f"Dashboard-Wechsel fehlgeschlagen: {e}")

        self.lektions_xp = 0
        self.manager.current = 'web_dashboard'


