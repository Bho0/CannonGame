from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.app import App

from mainpage import MainPage

from level import Level1, Level2, Level3, Level4, Level5, Level6, Level7, Level8

import json
import os

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
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

            if save_data['bullet'] == True:
                button = ToggleButton(text=f"bullet", font_name= 'fonts/Caribbean.ttf', size_hint_y=.3,
                                      on_press=lambda btn, prj='bullet': self.select_projectiles(prj))
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED", font_name= 'fonts/Caribbean.ttf', font_size=12, size_hint_y=.3, disabled=True)
                grid.add_widget(button)
            
            if save_data['bomb'] == True:
                button = ToggleButton(text=f"bomb", font_name= 'fonts/Caribbean.ttf', size_hint_y=.3,
                                      on_press=lambda btn, prj='bomb': self.select_projectiles(prj))
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED", font_name= 'fonts/Caribbean.ttf', font_size=12, size_hint_y=.3, disabled=True)
                grid.add_widget(button)
            
            if save_data['laser'] == True:
                button = ToggleButton(text=f"laser", font_name= 'fonts/Caribbean.ttf', size_hint_y=.3,
                                      on_press=lambda btn, prj='laser': self.select_projectiles(prj))
                grid.add_widget(button)
            else: 
                button = ToggleButton(text=f"NOT  OWNED", font_name= 'fonts/Caribbean.ttf', font_size=12, size_hint_y=.3, disabled=True)
                grid.add_widget(button)
    
    def select_projectiles(self, type_of_prj):
        if type_of_prj in self.selected_prj:
            self.selected_prj.remove(type_of_prj)
        else:
            self.selected_prj.append(type_of_prj)
    
    def goto_level(self, timestamp, selected_prj, screen_class, name):
        if selected_prj == []:
            label = Label(text=f"Please select at least one type of ammo", font_name= 'fonts/Caribbean.ttf')
            self.ids.start_box.add_widget(label)
        else:
            self.dismiss()
            app = App.get_running_app()
            app.add_screen(screen_class, name)
            game_screen = app.root.get_screen(name)  # Ottieni il nuovo schermo
            game_screen.load_screen(selected_prj, timestamp)  # Passa i dati al nuovo schermo
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
        
        for element in range(1, 8):
            element_id = f'LVL{element}'
            if save_data['levels'] >= element:
                self.ids[element_id].disabled = False
            else:
                self.ids[element_id].disabled = True
        
        if save_data['levels'] == 8 and  save_data['secret'] == False:
            self.ids['LVL8'].disabled = False
            self.ids['LVL8'].opacity = 1
        else:
            self.ids['LVL8'].disabled = True
            self.ids['LVL8'].opacity = 0
            
    
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
                game_screen = self.manager.get_screen('mainpage')  # Ottieni il nuovo schermo
                game_screen.load_saved_game(save_data, timestamp)  # Passa i dati al nuovo schermo
                self.manager.current = 'mainpage'  # Cambia schermo

class ComingSoon(Screen):
    pass