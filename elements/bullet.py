from kivy.uix.widget import Widget
from kivy.uix.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Ellipse, Color, Line
from kivy.clock import Clock

bullet_shooted = 0

class ImageButton(ButtonBehavior, Image):
    pass

class CannonWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.3 , 0.3)
        self.new_button = ImageButton(source = "images/ship.png", size_hint=(1, 1), pos_hint= {'x': 0.1, 'y': 0.1})
        self.add_widget(self.new_button) 
        self.bulletloaded = False   
        self.time_passed = 0
        self.bullet = None
        self.BULLET_MASS = 150

        global bullet_shooted
        bullet_shooted = 0
    
    def on_touch_down(self, touch):
        global bullet_shooted
        #sistemare i casi limite dei conti aka se clicco due volte fuori e poi dentro
        if self.new_button.collide_point(*touch.pos):
            self.bulletloaded = True
        else:
            if self.bulletloaded == True and self.bullet == None:
                x, y = touch.pos
                self.mouse_delta = (x - self.new_button.x, y - self.new_button.y)
                self.create_bullet()
                self.bulletloaded = False
                bullet_shooted += 1

    def create_bullet (self):
        self.time_passed = 0
        initial_pos = self.new_button.center
        self.bullet = Bullet(pos = (initial_pos), size=(50,50))
        self.add_widget(self.bullet)
        
        Clock.schedule_interval(self.move_bullet, 0.01)
        Clock.schedule_interval(self.timer_bullet, 0.01)

    def move_bullet(self, dt):
     if self.bullet is not None:
        x, y = self.bullet.pos
        self.delta_x, self.delta_y = self.mouse_delta
        if self.delta_x > self.BULLET_MASS + 50:
            self.delta_x = self.BULLET_MASS + 50
        if self.delta_y > self.BULLET_MASS + 50:
            self.delta_y = self.BULLET_MASS + 50
        new_x = x +  (self.delta_x * 0.01)
        new_y = y + (self.delta_y * 0.01) - (0.98 * self.time_passed)
        self.bullet.pos = (new_x, new_y)
    
    def timer_bullet (self, dt):
        self.time_passed += dt
   
class Bullet (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'bullet'
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