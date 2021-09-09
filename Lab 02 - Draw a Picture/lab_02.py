import arcade

# Open a window
arcade.open_window(600, 600, "Cell")

arcade.set_background_color(arcade.csscolor.BLACK)

arcade.start_render()

#Draw a field of view
arcade.draw_circle_filled(300, 300, 300, arcade.csscolor.WHITE)

#Draw a cell
arcade.draw_circle_filled(300, 300, 250, arcade.csscolor.BLANCHED_ALMOND)
arcade.draw_circle_filled(300, 300, 245, arcade.csscolor.SALMON)
arcade.draw_circle_filled(300, 300, 240, arcade.csscolor.BLANCHED_ALMOND)

#Draw a nucleus
arcade.draw_circle_filled(265, 395, 75, arcade.csscolor.BLUE)
arcade.draw_circle_outline(265, 395, 70, arcade.csscolor.DARK_VIOLET)
arcade.draw_text("Nucleus", 240, 388, arcade.csscolor.WHITE)

#Draw mitochondria
arcade.draw_rectangle_filled(350, 140, 60, 30, arcade.csscolor.ORANGE_RED)
arcade.draw_arc_filled(325, 130, 17, 15, arcade.csscolor.BLANCHED_ALMOND, 135, 315)
arcade.draw_arc_filled(326, 131, 12, 15, arcade.csscolor.ORANGE_RED, 140, 330)
arcade.draw_circle_filled(360, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(365, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(370, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(375, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(380, 150, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(380, 145, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(380, 140, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(380, 135, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(380, 130, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(380, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(375, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(370, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(365, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(360, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(355, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(350, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(345, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(340, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(335, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(330, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 127, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 130, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 135, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 140, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 145, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 150, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(325, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(355, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(350, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(345, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(340, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(335, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_circle_filled(330, 155, 7, arcade.csscolor.ORANGE_RED)
arcade.draw_text("Mitochondria", 325, 140, arcade.csscolor.WHITE, 7)

#Draw Microtubule

arcade.draw_line(127, 127, 473, 473, arcade.csscolor.DARK_ORANGE)

#Draw Motor Protien

arcade.draw_line(300, 300, 307, 293, arcade.csscolor.BROWN)
arcade.draw_circle_filled(300, 300, 6, arcade.csscolor.BROWN)
arcade.draw_line(307, 293, 299, 278, arcade.csscolor.BROWN)
arcade.draw_circle_filled(310, 270, 20, arcade.csscolor.AQUA)
arcade.draw_text("Vesicle", 298, 270,arcade.csscolor.WHITE, 6)
arcade.finish_render()

arcade.run()
