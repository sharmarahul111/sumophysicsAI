from settings import *
from circle import Circle

class Wrestler(Circle):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius, YELLOW)
