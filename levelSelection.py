# Import necessary modules from Kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.app import App

# Import the MainPage class for transitioning between screens
from mainpage import MainPage

# Import json and os modules for handling file operations
import json
import os

# StartPopup class for handling the popup when selecting projectiles
class StartPopup(Popup):
    timestamp = StringProperty("")  # Timestamp to track saved progress
    selected_prj = []  # List of selected projectiles (ammunition)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""  # Set the popup title
        self.size_hint = (0.5, 0.5)  # Set the size of the popup
        self.auto_dismiss = True  # Automatically dismiss the popup when clicked outside
    
    # Method to load the popup with relevant data (based on timestamp)
    def load_popup(self, timestamp, screen_name, name):
        self.timestamp = timestamp  # Store the timestamp for data retrieval
        self.screen_name = screen_name  # Store the screen name for navigation
        self.name = name  # Store the name for the screen
        grid = self.ids.ammo_grid  # Access the ammo grid inside the popup
        grid.clear_widgets()  # Clear any existing widgets before adding new ones

        # Read save data from a file (if it exists)
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            # Check if data for the current timestamp exists
            if timestamp in all_data:
                save_data = all_data[timestamp]

            # Create buttons for each type of projectile (bullet, bomb, laser)
            for prj, label in [('bullet', 'bullet'), ('bomb', 'bomb'), ('laser', 'laser')]:
                if save_data[prj] == True:
                    button = ToggleButton(text=label, font_name='fonts/Caribbean.ttf', size_hint_y=.3,
                                          on_press=lambda btn, prj=label: self.select_projectiles(prj))
                else:
                    button = ToggleButton(text="NOT OWNED", font_name='fonts/Caribbean.ttf', font_size=12,
                                          size_hint_y=.3, disabled=True)
                grid.add_widget(button)  # Add the button to the grid
    
    # Method to handle the selection or deselection of projectiles
    def select_projectiles(self, type_of_prj):
        if type_of_prj in self.selected_prj:
            self.selected_prj.remove(type_of_prj)  # Remove from the selected list if already selected
        else:
            self.selected_prj.append(type_of_prj)  # Add to the selected list if not already selected
    
    # Method to transition to the game level with selected projectiles
    def goto_level(self, timestamp, selected_prj, screen_class, name):
        if not selected_prj:
            # Display a message if no projectile is selected
            label = Label(text="Please select at least one type of ammo", font_name='fonts/Caribbean.ttf')
            self.ids.start_box.add_widget(label)  # Add the label to the popup
        else:
            # Dismiss the popup and start the level
            self.dismiss()
            app = App.get_running_app()  # Get the running app instance
            app.add_screen(screen_class, name)  # Add the new screen to the app
            game_screen = app.root.get_screen(name)  # Get the new game screen
            game_screen.load_screen(selected_prj, timestamp, screen_class)  # Pass data to the game screen
            app.root.current = name  # Switch to the game screen

# LevelSelection class for managing the level selection screen
class LevelSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_popup = None  # Initialize start popup as None

    # Method to load the level selection screen with saved data
    def load_screen(self, timestamp):
        self.timestamp = timestamp  # Store the timestamp for data retrieval
        
        # Read save data from a file (if it exists)
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            # Check if data for the current timestamp exists
            if self.timestamp in all_data:
                save_data = all_data[self.timestamp]

        # Enable or disable level buttons based on saved data (levels unlocked)
        for element in range(1, 8):
            element_id = f'LVL{element}'
            if save_data['levels'] >= element:
                self.ids[element_id].disabled = False  # Enable button if level is unlocked
            else:
                self.ids[element_id].disabled = True  # Disable button if level is locked
    
    # Method to open the start popup when selecting a level
    def open_start_popup(self, timestamp, screen_name, name):
        if not self.start_popup:
            self.start_popup = StartPopup()  # Create the start popup if it doesn't exist
        self.start_popup.load_popup(timestamp, screen_name, name)  # Load data into the popup
        self.start_popup.open()  # Open the popup
    
    # Method to go back to the main page from the level selection screen
    def goto_mainpage(self, timestamp):
        app = App.get_running_app()  # Get the running app instance
        app.add_screen(MainPage, 'mainpage')  # Add the main page screen to the app
        filename = 'save_data.json'
        
        # Read saved data and load it into the main page screen
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
                game_screen = self.manager.get_screen('mainpage')  # Get the main page screen
                game_screen.load_saved_game(save_data, timestamp)  # Pass saved data to the main page screen
                self.manager.current = 'mainpage'  # Switch to the main page screen

# ComingSoon class for a screen that is yet to be implemented (empty screen)
class ComingSoon(Screen):
    pass
