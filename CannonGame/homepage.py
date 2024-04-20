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
from Credits.credits import Credits
from GeneralSettings.generalsettings import GeneralSettings
from NewGame.newgame import NewGame

class Play(Screen):
    pass

class Homepage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        Builder.load_file('homepage.kv')
        Builder.load_file('HallOfFame\halloffame.kv')
        Builder.load_file('LoadGame\loadgame.kv')
        Builder.load_file('Credits\credits.kv')
        Builder.load_file('GeneralSettings\generalsettings.kv')
        Builder.load_file('NewGame/newgame.kv')
        self.window_manager = WindowManager()
        self.window_manager.add_widget(Play(name='play'))
        self.window_manager.add_widget(Homepage(name='main'))
        self.window_manager.add_widget(HallOfFame(name='HoF'))
        self.window_manager.add_widget(LoadGame(name='LG'))
        self.window_manager.add_widget(Credits(name='C'))
        self.window_manager.add_widget(GeneralSettings(name='GS'))
        self.window_manager.add_widget(NewGame(name='NG'))
        return self.window_manager


if __name__=="__main__":
    MyApp().run()