from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Line
from kivy.clock import Clock
import math

from elements.projectile import Bullet, Bomb, Laser, Eraser

# Global variable to keep track of the number of shots fired
shoot_count = 0

# Custom button class with an image background
class ImageButton(ButtonBehavior, Image):
    pass

# Shooter base class that handles projectile creation and movement
class Shooter(FloatLayout):
    def __init__(self, button_image, label_text, **kwargs):
        super().__init__(**kwargs)
        # Initializing size and button for the shooter
        self.size_hint = (0.3, 0.3)
        self.new_button = ImageButton(source=button_image, size_hint=(1, 1), pos_hint={'x': 0.1, 'y': 0.1})
        self.new_label = Label(text=label_text, font_name='fonts/Caribbean.ttf', color=(0, 0, 0, 1), pos_hint={'x': 0.1, 'y': 0.3})
        # Add button and label to the layout
        self.add_widget(self.new_button)
        self.add_widget(self.new_label)
        # Additional variables to manage projectile state
        self.loaded = False
        self.time_passed = 0
        self.projectile = None
        self.MASS = None
        # Loading and setting the sound for shooting
        sound = self.use_specific_sound()
        self.sound = SoundLoader.load(sound)

        # Reset global shoot_count to 0
        global shoot_count
        shoot_count = 0

    def on_touch_down(self, touch):
        global shoot_count
        # Check if the button was pressed, then set loaded to True
        if self.new_button.collide_point(*touch.pos):
            self.loaded = True
        else:
            # If the button was pressed and no projectile is active, create a new one
            if self.loaded and self.projectile is None:
                x, y = touch.pos
                self.mouse_delta = (x - self.new_button.x, y - self.new_button.y)
                self.delta_x, self.delta_y = self.mouse_delta
                self.delta_x_eraser = self.delta_x
                self.delta_y_eraser = self.delta_y
                self.create_projectile()  # Create projectile
                if self.sound:
                    self.sound.play()  # Play sound on shoot
                self.loaded = False
                shoot_count += 1  # Increment shoot count

    def create_projectile(self):
        # Reset time and create the projectile
        self.time_passed = 0
        initial_pos = self.new_button.center
        self.projectile = self.create_specific_projectile(pos=(initial_pos))
        self.add_widget(self.projectile)
        # Schedule movement and timer for projectile
        Clock.schedule_interval(self.move_projectile, 0.01)
        Clock.schedule_interval(self.timer_projectile, 0.01)

    def move_projectile(self, dt):
        # If the projectile exists, move it according to the velocity
        if self.projectile is not None:
            x, y = self.projectile.pos
            if self.delta_x > self.MASS:
                self.delta_x = self.MASS  # Limit the movement on x-axis
            if self.delta_y > self.MASS:
                self.delta_y = self.MASS  # Limit the movement on y-axis
            # Move projectile position with respect to the velocity
            new_x = x + (self.delta_x * 0.01)
            new_y = y + (self.delta_y * 0.01) - (0.98 * self.time_passed)
            self.projectile.pos = (new_x, new_y)

    def timer_projectile(self, dt):
        # Increment the time passed for the projectile
        self.time_passed += dt

    def create_specific_projectile(self, pos):
        # This method needs to be implemented by subclasses
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def use_specific_sound(self):
        # This method needs to be implemented by subclasses to specify the shooting sound
        raise NotImplementedError("This method should be implemented by subclasses.")

# BomberWidget subclass that creates and handles Bomb projectiles
class BomberWidget(Shooter):
    def __init__(self, **kwargs):
        super().__init__("images/ship.png", "Bomb selected", **kwargs)

    def create_specific_projectile(self, pos):
        self.MASS = 150  # Set mass for the Bomb
        return Bomb(pos=pos)  # Return a Bomb instance
    
    def use_specific_sound(self):
        return "sounds/cannon-fire-161072.mp3"  # Return sound for Bomb

# CannonWidget subclass that creates and handles Bullet projectiles
class CannonWidget(Shooter):
    def __init__(self, **kwargs):
        super().__init__("images/ship.png", "Bullet selected", **kwargs)

    def create_specific_projectile(self, pos):
        self.MASS = 230  # Set mass for the Bullet
        return Bullet(pos=pos)  # Return a Bullet instance
    
    def use_specific_sound(self):
        return "sounds/bomb.mp3"  # Return sound for Bullet

