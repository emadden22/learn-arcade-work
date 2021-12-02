"""

Artwork from https://api.arcade.academy/en/latest/resources.html

"""

import random
import arcade

SPRITE_SCALING = 0.5
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_HEALTH = 1
SPRITE_SCALING_NOT_HEALTH = 1
HEALTH_COUNT = 2
ENEMY_COUNT = 15

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Adventures of the Blob"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7

class Player(arcade.Sprite):

    def __init__(self, filename, scale=0.4):

        super().__init__(filename, scale=0.4)

        self.scale = 0.4


    def update(self):

        self.change_x += self.change_x
        self.change_y += self.change_y

class Enemy(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x += self.change_x
        self.change_y += self.change_y


    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 40:
            self.change_x *= -1

        if self.right > 1480:
            self.change_x *= -1

        if self.bottom < 64:
            self.change_y *= -1

        if self.top > 1920:
            self.change_y *= -1


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.enemy_list = None

        # Set up the player
        self.player_sprite = None

        self.change_x = 0
        self.change_y = 0

        # Physics engine so we don't run into walls.
        self.physics_engine = None

        self.set_mouse_visible(False)

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()

        self.hurt_sound = arcade.load_sound("arcade_resources_sounds_hurt4.wav")

        self.bad_sound = arcade.load_sound("arcade_resources_sounds_rockHit2.wav")

        self.score = 0

        self.lives = 5

        # https://api.arcade.academy/en/latest/resources.html

        # Set up the player
        self.player_sprite = Player("slimeBlue_move.png",
                                           scale=0.4)

        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)

        for x in range(64, 1480, 40):
            for y in range(0, 1930, 175):

                # https://api.arcade.academy/en/latest/resources.html

                if random.randrange(30) > 14:
                    wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        # https://api.arcade.academy/en/latest/resources.html

        for x in range(0, 1550, 64):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = -50
            self.wall_list.append(wall)

        for x in range(0, 1550, 64):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 2000
            self.wall_list.append(wall)

        for y in range(0, 2000, 64):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.center_x = 0
            wall.center_y = y
            self.wall_list.append(wall)

        for y in range(0, 2000, 64):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.center_x = 1535
            wall.center_y = y
            self.wall_list.append(wall)


        for i in range(HEALTH_COUNT):

            # https://api.arcade.academy/en/latest/resources.html

            health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

            health_placed_successfully = False

            # Keep trying until success
            while not health_placed_successfully:
                # Position the coin
                health.center_x = random.randrange(1420)
                health.center_y = random.randrange(1920)

                # See if the coin is hitting a wall
                wall_hit_list = arcade.check_for_collision_with_list(health, self.wall_list)

                # See if the coin is hitting another coin
                health_hit_list = arcade.check_for_collision_with_list(health, self.health_list)

                if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                    # It is!
                    health_placed_successfully = True

            # Add the coin to the lists
            self.health_list.append(health)

        for i in range(ENEMY_COUNT):

            # https://api.arcade.academy/en/latest/resources.html

            enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

            enemy_placed_successfully = False

            # Keep trying until success
            while not enemy_placed_successfully:
                # Position the coin
                enemy.center_x = random.randrange(1420)
                enemy.center_y = random.randrange(1920)
                enemy.change_x = random.randrange(1, 9)

                # See if the coin is hitting a wall
                wall_hit_list = arcade.check_for_collision_with_list(enemy, self.wall_list)

                # See if the coin is hitting another coin
                enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.enemy_list)

                if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                    # It is!
                    enemy_placed_successfully = True

            # Add the coin to the lists
            self.enemy_list.append(enemy)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.PEARL_AQUA)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.health_list.draw()
        self.enemy_list.draw()

        self.camera_gui.use()

        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.BLACK, 14)

        arcade.draw_text(f"Lives: {self.lives}", 10, 50, arcade.color.BLACK, 14)

        if self.lives == 0:
            arcade.draw_text("GAME OVER", 200, 300, arcade.color.BLACK, 50)

        if len(self.health_list) == 0:
            arcade.draw_text("You Win!", 290, 300, arcade.color.AVOCADO, 50)



    def on_key_press(self, key, modifiers):
        if len(self.health_list) <= HEALTH_COUNT and self.lives > 0:
            if key == arcade.key.UP:
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        if len(self.health_list) > 0:
            self.health_list.update()

            health_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                  self.health_list)

            for health in health_up_list:
                health.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.hurt_sound)

        if len(self.enemy_list) > 0:
            self.enemy_list.update()

            enemy_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                  self.enemy_list)

            for enemy in enemy_up_list:
                enemy.remove_from_sprite_lists()
                self.lives -= 1
                arcade.play_sound(self.bad_sound)


        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = self.player_sprite.center_x - self.width / 2, \
            self.player_sprite.center_y - self.height / 2
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()