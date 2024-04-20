import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from HallOfFame.halloffame import HallOfFame
from LoadGame.loadgame import LoadGame

class Homepage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        Builder.load_file('homepage.kv')
        Builder.load_file('HallOfFame\halloffame.kv')
        Builder.load_file('LoadGame\loadgame.kv')
        self.window_manager = WindowManager()
        self.window_manager.add_widget(Homepage(name='main'))
        self.window_manager.add_widget(HallOfFame(name='HoF'))
        self.window_manager.add_widget(LoadGame(name='LG'))
        return self.window_manager


if __name__=="__main__":
    MyApp().run()