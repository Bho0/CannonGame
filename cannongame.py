from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty

from homepage import HomePage
from loadgame import LoadGame
from levelSelection import LevelSelection, ComingSoon
from ship import Ship, Captain
from market import Market, DressingRoom, ProjectileStore
from level import Transition

class Start(Screen):
    pass

class CannonGame(App):

    def build(self):
        self.sound = SoundLoader.load('sounds/music.mp3')
        if self.sound:
            self.sound.loop = True
            self.sound.play()

        Builder.load_file('CannonGame.kv')
        Builder.load_file('Homepage.kv')
        Builder.load_file('LoadGame.kv')
        Builder.load_file('NewGame.kv')
        Builder.load_file('MainPage.kv')
        Builder.load_file('LevelSelection.kv')
        Builder.load_file('Ship.kv')
        Builder.load_file('Market.kv')
        Builder.load_file('Level.kv')

        sm = ScreenManager()
        sm.add_widget(Start(name='start'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(LoadGame(name='loadgame'))
        sm.add_widget(LevelSelection(name='levelSelection'))
        sm.add_widget(ComingSoon(name='comingsoon'))
        sm.add_widget(Ship(name='ship'))
        sm.add_widget(Market(name='market'))
        sm.add_widget(Captain(name='captain'))
        sm.add_widget(DressingRoom(name='dressingRoom'))
        sm.add_widget(ProjectileStore(name='projectileStore'))
        sm.add_widget(Transition(name='transition'))
        return sm 

    def change_volume(self, value):
        # Cambia il volume della musica
        if self.sound:
            self.sound.volume = value
    
    def remove_screen(self, name):
        self.root.remove_widget(self.root.get_screen(name))
    
    def add_screen(self, screen_class, name):
        self.root.add_widget(screen_class(name = name))
    
    def get_file_content(self, rfile):
        with open(rfile, 'r', encoding='utf-8') as file:
            return file.read()

if __name__ == '__main__':
    CannonGame().run()