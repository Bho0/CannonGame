from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty


class MainPage(Screen):
    texts = ListProperty(["Tutorial1", "Tutorial2", "Tutorial3", "Tutorial4"])
    index = 0

    def change_text(self):
        # Incrementa l'indice
        self.index += 1
        
        # Controlla se siamo all'ultimo elemento
        if self.index < len(self.texts):
            self.ids.tutorial_label.text = self.texts[self.index]
        else:
            # Nascondi il bottone quando si raggiunge l'ultimo elemento
            self.ids.tutorial_button.opacity = 0  # Rende il bottone invisibile
            self.ids.tutorial_button.disabled = True  # Disabilita il bottone
            self.ids.tutorial_label.opacity = 0
            self.ids.cap_img.opacity = 0