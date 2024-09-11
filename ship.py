from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

import json
import os

class Ship(Screen):
    timestamp = StringProperty("")
    selected_projectile = StringProperty('')

    def load_screen(self, timestamp):
        self.timestamp = timestamp
        
    def select_projectile(self, projectile_type):
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if self.timestamp in all_data:
                save_data = all_data[self.timestamp]
        
        if self.selected_projectile == projectile_type:
            self.selected_projectile = ''
        else:
            self.selected_projectile = projectile_type

class Captain(Screen):
    selected_dress = StringProperty('')

    def select_dress(self, dress_type):
        
        if self.selected_dress == dress_type:
            self.selected_dress = ''
        else:
            self.selected_dress = dress_type