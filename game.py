from settings import *
from circle import Circle
from wrestler import *
from random import choices

class Game(Circle):
	def __init__(self, players: Wrestler):
		# setting up the playground
		x = WINDOW_WIDTH/2
		y = WINDOW_HEIGHT/2
		radius = min(x, y) * .98 # leave some margin for playground
		super().__init__(x, y, radius, BLUE)

		self.players = players
		self.player1 = None
		self.player2 = None
		self.timer = 0

	def match(self, player1: Wrestler, player2: Wrestler):
		self.player1 = player1
		self.player2 = player2

	def update(self):
		if not (self.player1 and self.player2):
			return
		
		self.player1.update()
		self.player1.update()
		if self.check_gameover():
			pass

		if check_collision(self.player1, self.player2):
			resolve_penetration(self.player1, self.player2)
			collision_resolution(self.player1, self.player2)
		
		self.timer += 1

	def check_gameover(self):
		player1_out = (self.pos - self.player1.pos).mag() > self.radius-self.border - self.player1.radius
		player2_out = (self.pos - self.player2.pos).mag() > self.radius-self.border - self.player2.radius

		if player1_out or player2_out or self.timer % (60*5):
			if player2_out and not player1_out:
				self.player1.score += 10
				self.player2.score -= 10
			if player1_out and not player2_out:
				self.player1.score -= 10
				self.player2.score += 10

			if self.timer % (60*5):
				self.player1.score -= 5
				self.player2.score -= 5


				# setting up next match
				self.timer = 0
				return True
			else:
				return False

	def draw(self):
		super().draw()
		self.player1.draw()
		self.player2.draw()