from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from homepage import HomePage

class NewGame(Screen):
    pass

class CannonGame(App):
    def build(self):
        Builder.load_file('CannonGame.kv')
        Builder.load_file('Homepage.kv')

        sm = ScreenManager()
        sm.add_widget(NewGame(name='newgame'))
        sm.add_widget(HomePage(name='homepage'))
        return sm


if __name__ == '__main__':
    CannonGame().run()