import arcade

ROW_COUNT = 10
COLUMN_COUNT = 10

WIDTH = 20
HEIGHT = 20

MARGIN = 5

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


class MyGame(arcade.Window):

    def __init__(self, width, height):

        super().__init__(width, height)

        self.grid = []
        for row in range(ROW_COUNT):

            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):

        arcade.start_render()


        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):

                if self.grid[row][column] == 1:
                    color = arcade.color.GREEN
                else:
                    color = arcade.color.WHITE

                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_mouse_press(self, x, y, button, modifiers):

        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        if row < ROW_COUNT and column < COLUMN_COUNT:

            if row < ROW_COUNT and column < COLUMN_COUNT:

                if self.grid[row][column] == 0:
                    self.grid[row][column] = 1
                else:
                    self.grid[row][column] = 0

            if row + 1 < ROW_COUNT:

                if self.grid[row + 1][column] == 0:
                    self.grid[row + 1][column] = 1
                else:
                    self.grid[row + 1][column] = 0

            if row - 1 > 0:
                if self.grid[row - 1][column] == 0:
                    self.grid[row - 1][column] = 1
                else:
                    self.grid[row - 1][column] = 0

            if column - 1 > 0:
                if self.grid[row][column - 1] == 0:
                    self.grid[row][column - 1] = 1
                else:
                    self.grid[row][column - 1] = 0

            if column + 1 < COLUMN_COUNT:
                if self.grid[row][column + 1] == 0:
                    self.grid[row][column + 1] = 1
                else:
                    self.grid[row][column + 1] = 0




def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()