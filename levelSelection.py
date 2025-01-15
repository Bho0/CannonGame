from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.app import App

from mainpage import MainPage

import json
import os

#class for handling the popup when selecting projectiles
class StartPopup(Popup):
    timestamp = StringProperty("")  
    selected_prj = []  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""  
        self.size_hint = (0.5, 0.5)  
        self.auto_dismiss = True 
    
    def load_popup(self, timestamp, screen_name, name):
        self.timestamp = timestamp  
        self.screen_name = screen_name  
        self.name = name  
        grid = self.ids.ammo_grid 
        grid.clear_widgets()  

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

            # Create buttons for each type of projectile
            for prj, label in [('bullet', 'bullet'), ('bomb', 'bomb'), ('laser', 'laser')]:
                if save_data[prj] == True:
                    button = ToggleButton(text=label, font_name='fonts/Caribbean.ttf', size_hint_y=.3,
                                          on_press=lambda btn, prj=label: self.select_projectiles(prj))
                else:
                    button = ToggleButton(text="NOT OWNED", font_name='fonts/Caribbean.ttf', font_size=12,
                                          size_hint_y=.3, disabled=True)
                grid.add_widget(button)  

    def select_projectiles(self, type_of_prj):
        if type_of_prj in self.selected_prj:
            self.selected_prj.remove(type_of_prj)
        else:
            self.selected_prj.append(type_of_prj)
    
    
    def goto_level(self, timestamp, selected_prj, screen_class, name):
        if not selected_prj:
            
            label = Label(text="Please select at least one type of ammo", font_name='fonts/Caribbean.ttf')
            self.ids.start_box.add_widget(label) 
        else:
            # Dismiss the popup and start the level
            self.dismiss()
            app = App.get_running_app()  
            app.add_screen(screen_class, name)  
            game_screen = app.root.get_screen(name)  
            game_screen.load_screen(selected_prj, timestamp, screen_class)  
            app.root.current = name  

class LevelSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_popup = None  

    def load_screen(self, timestamp):
        self.timestamp = timestamp  
    
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if self.timestamp in all_data:
                save_data = all_data[self.timestamp]

        # Enable or disable level buttons based on saved data (levels unlocked)
        for element in range(1, 8):
            element_id = f'LVL{element}'
            if save_data['levels'] >= element:
                self.ids[element_id].disabled = False 
            else:
                self.ids[element_id].disabled = True
    
    
    def open_start_popup(self, timestamp, screen_name, name):
        if not self.start_popup:
            self.start_popup = StartPopup()  
        self.start_popup.load_popup(timestamp, screen_name, name)  
        self.start_popup.open() 
    
    
    def goto_mainpage(self, timestamp):
        app = App.get_running_app()  
        app.add_screen(MainPage, 'mainpage')  
        filename = 'save_data.json'
        
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
                game_screen = self.manager.get_screen('mainpage')  
                game_screen.load_saved_game(save_data, timestamp) 
                self.manager.current = 'mainpage'  

class ComingSoon(Screen):
    pass
