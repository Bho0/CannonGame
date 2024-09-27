from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Line
from kivy.clock import Clock

from elements.projectile import Bullet, Bomb, Laser, Eraser

shoot_count = 0

class ImageButton(ButtonBehavior, Image):
    pass

class Shooter(FloatLayout):
    def __init__(self, button_image, label_text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.3, 0.3)
        self.new_button = ImageButton(source=button_image, size_hint=(1, 1), pos_hint={'x': 0.1, 'y': 0.1})
        self.new_label = Label(text=label_text, font_name='fonts/Caribbean.ttf', color=(0, 0, 0, 1), pos_hint={'x': 0.1, 'y': 0.3})
        self.add_widget(self.new_button)
        self.add_widget(self.new_label)
        self.loaded = False
        self.time_passed = 0
        self.projectile = None
        self.MASS = 150
        self.sound = None

        global shoot_count
        shoot_count = 0

    def on_touch_down(self, touch):
        global shoot_count
        if self.new_button.collide_point(*touch.pos):
            self.loaded = True
        else:
            if self.loaded and self.projectile is None:
                x, y = touch.pos
                self.mouse_delta = (x - self.new_button.x, y - self.new_button.y)
                self.create_projectile()
                sound = self.use_specific_sound()
                self.sound = SoundLoader.load(sound)
                if self.sound:
                    self.sound.play()
                self.loaded = False
                shoot_count += 1

    def create_projectile(self):
        self.time_passed = 0
        initial_pos = self.new_button.center
        self.projectile = self.create_specific_projectile(pos=(initial_pos))
        self.add_widget(self.projectile)
        Clock.schedule_interval(self.move_projectile, 0.01)
        Clock.schedule_interval(self.timer_projectile, 0.01)

    def move_projectile(self, dt):
        if self.projectile is not None:
            x, y = self.projectile.pos
            self.delta_x, self.delta_y = self.mouse_delta
            if self.delta_x > self.MASS:
                self.delta_x = self.MASS
            if self.delta_y > self.MASS:
                self.delta_y = self.MASS
            new_x = x + (self.delta_x * 0.01)
            new_y = y + (self.delta_y * 0.01) - (0.98 * self.time_passed)
            self.projectile.pos = (new_x, new_y)

    def timer_projectile(self, dt):
        self.time_passed += dt

    def create_specific_projectile(self, pos):
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def use_specific_sound(self):
        raise NotImplementedError("This method should be implemented by subclasses.")


class BomberWidget(Shooter):
    def __init__(self, **kwargs):
        super().__init__("images/ship.png", "Bomb selected", **kwargs)

    def create_specific_projectile(self, pos):
        return Bomb(pos=pos)  # Restituisci un'istanza di Bomb
    
    def use_specific_sound(self):
        return "sounds/cannon-fire-161072.mp3"

class CannonWidget(Shooter):
    def __init__(self, **kwargs):
        super().__init__("images/ship.png", "Bullet selected", **kwargs)

    def create_specific_projectile(self, pos):
        return Bullet(pos=pos)  # Restituisci un'istanza di Bullet
    
    def use_specific_sound(self):
        return "sounds/bomb.mp3"

class LasergunWidget(Shooter):
    def __init__(self, **kwargs):
        # Passa i parametri specifici al costruttore della classe base
        super().__init__(button_image="images/ship.png", label_text="Laser selected", **kwargs)
        self.eraser = None
        self.lines = []

    def create_specific_projectile(self, pos):
        # Qui creiamo un laser specifico per la Lasergun
        laser = Laser(pos=pos)  # Puoi usare la dimensione desiderata
        laser.size_hint = (None, None)
        return laser

    def move_projectile(self, dt):
        if self.projectile is not None:
            x, y = self.projectile.pos
            self.delta_x, self.delta_y = self.mouse_delta
            new_x = x + (self.delta_x * 0.01)
            new_y = y + (self.delta_y * 0.01)
            self.projectile.pos = (new_x, new_y)
            # Disegna la traccia laser
            with self.canvas:
                Color(1, 0, 0, 1)  # Colore rosso per il laser
                self.line = Line(points=[x, y, new_x, new_y], width=2)
                self.lines.append(self.line)

    def timer_projectile(self, dt):
        super().timer_projectile(dt)
        if self.time_passed >= 1 and not self.eraser:
            self.create_eraser()

    def create_eraser(self):
        self.eraser = Eraser()
        self.eraser.center = self.new_button.center
        self.add_widget(self.eraser)
        Clock.schedule_interval(self.move_eraser, 0.01)

    def move_eraser(self, dt):
        if self.eraser:
            x, y = self.eraser.pos
            new_x = x + (self.delta_x * 0.01)
            new_y = y + (self.delta_y * 0.01)
            self.eraser.pos = (new_x, new_y)
            self.check_collision_with_line()
            if self.projectile and self.eraser.collide_widget(self.projectile):
                self.remove_widget(self.projectile)
                self.projectile = None

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
        return (min(x1, x2) < ex + ew and max(x1, x2) > ex and 
                min(y1, y2) < ey + eh and max(y1, y2) > ey)
    
    def use_specific_sound(self):
        return "sounds/laser.mp3"