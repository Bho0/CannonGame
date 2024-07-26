from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from homepage import HomePage
from loadgame import LoadGame
from newgame import NewGame

class Start(Screen):
    pass

class CannonGame(App):
    def build(self):
        Builder.load_file('CannonGame.kv')
        Builder.load_file('Homepage.kv')
        Builder.load_file('LoadGame.kv')
        Builder.load_file('NewGame.kv')

        sm = ScreenManager()
        sm.add_widget(Start(name='start'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(LoadGame(name='loadgame'))
        sm.add_widget(NewGame(name='newgame'))
        return sm


if __name__ == '__main__':
    CannonGame().run()