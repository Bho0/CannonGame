from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty

import json
import os

class Cannon(Popup):
    def select_projectile(self, projectile_type):        
        if self.selected_projectile == projectile_type:
            self.selected_projectile = ''
        else:
            self.selected_projectile = projectile_type
    
    def open(self, timestamp):
        grid = self.ids.ammo_grid
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

            for projectile in save_data['projectiles']:
                button = ToggleButton(text=f"{projectile} dress",
                                on_press=lambda btn, pr=projectile: self.select_projectile(pr)
                                )
                grid.add_widget(button)

class Ship(Screen):
    timestamp = StringProperty("")
    selected_projectile = StringProperty('')

    def load_screen(self, timestamp):
        self.timestamp = timestamp
    
    def goto_captain(self, timestamp):
        game_screen = self.manager.get_screen('captain')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'captain'  # Cambia schermo

class Captain(Screen):
    selected_dress = StringProperty('')

    def select_dress(self, dress_type):
        
        if self.selected_dress == dress_type:
            self.selected_dress = ''
        else:
            self.selected_dress = dress_type
    
    def load_screen(self, timestamp):
        grid = self.ids.cap_grid
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

            for dress in save_data['dresses']:
                button = ToggleButton(text=f"{dress} dress",
                                group='C',
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr=dress: self.select_dress(dr)
                                )
                grid.add_widget(button)