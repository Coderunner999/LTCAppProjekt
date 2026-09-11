from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.button import Button

class QuizTestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        frage = Label(
            text="Testfrage: Ist das Zwei-Klick-System aktiv?",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )

        self.option1 = Button(
            text="Falsche Antwort",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.option1.bind(on_press=self.antwort_falsch)

        self.option2 = Button(
            text="Richtige Antwort (2x klicken)",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.option2.bind(on_press=self.antwort_richtig)

        layout.add_widget(frage)
        layout.add_widget(self.option1)
        layout.add_widget(self.option2)
        self.add_widget(layout)

    def antwort_falsch(self, instance):
        self.option1.background_color = (0.9, 0.3, 0.3, 1)

    def antwort_richtig(self, instance):
        # 1. Klick-Prüfung: Ist der Button noch nicht hellgrün?
        if instance.background_color != [0.3, 0.9, 0.3, 1]:
            # Eventuelle Fehlerfarben anderer Optionen zurücksetzen
            self.option1.background_color = (1, 1, 1, 1)
            if hasattr(self, 'option3'):  # Falls der Screen 3 Optionen hat
                self.option3.background_color = (1, 1, 1, 1)
            
            # Button hellgrün färben
            instance.background_color = (0.3, 0.9, 0.3, 1)
            return  # Auf den zweiten Klick warten

        # 2. Klick: Farbe zurücksetzen und zum nächsten Screen springen
        instance.background_color = (1, 1, 1, 1)
        self.manager.current = 'erfolg_screen'


class ErfolgScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        label = Label(
            text="Erfolgreich weitergeleitet!",
            font_size=50,
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        layout.add_widget(label)
        self.add_widget(layout)

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.transition = NoTransition()
        sm.add_widget(QuizTestScreen(name='quiz_screen'))
        sm.add_widget(ErfolgScreen(name='erfolg_screen'))
        return sm

if __name__ == '__main__':
    TestApp().run()

