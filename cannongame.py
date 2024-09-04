from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty

from homepage import HomePage
from loadgame import LoadGame
from newgame import NewGame
from mainpage import MainPage
from levels import Levels, ComingSoon
from ship import Ship
from market import Market

class Start(Screen):
    pass

class CannonGame(App):

    def build(self):

        self.sound = SoundLoader.load('pirate-tavern-full-version-167990.mp3')
        if self.sound:
            self.sound.loop = True
            self.sound.play()

        Builder.load_file('CannonGame.kv')
        Builder.load_file('Homepage.kv')
        Builder.load_file('LoadGame.kv')
        Builder.load_file('NewGame.kv')
        Builder.load_file('MainPage.kv')
        Builder.load_file('Levels.kv')
        Builder.load_file('Ship.kv')
        Builder.load_file('Market.kv')

        sm = ScreenManager()
        sm.add_widget(Start(name='start'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(LoadGame(name='loadgame'))
        sm.add_widget(Levels(name='levels'))
        sm.add_widget(ComingSoon(name='comingsoon'))
        sm.add_widget(Ship(name='ship'))
        sm.add_widget(Market(name='market'))
        return sm 

    def change_volume(self, value):
        # Cambia il volume della musica
        if self.sound:
            self.sound.volume = value
    
    def remove_mainpage(self):
        self.root.remove_widget(self.root.get_screen('mainpage'))
    
    def remove_newgame(self):
        self.root.remove_widget(self.root.get_screen('newgame'))
    
    def add_mainpage(self):
        self.root.add_widget(MainPage(name='mainpage'))
    
    def add_newgame(self):
        self.root.add_widget(NewGame(name='newgame'))

if __name__ == '__main__':
    CannonGame().run()