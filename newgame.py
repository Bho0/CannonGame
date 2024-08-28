from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty

from mainpage import MainPage

class CustomLabel(Label):
    # Create a property to dynamically store the background color
    background_color = ListProperty([1, 1, 1, 1])  # White with full opacity
    padding = NumericProperty(10)  # Padding around the text

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*self.background_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        # Bind size and pos updates to the update_canvas method
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        # Update the size and position of the rectangle
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

class NewGame(Screen):
    def check_name(self):
        app = App.get_running_app()
        if self.ids.text_input.text.strip():
            app.add_mainpage()
            app.root.current = 'mainpage'
        else:
            self.ids.label.text = "I need to know your name!"
            self.ids.text_input.hint_text = 'Insert here your name'