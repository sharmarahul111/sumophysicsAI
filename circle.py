from settings import *
from vector import Vector
class Circle:
	def __init__(self, x, y, radius, color):
		self.pos = Vector(x, y)
		self.radius = radius
		self.color = color
		self.border = .05

	def draw(self, index=None):
		draw_circle(int(self.pos.x), int(self.pos.y), self.radius, BLACK)
		draw_circle(int(self.pos.x), int(self.pos.y), self.radius*(1-self.border), self.color)
		if index is not None:
			text = f"{index}"
			font_size = 25
			width = measure_text(text, font_size)
			draw_text(text, int(self.pos.x-width/2), int(self.pos.y-font_size/2), font_size, BLACK)