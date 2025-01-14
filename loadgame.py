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
        # This method is called when the screen is entered (visible to the user).
        # It loads available saved games into the interface.

        grid = self.ids.load_grid  # Get the GridLayout widget where save game buttons will be added
        grid.clear_widgets()  # Clear any existing widgets in the grid before adding new ones

        filename = 'save_data.json'  # Specify the filename that stores the save data
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the data from the JSON file
            
            grid.add_widget(Label(size_hint_y=None, height=120))  # Add a spacer label for layout

            # Loop through the loaded save data
            for timestamp, data in all_data.items():
                # Create a button for each saved game
                button = Button(
                    text=f"Carica salvataggio: {data['name']}",  # Display the saved game name
                    size_hint_y=None,  # Allow custom height for the button
                    height=40,  # Set the button's height
                    background_color=(0, 0, 0, .7),  # Set the background color to semi-transparent black
                    on_press=lambda btn, ts=timestamp: self.load_game(ts)  # Define the action when the button is pressed
                )
                grid.add_widget(button)  # Add the button to the grid
    
    def load_game(self, timestamp):
        # This method loads the game based on the selected save game timestamp.

        app = App.get_running_app()  # Get the current running Kivy app
        filename = 'save_data.json'  # The save data file to load from

        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved game data
            
            if timestamp in all_data:  # Check if the selected timestamp exists in the data
                save_data = all_data[timestamp]  # Get the saved data for this timestamp

                # Navigate to the main game screen
                app.add_screen(MainPage, 'mainpage')  # Add the MainPage screen to the app
                app.add_screen(NewGame, 'newgame')  # Add the NewGame screen to the app

                # Get the main game screen
                game_screen = self.manager.get_screen('mainpage')
                # Load the saved game data into the main game screen
                game_screen.load_saved_game(save_data, timestamp)
                # Switch to the main game screen
                self.manager.current = 'mainpage'  # Change to the 'mainpage' screen
