from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

class Obstacle(Widget):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.key = None  # Placeholder, da specificare nelle classi figlio

        # Configurazione del rettangolo grafico
        with self.canvas.before:
            self.rect = Rectangle(source=source, pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        # Aggiorna la posizione e la dimensione del rettangolo
        self.rect.pos = self.pos
        self.rect.size = self.size

# Classe rocks che eredita da Obstacle
class Rocks(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/Rock.png', **kwargs)
        self.key = 'rocks'

# Classe treasure che eredita da Obstacle
class Treasure(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/treasure.png', **kwargs)
        self.key = 'treasure'

# Classe perpetios che eredita da Obstacle
class Perpetios(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='image/perpetio.png', **kwargs)
        self.key = 'perpetios'

# Classe mirror che eredita da Obstacle
class Mirror(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/mirror.png', **kwargs)
        self.key = 'mirror'
