from settings import *
from wrestler import *
from game import Game

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Single Player Sumo AI")
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

	# stats
	min_score = min(game.players, key=lambda player: player.score).score
	max_score = max(game.players, key=lambda player: player.score).score
	# print(min_score, max_score)
	for i in range(len(game.players)):
		score = game.players[i].score
		if score == min_score:
			draw_text(f"Score {i}: { score: .3f}", WINDOW_WIDTH - 250, i*30+30, 20, RED)
		elif score == max_score:
			draw_text(f"Score {i}: { score: .3f}", WINDOW_WIDTH - 250, i*30+30, 20, GREEN)
		else:
			draw_text(f"Score {i}: { score: .3f}", WINDOW_WIDTH - 250, i*30+30, 20, WHITE)
		if game.players[i].past_champion:
			draw_text("*", WINDOW_WIDTH - 265, i*30+30,25, GREEN)
	end_drawing()

close_window()