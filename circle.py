from settings import *
from vector import Vector
class Circle:
	def __init__(self, x, y, radius, color):
		self.pos = Vector(x, y)
		self.radius = radius
		self.color = color
		self.border = .05

	def draw(self):
		draw_circle(int(self.pos.x), int(self.pos.y), self.radius, BLACK)
		draw_circle(int(self.pos.x), int(self.pos.y), self.radius*(1-self.border), self.color)