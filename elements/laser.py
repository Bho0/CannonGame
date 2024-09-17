from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window


class Lasergun(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.15 , 0.15)
        self.new_button = Button(text='shoot a laser', size_hint=(1, 1), pos_hint= {'x': 0.2, 'y': 0.5})
        self.add_widget(self.new_button) 
        self.laserloaded = False
        self.click_count = 0    
        self.time_passed = 0
        self.laser = None
        self.laser_MASS = 150
        self.eraser = None
        self.lines = []
    
    def on_touch_down(self, touch):  #sistemare i casi limite dei conti aka se clicco due volte fuori e poi dentro
        self.click_count = self.click_count + 1
        if self.new_button.collide_point(*touch.pos):
            self.laserloaded = True
            pass
        if self.laserloaded == True and self.click_count % 2 == 0 and self.laser == None:
            x, y = touch.pos
            self.mouse_delta = (x - self.new_button.x, y - self.new_button.y)
            self.create_laser()
            self.laserloaded = False
        
    def create_laser (self):            
        self.time_passed = 0
        initial_pos = self.new_button.center
        self.laser = laser(pos = (initial_pos), size=(0.5, 0.5))
        self.laser.size_hint = (None, None)
        if self.eraser:
            Clock.unschedule(self.move_eraser)
            self.remove_widget(self.eraser)
            self.eraser = None
        self.add_widget(self.laser)
        Clock.schedule_interval(self.timer, 0.01)    

    def move_laser(self):
        if self.laser is not None:
            x, y = self.laser.pos
            self.delta_x, self.delta_y = self.mouse_delta
            self.xspeed, self.yspeed = self.delta_x, self.delta_y
            self.new_x = x -  (self.delta_x * 0.01)
            self.new_y = y - (self.delta_y * 0.01) 
            self.laser.pos = (self.new_x, self.new_y)
            with self.canvas:
                Color(1, 0, 0, 1)  # Set line color (red)
                self.line_color = Color(1, 0, 0, 1)
                self.line = Line(points=[x, y ,self.new_x, self.new_y], width=2)
                self.lines.append((self.line))
    
    def create_eraser(self):
        # Create the eraser and move it to the last position
        self.eraser = eraser()
        self.eraser.center = self.new_button.center
        self.add_widget(self.eraser)
        Clock.schedule_interval(self.move_eraser, 0.01)

    def move_eraser(self, dt):
        x, y = self.eraser.pos
        self.new_x = x -  (self.xspeed* 0.01)  
        self.new_y = y - (self.yspeed * 0.01) 
        self.eraser.pos = (self.new_x, self.new_y)
        self.check_collision_with_line()
        if self.laser is not None and self.eraser.collide_widget(self.laser):
            self.remove_widget(self.laser)   
            self.laser = None
    
    def check_collision_with_line(self):
        eraser_x, eraser_y = self.eraser.pos
        eraser_width, eraser_height = self.eraser.size

        lines_to_remove = []
        for line in self.lines:
            x1, y1, x2, y2 = line.points

            if self.eraser_collides_with_line(eraser_x, eraser_y, eraser_width, eraser_height, x1, y1, x2, y2):
                lines_to_remove.append(line)
            
        for line in lines_to_remove:
            self.lines.remove(line)
            self.canvas.remove(line)

    def eraser_collides_with_line(self, ex, ey, ew, eh, x1, y1, x2, y2):
        # Check if the eraser rectangle intersects the line segment
        return (min(x1, x2) < ex + ew and max(x1, x2) > ex and 
                min(y1, y2) < ey + eh and max(y1, y2) > ey)

    def timer (self, dt):
        if self.laser is not None and self.time_passed <= 10:
         self.move_laser()
        self.time_passed = self.time_passed + dt
        if self.time_passed >= 10 and not self.eraser:
            self.create_eraser()
        
class eraser (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)
        self.size_hint= (None, None)

class laser (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = 'laser'
        self.size = ( 0.5, 0.5)
        self.size_hint = (None, None)
        
        with self.canvas:
            Color(1, 0, 0, 1)  # Red color
            self.rect = Rectangle(size=(0.5, 0.5), pos=(self.pos)) 

        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        # Update the rectangle's position to match the laser's position
        self.rect.pos = self.pos