from settings import *
from wrestler import *
from game import Game

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sumo Physics AI")
set_target_fps(60)

game = Game()
wrestler1 = Wrestler(400, 400, 50)
wrestler2 = AgenticWrestler(600, 400, 50)

while not window_should_close():
	wrestler1.update()
	wrestler2.update()
	if check_collision(wrestler1, wrestler2):
		resolve_penetration(wrestler1, wrestler2)
		collision_resolution(wrestler1, wrestler2)
	begin_drawing()
	clear_background((55, 55, 55))
	game.draw()
	wrestler1.draw()
	wrestler2.draw()
	end_drawing()

close_window()