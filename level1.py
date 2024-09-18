from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

from elements import bullet, bomb, laser, obstacles


class Level1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.basic_bomber = None
        self.basic_cannon = None
        self.basic_laser = None
        self.weaponcounter = 0
        self.keyboard = None
        self.rocklist = []
        self.obstacles_placer()

    def load_screen(self, selected_prj, timestamp):
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.selected_prj = selected_prj
        
        if 'bullet' in selected_prj:
            self.basic_cannon = bullet.CannonWidget(pos_hint={'x': 0.1, 'y': 0.2})
            if 'bullet' == selected_prj[0]:
                self.add_widget(self.basic_cannon)
        if 'bomb' in selected_prj:
            self.basic_bomber = bomb.Bombshooter(pos_hint={'x': 0.1, 'y': 0.2})
            if 'bomb' == selected_prj[0]:
                self.add_widget(self.basic_bomber)
        if 'laser' in selected_prj:
            self.basic_laser = laser.Lasergun(pos_hint={'x': 0.1, 'y': 0.2})
            if 'laser' == selected_prj[0]:
                self.add_widget(self.basic_laser)
        
        Clock.schedule_interval(self.game_update, 0.01)
        Clock.schedule_interval(self.keyboard_Handler, 0.01)
    
    def collisions(self, w1, w2):
        if w1 and w2:
            # Get positions and sizes of both widgets
            x11, y11 = w1.pos  # bottom-left corner of w1
            x12, y12 = x11 + w1.size[0], y11 + w1.size[1]  # top-right corner of w1
            x21, y21 = w2.pos  # bottom-left corner of w2
            x22, y22 = x21 + w2.size[0], y21 + w2.size[1]  # top-right corner of w2
            x11, y11 = self.to_window(*w1.pos)
            x21, y21 = self.to_window(*w2.pos)

            # Check if there's any overlap between the bounding boxes
            if (x11 < x22 and x12 > x21) and (y11 < y22 and y12 > y21):
                return True
        return False

    def game_update(self, dt):
        if hasattr(self, 'rock'):     
            for self.rock in self.rocklist[:]:
                if self.basic_cannon :
                    if self.basic_cannon.bullet and self.collisions(self.rock, self.basic_cannon.bullet):
                        self.remove_widget(self.rock)
                if self.basic_bomber :
                    if self.basic_bomber.bomb and self.collisions(self.rock, self.basic_bomber.bomb):
                        self.remove_widget(self.rock)
                if self.basic_laser :
                    if self.basic_laser.laser and self.collisions(self.rock, self.basic_laser.laser):
                        self.remove_widget(self.rock)
        self.update_projectiles()
        self.keyboard_Handler

    def keyboard_Handler(self, dt):
        if (self.basic_bomber is None or self.basic_bomber.bomb is None) and (self.basic_cannon is None or self.basic_cannon.bullet is  None) and  (self.basic_laser is None  or self.basic_laser.laser is  None):
            self.keyboard.bind(on_key_down=self._on_keyboard_down)
        if (self.basic_bomber and self.basic_bomber.bomb) or (self.basic_cannon and self.basic_cannon.bullet) or (self.basic_laser and self.basic_laser.laser):
           self.keyboard.unbind(on_key_down=self._on_keyboard_down)
    
    def update_projectiles(self):
    # Check for boundary conditions of projectiles and remove them if they leave the screen
        if self.basic_bomber:
            if self.basic_bomber.bomb:
                if (self.basic_bomber.bomb.pos[0] < 0 - self.basic_bomber.bomb.size [0] or self.basic_bomber.bomb.pos[0] > 1000 + self.basic_bomber.bomb.size[0] or 
                    self.basic_bomber.bomb.pos[1] < 0 - self.basic_bomber.bomb.size[1] or self.basic_bomber.bomb.pos[1] > 750 + self.basic_bomber.bomb.size[1]):
                    self.basic_bomber.bomb = None
        
        if self.basic_cannon:
            if self.basic_cannon.bullet:
                if (self.basic_cannon.bullet.pos[0] < 0 - self.basic_cannon.bullet.size[0] or self.basic_cannon.bullet.pos[0] > 1000 + self.basic_cannon.bullet.size[0] or 
                    self.basic_cannon.bullet.pos[1] < 0 - self.basic_cannon.bullet.size[1] or self.basic_cannon.bullet.pos[1] > 750 + self.basic_cannon.bullet.size[1]):
                    self.basic_cannon.bullet = None 

    def _keyboard_closed(self):
        if self.keyboard:
            self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None   

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):  
        if keycode[1] == 'left':
            self.weaponcounter -= 1
            self.weaponswitcher(self.selected_prj)
        elif keycode[1] == 'right':
            self.weaponcounter += 1
            self.weaponswitcher(self.selected_prj)

    def weaponswitcher(self, selected_prj):
        if self.basic_cannon:
            self.remove_widget(self.basic_cannon)
        if self.basic_bomber:
            self.remove_widget(self.basic_bomber)
        if self.basic_laser:
            self.remove_widget(self.basic_laser)

        if self.weaponcounter < 0:
            self.weaponcounter = len(selected_prj)-1
            if selected_prj[self.weaponcounter]:
                if 'bullet' == selected_prj[self.weaponcounter]:
                    self.add_widget(self.basic_cannon)
                
                if 'bomb' == selected_prj[self.weaponcounter]:
                    self.add_widget(self.basic_bomber)
                
                if 'laser' == selected_prj[self.weaponcounter]:
                    self.add_widget(self.basic_laser)
        
        elif self.weaponcounter > len(selected_prj)-1:
            self.weaponcounter = 0
            if selected_prj[self.weaponcounter]:
                if 'bullet' == selected_prj[self.weaponcounter]:
                    self.add_widget(self.basic_cannon)
                
                if 'bomb' == selected_prj[self.weaponcounter]:
                    self.add_widget(self.basic_bomber)
                
                if 'laser' == selected_prj[self.weaponcounter]:
                    self.add_widget(self.basic_laser)

        elif selected_prj[self.weaponcounter]:
            if 'bullet' == selected_prj[self.weaponcounter]:
                self.add_widget(self.basic_cannon)
            
            if 'bomb' == selected_prj[self.weaponcounter]:
                self.add_widget(self.basic_bomber)
            
            if 'laser' == selected_prj[self.weaponcounter]:
                self.add_widget(self.basic_laser)
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (50, 50), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)