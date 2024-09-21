from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line

class rocks(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'rocks'

        with self.canvas.before:
             self.rect = Rectangle(source='images/Rock.png', pos=self.pos, size=self.size)
             self.bind(size=self.update_rect)
         

    def update_rect(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.size = self.size
        self.rect.pos = self.pos
       
class treasure(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'treasure'

        with self.canvas.before:
             self.rect = Rectangle(source='images/treasure.png', pos=self.pos, size=self.size)
             self.bind(size=self.update_rect)
         

    def update_rect(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.size = self.size
        self.rect.pos = self.pos

class perpetios(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'perpetios'

        with self.canvas.before:
             self.rect = Rectangle(source='Cannon_project/Rock.png', pos=self.pos, size=(50, 50))
             self.bind(pos=self.update_rect, size=self.update_rect)

         

    def update_rect(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.pos = self.pos
        self.rect.size = self.size