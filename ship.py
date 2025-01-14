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
        super().__init__(**kwargs)  # Initialize the Screen class
        self.projectile_popup = None  # Initialize the popup as None

    def load_screen(self, timestamp):
        self.timestamp = timestamp  # Load the timestamp data when the screen is accessed
    
    def goto_captain(self, timestamp):
        game_screen = self.manager.get_screen('captain')  # Get the 'captain' screen from the screen manager
        game_screen.load_screen(timestamp)  # Pass the timestamp to the captain screen
        self.manager.current = 'captain'  # Switch to the captain screen
    
    def goto_projectile(self, timestamp):
        if not self.projectile_popup:  # If the popup is not already created
            self.projectile_popup = Projectile_Popup()  # Create the popup for projectiles
        self.projectile_popup.load_popup(timestamp)  # Load the projectile data into the popup
        self.projectile_popup.open()  # Open the popup window
    
    def goto_mainpage(self, timestamp):
        app = App.get_running_app()  # Get the running instance of the app
        app.add_screen(MainPage, 'mainpage')  # Add the main page to the screen manager
        filename = 'save_data.json'  # Define the file for saving data
        
        if os.path.exists(filename):  # If the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data
            
            if timestamp in all_data:  # If the timestamp exists in the saved data
                save_data = all_data[timestamp]  # Get the saved data for the current timestamp
                game_screen = self.manager.get_screen('mainpage')  # Get the 'mainpage' screen
                game_screen.load_saved_game(save_data, timestamp)  # Pass the saved data to the main page
                self.manager.current = 'mainpage'  # Switch to the main page screen

class Captain(Screen):
    selected_dress = StringProperty('')  # Store the selected dress type for the captain

    def select_dress(self, dress_type, timestamp):
        filename = 'save_data.json'  # Define the file for saving data
        if os.path.exists(filename):  # If the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data
            
            if timestamp in all_data:  # If the timestamp exists in the saved data
                save_data = all_data[timestamp]  # Get the saved data for the current timestamp

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
                'selected_dress': 'red',  # Set the selected dress to 'red' as an example
                'secret': save_data['secret']
            }

            # Update the data with the new selection
            all_data[timestamp] = updated_data
            
            # Save the updated data back to the file
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
        else:
            # Update the selected dress if a different one is chosen
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
                'selected_dress': dress_type,  # Set the selected dress to the chosen one
                'secret': save_data['secret']
            }

            # Update the data with the new selection
            all_data[timestamp] = updated_data
            
            # Save the updated data back to the file
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)

    def load_screen(self, timestamp):
        grid = self.ids.cap_grid  # Get the grid for displaying the dress options
        grid.clear_widgets()  # Clear any existing widgets in the grid

        filename = 'save_data.json'  # Define the file for saving data
        if os.path.exists(filename):  # If the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data

            if timestamp in all_data:  # If the timestamp exists in the saved data
                save_data = all_data[timestamp]  # Get the saved data for the current timestamp

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
        super().__init__(**kwargs)  # Initialize the Popup class
        self.title = ""  # Set the title of the popup
        self.size_hint = (0.5, 0.5)  # Set the size of the popup
        self.auto_dismiss = True  # Allow the popup to be dismissed automatically

    def load_popup(self, timestamp):
        grid = self.ids.ammo_grid  # Get the grid for displaying the projectiles
        grid.clear_widgets()  # Clear any existing widgets in the grid

        filename = 'save_data.json'  # Define the file for saving data
        if os.path.exists(filename):  # If the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data

            if timestamp in all_data:  # If the timestamp exists in the saved data
                save_data = all_data[timestamp]  # Get the saved data for the current timestamp

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
