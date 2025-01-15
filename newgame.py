from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty

from mainpage import MainPage

import json
import os
from datetime import datetime

class CustomLabel(Label):
    background_color = ListProperty([1, 1, 1, 1]) 
    padding = NumericProperty(10)  

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        
        # Drawing the background color and rectangle behind the label text
        with self.canvas.before:
            self.bg_color = Color(*self.background_color)  
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)  

        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

class NewGame(Screen):
    def check_name(self):
        # Method to check if the player has entered a valid name
        app = App.get_running_app()
        
        # Check if the text input is not empty
        if self.ids.text_input.text.strip():
            # Check if the name is already taken by another pirate
            if self.check_name_repetition():
                self.ids.label.text = "There exists another pirate with the same name, choose another name"
            else:
                # If valid, proceed to save the data
                self.save_data()
        else:
            self.ids.label.text = "I need to know your name!"
            self.ids.text_input.hint_text = 'Insert here your name'  # Provide hint text for the input field
    
    def save_data(self):
        # Method to save the game data when a new game starts
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp as a string
        data = {
            'name': self.ids.text_input.text,  
            'tutorial': True,  
            'levels' : 1,  
            'points' : 0,  
            'coins' : 0,  
            'bullet': True,  
            'bomb': False,  
            'laser': False, 
            'red_dress': True,  
            'blu_dress': False,  
            'green_dress': False,  
            'yellow_dress': False,  
            'selected_dress': 'red',  
        }

        filename = 'save_data.json' 

        # If the save file exists, load the existing data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
        else:
            all_data = {}  # Create an empty dictionary if the file doesn't exist

        all_data[timestamp] = data
        
        # Save the updated data to the file
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
        
  
        self.load_game(timestamp)
    
    def load_game(self, timestamp):
        app = App.get_running_app()
        filename = 'save_data.json'
        
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]

                app.add_screen(MainPage, 'mainpage')
                game_screen = self.manager.get_screen('mainpage')  
                game_screen.load_saved_game(save_data, timestamp)  
                self.manager.current = 'mainpage'

    def check_name_repetition(self):
        filename = 'save_data.json'
        
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            for timestamp, data in all_data.items():
                if self.ids.text_input.text == data['name']:
                    return True  # Return True if the name is already taken
        
        return False
