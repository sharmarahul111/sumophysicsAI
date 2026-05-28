from settings import *
class Circle:
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color

	def draw(self):
		draw_circle(int(self.x), int(self.y), self.radius*1.05, BLACK)
		draw_circle(int(self.x), int(self.y), self.radius, self.color)