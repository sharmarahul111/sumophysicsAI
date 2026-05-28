from settings import *
from circle import Circle
from wrestler import *

class Game(Circle):
	def __init__(self, players: Wrestler):
		# setting up the playground
		x = WINDOW_WIDTH/2
		y = WINDOW_HEIGHT/2
		radius = min(x, y) * .98 # leave some margin for playground
		super().__init__(x, y, radius, BLUE)

		self.players = players
		# i => player1, j => player2
		self.generation = 1
		self.i = 0
		self.j = 1
		self.timer = 0

		self.players[self.i].pos = self.pos - Vector(200, 0)
		self.players[self.j].pos = self.pos + Vector(200, 0)

	def next_match(self):
		# setting up players
		if self.i + 2 >= len(self.players) and self.j + 1 >= len(self.players):
			self.next_gen()
		elif self.j + 1 >= len(self.players):
			self.i += 1
			self.j = self.i + 1
		else:
			self.j += 1

		self.players[self.i].pos = self.pos - Vector(200, 0)
		self.players[self.j].pos = self.pos + Vector(200, 0)

			


	def update(self):
		[i,j] = [self.i, self.j]
		if not (self.players[i] and self.players[j]):
			print(len(self.players), i, j)
			raise "Player indices not available"
		
		self.players[i].update()
		self.players[i].opponent = self.players[j]
		self.players[j].update()
		self.players[j].opponent = self.players[i]
		if self.check_gameover():
			self.next_match()

		if check_collision(self.players[i], self.players[j]):
			resolve_penetration(self.players[i], self.players[j])
			collision_resolution(self.players[i], self.players[j])
		
		self.timer += 1

	def check_gameover(self):
		[i,j] = [self.i, self.j]
		player1_out = (self.pos - self.players[i].pos).mag() > self.radius-self.border - self.players[i].radius
		player2_out = (self.pos - self.players[j].pos).mag() > self.radius-self.border - self.players[j].radius
		if player1_out or player2_out or self.timer % (60*10)==0:
			if player2_out and not player1_out:
				self.players[i].score += 10
				self.players[j].score -= 10
			if player1_out and not player2_out:
				self.players[i].score -= 10
				self.players[j].score += 10

			if self.timer % (60*5):
				self.players[i].score -= 5
				self.players[j].score -= 5

			self.timer = 0
			return True
		else:
			return False

	def next_gen(self):
		topk: list[AgenticWrestler] = sorted(self.players, key=lambda player: player.score, reverse=True)[:2]
		self.players = []
		for player in topk:
			self.players += player.mutate(2, diversity=.01)
		self.players += topk
		self.generation += 1
		self.i = 0
		self.j = 1


	def draw(self):
		super().draw()
		self.players[self.i].draw()
		self.players[self.j].draw()

	def draw_status(self):
		draw_text(f"Generation: {self.generation}", 20, 20, 20, WHITE)
		draw_text(f"Player Count: {len(self.players)}", 20, 40, 20, WHITE)
		draw_text(f"Player {self.i} vs {self.j}", 20, 60, 20, WHITE)
