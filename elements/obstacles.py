from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line

class rocks(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'rocks'

        with self.canvas.before:
             self.rect = Rectangle(source='images/Default_rock_3_2d019bb5-fdea-4fbb-9776-7b6f9ba6e114_0.png', pos=self.pos, size=self.size)
             self.bind(size=self.update_rect)
        
        self.add_bb(self)
    
    def add_bb (self, widget):
        with widget.canvas.after:
            Color(1, 0, 0, 1)
            Line(rectangle = (widget.x, widget.y, widget.width, widget.height), width = 2)
         

    def update_rect(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.size = self.size
        self.rect.pos = self.pos
       
class treasure(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'treasure'

        with self.canvas.before:
             self.rect = Rectangle(source='images/Default_treasure_3_7c767107-12f9-43e5-a19b-b7361e4a4b48_0.png', pos=self.pos, size=(100, 100))
             self.bind(pos=self.update_rect, size=self.update_rect)

         

    def update_rect(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.pos = self.pos
        self.rect.size = self.size

class perpetios(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'perpetios'

        with self.canvas.before:
             self.rect = Rectangle(source='Cannon_project\Rock.png', pos=self.pos, size=(50, 50))
             self.bind(pos=self.update_rect, size=self.update_rect)

         

    def update_rect(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.pos = self.pos
        self.rect.size = self.size