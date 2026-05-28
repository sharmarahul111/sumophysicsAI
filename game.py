from settings import *
from circle import Circle
from wrestler import *

class Game(Circle):
	def __init__(self, players: Wrestler):
		# setting up the playground
		x = WINDOW_WIDTH/2
		y = WINDOW_HEIGHT/2
		radius = min(x, y) * .8 # leave some margin for playground
		super().__init__(x, y, radius, BLUE)

		self.players = players
		self.opponent = DummyWrestler(self.pos.x, self.pos.y)
		# i => player1, j => player2
		self.generation = 1
		self.i = 0
		self.timer = 0

		self.players[self.i].pos = self.pos - Vector(100, 0)
		self.opponent.pos = self.pos + Vector(0, 0)

	def next_match(self):
		# setting up players
		if self.i + 1 >= len(self.players):
			self.next_gen()
		else:
			self.i += 1

		self.players[self.i].pos = self.pos - Vector(100, 0)
		self.opponent.pos = self.pos + Vector(0, 0)
		self.players[self.i].vel = Vector(0,0)
		self.players[self.i].acc = Vector(0,0)

		self.opponent.vel = Vector(0,0)
		self.opponent.acc = Vector(0,0)

			


	def update(self):
		i = self.i
		
		self.players[i].opponent = self.opponent
		self.players[i].update()
		self.opponent.update()
		if self.check_gameover():
			self.next_match()

		if check_collision(self.players[i], self.opponent):
			# reward impact
			normal = (self.opponent.pos - self.players[i].pos).unit()
			relative_vel = self.opponent.vel - self.players[i].vel
			impact = Vector.dot(relative_vel, normal)
			self.players[i].score += max(impact, 0) * 2
			self.opponent.score += min(-impact, 0) * 2

			resolve_penetration(self.players[i], self.opponent)
			collision_resolution(self.players[i], self.opponent)
		
		self.timer += 1

	def check_gameover(self):
		i = self.i
		player1_out = (self.pos - self.players[i].pos).mag() > self.radius-self.border - self.players[i].radius
		player2_out = (self.pos - self.opponent.pos).mag() > self.radius-self.border - self.opponent.radius
		if player1_out or player2_out or self.timer % (FPS*2)==0:
			if player2_out and not player1_out:
				self.players[i].score += 1000
			if player1_out and not player2_out:
				self.players[i].score -= 1000

			if self.timer % (FPS*2) == 0:
				self_dist = (self.players[i].pos - self.pos).mag()
				opp_dist = (self.opponent.pos - self.pos).mag()
				if self_dist < opp_dist:
					self.players[i].score += 20
				else:
					self.players[i].score -= 20
					

			self.timer = 0
			return True
		else:
			return False

	def next_gen(self):
		topk: list[AgenticWrestler] = sorted(self.players, key=lambda player: player.score, reverse=True)[:4]
		for top in topk:
			# resetting scores
			top.score = 0
			top.past_champion = True
		self.players = []
		for player in topk:
			self.players += player.mutate(3, diversity=.01)
			# self.players += player.mutate(1, diversity=.2)
			self.players += [AgenticWrestler() for _ in range(1)]
		self.players += topk
		self.generation += 1
		self.i = 0

	def draw(self):
		super().draw()
		self.players[self.i].draw(self.i)
		self.opponent.draw("Op")

	def draw_status(self):
		draw_text(f"Generation: {self.generation}", 20, 20, 20, WHITE)
		draw_text(f"Player Count: {len(self.players)}", 20, 40, 20, WHITE)
		draw_text(f"Player {self.i}", 20, 60, 20, WHITE)
		draw_fps(20,200)
