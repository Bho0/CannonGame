from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

bomb_shooted = 0

class ImageButton(ButtonBehavior, Image):
    pass

class Bombshooter(FloatLayout):   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.3 , 0.3)
        self.new_button = ImageButton(source = "images/ship.png", size_hint=(1, 1), pos_hint= {'x': 0.1, 'y': 0.1})
        self.new_label = Label(text = "Bomb selected", font_name = 'fonts/Caribbean.ttf', color = (0, 0, 0, 1), pos_hint = {'x': 0.1, 'y': 0.3})
        self.add_widget(self.new_button)
        self.add_widget(self.new_label)  
        self.bombloaded = False 
        self.time_passed = 0
        self.bomb = None
        self.BOMB_MASS = 150

        global bomb_shooted
        bomb_shooted = 0
    
    def on_touch_down(self, touch):
        global bomb_shooted
        #sistemare i casi limite dei conti aka se clicco due volte fuori e poi dentro
        if self.new_button.collide_point(*touch.pos):
            self.bombloaded = True
        else:
            if self.bombloaded == True and self.bomb == None:
                x, y = touch.pos
                self.mouse_delta = (x - self.new_button.x, y - self.new_button.y)
                self.create_bomb()
                self.bombloaded = False
                bomb_shooted += 1

    def create_bomb (self):
        self.time_passed = 0
        initial_pos = self.new_button.center
        self.bomb = Bomb(pos = (initial_pos), size=(50, 50))
        self.add_widget(self.bomb)
        Clock.schedule_interval(self.move_bomb, 0.01)
        Clock.schedule_interval(self.timer_bomb, 0.01)

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

    def timer_bomb (self, dt):
        self.time_passed = self.time_passed + dt

class Bomb (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'bomb'
        self.size_hint=(None, None)

        with self.canvas:
            Color(0, 0, 0, 1)  # Colore rosso
            self.circle = Ellipse(pos=self.pos, size=(self.width, self.height))  # Dimensioni iniziali
            self.bind(pos=self.update_circle, size=self.update_circle)
         

    def update_circle(self, *args):
        # Aggiorna la posizione e le dimensioni del cerchio
        self.circle.pos = self.pos
        # Imposta le dimensioni del cerchio in modo che sia un cerchio perfetto
        diameter = min(self.width, self.height)  # Usa il valore min per mantenere la forma circolare
        self.circle.size = (diameter, diameter)