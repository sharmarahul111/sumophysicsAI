from settings import *
from wrestler import *
from game import Game

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sumo Physics AI")
set_target_fps(60)

players = [AgenticWrestler() for _ in range(100)]

game = Game(players)

while not window_should_close():
	# updating
	game.update()

	# drawing
	begin_drawing()
	clear_background((55, 55, 55))
	game.draw()
	end_drawing()

close_window()