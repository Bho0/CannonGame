from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.app import App

import json
import os

# CustomLabel is a subclass of Label that allows setting a background color
class CustomLabel(Label):
    background_color = ListProperty([1, 1, 1, 1])  # Property to store background color (default is white)
    padding = NumericProperty(10)  # Padding around the label's text

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        # Draw a rectangle behind the label's text to simulate a background color
        with self.canvas.before:
            self.bg_color = Color(*self.background_color)  # Set the background color
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)  # Create a rectangle behind the label

        # Bind the size and position of the label to the rectangle's size and position
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        # Update the size and position of the rectangle whenever the label's size or position changes
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

# Hof is a Popup window that displays a leaderboard
class Hof(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""  # Set the title of the popup to an empty string
        self.size_hint = (0.5, 0.5)  # Set the size of the popup to 50% of the screen
        self.auto_dismiss = True  # Automatically dismiss the popup when clicked outside
    
    def load_popup(self):
        # Set up the layout and load the leaderboard data
        self.content = BoxLayout(orientation='vertical')  # Use a vertical layout for the popup content
        Hof = []  # List to store the leaderboard data
        filename = 'save_data.json'  # The JSON file storing the save data
        if os.path.exists(filename):
            # Open the file and load the saved game data
            with open(filename, 'r') as f:
                all_data = json.load(f)

            # Add name and points to the leaderboard
            for timestamp, data in all_data.items():
                tuple_temp = (data['name'], data['points'])
                Hof.append(tuple_temp)
        
        Hof.sort(key=lambda points: points[1], reverse=True)  # Sort the leaderboard by points (descending order)
        index = 1  # Initialize index for leaderboard entries

        # Add each entry to the popup
        for element in Hof:
            label = Label(text=f"N.{index} {element[0]} {element[1]}", 
                          size_hint_y=None, height=40, font_name='fonts/Caribbean.ttf')
            self.content.add_widget(label)  # Add the label to the popup content
            index += 1  # Increment index for the next entry

# MainPage is the screen representing the main game page
class MainPage(Screen):
    texts = ListProperty(["Here you can find anything ye need:", 
                          "our ship with all our arsenal", 
                          "a market with some more gear", 
                          "and then the map of the treasures' island"])  # Texts for the tutorial
    index = -1  # Keeps track of the current tutorial step
    timestamp = StringProperty("")  # Store the timestamp of the saved game

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Hof_popup = None  # Initialize the leaderboard popup to None

    def change_text(self, timestamp):
        # Increment the tutorial step and update the tutorial text
        self.index += 1
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]  # Get saved data for the current timestamp

        # If the tutorial is not complete, continue updating the text
        if self.index < len(self.texts):
            self.ids.tutorial_label.text = self.texts[self.index]
        else:
            # Tutorial is finished; update the game state
            update_tutorial = {
                'name': save_data['name'],
                'tutorial': False,
                'levels' : save_data['levels'],
                'points' : save_data['points'],
                'coins' : save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': save_data['selected_dress']
            }
            # Update the saved game data with the completed tutorial
            all_data[timestamp] = update_tutorial
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
            
            # Hide tutorial-related elements and enable game-related buttons
            self.ids.tutorial_button.opacity = 0
            self.ids.tutorial_button.disabled = True
            self.ids.tutorial_label.opacity = 0
            self.ids.cap_img.opacity = 0
            
            self.ids.level_button.opacity = 1
            self.ids.level_button.disabled = False
            self.ids.level_label.opacity = 1

            self.ids.ship_button.opacity = 1
            self.ids.ship_button.disabled = False
            self.ids.ship_label.opacity = 1

            self.ids.market_button.opacity = 1
            self.ids.market_button.disabled = False
            self.ids.market_label.opacity = 1

            self.ids.option_button.opacity = 1
            self.ids.option_button.disabled = False

            self.ids.Hof_button.opacity = 1
            self.ids.Hof_button.disabled = False
    
    def load_saved_game(self, save_data, timestamp):
        # Load the saved game data and update the UI accordingly
        self.timestamp = timestamp
        if save_data['tutorial'] == True:
            # Hide game buttons if tutorial is not completed
            self.ids.level_button.opacity = 0
            self.ids.level_button.disabled = True
            self.ids.level_label.opacity = 0

            self.ids.ship_button.opacity = 0
            self.ids.ship_button.disabled = True
            self.ids.ship_label.opacity = 0

            self.ids.market_button.opacity = 0
            self.ids.market_button.disabled = True
            self.ids.market_label.opacity = 0

            self.ids.option_button.opacity = 0
            self.ids.option_button.disabled = True

            self.ids.Hof_button.opacity = 0
            self.ids.Hof_button.disabled = True

            self.change_text(timestamp)  # Continue the tutorial flow
        else:
            # Enable game-related buttons after the tutorial
            self.ids.tutorial_button.opacity = 0
            self.ids.tutorial_button.disabled = True
            self.ids.tutorial_label.opacity = 0
            self.ids.cap_img.opacity = 0
            
            self.ids.level_button.opacity = 1
            self.ids.level_button.disabled = False
            self.ids.level_label.opacity = 1

            self.ids.ship_button.opacity = 1
            self.ids.ship_button.disabled = False
            self.ids.ship_label.opacity = 1

            self.ids.market_button.opacity = 1
            self.ids.market_button.disabled = False
            self.ids.market_label.opacity = 1

            self.ids.option_button.opacity = 1
            self.ids.option_button.disabled = False

            self.ids.Hof_button.opacity = 1
            self.ids.Hof_button.disabled = False
    
    def save_game(self, timestamp):
        # Save the current game data to the JSON file
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
        
        # Update the game data
        updated_data = {
            'name': save_data['name'],
            'tutorial': save_data['tutorial'],
            'levels' : save_data['levels'],
            'points' : save_data['points'],
            'coins' : save_data['coins'],
            'bullet': save_data['bullet'],
            'bomb': save_data['bomb'],
            'laser': save_data['laser'],
            'red_dress': save_data['red_dress'],
            'blu_dress': save_data['blu_dress'],
            'green_dress': save_data['green_dress'],
            'yellow_dress': save_data['yellow_dress'],
            'selected_dress': save_data['selected_dress']
        }

        # Save the updated game data back to the file
        all_data[timestamp] = updated_data
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
    
    def get_json_value(self, timestamp, data):
        # Get a specific value from the saved game data
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
                result = str(save_data[data])
                return result
            else: 
                return 'ERROR!'
    
    def chosen_dress(self, timestamp):
        # Retrieve the selected dress image based on the saved game data
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
                result = str(save_data['selected_dress'])
                # Return corresponding image based on selected dress
                if result == "red":
                    return 'images/captain.png'
                if result == "blu":
                    return 'images/blue_dress.png'
                if result == "green":
                    return 'images/green_dress(1).png'
                if result == "yellow":
                    return 'images/yellow_dress.png'
    
    # Navigation functions to switch between different screens
    def goto_ship(self, timestamp):
        app = App.get_running_app()
        game_screen = self.manager.get_screen('ship')
        game_screen.load_screen(timestamp)
        self.manager.current = 'ship'
        app.remove_screen('mainpage')

    def goto_market(self, timestamp):
        app = App.get_running_app()
        game_screen = self.manager.get_screen('market')
        game_screen.load_screen(timestamp)
        self.manager.current = 'market'
        app.remove_screen('mainpage')
    
    def goto_levels(self, timestamp):
        app = App.get_running_app()
        game_screen = self.manager.get_screen('levelSelection')
        game_screen.load_screen(timestamp)
        self.manager.current = 'levelSelection'
        app.remove_screen('mainpage')

    def open_Hof_popup(self):
        # Open the Hall of Fame popup window
        if not self.Hof_popup:
            self.Hof_popup = Hof()
        self.Hof_popup.load_popup()
        self.Hof_popup.open()
