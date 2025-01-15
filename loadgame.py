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
        grid = self.ids.load_grid 
        grid.clear_widgets() 

        filename = 'save_data.json'  
        if os.path.exists(filename): 
            with open(filename, 'r') as f:
                all_data = json.load(f) 
            grid.add_widget(Label(size_hint_y=None, height=120))  # Add a spacer label for layout

           
            for timestamp, data in all_data.items():
                # Create a button for each saved game
                button = Button(
                    text=f"Carica salvataggio: {data['name']}",  #
                    size_hint_y=None,  
                    height=40,  
                    background_color=(0, 0, 0, .7), 
                    on_press=lambda btn, ts=timestamp: self.load_game(ts)  
                )
                grid.add_widget(button) 

    def load_game(self, timestamp):
        # This method loads the game based on the selected save game timestamp.

        app = App.get_running_app() 
        filename = 'save_data.json' 

        if os.path.exists(filename): 
            with open(filename, 'r') as f:
                all_data = json.load(f) 
            
            if timestamp in all_data: 
                save_data = all_data[timestamp] 

                app.add_screen(MainPage, 'mainpage')  
                app.add_screen(NewGame, 'newgame')  

               
                game_screen = self.manager.get_screen('mainpage')
               
                game_screen.load_saved_game(save_data, timestamp)
                self.manager.current = 'mainpage' 
