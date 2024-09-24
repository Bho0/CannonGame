from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

import os
import json

from elements import bullet, bomb, laser, obstacles

class EndLevel(Popup):
    points = 1000
    tot_points = StringProperty('')
    tot_shooted = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.5, 0.5)
        self.auto_dismiss = False
        self.update_tot_points()
    
    def update_tot_points(self, *args):
        self.tot_shooted = bullet.bullet_shooted + bomb.bomb_shooted + laser.laser_shooted
        if self.tot_shooted <= 2:
            self.tot_points = f"You have earned {self.points} points"
        else:
            self.points = (1000 - 50*(self.tot_shooted-2))
            self.tot_points = f"You have earned {self.points} points"

class Level(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.basic_bomber = None
        self.basic_cannon = None
        self.basic_laser = None
        self.weaponcounter = 0
        self.keyboard = None
        self.rocklist = []
        self.endLevel_popup = None
        self.counter_shot = 0

    def load_screen(self, selected_prj, timestamp):
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self.keyboard:
            self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.selected_prj = selected_prj
        self.timestamp = timestamp
        
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
        if w1 is not None and w2 is not None:
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
                        self.basic_cannon.bullet.canvas.remove(self.basic_cannon.bullet.circle)
                        self.remove_widget(self.basic_cannon.bullet)
                        self.basic_cannon.bullet = None
                        self.rocklist.remove(self.rock)
                        Clock.unschedule(self.basic_cannon.move_bullet)
                        Clock.unschedule(self.basic_cannon.timer_bullet)

                if self.basic_bomber :
                    if self.basic_bomber.bomb and self.collisions(self.rock, self.basic_bomber.bomb):
                        self.remove_widget(self.rock)
                        self.remove_widget(self.basic_bomber.bomb)
                        self.basic_bomber.bomb.canvas.remove(self.basic_bomber.bomb.circle)
                        self.basic_bomber.bomb = None
                        self.rocklist.remove(self.rock)
                        Clock.unschedule(self.basic_bomber.move_bomb)
                        Clock.unschedule(self.basic_bomber.timer_bomb)

                if self.basic_laser :
                    if self.basic_laser.laser and self.collisions(self.rock, self.basic_laser.laser):
                        self.remove_widget(self.rock)
                        self.basic_laser.laser = None
                        self.rocklist.remove(self.rock)
        
        if hasattr(self, 'treasure'):
            if self.basic_cannon :
                if self.basic_cannon.bullet and self.collisions(self.treasure, self.basic_cannon.bullet):
                    if not self.endLevel_popup:
                        self.endLevel_popup = EndLevel()
                    self.endLevel_popup.open()
                    self.remove_widget(self.treasure)
                    self.remove_widget(self.basic_cannon.bullet)
                    self.basic_cannon.bullet.canvas.remove(self.basic_cannon.bullet.circle)
                    self.basic_cannon.bullet = None
                    Clock.unschedule(self.basic_cannon.move_bullet)
                    Clock.unschedule(self.basic_cannon.timer_bullet)

                    self.update_data()

            if self.basic_bomber :
                if self.basic_bomber.bomb and self.collisions(self.treasure, self.basic_bomber.bomb):
                    if not self.endLevel_popup:
                        self.endLevel_popup = EndLevel()
                    self.endLevel_popup.open()
                    self.remove_widget(self.treasure)
                    self.remove_widget(self.basic_bomber.bomb)
                    self.basic_bomber.bomb.canvas.remove(self.basic_bomber.bomb.circle)
                    self.basic_bomber.bomb = None
                    Clock.unschedule(self.basic_bomber.move_bomb)
                    Clock.unschedule(self.basic_bomber.timer_bomb)

                    self.update_data()

            if self.basic_laser :
                if self.basic_laser.laser and self.collisions(self.treasure, self.basic_laser.laser):
                    self.remove_widget(self.treasure)
                    self.basic_laser.laser = None
                    if not self.endLevel_popup:
                        self.endLevel_popup = EndLevel()
                    self.endLevel_popup.open()

                    self.update_data()

        self.update_projectiles()
        self.keyboard_Handler

    def keyboard_Handler(self, dt):
        if self.keyboard:
            if (self.basic_bomber is None or self.basic_bomber.bomb is None) and \
               (self.basic_cannon is None or self.basic_cannon.bullet is None) and \
               (self.basic_laser is None or self.basic_laser.laser is None):
                self.keyboard.bind(on_key_down=self._on_keyboard_down)
            else:
                self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        else:
            # If keyboard is None, try to request it again
            self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
            if self.keyboard:
                self.keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def update_projectiles(self):
    # Check for boundary conditions of projectiles and remove them if they leave the screen
        if self.basic_bomber:
            if self.basic_bomber.bomb:
                if (self.basic_bomber.bomb.pos[0] < 0 - self.basic_bomber.bomb.size [0] or self.basic_bomber.bomb.pos[0] > 1000 + self.basic_bomber.bomb.size[0] or 
                    self.basic_bomber.bomb.pos[1] < 0 - self.basic_bomber.bomb.size[1] or self.basic_bomber.bomb.pos[1] > 750 + self.basic_bomber.bomb.size[1]):
                    self.basic_bomber.bomb = None
                    Clock.unschedule(self.basic_bomber.move_bomb)
                    Clock.unschedule(self.basic_bomber.timer_bomb)
        
        if self.basic_cannon:
            if self.basic_cannon.bullet:
                if (self.basic_cannon.bullet.pos[0] < 0 - self.basic_cannon.bullet.size[0] or self.basic_cannon.bullet.pos[0] > 1000 + self.basic_cannon.bullet.size[0] or 
                    self.basic_cannon.bullet.pos[1] < 0 - self.basic_cannon.bullet.size[1] or self.basic_cannon.bullet.pos[1] > 750 + self.basic_cannon.bullet.size[1]):
                    self.basic_cannon.bullet = None 
                    Clock.unschedule(self.basic_cannon.move_bullet)
                    Clock.unschedule(self.basic_cannon.timer_bullet)

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

    def return_to_levels(self):
        self.on_leave()
        for element in self.selected_prj:
                self.selected_prj.pop()
        app = App.get_running_app()
        app.root.remove_widget(app.root.current_screen)
        app.root.current = 'levelSelection'
    
    def refresh_screen(self):
        self.on_leave()  # Aggiungi controlli se necessario
        app = App.get_running_app()

        # Rimuovere il widget corrente
        self.clear_widgets()

        # Ricaricare il file .kv e la schermata
        Builder.unload_file('Level.kv')  # Unload the current .kv file
        Builder.load_file('Level.kv')  # Reload the .kv file

        # Ripristina la schermata (se necessario)
        reload_screen = app.root.current_screen
        app.root.remove_widget(app.root.current_screen)
        app.root.add_widget(reload_screen)

        self.load_screen(self.selected_prj, self.timestamp)
        
        # Cambia schermata, se necessario
        app.root.current = reload_screen.name
    
    def on_leave(self):
        # Make sure to clean up the keyboard when leaving the screen
        if self.keyboard:
            self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None
        Clock.unschedule(self.keyboard_Handler)
    
    def update_data(self):
        filename = 'save_data.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                all_data = json.load(f)
            
            if self.timestamp in all_data:
                save_data = all_data[self.timestamp]
        
        save_data['coins'] += 50
        save_data['points'] += (1000 - 50*(EndLevel.tot_shooted-2))

        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)

class Level1(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level2(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level3(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level4(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level5(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level6(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level7(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level8(Level):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
    
    def obstacles_placer(self):
        self.rock = obstacles.rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)