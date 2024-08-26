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
from levels import Level02, Level35, Level68, Level911, Level1214, Level1517, Level1820

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

        sm = ScreenManager()
        sm.add_widget(Start(name='start'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(LoadGame(name='loadgame'))
        sm.add_widget(NewGame(name='newgame'))
        sm.add_widget(MainPage(name='mainpage'))
        sm.add_widget(Level02(name='level0-2'))
        sm.add_widget(Level35(name='level3-5'))
        sm.add_widget(Level68(name='level6-8'))
        sm.add_widget(Level911(name='level9-11'))
        sm.add_widget(Level1214(name='level12-14'))
        sm.add_widget(Level1517(name='level15-17'))
        sm.add_widget(Level1820(name='level18-20'))
        return sm 

    def change_volume(self, value):
        # Cambia il volume della musica
        if self.sound:
            self.sound.volume = value

if __name__ == '__main__':
    CannonGame().run()