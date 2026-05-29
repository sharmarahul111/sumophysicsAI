from settings import *
from circle import Circle
from wrestler import *
from random import random

class Game(Circle):
	def __init__(self, players: Wrestler):
		# setting up the playground
		x = WINDOW_WIDTH/2
		y = WINDOW_HEIGHT/2
		radius = ARENA_RADIUS
		super().__init__(x, y, radius, BLUE)

		self.players = players
		# i => player1, j => player2
		self.generation = 1
		self.i = 0
		self.j = 1
		self.timer = 0

		self.players[self.i].pos = self.pos - Vector(100, 0)
		self.players[self.j].pos = self.pos + Vector(100, 0)

	def next_match(self):
		# setting up players
		if self.i + 2 >= len(self.players) and self.j + 1 >= len(self.players):
			self.next_gen()
		elif self.j + 1 >= len(self.players):
			self.i += 1
			self.j = self.i + 1
		else:
			self.j += 1

		angle = random() * math.pi * 2
		offset = Vector(math.cos(angle), math.sin(angle)) * 100
		self.players[self.i].pos = self.pos - offset
		self.players[self.j].pos = self.pos + offset
		self.players[self.i].vel = Vector(0,0)
		self.players[self.i].acc = Vector(0,0)

		self.players[self.j].vel = Vector(0,0)
		self.players[self.j].acc = Vector(0,0)

			


	def update(self):
		if not (self.players[self.i] and self.players[self.j]):
			print(len(self.players), i, j)
			raise "Player indices not available"
		
		self.players[self.i].opponent = self.players[self.j]
		self.players[self.j].opponent = self.players[self.i]
		self.players[self.i].update()
		self.players[self.j].update()
		if self.check_gameover():
			self.next_match()
		print(len(self.players), self.i, self.j, i, j)
		if check_collision(self.players[self.i], self.players[self.j]):
			# reward impact
			normal = (self.players[self.j].pos - self.players[self.i].pos).unit()
			relative_vel = self.players[self.j].vel - self.players[self.i].vel
			impact = Vector.dot(relative_vel, normal)
			self.players[self.i].score += max(impact, 0) * 2
			self.players[self.j].score += min(-impact, 0) * 2

			resolve_penetration(self.players[self.i], self.players[self.j])
			collision_resolution(self.players[self.i], self.players[self.j])
		
		# survival tax
		self.players[self.i].score -= 0.01
		self.players[self.j].score -= 0.01
		self.timer += 1

	def check_gameover(self):
		player1_out = (self.pos - self.players[self.i].pos).mag() > self.radius-self.border - self.players[self.i].radius
		player2_out = (self.pos - self.players[self.j].pos).mag() > self.radius-self.border - self.players[self.j].radius
		if player1_out or player2_out or self.timer >= FPS*2:
			if player2_out and not player1_out:
				self.players[self.i].score += 2500
				self.players[self.j].score -= 2500
			if player1_out and not player2_out:
				self.players[self.i].score -= 2500
				self.players[self.j].score += 2500

			if self.timer >= (FPS*2):
				self_dist = (self.players[self.i].pos - self.pos).mag()
				opp_dist = (self.players[self.j].pos - self.pos).mag()
				if self_dist < opp_dist:
					self.players[self.i].score += 500
					self.players[self.j].score -= 500
				else:
					self.players[self.i].score -= 500
					self.players[self.j].score += 500
					

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
		diversity = max(0.2 * (0.99 ** self.generation), 0.01)
		for player in topk:
			self.players += player.mutate(3, diversity=diversity)
			# self.players += player.mutate(1, diversity=.2)
			self.players += [AgenticWrestler() for _ in range(1)]
		self.players += topk
		self.generation += 1
		self.i = 0
		self.j = 1


	def draw(self):
		super().draw()
		self.players[self.i].draw(self.i)
		self.players[self.j].draw(self.j)

	def draw_status(self):
		draw_text(f"Generation: {self.generation}", 20, 20, 20, WHITE)
		draw_text(f"Player Count: {len(self.players)}", 20, 40, 20, WHITE)
		draw_text(f"Player {self.i} vs {self.j}", 20, 60, 20, WHITE)
		draw_fps(20,200)
