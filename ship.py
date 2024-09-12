from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty

import json
import os

class Ship(Screen):
    timestamp = StringProperty("")
    selected_projectile = StringProperty('')

    def load_screen(self, timestamp):
        self.timestamp = timestamp
    
    def goto_captain(self, timestamp):
        game_screen = self.manager.get_screen('captain')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'captain'  # Cambia schermo
    
    def goto_projectile(self, timestamp):
        game_screen = self.manager.get_screen('projectile')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'projectile'  # Cambia schermo

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

            if save_data['red_dress'] == True:
                button = ToggleButton(text=f"red dress",
                                group='C',
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='red_dress': self.select_dress(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)
            
            if save_data['blu_dress'] == True:
                button = ToggleButton(text=f"blu dress",
                                group='C',
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='blu_dress': self.select_dress(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)
            
            if save_data['green_dress'] == True:
                button = ToggleButton(text=f"green dress",
                                group='C',
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='green_dress': self.select_dress(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)
            
            if save_data['yellow_dress'] == True:
                button = ToggleButton(text=f"yellow dress",
                                group='C',
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='yellow_dress': self.select_dress(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)

class Projectile(Screen):
    selected_projectile = StringProperty('')

    def select_projectile(self, projectile_type):        
        if self.selected_projectile == projectile_type:
            self.selected_projectile = ''
        else:
            self.selected_projectile = projectile_type
    
    def load_screen(self, timestamp):
        grid = self.ids.ammo_grid
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

            if save_data['bullet'] == True:
                button = ToggleButton(text=f"bullet",
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='bullet': self.select_projectile(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)
            
            if save_data['bomb'] == True:
                button = ToggleButton(text=f"bomb",
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='bomb': self.select_projectile(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)
            
            if save_data['laser'] == True:
                button = ToggleButton(text=f"laser",
                                background_normal='images\captain.png',
                                on_press=lambda btn, dr='laser': self.select_projectile(dr)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)