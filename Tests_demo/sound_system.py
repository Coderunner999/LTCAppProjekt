
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label

class LektionAbgeschlossenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Sound VORLADEN beim Erstellen des Screens (Perfekt für die Performance)
        # SoundLoader wählt auf Android automatisch den richtigen Player
        self.sound = SoundLoader.load('level_complete.mp3')
        
        # Einfacher, großer Text in der Mitte
        self.add_widget(Label(
            text="Lektion abgeschlossen!\n(Sound startet jetzt)", 
            font_size='32sp',
            halign='center'
        ))

    def on_enter(self, *args):
        # 2. Sound beim Betreten des Screens sofort ohne Verzögerung abspielen
        try:
            if self.sound:
                self.sound.play()
            else:
                print("Fehler: Sounddatei konnte beim Start nicht geladen werden.")
        except Exception as e:
            print(f"Fehler beim Abspielen: {e}")

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LektionAbgeschlossenScreen(name='erfolg'))
        return sm

if __name__ == '__main__':
    TestApp().run()

