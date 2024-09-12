from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

import json
import os

class BluDress(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss: True
    
    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]
            
        self.content.add_widget(Label(text="Blue Dress", height=44))
        self.content.add_widget(Label(text="50$", height=44))

        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", height=44))
        
        buy_button = Button(text="BUY")
        self.content.add_widget(buy_button)


class GreenDress(Popup):
    pass

class YellowDress(Popup):
    pass

class Bomb(Popup):
    pass

class Laser(Popup):
    pass

class Market(Screen):
    timestamp = StringProperty("")
    
    def load_screen(self, timestamp):
        self.timestamp = timestamp
    
    def goto_dressingRoom(self, timestamp):
        # Naviga verso il nuovo schermo
        game_screen = self.manager.get_screen('dressingRoom')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'dressingRoom'  # Cambia schermo
    
    def goto_projectileStore(self, timestamp):
        # Naviga verso il nuovo schermo
        game_screen = self.manager.get_screen('projectileStore')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'projectileStore'  # Cambia schermo

class DressingRoom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blu_dress_popup = None
    
    def load_screen(self, timestamp):
        grid = self.ids.dress_grid
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

                if save_data['blu_dress'] == False:
                    button = Button(text=f"blu dress",
                                    background_normal='images\captain.png',
                                    on_press=lambda btn, ts=timestamp: self.open_blu_dress_popup(timestamp)
                                    )
                    grid.add_widget(button)
                else: 
                    button = Button(text=f"SOLD",
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                if save_data['green_dress'] == False:
                    button = Button(text=f"green dress",
                                    background_normal='images\captain.png',
                                    on_press=lambda btn, ts=timestamp: GreenDress.load_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    button = Button(text=f"SOLD",
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                if save_data['yellow_dress'] == False:
                    button = Button(text=f"yellow dress",
                                    background_normal='images\captain.png',
                                    on_press=lambda btn, ts=timestamp: YellowDress.load_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    button = Button(text=f"SOLD",
                                    disabled=True
                                    )
                    grid.add_widget(button)
    
    def open_blu_dress_popup(self, timestamp):
        if not self.blu_dress_popup:
            self.blu_dress_popup = BluDress()
        self.blu_dress_popup.load_popup(timestamp)
        self.blu_dress_popup.open()

class ProjectileStore(Screen):
    def load_screen(self, timestamp):
        grid = self.ids.dress_grid
        grid.clear_widgets()  # Pulisci la lista prima di aggiungere nuovi elementi

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

                if save_data['bomb'] == False:
                    button = Button(text=f"bomb",
                                    on_press=lambda btn, ts=timestamp: Bomb.load_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    button = Button(text=f"SOLD",
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                if save_data['laser'] == False:
                    button = Button(text=f"laser",
                                    on_press=lambda btn, ts=timestamp: Laser.load_popup(ts)
                                    )
                    grid.add_widget(button)
                else: 
                    button = Button(text=f"SOLD",
                                    disabled=True
                                    )
                    grid.add_widget(button)