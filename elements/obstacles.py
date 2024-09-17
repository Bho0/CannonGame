from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color , Ellipse

class rocks(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'rocks'
        with self.canvas:
            Color(1, 0, 1, 1)  # White color for rock
            self.circle = Ellipse(size=(50, 50), pos=self.pos)  # Set initial size and position

        # Bind to update the Ellipse when the widget size or position changes
        self.bind(pos=self.update_shape, size=self.update_shape)
     
        # Debug: track changes to size
        self.bind(size=self.on_size_change)

    def on_size_change(self, instance, value):
        print(f"Size changed: {value}")
    def update_shape(self, *args):
        # Update the position and size of the ellipse to match the widget
        self.circle.pos = self.pos
       


class perpetios(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'perpetios'
        self.size = (50, 50)
        self.size_hint = (None, None)
        with self.canvas:
            Color(1, 1, 1, 1)  # Purple color for perpetio
            self.circle = Ellipse(size=(50, 50), pos=self.pos)  # Set initial size and position

        # Bind to update the Ellipse when the widget size or position changes
        self.bind(pos=self.update_shape)

    def update_shape(self, *args):
        # Update the position and size of the ellipse to match the widget
        self.circle.pos = self.pos