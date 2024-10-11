from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from math import sqrt

import os
import json

from elements import cannon, obstacles

class EndLevel(Popup):
    points = 1000
    tot_points = StringProperty('')
    tot_shooted = 0
    def __init__(self, par, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.size_hint = (0.5, 0.5)
        self.auto_dismiss = False
        self.update_tot_points(par)
    
    def update_tot_points(self, par, *args):
        self.tot_shooted = cannon.shoot_count
        if self.tot_shooted <= par:
            self.tot_points = f"You have earned {self.points} points"
        else:
            self.points = (1000 - 50*(self.tot_shooted-par))
            self.tot_points = f"You have earned {self.points} points"

class Transition(Screen):
    def load_screen(self, selected_prj, timestamp, screen_class, name):
        app = App.get_running_app()
        app.add_screen(screen_class, name)
        game_screen = app.root.get_screen(name)  # Ottieni il nuovo schermo
        game_screen.load_screen(selected_prj, timestamp, screen_class)  # Passa i dati al nuovo schermo
        app.root.current = name


class Level(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.basic_bomber = None
        self.basic_cannon = None
        self.basic_laser = None
        self.weaponcounter = 0
        self.keyboard = None
        self.rocklist = []
        self.perpetiolist = []
        self.endLevel_popup = None
        self.par = None
        self.counter_shot = 0

    def load_screen(self, selected_prj, timestamp, screen_name):
        self.screen_name = screen_name
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self.keyboard:
            self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.selected_prj = selected_prj
        self.timestamp = timestamp
        
        if 'bullet' in selected_prj:
            self.basic_cannon = cannon.CannonWidget(pos_hint={'x': 0.1, 'y': 0.2})
            if 'bullet' == selected_prj[0]:
                self.add_widget(self.basic_cannon)
        if 'bomb' in selected_prj:
            self.basic_bomber = cannon.BomberWidget(pos_hint={'x': 0.1, 'y': 0.2})
            if 'bomb' == selected_prj[0]:
                self.add_widget(self.basic_bomber)
        if 'laser' in selected_prj:
            self.basic_laser = cannon.LasergunWidget(pos_hint={'x': 0.1, 'y': 0.2})
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

    def distance(self, pos1, pos2):
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def game_update(self, dt):
        if hasattr(self, 'rock'):     
            for self.rock in self.rocklist[:]:
                if self.basic_cannon :
                    if self.basic_cannon.projectile and self.collisions(self.rock, self.basic_cannon.projectile):
                        self.remove_widget(self.rock)
                        self.basic_cannon.projectile.canvas.remove(self.basic_cannon.projectile.shape)
                        self.remove_widget(self.basic_cannon.projectile)
                        self.basic_cannon.projectile = None
                        self.rocklist.remove(self.rock)
                        Clock.unschedule(self.basic_cannon.move_projectile)
                        Clock.unschedule(self.basic_cannon.timer_projectile)

                if self.basic_bomber :
                    if self.basic_bomber.projectile and self.collisions(self.rock, self.basic_bomber.projectile):
                        self.remove_widget(self.rock)
                        self.rocklist.remove(self.rock)
                        # Raggio di esplosione di 15 pixel
                        explosion_radius = 200
                        
                        # Posizione della bomba
                        bomb_pos = self.basic_bomber.projectile.pos
                        
                        # Controlla le rocce nel raggio dell'esplosione
                        for element in self.rocklist[:]:
                            if self.distance(bomb_pos, element.pos) <= explosion_radius:
                                self.remove_widget(element)
                                self.rocklist.remove(element)
                        
                        self.remove_widget(self.basic_bomber.projectile)
                        self.basic_bomber.projectile.canvas.remove(self.basic_bomber.projectile.shape)
                        self.basic_bomber.projectile = None
                        Clock.unschedule(self.basic_bomber.move_projectile)
                        Clock.unschedule(self.basic_bomber.timer_projectile)

                if self.basic_laser :
                    if self.basic_laser.projectile and self.collisions(self.rock, self.basic_laser.projectile):
                        self.remove_widget(self.rock)
                        self.basic_laser.projectile = None
                        self.rocklist.remove(self.rock)
        
        if hasattr(self, 'treasure'):
            if self.basic_cannon :
                if self.basic_cannon.projectile and self.collisions(self.treasure, self.basic_cannon.projectile):
                    if not self.endLevel_popup:
                        self.endLevel_popup = EndLevel(par=self.par)
                    self.endLevel_popup.open()
                    self.remove_widget(self.treasure)
                    self.remove_widget(self.basic_cannon.projectile)
                    self.basic_cannon.projectile.canvas.remove(self.basic_cannon.projectile.shape)
                    self.basic_cannon.projectile = None
                    Clock.unschedule(self.basic_cannon.move_projectile)
                    Clock.unschedule(self.basic_cannon.timer_projectile)

                    self.update_data()

            if self.basic_bomber :
                if self.basic_bomber.projectile and self.collisions(self.treasure, self.basic_bomber.projectile):
                    if not self.endLevel_popup:
                        self.endLevel_popup = EndLevel(par=self.par)
                    self.endLevel_popup.open()
                    self.remove_widget(self.treasure)
                    self.remove_widget(self.basic_bomber.projectile)
                    self.basic_bomber.projectile.canvas.remove(self.basic_bomber.projectile.shape)
                    self.basic_bomber.projectile = None
                    Clock.unschedule(self.basic_bomber.move_projectile)
                    Clock.unschedule(self.basic_bomber.timer_projectile)

                    self.update_data()

            if self.basic_laser :
                if self.basic_laser.projectile and self.collisions(self.treasure, self.basic_laser.projectile):
                    self.remove_widget(self.treasure)
                    self.basic_laser.projectile = None
                    if not self.endLevel_popup:
                        self.endLevel_popup = EndLevel(par=self.par)
                    self.endLevel_popup.open()

                    self.update_data()
        
        if hasattr(self, 'perpetio'):
            for self.perpetio in self.perpetiolist[:]:
                if self.basic_cannon :
                    if self.basic_cannon.projectile and self.collisions(self.perpetio, self.basic_cannon.projectile):
                        self.remove_widget(self.basic_cannon.projectile)
                        self.basic_cannon.projectile.canvas.remove(self.basic_cannon.projectile.shape)
                        self.basic_cannon.projectile = None
                        Clock.unschedule(self.basic_cannon.move_projectile)
                        Clock.unschedule(self.basic_cannon.timer_projectile)

                if self.basic_bomber :
                    if self.basic_bomber.projectile and self.collisions(self.perpetio, self.basic_bomber.projectile):
                        # Raggio di esplosione di 15 pixel
                        explosion_radius = 200
                        
                        # Posizione della bomba
                        bomb_pos = self.basic_bomber.projectile.pos
                        
                        # Controlla le rocce nel raggio dell'esplosione
                        for element in self.rocklist[:]:
                            if self.distance(bomb_pos, element.pos) <= explosion_radius:
                                self.remove_widget(element)
                                self.rocklist.remove(element)
            
                        self.remove_widget(self.basic_bomber.projectile)
                        self.basic_bomber.projectile.canvas.remove(self.basic_bomber.projectile.shape)
                        self.basic_bomber.projectile = None
                        Clock.unschedule(self.basic_bomber.move_projectile)
                        Clock.unschedule(self.basic_bomber.timer_projectile)

                if self.basic_laser :
                    if self.basic_laser.projectile and self.collisions(self.perpetio, self.basic_laser.projectile):
                        self.basic_laser.projectile = None
        
        if hasattr(self, 'mirror'):
            if self.basic_cannon :
                if self.basic_cannon.projectile and self.collisions(self.mirror, self.basic_cannon.projectile):
                    self.remove_widget(self.basic_cannon.projectile)
                    self.basic_cannon.projectile.canvas.remove(self.basic_cannon.projectile.shape)
                    self.basic_cannon.projectile = None
                    Clock.unschedule(self.basic_cannon.move_projectile)
                    Clock.unschedule(self.basic_cannon.timer_projectile)

            if self.basic_bomber :
                if self.basic_bomber.projectile and self.collisions(self.mirror, self.basic_bomber.projectile):
                    self.remove_widget(self.basic_bomber.projectile)
                    self.basic_bomber.projectile.canvas.remove(self.basic_bomber.projectile.shape)
                    self.basic_bomber.projectile = None
                    Clock.unschedule(self.basic_bomber.move_projectile)
                    Clock.unschedule(self.basic_bomber.timer_projectile)

            if self.basic_laser :
                if self.basic_laser.projectile and self.collisions(self.mirror, self.basic_laser.projectile):
                    self.basic_laser.check_reflection()
            if self.basic_laser :
                if self.basic_laser.eraser and self.collisions(self.mirror, self.basic_laser.eraser):
                    self.basic_laser.check_reflection_eraser()
        self.update_projectiles()
        self.keyboard_Handler

    def keyboard_Handler(self, dt):
        if self.keyboard:
            if (self.basic_bomber is None or self.basic_bomber.projectile is None) and \
               (self.basic_cannon is None or self.basic_cannon.projectile is None) and \
               (self.basic_laser is None or self.basic_laser.projectile is None):
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
            if self.basic_bomber.projectile:
                if (self.basic_bomber.projectile.pos[0] < 0 - self.basic_bomber.projectile.size [0] or self.basic_bomber.projectile.pos[0] > 1000 + self.basic_bomber.projectile.size[0] or 
                    self.basic_bomber.projectile.pos[1] < 0 - self.basic_bomber.projectile.size[1] or self.basic_bomber.projectile.pos[1] > 750 + self.basic_bomber.projectile.size[1]):
                    self.basic_bomber.projectile = None
                    Clock.unschedule(self.basic_bomber.move_projectile)
                    Clock.unschedule(self.basic_bomber.timer_projectile)
        
        if self.basic_cannon:
            if self.basic_cannon.projectile:
                if (self.basic_cannon.projectile.pos[0] < 0 - self.basic_cannon.projectile.size[0] or self.basic_cannon.projectile.pos[0] > 1000 + self.basic_cannon.projectile.size[0] or 
                    self.basic_cannon.projectile.pos[1] < 0 - self.basic_cannon.projectile.size[1] or self.basic_cannon.projectile.pos[1] > 750 + self.basic_cannon.projectile.size[1]):
                    self.basic_cannon.projectile = None 
                    Clock.unschedule(self.basic_cannon.move_projectile)
                    Clock.unschedule(self.basic_cannon.timer_projectile)
        
        if self.basic_laser:
            if self.basic_laser.projectile:
                if (self.basic_laser.projectile.pos[0] < 0 - self.basic_laser.projectile.size[0] or self.basic_laser.projectile.pos[0] > 1000 + self.basic_laser.projectile.size[0] or 
                    self.basic_laser.projectile.pos[1] < 0 - self.basic_laser.projectile.size[1] or self.basic_laser.projectile.pos[1] > 750 + self.basic_laser.projectile.size[1]):
                    self.basic_laser.projectile = None 
                    Clock.unschedule(self.basic_laser.move_projectile)
                    
        
        if self.basic_laser:
            if self.basic_laser.eraser:
                if (self.basic_laser.eraser.pos[0] < 0 - self.basic_laser.eraser.size[0] or self.basic_laser.eraser.pos[0] > 1000 + self.basic_laser.eraser.size[0] or 
                    self.basic_laser.eraser.pos[1] < 0 - self.basic_laser.eraser.size[1] or self.basic_laser.eraser.pos[1] > 750 + self.basic_laser.eraser.size[1]):
                    self.basic_laser.eraser = None 
                    Clock.unschedule(self.basic_laser.move_eraser)
                    Clock.unschedule(self.basic_laser.timer_projectile)
        
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
        self.selected_prj.clear()
        app = App.get_running_app()
        game_screen = app.root.get_screen('levelSelection')  # Ottieni il nuovo schermo
        app.root.remove_widget(app.root.current_screen)
        app.root.current = 'levelSelection'
        game_screen.load_screen(self.timestamp)
    
    def refresh_screen(self):
        self.on_leave()
        app = App.get_running_app()
        app.root.remove_widget(app.root.current_screen)
        game_screen = app.root.get_screen('transition')  # Ottieni il nuovo schermo
        app.root.current = 'transition'
        game_screen.load_screen(self.selected_prj, self.timestamp, self.screen_name, self.name)  # Passa i dati al nuovo schermo
    
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
        
        app = App.get_running_app()
        reload_screen = app.root.current_screen
        reload_screen = str(reload_screen)
        if str(save_data['levels']) == reload_screen[19]:
            save_data['levels']+=1
        
        if save_data['levels'] == 8:
            save_data['secret'] = False

        save_data['coins'] += 50
        save_data['points'] += (1000 - 50*(EndLevel.tot_shooted-self.par))

        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)

class Level1(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 2
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level2(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 3
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(500, 153))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(130, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(715, 425))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(372, 344))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level3(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 1
    
    def obstacles_placer(self):
        self.perpetio = obstacles.Perpetios(size = (100, 100), pos=(394, 400))
        self.perpetio.size_hint = (None, None)
        self.add_widget(self.perpetio)
        self.perpetiolist.append(self.perpetio)

        self.perpetio = obstacles.Perpetios(size = (100, 100), pos=(100, 100))
        self.perpetio.size_hint = (None, None)
        self.add_widget(self.perpetio)
        self.perpetiolist.append(self.perpetio)

        self.perpetio = obstacles.Perpetios(size = (100, 100), pos=(407, 600))
        self.perpetio.size_hint = (None, None)
        self.add_widget(self.perpetio)
        self.perpetiolist.append(self.perpetio)

        self.perpetio = obstacles.Perpetios(size = (100, 100), pos=(630, 195))
        self.perpetio.size_hint = (None, None)
        self.add_widget(self.perpetio)
        self.perpetiolist.append(self.perpetio)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 300))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level4(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 2
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(635, 525))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(635, 375))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.perpetio = obstacles.Perpetios(size = (100, 100), pos=(630, 210))
        self.perpetio.size_hint = (None, None)
        self.add_widget(self.perpetio)
        self.perpetiolist.append(self.perpetio)

        self.perpetio = obstacles.Perpetios(size = (100, 100), pos=(430, 495))
        self.perpetio.size_hint = (None, None)
        self.add_widget(self.perpetio)
        self.perpetiolist.append(self.perpetio)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(870, 460))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level5(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 1
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.mirror = obstacles.Mirror(size = (100, 100), pos = (500, 500))
        self.mirror.size_hint = (None, None)
        self.add_widget(self.mirror)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level6(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 4
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level7(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 3
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)

class Level8(Level, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obstacles_placer()
        self.par = 1
    
    def obstacles_placer(self):
        self.rock = obstacles.Rocks(size = (100, 100), pos=(472, 400))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(100, 100))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.rock = obstacles.Rocks(size = (100, 100), pos=(765, 225))
        self.rock.size_hint = (None, None)
        self.add_widget(self.rock)
        self.rocklist.append(self.rock)

        self.treasure = obstacles.Treasure(size = (70, 70), pos=(800, 100))
        self.treasure.size_hint = (None, None)
        self.add_widget(self.treasure)