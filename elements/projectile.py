from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle

class Projectile(Widget):
    def __init__(self, color, size, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size

        with self.canvas:
            Color(*color)  # Colore passato come argomento
            if self.key == 'bomb':
                self.shape = Ellipse(pos=self.pos, size=(self.width, self.height))
            else:
                self.shape = Rectangle(size=size, pos=self.pos)

        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        # Aggiorna la posizione e le dimensioni della forma
        self.shape.pos = self.pos
        if self.key == 'bomb':
            diameter = min(self.width, self.height)
            self.shape.size = (diameter, diameter)


class Bomb(Projectile):
    def __init__(self, **kwargs):
        self.key = 'bomb'
        super().__init__(color=(0, 0, 0, 1), size=(50, 50), **kwargs)  # Colore e dimensioni specifiche

class Bullet(Projectile):
    def __init__(self, **kwargs):
        self.key = 'bullet'
        super().__init__(color=(0, 0, 0, 1), size=(50, 50), **kwargs)  # Colore e dimensioni specifiche

class Laser(Projectile):
    def __init__(self, **kwargs):
        self.key = 'laser'
        super().__init__(color=(1, 0, 0, 1), size=(.5,.5), **kwargs)  # Colore e dimensioni specifiche

class Eraser(Projectile):
    def __init__(self, size=(30, 30), **kwargs):
        # Chiamata al costruttore della classe padre Projectile con il colore specifico per l'eraser
        self.key = 'eraser'
        super().__init__(color=(1, 1, 1, 1), size=size, **kwargs)  # Bianco come colore dell'eraser

    def update_shape(self, *args):
        # Aggiorna la forma dell'eraser (può essere rettangolare o circolare come per il bomb)
        self.shape.pos = self.pos
        # Mantiene una forma rettangolare per l'eraser
        self.shape.size = self.size