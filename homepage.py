from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import json
import os


class Hof(Popup):
    # Class for creating a "Hall of Fame" popup

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""  # Title of the popup
        self.size_hint = (0.5, 0.5)  # Size of the popup as a fraction of the window
        self.auto_dismiss = True  # Allow dismissal by clicking outside

    def load_popup(self):
        # Method to load data into the popup

        self.content = BoxLayout(orientation='vertical')
        # Setting the content of the popup as a vertical box layout
        
        Hof = []  # List to store Hall of Fame entries
        filename = 'save_data.json'  # Name of the file containing saved data
        
        if os.path.exists(filename):
            # Check if the file exists

            with open(filename, 'r') as f:
                all_data = json.load(f)
                # Load the JSON data from the file

            for timestamp, data in all_data.items():
                tuple_temp = (data['name'], data['points'])
                # Create a tuple of name and points for each entry
                Hof.append(tuple_temp)
                # Add the tuple to the Hall of Fame list

        Hof.sort(key=lambda points: points[1], reverse=True)
        # Sort the Hall of Fame list by points in descending order

        index = 1  # Initialize index for ranking

        for element in Hof:
            # Iterate through sorted Hall of Fame list

            label = Label(
                text=f"N.{index} {element[0]} {element[1]}",
                # Format the label text with rank, name, and points
                size_hint_y=None, height=40,
                # Set label height and remove size hint for y-axis
                font_name='fonts/Caribbean.ttf'
                # Use a custom font for the label
            )
            self.content.add_widget(label)
            # Add the label to the popup content

            index += 1  # Increment the rank

class HomePage(Screen):
    # Class for the HomePage screen

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Hof_popup = None  # Initialize the Hall of Fame popup as None

    def open_Hof_popup(self):
        # Method to open the Hall of Fame popup

        if not self.Hof_popup:
            # Check if the Hall of Fame popup is not already created

            self.Hof_popup = Hof()  # Create a new Hall of Fame popup
        
        self.Hof_popup.load_popup()
        # Load data into the popup

        self.Hof_popup.open()
        # Open the popup
