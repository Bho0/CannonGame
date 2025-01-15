from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import json
import os


class Hof(Popup):
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""  
        self.size_hint = (0.5, 0.5)  
        self.auto_dismiss = True  
    def load_popup(self):
        

        self.content = BoxLayout(orientation='vertical')
        
        
        Hof = []  
        filename = 'save_data.json' 
        
        if os.path.exists(filename):
            

            with open(filename, 'r') as f:
                all_data = json.load(f)
                

            for timestamp, data in all_data.items():
                tuple_temp = (data['name'], data['points'])
                # Create a tuple of name and points for each entry
                Hof.append(tuple_temp)
                # Add the tuple to the Hall of Fame list

        Hof.sort(key=lambda points: points[1], reverse=True)
        # Sort the Hall of Fame list by points in descending order

        index = 1  # Initialize index for ranking

        for element in Hof:
           
            label = Label(
                text=f"N.{index} {element[0]} {element[1]}",
                # Format the label text with rank, name, and points
                size_hint_y=None, height=40,
                
                font_name='fonts/Caribbean.ttf'
               
            )
            self.content.add_widget(label)
           
            index += 1  

class HomePage(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Hof_popup = None  

    def open_Hof_popup(self):
       
        if not self.Hof_popup:
           
            self.Hof_popup = Hof()  
        
        self.Hof_popup.load_popup()
        

        self.Hof_popup.open()
        
