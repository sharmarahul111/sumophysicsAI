from settings import *
class Wrestler:
	def __init__(self, x, y, radius):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = YELLOW

	def draw(self):
		draw_circle(int(self.x), int(self.y), self.radius, self.color)