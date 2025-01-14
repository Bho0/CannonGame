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
    # Custom Label that includes a background color and padding
    background_color = ListProperty([1, 1, 1, 1])  # Define a list property to store background color (white with full opacity)
    padding = NumericProperty(10)  # Define padding around the text in the label

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        
        # Drawing the background color and rectangle behind the label text
        with self.canvas.before:
            self.bg_color = Color(*self.background_color)  # Set the background color
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)  # Create a rectangle for the background

        # Bind the size and position of the label to the update_canvas method
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        # Update the background rectangle's size and position whenever the label changes size or position
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
            # If the name input is empty, show an error message
            self.ids.label.text = "I need to know your name!"
            self.ids.text_input.hint_text = 'Insert here your name'  # Provide hint text for the input field
    
    def save_data(self):
        # Method to save the game data when a new game starts
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp as a string
        data = {
            'name': self.ids.text_input.text,  # Store the entered name
            'tutorial': True,  # Set tutorial to True by default
            'levels' : 1,  # Initial level
            'points' : 0,  # Initial points
            'coins' : 0,  # Initial coins
            'bullet': True,  # Bullet is available at the start
            'bomb': False,  # Bomb is not available initially
            'laser': False,  # Laser is not available initially
            'red_dress': True,  # Red dress is selected initially
            'blu_dress': False,  # Blue dress is not bought yet
            'green_dress': False,  # Green dress is not bought yet
            'yellow_dress': False,  # Yellow dress is not bought yet
            'selected_dress': 'red',  # Red dress is selected by default
            'secret': True  # Secret is unlocked at the beginning
        }

        filename = 'save_data.json'  # File where game data will be saved

        # If the save file exists, load the existing data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
        else:
            all_data = {}  # Create an empty dictionary if the file doesn't exist

        # Add the new game data with the timestamp as the key
        all_data[timestamp] = data
        
        # Save the updated data to the file
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
        
        # Load the game with the newly saved data
        self.load_game(timestamp)
    
    def load_game(self, timestamp):
        # Method to load the saved game and navigate to the main game screen
        app = App.get_running_app()
        filename = 'save_data.json'
        
        # If the save file exists, load the data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]

                # Navigate to the MainPage screen
                app.add_screen(MainPage, 'mainpage')
                game_screen = self.manager.get_screen('mainpage')  # Get the new game screen
                game_screen.load_saved_game(save_data, timestamp)  # Load the saved game data into the new screen
                self.manager.current = 'mainpage'  # Switch to the main game screen

    def check_name_repetition(self):
        # Method to check if the entered name already exists in the saved game data
        filename = 'save_data.json'
        
        # If the save file exists, load the data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            # Check each existing player's name in the save data
            for timestamp, data in all_data.items():
                if self.ids.text_input.text == data['name']:
                    return True  # Return True if the name is already taken
        
        return False  # Return False if the name is unique
