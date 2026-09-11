
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

class FertigPulseButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Die exakten Erfolgs-Grüntöne definieren
        self.success_green = (0.12, 0.53, 0.22, 1)  # Sattes, seriöses Grün
        self.bright_green = (0.18, 0.65, 0.28, 1)   # Helleres Akzent-Grün zum Pulsieren
        
        # 2. Kivy-Standard-Grafiken ausschalten
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        
        # 3. Den Button mit deinen einheitlichen 20dp abgerundeten Ecken zeichnen
                # 3. Den Button mit deinen einheitlichen 20dp abgerundeten Ecken zeichnen
        with self.canvas.before:
            self.rect_color = Color(*self.success_green)
            self.rect_shape = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=[dp(20)]  # Dein globaler 20dp App-Standard!
            )

            
        # 4. Automatisches Mitwandern bei Layout-Verschiebungen
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 5. Die pulsierende Farb-Animation (Dauer: jeweils 1.0 Sekunde für ein sanftes Atmen)
        to_bright = Animation(rgba=self.bright_green, duration=0.2, t='in_out_quad')
        to_dark = Animation(rgba=self.success_green, duration=0.2, t='in_out_quad')
        
        # Verkettung und unendliche Wiederholung aktivieren
        pulse_loop = to_bright + to_dark
        pulse_loop.repeat = True
        pulse_loop.start(self.rect_color)

    def update_rect(self, instance, *args):
        # Aktualisiert die Position und Größe der abgerundeten Form
        instance.rect_shape.pos = instance.pos
        instance.rect_shape.size = instance.size

# ==========================================
# TEST-UMGEBUNG (Deine Lektion ist abgeschlossen)
# ==========================================
class MyApp(App):
    def build(self):
        layout = BoxLayout(padding=dp(50))
        
        # Der fertige Abschluss-Button wird platziert
        fertig_button = FertigPulseButton(
            text="Lektion abschließen", 
            color=(1, 1, 1, 1),  # Weißer Text für perfekten Kontrast auf Grün
            size_hint=(1, 0.15),
            font_size=dp(18)
        )
        
        layout.add_widget(fertig_button)
        return layout

if __name__ == '__main__':
    MyApp().run()
