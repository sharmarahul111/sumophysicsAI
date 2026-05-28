from settings import *
from wrestler import Wrestler
from game import Game

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sumo Physics AI")
set_target_fps(60)

game = Game()
wrestler = Wrestler(300, 400, 50)

while not window_should_close():
	wrestler.update()
	begin_drawing()
	clear_background((55, 55, 55))
	game.draw()
	wrestler.draw()
	end_drawing()

close_window()