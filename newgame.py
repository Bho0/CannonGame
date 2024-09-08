from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty

import json
import os
from datetime import datetime

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
            self.save_data()
            app.add_mainpage()
            app.root.current = 'mainpage'
        else:
            self.ids.label.text = "I need to know your name!"
            self.ids.text_input.hint_text = 'Insert here your name'
    
    def save_data(self):
         # Dati da salvare
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            'name': self.ids.text_input.text
        }

        filename = 'save_data.json'

        # Se il file esiste, carica i dati precedenti
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
        else:
            all_data = {}

        # Aggiungi i nuovi dati al dizionario con timestamp come chiave
        all_data[timestamp] = data
        
        # Salva il dizionario aggiornato nel file JSON
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)