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
                # Usa un'immagine per la bomba
                self.shape = Rectangle(source='images/bomb.png', pos=self.pos, size=self.size)
            elif self.key == 'bullet':
                # Se vuoi continuare a usare un'ellisse per il proiettile, lascia il codice come prima
                self.shape = Ellipse(pos=self.pos, size=(self.width, self.height))
            else:
                # Usa un rettangolo per altre forme
                self.shape = Rectangle(size=size, pos=self.pos)

        self.bind(pos=self.update_shape, size=self.update_shape)

        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        # Aggiorna la posizione e le dimensioni della forma
        self.shape.pos = self.pos
        if self.key == 'bomb' or self.key == 'bullet':
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
        super().__init__(color=(1, 1, 1, 1), size=(50, 50), **kwargs)  # Bianco come colore dell'eraser

    def update_shape(self, *args):
        # Aggiorna la forma dell'eraser (può essere rettangolare o circolare come per il bomb)
        self.shape.pos = self.pos
        # Mantiene una forma rettangolare per l'eraser
        self.shape.size = self.size