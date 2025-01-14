from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App

from mainpage import MainPage

import json
import os

# BluDress is a Popup window where the user can purchase the blue dress.
class BluDress(Popup):
    manager = ObjectProperty(None)  # Reference to the manager for navigation
    on_buy_callback = ObjectProperty(None)  # Callback function for after the buy action

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the constructor of the Popup class
        self.title = ""  # Set the title of the popup to an empty string
        self.size_hint = (0.8, 0.8)  # Set the size of the popup to 80% of the screen width and height
        self.auto_dismiss = True  # Automatically dismiss the popup when clicking outside of it
    
    # Method to load the popup content
    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')  # Create a vertical layout for the content

        filename = 'save_data.json'  # File where game data (including coins) is saved
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data from the file

            if timestamp in all_data:  # If there is data for the given timestamp
                save_data = all_data[timestamp]  # Get the saved data for the timestamp
            
        # Add the title and price labels to the popup
        self.content.add_widget(Label(text="Blue Dress", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        # Check if the user has enough coins to buy the dress
        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)  # Disable the buy button if not enough coins
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf',)
            buy_button.bind(on_press=self.on_buy)  # Bind the buy action to the on_buy method
        
        # Add the buy button to the popup
        self.content.add_widget(buy_button)

    # Method called when the buy button is pressed
    def on_buy(self, instance):
        if self.on_buy_callback:  # If a callback function is defined
            self.on_buy_callback()  # Execute the callback
        self.dismiss()  # Close the popup


# GreenDress is a Popup window where the user can purchase the green dress (similar to BluDress)
class GreenDress(Popup):
    manager = ObjectProperty(None)  # Reference to the manager for navigation
    on_buy_callback = ObjectProperty(None)  # Callback function for after the buy action

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the constructor of the Popup class
        self.title = ""  # Set the title of the popup to an empty string
        self.size_hint = (0.8, 0.8)  # Set the size of the popup to 80% of the screen width and height
        self.auto_dismiss = True  # Automatically dismiss the popup when clicking outside of it
    
    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')  # Create a vertical layout for the content

        filename = 'save_data.json'  # File where game data (including coins) is saved
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data from the file

            if timestamp in all_data:  # If there is data for the given timestamp
                save_data = all_data[timestamp]  # Get the saved data for the timestamp
            
        # Add the title and price labels to the popup
        self.content.add_widget(Label(text="Green Dress", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        # Check if the user has enough coins to buy the dress
        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)  # Disable the buy button if not enough coins
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf',)
            buy_button.bind(on_press=self.on_buy)  # Bind the buy action to the on_buy method
        
        # Add the buy button to the popup
        self.content.add_widget(buy_button)

    # Method called when the buy button is pressed
    def on_buy(self, instance):
        if self.on_buy_callback:  # If a callback function is defined
            self.on_buy_callback()  # Execute the callback
        self.dismiss()  # Close the popup


# YellowDress is a Popup window where the user can purchase the yellow dress (similar to BluDress)
class YellowDress(Popup):
    manager = ObjectProperty(None)  # Reference to the manager for navigation
    on_buy_callback = ObjectProperty(None)  # Callback function for after the buy action

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the constructor of the Popup class
        self.title = ""  # Set the title of the popup to an empty string
        self.size_hint = (0.8, 0.8)  # Set the size of the popup to 80% of the screen width and height
        self.auto_dismiss = True  # Automatically dismiss the popup when clicking outside of it
    
    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')  # Create a vertical layout for the content

        filename = 'save_data.json'  # File where game data (including coins) is saved
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data from the file

            if timestamp in all_data:  # If there is data for the given timestamp
                save_data = all_data[timestamp]  # Get the saved data for the timestamp
            
        # Add the title and price labels to the popup
        self.content.add_widget(Label(text="Yellow Dress", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        # Check if the user has enough coins to buy the dress
        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)  # Disable the buy button if not enough coins
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf',)
            buy_button.bind(on_press=self.on_buy)  # Bind the buy action to the on_buy method
        
        # Add the buy button to the popup
        self.content.add_widget(buy_button)

    # Method called when the buy button is pressed
    def on_buy(self, instance):
        if self.on_buy_callback:  # If a callback function is defined
            self.on_buy_callback()  # Execute the callback
        self.dismiss()  # Close the popup


# Bomb is a Popup window where the user can purchase a bomb (similar to previous items)
class Bomb(Popup):
    manager = ObjectProperty(None)  # Reference to the manager for navigation
    on_buy_callback = ObjectProperty(None)  # Callback function for after the buy action

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the constructor of the Popup class
        self.title = ""  # Set the title of the popup to an empty string
        self.size_hint = (0.8, 0.8)  # Set the size of the popup to 80% of the screen width and height
        self.auto_dismiss = True  # Automatically dismiss the popup when clicking outside of it
    
    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')  # Create a vertical layout for the content

        filename = 'save_data.json'  # File where game data (including coins) is saved
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data from the file

            if timestamp in all_data:  # If there is data for the given timestamp
                save_data = all_data[timestamp]  # Get the saved data for the timestamp
            
        # Add the title and price labels to the popup
        self.content.add_widget(Label(text="Bomb", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        # Check if the user has enough coins to buy the bomb
        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)  # Disable the buy button if not enough coins
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf',)
            buy_button.bind(on_press=self.on_buy)  # Bind the buy action to the on_buy method
        
        # Add the buy button to the popup
        self.content.add_widget(buy_button)

    # Method called when the buy button is pressed
    def on_buy(self, instance):
        if self.on_buy_callback:  # If a callback function is defined
            self.on_buy_callback()  # Execute the callback
        self.dismiss()  # Close the popup


# Laser is a Popup window where the user can purchase a laser (similar to previous items)
class Laser(Popup):
    manager = ObjectProperty(None)  # Reference to the manager for navigation
    on_buy_callback = ObjectProperty(None)  # Callback function for after the buy action

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the constructor of the Popup class
        self.title = ""  # Set the title of the popup to an empty string
        self.size_hint = (0.8, 0.8)  # Set the size of the popup to 80% of the screen width and height
        self.auto_dismiss = True  # Automatically dismiss the popup when clicking outside of it
    
    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')  # Create a vertical layout for the content

        filename = 'save_data.json'  # File where game data (including coins) is saved
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the saved data from the file

            if timestamp in all_data:  # If there is data for the given timestamp
                save_data = all_data[timestamp]  # Get the saved data for the timestamp
            
        # Add the title and price labels to the popup
        self.content.add_widget(Label(text="Laser", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        # Check if the user has enough coins to buy the laser
        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)  # Disable the buy button if not enough coins
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf',)
            buy_button.bind(on_press=self.on_buy)  # Bind the buy action to the on_buy method
        
        # Add the buy button to the popup
        self.content.add_widget(buy_button)

    # Method called when the buy button is pressed
    def on_buy(self, instance):
        if self.on_buy_callback:  # If a callback function is defined
            self.on_buy_callback()  # Execute the callback
        self.dismiss()  # Close the popup
# The Market class is a screen that allows users to navigate through different stores in the game.
class Market(Screen):
    timestamp = StringProperty("")  # Stores the current timestamp for game save data

    def load_screen(self, timestamp):
        # Method to load the screen and set the timestamp
        self.timestamp = timestamp
    
    def goto_dressingRoom(self, timestamp):
        # Navigate to the DressingRoom screen
        game_screen = self.manager.get_screen('dressingRoom')  # Get the DressingRoom screen
        game_screen.load_screen(timestamp)  # Pass the timestamp to the DressingRoom screen
        self.manager.current = 'dressingRoom'  # Switch to the DressingRoom screen
    
    def goto_projectileStore(self, timestamp):
        # Navigate to the ProjectileStore screen
        game_screen = self.manager.get_screen('projectileStore')  # Get the ProjectileStore screen
        game_screen.load_screen(timestamp)  # Pass the timestamp to the ProjectileStore screen
        self.manager.current = 'projectileStore'  # Switch to the ProjectileStore screen
    
    def goto_mainpage(self, timestamp):
        # Navigate to the MainPage screen
        app = App.get_running_app()
        app.add_screen(MainPage, 'mainpage')  # Add MainPage screen to the app
        filename = 'save_data.json'
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the save data from the file
            
            if timestamp in all_data:  # If data exists for the timestamp
                save_data = all_data[timestamp]  # Get the saved game data
                game_screen = self.manager.get_screen('mainpage')  # Get the MainPage screen
                game_screen.load_saved_game(save_data, timestamp)  # Pass the saved game data to the MainPage screen
                self.manager.current = 'mainpage'  # Switch to the MainPage screen


# The DressingRoom class represents the dressing room screen, where users can buy dresses.
class DressingRoom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blu_dress_popup = None  # Initialize the blue dress popup as None
        self.green_dress_popup = None  # Initialize the green dress popup as None
        self.yellow_dress_popup = None  # Initialize the yellow dress popup as None
    
    def load_screen(self, timestamp):
        # Load the screen and display the available dresses based on the timestamp (saved game data)
        grid = self.ids.dress_grid
        grid.clear_widgets()  # Clear the grid before adding new buttons

        filename = 'save_data.json'
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the save data from the file

            if timestamp in all_data:  # If data exists for the timestamp
                save_data = all_data[timestamp]  # Get the saved game data

                # Check if the blue dress is not bought
                if save_data['blu_dress'] == False:
                    # Create a button to buy the blue dress
                    button = Button(text=f"blu dress",
                                    background_normal='images/blue_dress.png',
                                    font_name= 'fonts/Caribbean.ttf',
                                    on_press=lambda btn, ts=timestamp: self.open_blu_dress_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    # Disable the button if the blue dress is already bought
                    button = Button(text=f"SOLD",
                                    font_name= 'fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                # Check if the green dress is not bought
                if save_data['green_dress'] == False:
                    # Create a button to buy the green dress
                    button = Button(text=f"green dress",
                                    background_normal='images/green_dress(1).png',
                                    font_name= 'fonts/Caribbean.ttf',
                                    on_press=lambda btn, ts=timestamp: self.open_green_dress_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    # Disable the button if the green dress is already bought
                    button = Button(text=f"SOLD",
                                    font_name= 'fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                # Check if the yellow dress is not bought
                if save_data['yellow_dress'] == False:
                    # Create a button to buy the yellow dress
                    button = Button(text=f"yellow dress",
                                    background_normal='images/yellow_dress.png',
                                    font_name= 'fonts/Caribbean.ttf',
                                    on_press=lambda btn, ts=timestamp: self.open_yellow_dress_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    # Disable the button if the yellow dress is already bought
                    button = Button(text=f"SOLD",
                                    font_name= 'fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
    
    # Opens a popup to buy the blue dress
    def open_blu_dress_popup(self, timestamp):
        if not self.blu_dress_popup:  # If the blue dress popup is not yet created
            self.blu_dress_popup = BluDress(manager=self.manager)  # Create the popup
            self.blu_dress_popup.on_buy_callback = lambda: self.on_blu_dress_bought(timestamp)  # Set the callback after purchase
        self.blu_dress_popup.load_popup(timestamp)  # Load the popup with the timestamp data
        self.blu_dress_popup.open()  # Open the popup

    # Logic for buying the blue dress
    def on_blu_dress_bought(self, timestamp):
        self.update_save_data(timestamp, "blu_dress", 50)  # Update the save data for blue dress purchase
        self.load_screen(timestamp)  # Reload the screen to update the buttons
    
    # Opens a popup to buy the green dress
    def open_green_dress_popup(self, timestamp):
        if not self.green_dress_popup:  # If the green dress popup is not yet created
            self.green_dress_popup = GreenDress(manager=self.manager)  # Create the popup
            self.green_dress_popup.on_buy_callback = lambda: self.on_green_dress_bought(timestamp)  # Set the callback after purchase
        self.green_dress_popup.load_popup(timestamp)  # Load the popup with the timestamp data
        self.green_dress_popup.open()  # Open the popup

    # Logic for buying the green dress
    def on_green_dress_bought(self, timestamp):
        self.update_save_data(timestamp, "green_dress", 50)  # Update the save data for green dress purchase
        self.load_screen(timestamp)  # Reload the screen to update the buttons
    
    # Opens a popup to buy the yellow dress
    def open_yellow_dress_popup(self, timestamp):
        if not self.yellow_dress_popup:  # If the yellow dress popup is not yet created
            self.yellow_dress_popup = YellowDress(manager=self.manager)  # Create the popup
            self.yellow_dress_popup.on_buy_callback = lambda: self.on_yellow_dress_bought(timestamp)  # Set the callback after purchase
        self.yellow_dress_popup.load_popup(timestamp)  # Load the popup with the timestamp data
        self.yellow_dress_popup.open()  # Open the popup

    # Logic for buying the yellow dress
    def on_yellow_dress_bought(self, timestamp):
        self.update_save_data(timestamp, "yellow_dress", 50)  # Update the save data for yellow dress purchase
        self.load_screen(timestamp)  # Reload the screen to update the buttons
    
    # Updates the save data with the purchase of the dress
    def update_save_data(self, timestamp, dress_type, cost):
        filename = 'save_data.json'
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the save data from the file

            if timestamp in all_data:  # If data exists for the timestamp
                save_data = all_data[timestamp]  # Get the saved game data
                save_data[dress_type] = True  # Mark the dress as bought
                save_data['coins'] -= cost  # Deduct the cost from the coins

            # Save the updated data back to the file
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)


# The ProjectileStore class represents the screen where users can buy projectiles like bombs and lasers.
class ProjectileStore(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bomb_popup = None  # Initialize the bomb popup as None
        self.laser_popup = None  # Initialize the laser popup as None

    def load_screen(self, timestamp):
        # Load the screen and display the available projectiles based on the timestamp (saved game data)
        grid = self.ids.prj_grid
        grid.clear_widgets()  # Clear the grid before adding new buttons

        filename = 'save_data.json'
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the save data from the file

            if timestamp in all_data:  # If data exists for the timestamp
                save_data = all_data[timestamp]  # Get the saved game data

                # Check if the bomb is not bought
                if save_data['bomb'] == False:
                    # Create a button to buy the bomb
                    button = Button(text=f"bomb",
                                    font_name= 'fonts/Caribbean.ttf',
                                    background_color=(0, 0, 0, 0.6),
                                    on_press=lambda btn, ts=timestamp: self.open_bomb_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    # Disable the button if the bomb is already bought
                    button = Button(text=f"SOLD",
                                    font_name= 'fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                # Check if the laser is not bought
                if save_data['laser'] == False:
                    # Create a button to buy the laser
                    button = Button(text=f"laser",
                                    font_name= 'fonts/Caribbean.ttf',
                                    background_color=(0, 0, 0, 0.6),
                                    on_press=lambda btn, ts=timestamp: self.open_laser_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    # Disable the button if the laser is already bought
                    button = Button(text=f"SOLD",
                                    font_name= 'fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
    
    # Opens a popup to buy the bomb
    def open_bomb_popup(self, timestamp):
        if not self.bomb_popup:  # If the bomb popup is not yet created
            self.bomb_popup = Bomb(manager=self.manager)  # Create the popup
            self.bomb_popup.on_buy_callback = lambda: self.on_bomb_bought(timestamp)  # Set the callback after purchase
        self.bomb_popup.load_popup(timestamp)  # Load the popup with the timestamp data
        self.bomb_popup.open()  # Open the popup

    # Logic for buying the bomb
    def on_bomb_bought(self, timestamp):
        self.update_save_data(timestamp, "bomb", 50)  # Update the save data for bomb purchase
        self.load_screen(timestamp)  # Reload the screen to update the buttons
    
    # Opens a popup to buy the laser
    def open_laser_popup(self, timestamp):
        if not self.laser_popup:  # If the laser popup is not yet created
            self.laser_popup = Laser(manager=self.manager)  # Create the popup
            self.laser_popup.on_buy_callback = lambda: self.on_laser_bought(timestamp)  # Set the callback after purchase
        self.laser_popup.load_popup(timestamp)  # Load the popup with the timestamp data
        self.laser_popup.open()  # Open the popup

    # Logic for buying the laser
    def on_laser_bought(self, timestamp):
        self.update_save_data(timestamp, "laser", 50)  # Update the save data for laser purchase
        self.load_screen(timestamp)  # Reload the screen to update the buttons
    
    # Updates the save data with the purchase of the projectile
    def update_save_data(self, timestamp, projectile_type, cost):
        filename = 'save_data.json'
        if os.path.exists(filename):  # Check if the save data file exists
            with open(filename, 'r') as f:
                all_data = json.load(f)  # Load the save data from the file

            if timestamp in all_data:  # If data exists for the timestamp
                save_data = all_data[timestamp]  # Get the saved game data
                save_data[projectile_type] = True  # Mark the projectile as bought
                save_data['coins'] -= cost  # Deduct the cost from the coins

            # Save the updated data back to the file
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
