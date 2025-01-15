from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

# Base class for obstacles
class Obstacle(Widget):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent class Widget
        self.key = None  # Placeholder for the key, which will be defined in subclasses
        with self.canvas.before:
            self.rect = Rectangle(source=source, pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos  
        self.rect.size = self.size  
class Rocks(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/Rock.png', **kwargs)
        self.key = 'rocks' 

class Treasure(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/treasure.png', **kwargs)  
        self.key = 'treasure' 


class Perpetios(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/perpetio.png', **kwargs)  
        self.key = 'perpetio' 

class Mirror(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/mirror.png', **kwargs) 
        self.key = 'mirror' 
