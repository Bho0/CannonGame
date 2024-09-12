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

    def select_dress(self, dress_type, timestamp):
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]

        if self.selected_dress == dress_type:
            self.selected_dress = ''
            updated_data = {
                'name': save_data['name'],
                'tutorial': save_data['tutorial'],
                'levels' : save_data['levels'],
                'coins' : save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': 'red',
                'selected_projectiles': save_data['selected_projectiles']
            }

            # Aggiungi i nuovi dati al dizionario con timestamp come chiave
            all_data[timestamp] = updated_data
            
            # Salva il dizionario aggiornato nel file JSON
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)

        else:
            self.selected_dress = dress_type
            updated_data = {
                'name': save_data['name'],
                'tutorial': save_data['tutorial'],
                'levels' : save_data['levels'],
                'coins' : save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': dress_type,
                'selected_projectiles': save_data['selected_projectiles']
            }

            # Aggiungi i nuovi dati al dizionario con timestamp come chiave
            all_data[timestamp] = updated_data
            
            # Salva il dizionario aggiornato nel file JSON
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)

    
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
                                on_press=lambda btn, dr='red', ts=timestamp: self.select_dress(dr,ts)
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
                                on_press=lambda btn, dr='blu', ts=timestamp: self.select_dress(dr,ts)
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
                                on_press=lambda btn, dr='green', ts=timestamp: self.select_dress(dr,ts)
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
                                on_press=lambda btn, dr='yellow', ts=timestamp: self.select_dress(dr,ts)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)

class Projectile(Screen):
    selected_projectile = StringProperty('')

    def select_projectile(self, projectile_type, timestamp):
        flag = True
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]

        if self.selected_projectile == projectile_type:
            self.selected_projectile = ''
            save_data['selected_projectiles'].remove(projectile_type)
            if save_data['selected_projectiles'] == []:
                save_data['selected_projectiles'].append('bullet')

            updated_data = {
                'name': save_data['name'],
                'tutorial': save_data['tutorial'],
                'levels' : save_data['levels'],
                'coins' : save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': save_data['selected_dress'],
                'selected_projectiles': save_data['selected_projectiles']
            }

            # Aggiungi i nuovi dati al dizionario con timestamp come chiave
            all_data[timestamp] = updated_data
            
            # Salva il dizionario aggiornato nel file JSON
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)

        else:
            self.selected_projectile = projectile_type
            for type in save_data['selected_projectiles']:
                if type == projectile_type:
                    flag = False
            if flag == True:
                save_data['selected_projectiles'].append(projectile_type)
            updated_data = {
                'name': save_data['name'],
                'tutorial': save_data['tutorial'],
                'levels' : save_data['levels'],
                'coins' : save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': save_data['selected_dress'],
                'selected_projectiles': save_data['selected_projectiles']
            }

            # Aggiungi i nuovi dati al dizionario con timestamp come chiave
            all_data[timestamp] = updated_data
            
            # Salva il dizionario aggiornato nel file JSON
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
    
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
                                on_press=lambda btn, dr='bullet', ts=timestamp: self.select_projectile(dr, ts)
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
                                on_press=lambda btn, dr='bomb', ts=timestamp: self.select_projectile(dr, ts)
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
                                on_press=lambda btn, dr='laser', ts=timestamp: self.select_projectile(dr, ts)
                                )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT OWNED",
                                disabled=True
                                )
                grid.add_widget(button)