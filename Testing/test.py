import random
import arcade

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_HEALTH = 0.2
HEALTH_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



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

        self.score = 0

        self.player_sprite = arcade.Sprite("slimeBlue_move.png)"), SPRITE_SCALING_PLAYER
        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 80
        self.player_list.append(self.player_sprite)

        for i in range(HEALTH_COUNT):


            health = arcade.Sprite("tankGreen_barrel3.png"), SPRITE_SCALING_HEALTH

            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(150, SCREEN_HEIGHT)

            # Add the coin to the lists
            self.health_list.append(health)

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):

        arcade.start_render()

        self.health_list.draw()
        self.player_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.BLACK, 14)

    def on_mouse_motion(self, x, y, dx, dy):

        self.player_sprite.center_x = x

    def update(self, delta_time):

        self.health_list.update()

        health_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.health_list)

        for health in health_up_list:
            health.remove_from_sprite_lists()
            self.score += 1

def main():

    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
