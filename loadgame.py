from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

from mainpage import MainPage
from newgame import NewGame

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
                                on_press=lambda btn, ts=timestamp: self.load_game(ts))
                grid.add_widget(button)
    
    def load_game(self, timestamp):
        app = App.get_running_app()
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]

                # Naviga verso il nuovo schermo
                app.add_screen(MainPage, 'mainpage')
                app.add_screen(NewGame, 'newgame')
                game_screen = self.manager.get_screen('mainpage')  # Ottieni il nuovo schermo
                game_screen.load_saved_game(save_data, timestamp)  # Passa i dati al nuovo schermo
                self.manager.current = 'mainpage'  # Cambia schermo