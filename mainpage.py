from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty

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


class MainPage(Screen):
    texts = ListProperty(["Tutorial1", "Tutorial2", "Tutorial3", "Tutorial4"])
    index = 0

    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids.level_button.opacity = 0
        self.ids.level_button.disabled = True
        self.ids.level_label.opacity = 0

        self.ids.ship_button.opacity = 0
        self.ids.ship_button.disabled = True
        self.ids.ship_label.opacity = 0

        self.ids.market_button.opacity = 0
        self.ids.market_button.disabled = True
        self.ids.market_label.opacity = 0

        self.ids.option_button.opacity = 0
        self.ids.option_button.disabled = True

    def change_text(self):
        # Incrementa l'indice
        self.index += 1
        
        # Controlla se siamo all'ultimo elemento
        if self.index < len(self.texts):
            self.ids.tutorial_label.text = self.texts[self.index]
        else:
            # Nascondi il bottone quando si raggiunge l'ultimo elemento
            self.ids.tutorial_button.opacity = 0  # Rende il bottone invisibile
            self.ids.tutorial_button.disabled = True  # Disabilita il bottone
            self.ids.tutorial_label.opacity = 0
            self.ids.cap_img.opacity = 0
            
            self.ids.level_button.opacity = 1
            self.ids.level_button.disabled = False
            self.ids.level_label.opacity = 1

            self.ids.ship_button.opacity = 1
            self.ids.ship_button.disabled = False
            self.ids.ship_label.opacity = 1

            self.ids.market_button.opacity = 1
            self.ids.market_button.disabled = False
            self.ids.market_label.opacity = 1

            self.ids.option_button.opacity = 1
            self.ids.option_button.disabled = False