# LasergunWidget subclass that creates and handles Laser projectiles with reflection behavior
class LasergunWidget(Shooter):
    def __init__(self, **kwargs):
        super().__init__(button_image="images/ship.png", label_text="Laser selected", **kwargs)
        self.eraser = None  # Eraser to clear laser
        self.lines = []  # Store laser lines for collision
        self.reflected = False  # Flag to track laser reflection

    def create_specific_projectile(self, pos):
        # Create a laser projectile
        laser = Laser(pos=pos)  
        laser.size_hint = (None, None)  # Set specific size
        self.reflected = False
        if not self.eraser:
            self.create_eraser()  # Create eraser if not present
        return laser

    def move_projectile(self, dt):
        # Move laser projectile and draw its trail
        if self.projectile is not None:
            x, y = self.projectile.pos
            new_x = x + (self.delta_x * 0.01)
            new_y = y + (self.delta_y * 0.01)
            self.projectile.pos = (new_x, new_y)
            # Draw laser line in red color
            with self.canvas:
                Color(1, 0, 0, 1)  # Set color to red for laser
                self.line = Line(points=[x, y, new_x, new_y], width=2)
                self.lines.append(self.line)

    def on_touch_down(self, touch):
        # Handle touch event for the eraser and projectile
        if not self.eraser:
            super().on_touch_down(touch)

    def create_eraser(self):
        # Create and position the eraser
        self.eraser = Eraser()
        self.eraser.center = self.new_button.center
        self.add_widget(self.eraser)
        Clock.schedule_once(self.start_moving_eraser, 1)

    def start_moving_eraser(self, dt):
        # Start moving the eraser
        Clock.schedule_interval(self.move_eraser, 0.01)

    def collsion_eraser_laser(self):
        # Check for collision between eraser and laser
        if self.projectile and self.eraser.collide_widget(self.projectile):
            self.eraser = None
            self.projectile = None
            Clock.unschedule(self.move_eraser)  # Stop moving the eraser
            Clock.unschedule(self.move_projectile)  # Stop moving the projectile

    def move_eraser(self, dt):
        # Move the eraser and check for collisions
        if self.eraser:
            x, y = self.eraser.pos
            new_x = x + (self.delta_x_eraser * 0.01)
            new_y = y + (self.delta_y_eraser * 0.01)
            self.eraser.pos = (new_x, new_y)
            self.check_collision_with_line()  # Check if eraser intersects with laser lines
            if self.projectile and self.eraser.collide_widget(self.projectile):
                self.remove_widget(self.projectile)  # Remove projectile if collision happens
                self.projectile = None
            self.collsion_eraser_laser()

    def check_collision_with_line(self):
        # Check if eraser collides with any laser lines
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
        # Check if the eraser collides with a laser line
        return (min(x1, x2) < ex + ew and max(x1, x2) > ex and 
                min(y1, y2) < ey + eh and max(y1, y2) > ey)

    def check_reflection(self, flag_collision):
        # Handle laser reflection
        self.reflect_laser(flag_collision)

    def check_reflection_eraser(self, flag_collision):
        # Handle eraser reflection
        self.reflect_eraser(flag_collision)

    def reflect_eraser(self, flag_collision):
        # Reflect the eraser based on collision with mirror
        if not flag_collision:
            mirror_angle = (math.pi)/2  # Reflect at 90 degrees
        else: 
            mirror_angle = 0  # Vertical reflection
        normal_vector = (math.cos(mirror_angle), math.sin(mirror_angle))
        eraser_direction = (self.delta_x_eraser, self.delta_y_eraser)
        dot_product = (eraser_direction[0] * normal_vector[0] + eraser_direction[1] * normal_vector[1])
        reflected_direction = (
            eraser_direction[0] - 2 * dot_product * normal_vector[0],
            eraser_direction[1] - 2 * dot_product * normal_vector[1]
        )
        # Update the direction after reflection
        self.delta_x_eraser, self.delta_y_eraser = reflected_direction

    def reflect_laser(self, flag_collision):
        # Reflect the laser based on collision with mirror
        if not flag_collision:
            mirror_angle = (math.pi)/2  # Reflect at 90 degrees
        else: 
            mirror_angle = 0  # Vertical reflection
        normal_vector = (math.cos(mirror_angle), math.sin(mirror_angle))
        laser_direction = (self.delta_x, self.delta_y)
        dot_product = (laser_direction[0] * normal_vector[0] + laser_direction[1] * normal_vector[1])
        reflected_direction = (
            laser_direction[0] - 2 * dot_product * normal_vector[0],
            laser_direction[1] - 2 * dot_product * normal_vector[1]
        )
        # Update the direction after reflection
        self.delta_x, self.delta_y = reflected_direction

    def use_specific_sound(self):
        # Return sound for laser
        return "sounds/laser.mp3"
