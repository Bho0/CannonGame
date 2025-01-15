from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.app import App

from mainpage import MainPage

import json
import os

class Ship(Screen):
    timestamp = StringProperty("")  # Store the timestamp for the current game session
    selected_projectile = StringProperty('')  # Store the selected projectile type

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.projectile_popup = None 

    def load_screen(self, timestamp):
        self.timestamp = timestamp 
    
    def goto_captain(self, timestamp):
        game_screen = self.manager.get_screen('captain') 
        game_screen.load_screen(timestamp) 
        self.manager.current = 'captain' 
    
    def goto_projectile(self, timestamp):
        if not self.projectile_popup:  
            self.projectile_popup = Projectile_Popup() 
        self.projectile_popup.load_popup(timestamp) 
        self.projectile_popup.open()  

    def goto_mainpage(self, timestamp):
        app = App.get_running_app()  # Get the running instance of the app
        app.add_screen(MainPage, 'mainpage')
        filename = 'save_data.json'  # Define the file for saving data
        
        if os.path.exists(filename):  
            with open(filename, 'r') as f:
                all_data = json.load(f)  
            
            if timestamp in all_data:
                save_data = all_data[timestamp] 
                game_screen = self.manager.get_screen('mainpage') 
                game_screen.load_saved_game(save_data, timestamp) 
                self.manager.current = 'mainpage' 

class Captain(Screen):
    selected_dress = StringProperty('')  

    def select_dress(self, dress_type, timestamp):
        filename = 'save_data.json'
        if os.path.exists(filename):  
            with open(filename, 'r') as f:
                all_data = json.load(f)  
            
            if timestamp in all_data: 
                save_data = all_data[timestamp] 

        # Check if the selected dress is the same as the current dress
        if self.selected_dress == dress_type:
            self.selected_dress = ''  # If the same dress is selected, reset the selection
            updated_data = {
                'name': save_data['name'],
                'tutorial': save_data['tutorial'],
                'levels': save_data['levels'],
                'points': save_data['points'],
                'coins': save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': 'red', 
            }

           
            all_data[timestamp] = updated_data
            
  
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
        else:
  
            self.selected_dress = dress_type
            updated_data = {
                'name': save_data['name'],
                'tutorial': save_data['tutorial'],
                'levels': save_data['levels'],
                'points': save_data['points'],
                'coins': save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': dress_type, 
            }

            all_data[timestamp] = updated_data
            
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)

    def load_screen(self, timestamp):
        grid = self.ids.cap_grid# Get the grid for displaying the dress options
        grid.clear_widgets()  
        filename = 'save_data.json'  
        if os.path.exists(filename):  
            with open(filename, 'r') as f:
                all_data = json.load(f) 

            if timestamp in all_data:  
                save_data = all_data[timestamp] 

            # Create toggle buttons for each available dress based on the saved data
            if save_data['red_dress'] == True:
                button = ToggleButton(text=f"red dress",
                                      group='C',
                                      font_name='fonts/Caribbean.ttf',
                                      background_normal='images/captain.png',
                                      on_press=lambda btn, dr='red', ts=timestamp: self.select_dress(dr, ts)
                                      )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED",
                                      font_name='fonts/Caribbean.ttf',
                                      disabled=True
                                      )
                grid.add_widget(button)
            
            if save_data['blu_dress'] == True:
                button = ToggleButton(text=f"blu dress",
                                      font_name='fonts/Caribbean.ttf',
                                      group='C',
                                      background_normal='images/blue_dress.png',
                                      on_press=lambda btn, dr='blu', ts=timestamp: self.select_dress(dr, ts)
                                      )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED",
                                      font_name='fonts/Caribbean.ttf',
                                      disabled=True
                                      )
                grid.add_widget(button)
            
            if save_data['green_dress'] == True:
                button = ToggleButton(text=f"green dress",
                                      font_name='fonts/Caribbean.ttf',
                                      group='C',
                                      background_normal='images/green_dress(1).png',
                                      on_press=lambda btn, dr='green', ts=timestamp: self.select_dress(dr, ts)
                                      )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED",
                                      font_name='fonts/Caribbean.ttf',
                                      disabled=True
                                      )
                grid.add_widget(button)
            
            if save_data['yellow_dress'] == True:
                button = ToggleButton(text=f"yellow dress",
                                      group='C',
                                      font_name='fonts/Caribbean.ttf',
                                      background_normal='images/yellow_dress.png',
                                      on_press=lambda btn, dr='yellow', ts=timestamp: self.select_dress(dr, ts)
                                      )
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED",
                                      font_name='fonts/Caribbean.ttf',
                                      disabled=True
                                      )
                grid.add_widget(button)

class Projectile_Popup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.title = "" 
        self.size_hint = (0.5, 0.5)  
        self.auto_dismiss = True  

    def load_popup(self, timestamp):
        grid = self.ids.ammo_grid 
        grid.clear_widgets()  

        filename = 'save_data.json'  
        if os.path.exists(filename): 
            with open(filename, 'r') as f:
                all_data = json.load(f)  

            if timestamp in all_data: 
                save_data = all_data[timestamp] 

            # Create labels for each available projectile based on the saved data
            if save_data['bullet'] == True:
                button = Label(text=f"bullet", font_name='fonts/Caribbean.ttf', size_hint_y=.3)
                grid.add_widget(button)
            else: 
                button = Label(text=f"NOT  OWNED", font_name='fonts/Caribbean.ttf', font_size=12, size_hint_y=.3)
                grid.add_widget(button)
            
            if save_data['bomb'] == True:
                button = Label(text=f"bomb", font_name='fonts/Caribbean.ttf', size_hint_y=.3)
                grid.add_widget(button)
            else: 
                button = Label(text=f"NOT  OWNED", font_name='fonts/Caribbean.ttf', font_size=12, size_hint_y=.3)
                grid.add_widget(button)
            
            if save_data['laser'] == True:
                button = Label(text=f"laser", font_name='fonts/Caribbean.ttf', size_hint_y=.3)
                grid.add_widget(button)
            else: 
                button = Label(text=f"NOT  OWNED", font_name='fonts/Caribbean.ttf', font_size=12, size_hint_y=.3)
                grid.add_widget(button)
