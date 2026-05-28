from settings import *
from circle import Circle
class Game(Circle):
	def __init__(self):
		# setting up the playground
		x = WINDOW_WIDTH/2
		y = WINDOW_HEIGHT/2
		radius = min(x, y) * .98 # leave some margin for playground
		color = BLUE
		super().__init__(x, y, radius, color)