from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.app import App

import json
import os

class CustomLabel(Label):
    # Create a property to dynamically store the background color
    background_color = ListProperty([1, 1, 1, 1])  # White with full opacity
    padding = NumericProperty(10)  # Padding around the text

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*self.background_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        # Bind size and pos updates to the update_canvas method
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        # Update the size and position of the rectangle
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos


class MainPage(Screen):
    texts = ListProperty(["Tutorial1", "Tutorial2", "Tutorial3", "Tutorial4"])
    index = -1
    timestamp = StringProperty("")

    def change_text(self, timestamp):
        # Incrementa l'indice
        self.index += 1
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]

        # Controlla se siamo all'ultimo elemento
        if self.index < len(self.texts):
            self.ids.tutorial_label.text = self.texts[self.index]
        else:
            update_tutorial = {
                'name': save_data['name'],
                'tutorial': False,
                'levels' : save_data['levels'],
                'coins' : save_data['coins'],
                'bullet': save_data['bullet'],
                'bomb': save_data['bomb'],
                'laser': save_data['laser'],
                'red_dress': save_data['red_dress'],
                'blu_dress': save_data['blu_dress'],
                'green_dress': save_data['green_dress'],
                'yellow_dress': save_data['yellow_dress'],
                'selected_dress': save_data['selected_dress'],
                'selected_projectiles': save_data['selected_projectiles']
            }
            all_data[timestamp] = update_tutorial
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=4)
            # Nascondi il bottone quando si raggiunge l'ultimo elemento
            self.ids.tutorial_button.opacity = 0  # Rende il bottone invisibile
            self.ids.tutorial_button.disabled = True  # Disabilita il bottone
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
    
    def load_saved_game(self, save_data, timestamp):
        # Funzione per caricare i dati del gioco salvato e visualizzarli
        # Qui puoi impostare i widget dello schermo con i dati caricati

        self.timestamp = timestamp
        if save_data['tutorial'] == True:
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

            self.change_text(timestamp)
        
        else:
            self.ids.tutorial_button.opacity = 0  # Rende il bottone invisibile
            self.ids.tutorial_button.disabled = True  # Disabilita il bottone
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
    
    def save_game(self, timestamp):
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
        
        updated_data = {
            'name': save_data['name'],
            'tutorial': save_data['tutorial'],
            'levels' : save_data['levels'],
            'coins' : save_data['coins'],
            'bullet': save_data['bullet'],
            'bomb': save_data['bomb'],
            'laser': save_data['laser'],
            'red_dress': save_data['red_dress'],
            'blu_dress': save_data['blu_dress'],
            'green_dress': save_data['green_dress'],
            'yellow_dress': save_data['yellow_dress'],
            'selected_dress': save_data['selected_dress'],
            'selected_projectiles': save_data['selected_projectiles']
        }

        # Aggiungi i nuovi dati al dizionario con timestamp come chiave
        all_data[timestamp] = updated_data
        
        # Salva il dizionario aggiornato nel file JSON
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
    
    def get_json_value(self, timestamp, data):
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
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if timestamp in all_data:
                save_data = all_data[timestamp]
                result = str(save_data['selected_dress'])
                if result == 'red':
                    return 'images\captain.png'
                if result == 'blu':
                    return 'image\captain.png'
                if result == 'grenn':
                    return 'image\captain.png'
                if result == 'yellow':
                    return 'image\captain.png'
    
    def goto_ship(self, timestamp):
        # Naviga verso il nuovo schermo
        game_screen = self.manager.get_screen('ship')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'ship'  # Cambia schermo
    
    def goto_market(self, timestamp):
        # Naviga verso il nuovo schermo
        app = App.get_running_app()
        game_screen = self.manager.get_screen('market')  # Ottieni il nuovo schermo
        game_screen.load_screen(timestamp)  # Passa i dati al nuovo schermo
        self.manager.current = 'market'  # Cambia schermo
        app.remove_mainpage()