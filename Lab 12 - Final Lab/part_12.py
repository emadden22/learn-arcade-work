"""
Artwork from https://api.arcade.academy/en/latest/resources.html
"""
import random
import arcade
import math

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_HEALTH = 1
SPRITE_SCALING_NOT_HEALTH = 1
HEALTH_COUNT = 2
ENEMY_COUNT = 15
BULLET_SPEED = 6
BOSS_BULLET_SPEED = 5
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Adventures of the Blob"
PLAYER_MOVEMENT_SPEED = 7

class InstructionsView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.PEARL_AQUA)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("The Adventures of the Blob!", self.window.width / 2, self.window.height - 100,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Use the Key-Pad to Move", self.window.width / 2, self.window.height - 175,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Use the Space-Bar to Shoot", self.window.width / 2, self.window.height - 220,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Avoid Enemy Blobs and Their Saws to Stay Alive!",
                         self.window.width / 2, self.window.height - 300,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Pick Up Smaller Blobs to Gain Back Lives!",
                         self.window.width / 2, self.window.height - 340,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Collect Bottles and Kill Enemy Blobs to Win", self.window.width
                         / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 4,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameOverView(arcade.View):
    """ View to show when game is over """

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.PEARL_AQUA)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("The Adventures of the Blob...", self.window.width / 2, self.window.height - 375,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Have Come to an End :/", self.window.width / 2, self.window.height - 450,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Click to Try Again!", self.window.width / 2, self.window.height / 4,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class Player(arcade.Sprite):
    def __init__(self, filename, scale=0.4):
        super().__init__(filename, scale=0.4)
        self.scale = 0.4
        self.textures = []
        texture = arcade.load_texture("slimeBlue_move.png")
        self.textures.append(texture)
        texture = arcade.load_texture("slimeBlue_move.png",
                                      flipped_horizontally=True)
        self.textures.append(texture)
        self.texture = texture

    def update(self):
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

class Enemy(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.change_x += self.change_x
        self.change_y += self.change_y
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 60:
            self.change_x *= -1
        if self.right > 800:
            self.change_x *= -1
        if self.bottom < 64:
            self.change_y *= -1
        if self.top > 730:
            self.change_y *= -1

class Boss(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.change_x += self.change_x
        self.change_y += self.change_y
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 60:
            self.change_x *= -1
        if self.right > 800:
            self.change_x *= -1
        if self.bottom < 64:
            self.change_y *= -1
        if self.top > 730:
            self.change_y *= -1

class Bullet(arcade.Sprite):
    # https://shimejis.xyz/directory/blobs-blob-by-reitanna
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.change_x += self.change_x
        self.change_y += self.change_y
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.player_list = None
        self.wall_list = None
        self.health_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.boss_bullet_list = None
        self.boss_list = None
        self.background = None
        self.aid_list = None

def setup_room_1():
    room = Room()
    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    #room.player_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()
    room.hurt_sound = arcade.load_sound("arcade_resources_sounds_hurt4.wav")
    room.bad_sound = arcade.load_sound("arcade_resources_sounds_rockHit2.wav")
    room.background_music = arcade.load_sound("Cyberpunk Moonlight Sonata.mp3")

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png",
                                 SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up on the right side
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3) or x == 0:
                wall = arcade.Sprite("water.png",
                                     SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 22:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(1):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", 0.2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(2):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    # Load the background image for this level.
    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room


def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png",
                                     SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 20:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,2)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(4):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_3():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 18:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,4)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(6):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 6)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 6)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_4():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 16:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,4)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(8):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 6)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_5():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 16:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,6)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(10):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 6)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_6():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 16:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for i in range(12):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for aid in range(random.randrange(0,6)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 7)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_7():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 16:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,6)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(14):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 7)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_8():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 16:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,6)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(16):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 7)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 7)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_9():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3):
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in range(85, 720, 40):
        for y in range(85, 770, 100):
            # https://api.arcade.academy/en/latest/resources.html
            if random.randrange(30) > 13:
                wall = arcade.Sprite("treeGreen_large.png", SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for aid in range(random.randrange(0,9)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(18):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimeBlock.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_x = random.randrange(1, 7)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", SPRITE_SCALING)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_x = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)

    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

def setup_room_10():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.boss_list = arcade.SpriteList()
    room.wall_list = arcade.SpriteList()
    room.health_list = arcade.SpriteList()
    room.bullet_list = arcade.SpriteList()
    room.enemy_list = arcade.SpriteList()
    room.enemy_bullet_list = arcade.SpriteList()
    room.boss_bullet_list = arcade.SpriteList()
    room.aid_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("water.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 2 and y != SPRITE_SIZE * 3) or x != 0:
                wall = arcade.Sprite("water.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for i in range(HEALTH_COUNT):

        # https://api.arcade.academy/en/latest/resources.html

        health = arcade.Sprite("tankGreen_barrel3.png", SPRITE_SCALING_HEALTH)

        health_placed_successfully = False

        # Keep trying until success
        while not health_placed_successfully:
            # Position the coin
            health.center_x = random.randrange(SCREEN_WIDTH)
            health.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(health, room.wall_list)

            # See if the coin is hitting another coin
            health_hit_list = arcade.check_for_collision_with_list(health, room.health_list)

            if len(wall_hit_list) == 0 and len(health_hit_list) == 0:
                # It is!
                health_placed_successfully = True

        # Add the coin to the lists
        room.health_list.append(health)

    for i in range(0):

        # https://api.arcade.academy/en/latest/resources.html

        enemy = Enemy("slimePurple.png", SPRITE_SCALING)

        enemy_placed_successfully = False

        # Keep trying until success
        while not enemy_placed_successfully:
            # Position the coin
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.change_y = random.randrange(1, 9)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(enemy, room.wall_list)

            # See if the coin is hitting another coin
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, room.enemy_list)

            if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                enemy_placed_successfully = True

        room.enemy_list.append(enemy)

    for aid in range(random.randrange(1,10)):

        # https://api.arcade.academy/en/latest/resources.html

        aid = arcade.Sprite("slimeBlue.png", .2)

        aid_placed_successfully = False

        # Keep trying until success
        while not aid_placed_successfully:
            # Position the coin
            aid.center_x = random.randrange(SCREEN_WIDTH)
            aid.center_y = random.randrange(SCREEN_HEIGHT)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(aid, room.wall_list)

            # See if the coin is hitting another coin
            aid_hit_list = arcade.check_for_collision_with_list(aid, room.aid_list)

            enemy_hit_list = arcade.check_for_collision_with_list(aid, room.enemy_list)

            if len(wall_hit_list) == 0 and len(aid_hit_list) == 0 and len(enemy_hit_list) == 0:
                # It is!
                aid_placed_successfully = True

        # Add the coin to the lists
        room.aid_list.append(aid)

    for i in range(2):

        # https://api.arcade.academy/en/latest/resources.html

        boss = Boss("slimePurple.png", 1.5)

        boss_placed_successfully = False

        # Keep trying until success
        while not boss_placed_successfully:
            # Position the coin
            boss.center_x = random.randrange(400, SCREEN_WIDTH)
            boss.center_y = random.randrange(SCREEN_HEIGHT)
            boss.change_y = random.randrange(2, 5)

            # See if the coin is hitting a wall
            wall_hit_list = arcade.check_for_collision_with_list(boss, room.wall_list)

            # See if the coin is hitting another coin
            boss_hit_list = arcade.check_for_collision_with_list(boss, room.boss_list)

            if len(wall_hit_list) == 0 and len(boss_hit_list) == 0:
                # It is!
                boss_placed_successfully = True

        room.boss_list.append(boss)
    room.background = arcade.set_background_color(arcade.color.PEARL_AQUA)

    return room

class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        self.current_room = 0
        # Sprite lists
        self.rooms = None
        self.player_list = None
        self.wall_list = None
        self.health_list = None
        self.enemy_list = None
        self.boss_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.aid_list = None

        # Set up the player
        self.player_sprite = None

        self.change_x = 0
        self.change_y = 0

        self.frame_count = 0

        # Physics engine so we don't run into walls.
        self.physics_engine = None

        self.window.set_mouse_visible(False)

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
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList()
        self.aid_list = arcade.SpriteList()

        self.hurt_sound = arcade.load_sound("arcade_resources_sounds_hurt4.wav")

        self.bad_sound = arcade.load_sound("arcade_resources_sounds_rockHit2.wav")

        self.kill_sound = arcade.load_sound("arcade_resources_sounds_jump3.wav")

        self.background_music = arcade.load_sound("Cyberpunk Moonlight Sonata.mp3")

        self.score = 0

        self.lives = 35

        self.boss_health = 20

        # https://api.arcade.academy/en/latest/resources.html

        # Set up the player
        self.player_sprite = Player("slimeBlue_move.png", 0.4)

        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.player_list.append(self.player_sprite)
        self.rooms = []

        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        room = setup_room_3()
        self.rooms.append(room)

        room = setup_room_4()
        self.rooms.append(room)

        room = setup_room_5()
        self.rooms.append(room)

        room = setup_room_6()
        self.rooms.append(room)

        room = setup_room_7()
        self.rooms.append(room)

        room = setup_room_8()
        self.rooms.append(room)

        room = setup_room_9()
        self.rooms.append(room)

        room = setup_room_10()
        self.rooms.append(room)


        self.current_room = 0


        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.rooms[self.current_room].wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.PEARL_AQUA)
        #https://opengameart.org/art-search-advanced?keys=&field_art_type_tid%5B%5D=13&sort_by=count&sort_order=DESC
        arcade.play_sound(self.background_music)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        arcade.set_background_color(arcade.color.PEARL_AQUA)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.rooms[self.current_room].health_list.draw()
        self.rooms[self.current_room].enemy_list.draw()
        self.rooms[self.current_room].boss_list.draw()
        self.rooms[self.current_room].boss_bullet_list.draw()
        self.rooms[self.current_room].bullet_list.draw()
        self.rooms[self.current_room].enemy_bullet_list.draw()
        self.rooms[self.current_room].aid_list.draw()

        #self.camera_gui.use()

        arcade.draw_text(f"Score: {self.score}", 10, 10, arcade.color.BLACK, 14)

        arcade.draw_text(f"Lives: {self.lives}", 10, 30, arcade.color.BLACK, 14)

        arcade.draw_text(f"Level: {self.current_room + 1}", 10, 50, arcade.color.BLACK, 14)

        if len(self.rooms[self.current_room].health_list) == 0 \
                and len(self.rooms[self.current_room].enemy_list) == 0\
                and self.current_room < 9:
            arcade.draw_text("Next Room!", 250, 400, arcade.color.AVOCADO, 50)

        if self.current_room == 9 and len(self.rooms[self.current_room].boss_list) == 0:
            arcade.draw_text("Boss Defeated!", SCREEN_WIDTH / 4,
                             SCREEN_HEIGHT / 2, arcade.color.AVOCADO, 50)
            arcade.draw_text("Destroy Remaining Enemies", 55,
                             SCREEN_HEIGHT - 460, arcade.color.AVOCADO, 40)
            arcade.draw_text("Collect Remaining Bottles", 70,
                             SCREEN_HEIGHT - 520, arcade.color.AVOCADO, 40)
            arcade.draw_text("And Win!", 300,
                             SCREEN_HEIGHT - 580, arcade.color.AVOCADO, 40)


    def on_key_press(self, key, modifiers):
        if len(self.rooms[self.current_room].health_list) <= HEALTH_COUNT and self.lives > 0:
            if key == arcade.key.UP:
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            if key == arcade.key.SPACE:
                # Create a bullet
                bullet = Bullet("shime1.png", .2)
                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y
                bullet.change_x = BULLET_SPEED

                # Add the bullet to the appropriate list
                self.rooms[self.current_room].bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.frame_count += 1

        if len(self.rooms[self.current_room].health_list) > 0:
            self.rooms[self.current_room].health_list.update()

            health_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                  self.rooms[self.current_room].health_list)

            for health in health_up_list:
                health.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.hurt_sound)

        if len(self.rooms[self.current_room].aid_list) > 0:
            self.rooms[self.current_room].aid_list.update()

            aid_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                  self.rooms[self.current_room].aid_list)

            for aid in aid_up_list:
                aid.remove_from_sprite_lists()
                self.lives += 1
                arcade.play_sound(self.hurt_sound)

        if len(self.rooms[self.current_room].enemy_list) > 0:
            self.rooms[self.current_room].enemy_list.update()

            enemy_up_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                  self.rooms[self.current_room].enemy_list)

            for enemy in enemy_up_list:
                enemy.remove_from_sprite_lists()
                self.lives -= 1
                arcade.play_sound(self.bad_sound)

        for bullet in self.rooms[self.current_room].bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.rooms[self.current_room].enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.kill_sound)

            if bullet.center_x <= 0:
                bullet.remove_from_sprite_lists()

        for bullet in self.rooms[self.current_room].bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.rooms[self.current_room].boss_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for boss in hit_list:
                self.boss_health -= 1

            if bullet.center_x <= 60:
                bullet.remove_from_sprite_lists()

        for enemy in self.rooms[self.current_room].enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) - 90

            # Shoot every 60 frames change of shooting each frame
            if enemy.center_x == self.player_sprite.center_x or enemy.center_y == self.player_sprite.center_y:
                enemy_bullet = arcade.Sprite("sawHalf.png", scale=0.4)
                enemy_bullet.center_x = start_x
                enemy_bullet.center_y = start_y

                # Angle the bullet sprite
                enemy_bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                enemy_bullet.change_x = math.cos(angle) * BULLET_SPEED
                enemy_bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.rooms[self.current_room].enemy_bullet_list.append(enemy_bullet)

        for enemy_bullet in self.rooms[self.current_room].enemy_bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                            self.rooms[self.current_room].enemy_bullet_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                enemy_bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.lives -= 1
                arcade.play_sound(self.bad_sound)

            if enemy_bullet.center_x <= 40:
                enemy_bullet.remove_from_sprite_lists()

        for boss in self.rooms[self.current_room].boss_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = boss.center_x
            start_y = boss.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)


            if self.frame_count % 65 == 0:
                boss_bullet = arcade.Sprite("saw.png", scale=1)
                boss_bullet.center_x = start_x
                boss_bullet.center_y = start_y

                # Angle the bullet sprite
                boss_bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                boss_bullet.change_x = math.cos(angle) * BOSS_BULLET_SPEED
                boss_bullet.change_y = math.sin(angle) * BOSS_BULLET_SPEED

                self.rooms[self.current_room].boss_bullet_list.append(boss_bullet)

            if self.boss_health == 0:
                boss.remove_from_sprite_lists()

        for boss_bullet in self.rooms[self.current_room].boss_bullet_list:

            # Check this bullet to see if it hit a coin
            boss_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                            self.rooms[self.current_room].boss_bullet_list)

            # If it did, get rid of the bullet
            if len(boss_hit_list) > 0:
                boss_bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for boss in boss_hit_list:
                boss.remove_from_sprite_lists()
                self.lives -= 2
                arcade.play_sound(self.bad_sound)

            if boss_bullet.center_x <= 40:
                boss_bullet.remove_from_sprite_lists()

        if self.lives > 0:
            self.rooms[self.current_room].enemy_bullet_list.update()
            self.rooms[self.current_room].enemy_list.update()
            self.rooms[self.current_room].bullet_list.update()
            self.rooms[self.current_room].boss_bullet_list.update()
            self.rooms[self.current_room].boss_list.update()
            self.player_list.update()
            self.physics_engine.update()

        if self.lives <= 0:
            view = GameOverView()
            self.window.show_view(view)

        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 1:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 2:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 2:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 3:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 3:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 4:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 4:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 5:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 5:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 6:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 6:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 7:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 7:
            self.current_room = 8
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 8:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH

        elif self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 8:
            self.current_room = 9
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 9:
            self.current_room = 8
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionsView()
    window.show_view(start_view)
    arcade.run()

main()