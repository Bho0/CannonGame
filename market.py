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
#Each purchasable item has similar implementation
class BluDress(Popup):
    manager = ObjectProperty(None)
    on_buy_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True

    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            if timestamp in all_data:
                save_data = all_data[timestamp]

        self.content.add_widget(Label(text="Blue Dress", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        if save_data['coins'] < 50: #Check the json file for the coins
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf')
            buy_button.bind(on_press=self.on_buy)

        self.content.add_widget(buy_button)

    def on_buy(self, instance): #Handle the purchase
        if self.on_buy_callback:
            self.on_buy_callback()
        self.dismiss()

class GreenDress(Popup):
    manager = ObjectProperty(None)
    on_buy_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True

    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            if timestamp in all_data:
                save_data = all_data[timestamp]

        self.content.add_widget(Label(text="Green Dress", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf')
            buy_button.bind(on_press=self.on_buy)

        self.content.add_widget(buy_button)

    def on_buy(self, instance):
        if self.on_buy_callback:
            self.on_buy_callback()
        self.dismiss()

class YellowDress(Popup):
    manager = ObjectProperty(None)
    on_buy_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True

    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            if timestamp in all_data:
                save_data = all_data[timestamp]

        self.content.add_widget(Label(text="Yellow Dress", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf')
            buy_button.bind(on_press=self.on_buy)

        self.content.add_widget(buy_button)

    def on_buy(self, instance):
        if self.on_buy_callback:
            self.on_buy_callback()
        self.dismiss()

class Bomb(Popup):
    manager = ObjectProperty(None)
    on_buy_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True

    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            if timestamp in all_data:
                save_data = all_data[timestamp]

        self.content.add_widget(Label(text="Bomb", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf')
            buy_button.bind(on_press=self.on_buy)

        self.content.add_widget(buy_button)

    def on_buy(self, instance):
        if self.on_buy_callback:
            self.on_buy_callback()
        self.dismiss()

class Laser(Popup):
    manager = ObjectProperty(None)
    on_buy_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True
        self.attention_popup = None

    def load_popup(self, timestamp):
        self.content = BoxLayout(orientation='vertical')
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            if timestamp in all_data:
                save_data = all_data[timestamp]

        self.content.add_widget(Label(text="Laser", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="50S", font_name='fonts/Caribbean.ttf', height=44))

        if save_data['coins'] < 50:
            self.content.add_widget(Label(text="YOU DON'T HAVE ENOUGH MONEY", font_name='fonts/Caribbean.ttf', height=44))
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf', disabled=True)
        else:
            buy_button = Button(text="BUY", font_name='fonts/Caribbean.ttf')
            buy_button.bind(on_press=self.on_buy)

        self.content.add_widget(buy_button)

    def on_buy(self, instance):
        instance.disabled = True
        if not self.attention_popup:
            self.attention_popup = Attention(manager=self.manager)
        self.attention_popup.load_popup()
        self.attention_popup.open()
        if self.on_buy_callback:
            self.on_buy_callback()
        self.dismiss()

class Attention(Popup): #Load a message
    manager = ObjectProperty(None)
    on_buy_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = True

    def load_popup(self):
        self.content = BoxLayout(orientation='vertical')
        self.content.add_widget(Label(text="OH NO! This Merchant sold us a defected laser!", font_name='fonts/Caribbean.ttf', height=44))
        self.content.add_widget(Label(text="Now the aim isn't precise as it should be!", font_name='fonts/Caribbean.ttf', height=44))

        close_button = Button(text="CLOSE", font_name='fonts/Caribbean.ttf')
        close_button.bind(on_press=self.on_close)

        self.content.add_widget(close_button)

    def on_close(self, instance):
        self.dismiss()

#Different screens and navigation instructions, using Json to keep track of data
class Market(Screen):
    timestamp = StringProperty("")

    def load_screen(self, timestamp):
        self.timestamp = timestamp

    def goto_dressingRoom(self, timestamp):
        game_screen = self.manager.get_screen('dressingRoom')
        game_screen.load_screen(timestamp)
        self.manager.current = 'dressingRoom'

    def goto_projectileStore(self, timestamp):
        game_screen = self.manager.get_screen('projectileStore')
        game_screen.load_screen(timestamp)
        self.manager.current = 'projectileStore'

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

class DressingRoom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blu_dress_popup = None
        self.green_dress_popup = None
        self.yellow_dress_popup = None
    
    def load_screen(self, timestamp):
        grid = self.ids.dress_grid
        grid.clear_widgets()

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

                if save_data['blu_dress'] == False: #Check if the blu dress has been bought, if not, make it available to purchase
                    button = Button(text="blu dress",
                                    background_normal='images/blue_dress.png',
                                    font_name='fonts/Caribbean.ttf',
                                    on_press=lambda btn, ts=timestamp: self.open_blu_dress_popup(ts)
                                    )
                    grid.add_widget(button)
                else:
                    button = Button(text="SOLD",
                                    font_name='fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                if save_data['green_dress'] == False:
                    button = Button(text="green dress",
                                    background_normal='images/green_dress(1).png',
                                    font_name='fonts/Caribbean.ttf',
                                    on_press=lambda btn, ts=timestamp: self.open_green_dress_popup(ts)
                                    )
                    grid.add_widget(button)
                else:
                    button = Button(text="SOLD",
                                    font_name='fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                if save_data['yellow_dress'] == False:
                    button = Button(text="yellow dress",
                                    background_normal='images/yellow_dress.png',
                                    font_name='fonts/Caribbean.ttf',
                                    on_press=lambda btn, ts=timestamp: self.open_yellow_dress_popup(ts)
                                    )
                    grid.add_widget(button)
                else:
                    button = Button(text="SOLD",
                                    font_name='fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
    #popup for each dress and methods for completing the purchase
    def open_blu_dress_popup(self, timestamp):
        if not self.blu_dress_popup:
            self.blu_dress_popup = BluDress(manager=self.manager)
            self.blu_dress_popup.on_buy_callback = lambda: self.on_blu_dress_bought(timestamp)
        self.blu_dress_popup.load_popup(timestamp)
        self.blu_dress_popup.open()

    def on_blu_dress_bought(self, timestamp):
        self.update_save_data(timestamp, "blu_dress", 50)
        self.load_screen(timestamp)
    
    def open_green_dress_popup(self, timestamp):
        if not self.green_dress_popup:
            self.green_dress_popup = GreenDress(manager=self.manager)
            self.green_dress_popup.on_buy_callback = lambda: self.on_green_dress_bought(timestamp)
        self.green_dress_popup.load_popup(timestamp)
        self.green_dress_popup.open()

    def on_green_dress_bought(self, timestamp):
        self.update_save_data(timestamp, "green_dress", 50)
        self.load_screen(timestamp)
    
    def open_yellow_dress_popup(self, timestamp):
        if not self.yellow_dress_popup:
            self.yellow_dress_popup = YellowDress(manager=self.manager)
            self.yellow_dress_popup.on_buy_callback = lambda: self.on_yellow_dress_bought(timestamp)
        self.yellow_dress_popup.load_popup(timestamp)
        self.yellow_dress_popup.open()

    def on_yellow_dress_bought(self, timestamp):
        self.update_save_data(timestamp, "yellow_dress", 50)
        self.load_screen(timestamp)
    
    def update_save_data(self, timestamp, dress_type, cost):
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]
                save_data[dress_type] = True
                save_data['coins'] -= cost

            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)


class ProjectileStore(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bomb_popup = None
        self.laser_popup = None

    def load_screen(self, timestamp):
        grid = self.ids.prj_grid
        grid.clear_widgets()

        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]

                if save_data['bomb'] == False: #display projectiles if they can be bought
                    button = Button(text="bomb",
                                    font_name='fonts/Caribbean.ttf',
                                    background_color=(0, 0, 0, 0.6),
                                    on_press=lambda btn, ts=timestamp: self.open_bomb_popup(ts)
                                    )
                    grid.add_widget(button)
                else:
                    button = Button(text="SOLD",
                                    font_name='fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
                
                if save_data['laser'] == False:
                    button = Button(text="laser",
                                    font_name='fonts/Caribbean.ttf',
                                    background_color=(0, 0, 0, 0.6),
                                    on_press=lambda btn, ts=timestamp: self.open_laser_popup(ts)
                                    )
                    grid.add_widget(button)
                else:
                    button = Button(text="SOLD",
                                    font_name='fonts/Caribbean.ttf',
                                    disabled=True
                                    )
                    grid.add_widget(button)
    #Handle purchase of bomb and laser
    def open_bomb_popup(self, timestamp):
        if not self.bomb_popup:
            self.bomb_popup = Bomb(manager=self.manager)
            self.bomb_popup.on_buy_callback = lambda: self.on_bomb_bought(timestamp)
        self.bomb_popup.load_popup(timestamp)
        self.bomb_popup.open()

    def on_bomb_bought(self, timestamp):
        self.update_save_data(timestamp, "bomb", 50)
        self.load_screen(timestamp)
    
    def open_laser_popup(self, timestamp):
        if not self.laser_popup:
            self.laser_popup = Laser(manager=self.manager)
            self.laser_popup.on_buy_callback = lambda: self.on_laser_bought(timestamp)
        self.laser_popup.load_popup(timestamp)
        self.laser_popup.open()

    def on_laser_bought(self, timestamp):
        self.update_save_data(timestamp, "laser", 50)
        self.load_screen(timestamp)
    
    def update_save_data(self, timestamp, projectile_type, cost):
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)

            if timestamp in all_data:
                save_data = all_data[timestamp]
                save_data[projectile_type] = True
                save_data['coins'] -= cost

            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
