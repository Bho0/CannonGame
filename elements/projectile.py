# Import necessary Kivy modules
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle

# Base class for projectiles
class Projectile(Widget):
    def __init__(self, color, size, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent Widget class
        self.size_hint = (None, None)  # Disable automatic resizing
        self.size = size  # Set the size of the projectile

        # Draw the projectile's shape on the canvas
        with self.canvas:
            Color(*color)  # Set the color using the RGBA values passed as argument
            if self.key == 'bomb':
                # If the key is 'bomb', use an image for the bomb projectile
                self.shape = Rectangle(source='images/bomb.png', pos=self.pos, size=self.size)
            elif self.key == 'bullet':
                # If the key is 'bullet', use an Ellipse for the bullet projectile
                self.shape = Ellipse(pos=self.pos, size=(self.width, self.height))
            else:
                # Use a rectangle for other shapes
                self.shape = Rectangle(size=size, pos=self.pos)

        # Bind the position and size of the shape to the widget's position and size
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        # Update the position and size of the shape based on the widget's properties
        self.shape.pos = self.pos  # Update position
        if self.key == 'bomb' or self.key == 'bullet':
            # If it's a bomb or bullet, set the shape's size to be a circle (diameter = min(width, height))
            diameter = min(self.width, self.height)
            self.shape.size = (diameter, diameter)

# Bomb class inheriting from Projectile
class Bomb(Projectile):
    def __init__(self, **kwargs):
        self.key = 'bomb'  # Set the key for the bomb
        super().__init__(color=(0, 0, 0, 1), size=(50, 50), **kwargs)  # Call parent constructor with specific color and size

# Bullet class inheriting from Projectile
class Bullet(Projectile):
    def __init__(self, **kwargs):
        self.key = 'bullet'  # Set the key for the bullet
        super().__init__(color=(0, 0, 0, 1), size=(50, 50), **kwargs)  # Call parent constructor with specific color and size

# Laser class inheriting from Projectile
class Laser(Projectile):
    def __init__(self, **kwargs):
        self.key = 'laser'  # Set the key for the laser
        super().__init__(color=(1, 0, 0, 0), size=(10, 10), **kwargs)  # Call parent constructor with specific color and size

# Eraser class inheriting from Projectile
class Eraser(Projectile):
    def __init__(self, size=(30, 30), **kwargs):
        self.key = 'eraser'  # Set the key for the eraser
        super().__init__(color=(1, 1, 1, 0), size=(10, 10), **kwargs)  # Call parent constructor with white color (transparent)
    
    def update_shape(self, *args):
        # Override the update_shape method for the eraser (can be rectangular or circular as for the bomb)
        self.shape.pos = self.pos  # Update position
        # Keep the eraser shape as rectangular with the specified size
        self.shape.size = self.size
