import arcade
arcade.open_window(500, 500, "drawing clouds")
arcade.set_background_color(arcade.csscolor.GREEN)
arcade.start_render()

def draw_ground():
    arcade.draw_rectangle_filled(300, 50, 600, 100, arcade.csscolor.BROWN)

def draw_cloud(x, y):
    """Draw ugly little cloud."""
    arcade.draw_circle_filled(x, y, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x, y, 5, arcade.csscolor.PURPLE)
    arcade.draw_circle_filled(x + 5, y, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x + 5, y, 5, arcade.csscolor.PURPLE)
    arcade.draw_circle_filled(x - 5, y, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x - 5, y, 5, arcade.csscolor.PURPLE)
    arcade.draw_circle_filled(x, y + 5, 10, arcade.csscolor.SALMON)
    arcade.draw_circle_filled(x, y + 5, 5, arcade.csscolor.PURPLE)

def draw_bird(x, y):
    """Draw ugly little bird."""
    arcade.draw_rectangle_filled(x, y, 10, 5, arcade.csscolor.BLACK)
    arcade.draw_circle_filled(x + 5, y, 3, arcade.csscolor.WHITE)

def draw_house(x, y):
    """Draw cute little house."""
    arcade.draw_rectangle_filled(x, y, 10, 10, arcade.csscolor.YELLOW)
    arcade.draw_rectangle_filled(x, y + 5, 14, 2, arcade.csscolor.RED)

def main():
    draw_ground()
    draw_cloud(400, 400)
    draw_cloud(100, 300)
    draw_bird(150, 400)
    draw_bird(350, 400)
    draw_house(100, 100)
    draw_house(300, 100)
    arcade.finish_render()
    arcade.run()

main()

