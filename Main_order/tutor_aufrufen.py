
from kivy.app import App
from kivy.uix.button import Button
import os
import webbrowser

class MyApp(App):

  def build(self):
    return Button(
        text="Website öffnen", on_press=lambda x: webbrowser.open("https://ltctutor-mobile.netlify.app")
    )


MyApp().run()