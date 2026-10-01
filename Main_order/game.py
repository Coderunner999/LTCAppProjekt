import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.label import Label

# Fenstergröße festlegen
Window.size = (600, 800)
# Nativer dunkelblauer Hintergrund (verhindert Skalierungsfehler auf allen Bildschirmen)
Window.clearcolor = (0.03, 0.03, 0.08, 1)

class StarBackground(Widget):
    """Generiert einen fließenden Sternenhimmel im Hintergrund"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stars = []
        for _ in range(40):
            self.stars.append({
                'pos': [random.randint(0, Window.width), random.randint(0, Window.height)],
                'speed': random.uniform(1, 4),
                'size': random.uniform(1, 3)
            })
        
        with self.canvas:
            self.color = Color(1, 1, 1, 0.7)
            self.ellipses = [Ellipse(pos=s['pos'], size=(s['size'], s['size'])) for s in self.stars]

    def update(self):
        for i, star in enumerate(self.stars):
            # FEHLER BEHOBEN: Verändert jetzt gezielt das Y-Element (Index 1) der Positionsliste
            star['pos'][1] -= star['speed']
            
            # Wenn der Stern unten aus dem Bild fliegt, oben neu generieren
            if star['pos'][1] < 0:
                star['pos'][1] = Window.height
                star['pos'][0] = random.randint(0, Window.width)
                
            self.ellipses[i].pos = star['pos']


class Asteroid(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        size_dim = random.randint(40, 70)
        self.size = (size_dim, size_dim)
        self.pos = (random.randint(0, Window.width - size_dim), Window.height)
        self.speed = random.uniform(5, 9)
        
        with self.canvas:
            # Äußerer rötlicher Schein
            Color(0.9, 0.2, 0.1, 0.3)
            self.glow1 = Ellipse(pos=(self.x - 10, self.y - 10), size=(self.width + 20, self.height + 20))
            # Mittlerer feuriger Kern
            Color(0.9, 0.4, 0.1, 0.7)
            self.glow2 = Ellipse(pos=(self.x - 4, self.y - 4), size=(self.width + 8, self.height + 8))
            # Innerer fester Kern
            Color(0.3, 0.25, 0.25, 1)
            self.core = Ellipse(pos=self.pos, size=self.size)
            
    def move(self):
        self.y -= self.speed
        self.glow1.pos = (self.x - 10, self.y - 10)
        self.glow2.pos = (self.x - 4, self.y - 4)
        self.core.pos = self.pos


class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (64, 64)
        self.pos = (Window.width / 2 - 32, Window.height / 3)
        
        # Sicheres Text-Gitter für die Pixelgrafik des Raumschiffs
        ship_blueprint = [
            "00011000",
            "00111100",
            "01111110",
            "11111111",
            "11111111",
            "11011011",
            "10011001",
            "10000001"
        ]
        
        self.pixel_matrix = [[int(pixel) for pixel in row] for row in ship_blueprint]
        self.pixel_size = self.width / 8
        self.rectangles = []

        with self.canvas:
            Color(0, 0.9, 1, 1) # Neon Cyan
            
            for row_idx, row in enumerate(self.pixel_matrix):
                for col_idx, pixel in enumerate(row):
                    if pixel == 1:
                        p_x = self.x + (col_idx * self.pixel_size)
                        p_y = self.y + ((7 - row_idx) * self.pixel_size)
                        rect = Rectangle(pos=(p_x, p_y), size=(self.pixel_size, self.pixel_size))
                        self.rectangles.append((row_idx, col_idx, rect))
            
    def move(self, touch_x):
        self.x = max(0, min(touch_x - self.width / 2, Window.width - self.width))
        for row_idx, col_idx, rect in self.rectangles:
            rect.pos = (
                self.x + (col_idx * self.pixel_size),
                self.y + ((7 - row_idx) * self.pixel_size)
            )


class GameWidget(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.space_bg = StarBackground()
        self.add_widget(self.space_bg)
        
        self.player = Player()
        self.add_widget(self.player)
        self.asteroids = []
        
        self.score_label = Label(
            text="SCORE: 0", 
            font_size=24, 
            bold=True,
            color=(0, 0.9, 1, 1),
            pos=(30, Window.height - 70)
        )
        self.add_widget(self.score_label)
        
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_asteroid, 0.4)
        
        self.game_over = False

    def spawn_asteroid(self, dt):
        if not self.game_over:
            asteroid = Asteroid()
            self.asteroids.append(asteroid)
            self.add_widget(asteroid)

    def on_touch_move(self, touch):
        if not self.game_over:
            self.player.move(touch.x)

    def on_touch_down(self, touch):
        if self.game_over:
            self.clear_widgets()
                
            self.space_bg = StarBackground()
            self.add_widget(self.space_bg)
            self.player = Player()
            self.add_widget(self.player)
            self.asteroids = []
            self.score = 0
            self.score_label.text = "SCORE: 0"
            self.add_widget(self.score_label)
            self.game_over = False
        else:
            self.player.move(touch.x)

    def update(self, dt):
        if self.game_over:
            return

        self.space_bg.update()
        self.score += 1
        self.score_label.text = f"SCORE: {self.score // 10}"

        for asteroid in self.asteroids[:]:
            asteroid.move()
            
            if (asteroid.x < self.player.x + self.player.width and
                asteroid.x + asteroid.width > self.player.x and
                asteroid.y < self.player.y + self.player.height and
                asteroid.y + asteroid.height > self.player.y):
                
                self.trigger_game_over()

            if asteroid.y < -100:
                self.remove_widget(asteroid)
                self.asteroids.remove(asteroid)

    def trigger_game_over(self):
        self.game_over = True
        game_over_label = Label(
            text=f"CRASH DETECTED\n\nFINAL SCORE: {self.score // 10}\n\n[ Klicke zum System-Reboot ]",
            font_size=32,
            bold=True,
            color=(1, 0.2, 0.2, 1),
            center=Window.center,
            halign="center"
        )
        self.add_widget(game_over_label)


class RetroAsteroidApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    RetroAsteroidApp().run()
