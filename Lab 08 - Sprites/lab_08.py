import random
import arcade
import math

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_HEALTH = 1
SPRITE_SCALING_NOT_HEALTH = 1
HEALTH_COUNT = 50
NOT_HEALTH_COUNT = 25

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
rock_sound = arcade.load_sound("../Lab 08 - Sprites/arcade_resources_sounds_rockHit2.wav")
hurt_sound = arcade.load_sound("../Lab 09 - Sprites and Walls/arcade_resources_sounds_hurt4.wav")

class Health(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1

class Not_health(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.circle_angle = 0

        self.circle_radius = 0

        self.circle_speed = 0.02

        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):

        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
                        + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
                        + self.circle_center_y

        self.circle_angle += self.circle_speed


class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites Lab")

        self.player_list = None
        self.health_list = None

        self.player_sprite = None
        self.score = 0

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.RED)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.not_health_list = arcade.SpriteList()

        self.hurt_sound = arcade.load_sound("../Lab 09 - Sprites and Walls/arcade_resources_sounds_hurt4.wav")
        self.rock_sound = arcade.load_sound("../Lab 08 - Sprites/arcade_resources_sounds_rockHit2.wav")

        self.score = 0

        self.player_sprite = arcade.Sprite("../Lab 09 - Sprites and Walls/slimeBlue_move.png", SPRITE_SCALING_PLAYER)

        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 80
        self.player_list.append(self.player_sprite)

        for i in range(HEALTH_COUNT):

            health = Health("../Lab 09 - Sprites and Walls/tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)
            health.change_x = random.randrange(-3, 4)
            health.change_y = random.randrange(-3, 4)

            self.health_list.append(health)

        for i in range(NOT_HEALTH_COUNT):
            not_health = Not_health("tankRed_barrel2.png", SPRITE_SCALING_NOT_HEALTH)

            # Position the center of the circle the coin will orbit
            not_health.circle_center_x = random.randrange(SCREEN_WIDTH)
            not_health.circle_center_y = random.randrange(SCREEN_HEIGHT)

            # Random radius from 10 to 200
            not_health.circle_radius = random.randrange(10, 200)

            # Random start angle from 0 to 2pi
            not_health.circle_angle = random.random() * 2 * math.pi

            # Add the coin to the lists
            self.not_health_list.append(not_health)

        arcade.set_background_color(arcade.color.PEARL_AQUA)

    def on_draw(self):

        arcade.start_render()

        self.health_list.draw()
        self.player_list.draw()
        self.not_health_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.BLACK, 14)

        if len(self.health_list) == 0:
            arcade.draw_text("GAME OVER", 200, 300, arcade.color.BLACK, 50)


    def on_mouse_motion(self, x, y, dx, dy):
        if len(self.health_list) > 0:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y

    def update(self, delta_time):

        if len(self.health_list) > 0:
            self.health_list.update()
            self.not_health_list.update()

            health_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                  self.health_list)
            not_health_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                      self.not_health_list)

            for health in health_up_list:
                health.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.hurt_sound)


            for not_health in not_health_up_list:
                not_health.remove_from_sprite_lists()
                self.score -= 1
                arcade.play_sound(self.rock_sound)

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()