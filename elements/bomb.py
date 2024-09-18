from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class Bombshooter(FloatLayout):   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.15 , 0.15)
        self.new_button = Button(text='shoot a bomb', size_hint=(1, 1), pos_hint= {'x': 0.2, 'y': 0.5})
        self.add_widget(self.new_button) 
        self.bombloaded = False 
        self.time_passed = 0
        self.bomb = None
        self.BOMB_MASS = 150
    
    def on_touch_down(self, touch):  #sistemare i casi limite dei conti aka se clicco due volte fuori e poi dentro
        if self.new_button.collide_point(*touch.pos):
            self.bombloaded = True
        else:
            if self.bombloaded == True and self.bomb == None:
                x, y = touch.pos
                self.mouse_delta = (x - self.new_button.x, y - self.new_button.y)
                self.create_bomb()
                self.bombloaded = False

    def create_bomb (self):
        self.time_passed = 0
        initial_pos = self.new_button.center
        self.bomb = bomb(pos = (initial_pos), size=(50, 50))
        self.add_widget(self.bomb)
        Clock.schedule_interval(self.move_bomb, 0.01)
        Clock.schedule_interval(self.timer, 0.01)

    def move_bomb(self, dt):
        if self.bomb is not None:
            x, y = self.bomb.pos
            self.delta_x, self.delta_y = self.mouse_delta
            if self.delta_x > self.BOMB_MASS:
                self.delta_x = self.BOMB_MASS
            if self.delta_y > self.BOMB_MASS:
                self.delta_y = self.BOMB_MASS
            new_x = x +  (self.delta_x * 0.01)
            new_y = y + (self.delta_y * 0.01) - (0.98 * self.time_passed)
            self.bomb.pos = (new_x, new_y)

    def timer (self, dt):
        self.time_passed = self.time_passed + dt

class bomb (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'bomb'
        self.size = (50 ,50)
        self.size_hint = (None, None)
        
        with self.canvas:
            Color(1, 1, 1, 1)  # Red color
            self.rect = Rectangle(size=(50, 50), pos=(self.pos)) 

        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        # Update the rectangle's position to match the bomb's position
        self.rect.pos = self.pos
         
