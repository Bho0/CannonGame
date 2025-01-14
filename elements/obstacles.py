# Import necessary modules from Kivy
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

# Base class for obstacles
class Obstacle(Widget):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent class Widget
        self.key = None  # Placeholder for the key, which will be defined in subclasses

        # Create a graphical rectangle to represent the obstacle
        with self.canvas.before:
            self.rect = Rectangle(source=source, pos=self.pos, size=self.size)
            # Bind the rectangle's position and size to the widget's position and size
            self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the position and size of the rectangle when the widget changes
    def update_rect(self, *args):
        self.rect.pos = self.pos  # Update the position
        self.rect.size = self.size  # Update the size

# Class for rocks, inherits from Obstacle
class Rocks(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/Rock.png', **kwargs)  # Pass the source image for the rock
        self.key = 'rocks'  # Assign the key to 'rocks'

# Class for treasure, inherits from Obstacle
class Treasure(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/treasure.png', **kwargs)  # Pass the source image for the treasure
        self.key = 'treasure'  # Assign the key to 'treasure'

# Class for perpetios, inherits from Obstacle
class Perpetios(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/perpetio.png', **kwargs)  # Pass the source image for perpetios
        self.key = 'perpetio'  # Assign the key to 'perpetio'

# Class for mirror, inherits from Obstacle
class Mirror(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(source='images/mirror.png', **kwargs)  # Pass the source image for the mirror
        self.key = 'mirror'  # Assign the key to 'mirror'
