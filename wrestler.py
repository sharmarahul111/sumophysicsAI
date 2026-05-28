from settings import *
from circle import Circle
from vector import Vector

class Wrestler(Circle):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius, YELLOW)
		self.vel = Vector(0, 0)
		self.acc = Vector(0, 0)
		self.border = .1 # drawing border
		self.accelaration = 1
		self.friction = .1
		self.keys = [0,0,0,0] # left/right/up/down

	def control(self):
		if is_key_down(KEY_LEFT):
			self.keys[0] = -1
		else:
			self.keys[0] = 0

		if is_key_down(KEY_RIGHT):
			self.keys[1] = 1
		else:
			self.keys[1] = 0

		if is_key_down(KEY_UP):
			self.keys[2] = -1
		else:
			self.keys[2] = 0

		if is_key_down(KEY_DOWN):
			self.keys[3] = 1
		else:
			self.keys[3] = 0


	def update(self):
		self.control() # get controls
		self.acc.x = self.keys[0] + self.keys[1]
		self.acc.y = self.keys[2] + self.keys[3]
		self.vel += self.acc
		self.vel *= 1-self.friction
		self.pos += self.vel

class DummyWrestler(Wrestler):
	def control(self):
		pass
def check_collision(w1: Wrestler, w2: Wrestler):
	dist = (w1.pos - w2.pos).mag()
	if w1.radius + w2.radius > dist:
		return True

def resolve_penetration(w1: Wrestler, w2: Wrestler):
	dist = (w1.pos - w2.pos)
	penetration_depth = w1.radius + w2.radius - dist.mag()
	penetration_resolution = dist.unit()*(penetration_depth/2)
	w1.pos += penetration_resolution
	w2.pos -= penetration_resolution
