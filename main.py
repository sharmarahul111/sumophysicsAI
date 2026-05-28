from settings import *
from wrestler import *
from game import Game

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sumo Physics AI")
set_target_fps(FPS)

players = [AgenticWrestler() for _ in range(5)]

game = Game(players)

while not window_should_close():
	# updating
	game.update()

	# drawing
	begin_drawing()
	clear_background((55, 55, 55))
	game.draw()
	game.draw_status()
	end_drawing()

close_window()