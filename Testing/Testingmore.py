def on_mouse_motion(self, x, y, dx, dy):
    self.ball.position_x = x
    self.ball.position_y = y


def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
    print(button)
    if button == arcade.MOUSE_BUTTON_LEFT:
        print("Left button")
    elif button == arcade.MOUSE_BUTTON_RIGHT:
        print("Right button")
