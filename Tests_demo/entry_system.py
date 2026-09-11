
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

class Main(App):
    def build(self):
        layout = FloatLayout()
        
        welcome = Label(
            text="Wie kann ich dir helfen?",
            font_size='27sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        
        # Ein stinknormales Kivy-TextInput ohne fehleranfällige Canvas-Hacks
        entry = TextInput(
            size_hint=(0.6, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            foreground_color=(1, 1, 1, 1),
            multiline=False,
            padding=(15, 12, 15, 0),
            background_normal='', # Entfernt die Standard-Kivy-Textur
            background_color=(0.28, 0.28, 0.28, 0) # Völlig transparent, wir nutzen das Layout darunter
        )
        
        # Wir hängen die runden Ecken direkt an das Layout, genau an die Position des Textfeldes
        with layout.canvas.before:
            Color(0.28, 0.28, 0.28, 1) # Dein Standard-Grau
            # Wir erstellen das Rechteck temporär
            layout.rect = RoundedRectangle(radius=[10])
            
        # Diese Funktion sorgt dafür, dass sich die grauen runden Ecken IMMER mit dem Textfeld mitbewegen
        def update_canvas_rect(instance, value):
            layout.rect.pos = entry.pos
            layout.rect.size = entry.size
            
        entry.bind(pos=update_canvas_rect, size=update_canvas_rect)
        
        layout.add_widget(welcome)
        layout.add_widget(entry)
        return layout

if __name__ == '__main__':
    Main().run()


