
from kivy.graphics import StencilPush, StencilUse, StencilUnUse, StencilPop, RoundedRectangle

#original_init = Button.__init__

# 2. Neue __init__ definieren, die NUR eine runde Maske über den Button legt
def custom_init(self, **kwargs):
    #original_init(self, **kwargs)
    
    # Wir starten die Schablone VOR dem Zeichnen des Buttons
    with self.canvas.before:
        StencilPush()
        self.stencil_before = RoundedRectangle(pos=self.pos, size=self.size, radius=[30]) # 10 Pixel Rundung
        StencilUse()
        
    # Wir schließen die Schablone NACH dem Zeichnen des Buttons wieder
    with self.canvas.after:
        StencilUnUse()
        self.stencil_after = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        StencilPop()
        
    # Die Maske muss mitwandern, wenn sich die Position oder Größe ändert
    self.bind(pos=update_stencil, size=update_stencil)

# 3. Hilfsfunktion, damit die runden Ecken bei Größenänderungen exakt mitgehen
def update_stencil(instance, *args):
    instance.stencil_before.pos = instance.pos
    instance.stencil_before.size = instance.size
    instance.stencil_after.pos = instance.pos
    instance.stencil_after.size = instance.size

# 4. Die originale Kivy-Button Klasse global überschreiben
#Button.__init__ = custom_init