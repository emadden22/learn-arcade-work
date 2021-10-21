import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 10
rock_sound = arcade.load_sound("arcade_resources_sounds_rockHit2.wav")
hurt_sound = arcade.load_sound("arcade_resources_sounds_hurt4.wav")


def draw_cells(x, y, radius, color):
    """Draw cluster of cells."""
    arcade.draw_circle_filled(x, y, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x, y, 5, arcade.csscolor.PURPLE)
    arcade.draw_circle_filled(x + 5, y, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x + 5, y, 5, arcade.csscolor.PURPLE)
    arcade.draw_circle_filled(x - 5, y, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x - 5, y, 5, arcade.csscolor.PURPLE)
    arcade.draw_circle_filled(x, y + 5, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x, y + 5, 5, arcade.csscolor.PURPLE)

class Cells:
    def __init__(self, position_x, position_y, change_x, change_y, radius, color):

        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

        self.hurt_sound = arcade.load_sound("arcade_resources_sounds_hurt4.wav")


    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x + 5, self.position_y, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x + 5, self.position_y, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x - 5, self.position_y, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x - 5, self.position_y, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x, self.position_y + 5, self.radius, self.color)
        arcade.draw_circle_filled(self.position_x, self.position_y + 5, self.radius, self.color)


    def update(self):

        self.position_y += self.change_y
        self.position_x += self.change_x

        if self.position_x < self.radius:
            self.position_x = self.radius
            arcade.play_sound(self.hurt_sound)

        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius
            arcade.play_sound(self.hurt_sound)

        if self.position_y < self.radius:
            self.position_y = self.radius
            arcade.play_sound(self.hurt_sound)

        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius
            arcade.play_sound(self.hurt_sound)

class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.set_mouse_visible(False)

        self.cells = Cells(50, 50, 0, 0, 15, arcade.csscolor.DARK_SALMON)

        self.rock_sound = arcade.load_sound("arcade_resources_sounds_rockHit2.wav")



    def on_draw(self):

        arcade.start_render()
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.draw_circle_filled(400, 300, 300, arcade.csscolor.RED)
        self.cells.draw()

    def update(self, delta_time):
        self.cells.update()

    def on_mouse_motion(self, x, y, change_x, change_y):
        self.cells.position_y = y
        self.cells.position_x = x

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.cells.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.cells.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.cells.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.cells.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.cells.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.cells.change_y = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            arcade.play_sound(self.rock_sound)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
    arcade.run()


main()