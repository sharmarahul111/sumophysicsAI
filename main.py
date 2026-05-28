from pyray import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sumo Physics AI")
while not window_should_close():
	begin_drawing()
	draw_circle(300, 300, 100, YELLOW)
	end_drawing()

close_window()