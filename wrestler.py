from settings import *
from circle import Circle
from vector import Vector

class Wrestler(Circle):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius, YELLOW)
		self.vel = Vector(0, 0)
		self.acc = Vector(0, 0)
