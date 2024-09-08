from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label

import json
import os


class LoadGame(Screen):
    def on_enter(self):
        # Quando entri nel carica schermo, mostra i salvataggi disponibili
        grid = self.ids.load_grid
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            grid.add_widget(Label(size_hint_y=None, height=120))

            for timestamp, data in all_data.items():
                button = Button(text=f"Carica salvataggio: {data['name']}",
                                size_hint_y=None, height=40,
                                background_color=(0, 0, 0, .7),
                                on_press=lambda btn, ts=timestamp: self.load_data(ts))
                grid.add_widget(button)