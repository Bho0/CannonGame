from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle

# Base class for projectiles
class Projectile(Widget):
    def __init__(self, color, size, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent Widget class
        self.size_hint = (None, None)
        self.size = size  

        with self.canvas:
            Color(*color)  
            if self.key == 'bomb':
                self.shape = Rectangle(source='images/bomb.png', pos=self.pos, size=self.size)
            elif self.key == 'bullet':
                self.shape = Ellipse(pos=self.pos, size=(self.width, self.height))
            else:
                self.shape = Rectangle(size=size, pos=self.pos)

        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.shape.pos = self.pos  
        if self.key == 'bomb' or self.key == 'bullet':
            diameter = min(self.width, self.height)
            self.shape.size = (diameter, diameter)

class Bomb(Projectile):
    def __init__(self, **kwargs):
        self.key = 'bomb' 
        super().__init__(color=(0, 0, 0, 1), size=(50, 50), **kwargs)  # Call parent constructor with specific color and size


class Bullet(Projectile):
    def __init__(self, **kwargs):
        self.key = 'bullet'  
        super().__init__(color=(0, 0, 0, 1), size=(50, 50), **kwargs)  # Call parent constructor with specific color and size


class Laser(Projectile):
    def __init__(self, **kwargs):
        self.key = 'laser'  
        super().__init__(color=(1, 0, 0, 0), size=(10, 10), **kwargs)  # Call parent constructor with specific color and size


class Eraser(Projectile):
    def __init__(self, size=(30, 30), **kwargs):
        self.key = 'eraser'  
        super().__init__(color=(1, 1, 1, 0), size=(10, 10), **kwargs)  # Call parent constructor with white color (transparent)
    
    def update_shape(self, *args):
        self.shape.pos = self.pos 
        self.shape.size = self.size
