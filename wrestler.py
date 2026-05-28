from settings import *
from circle import Circle
from vector import Vector
from network import Network
import numpy as np


class Wrestler(Circle):
	def __init__(self, x, y, radius=50):
		super().__init__(x, y, radius, YELLOW)
		self.vel = Vector(0, 0)
		self.acc = Vector(0, 0)
		self.border = .1 # drawing border
		self.score = 0
		self.accelaration = .5
		self.friction = .03
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
		self.acc.x = (self.keys[0] + self.keys[1])*self.accelaration
		self.acc.y = (self.keys[2] + self.keys[3])*self.accelaration
		self.vel += self.acc
		self.vel *= 1-self.friction
		self.pos += self.vel

class DummyWrestler(Wrestler):
	def control(self):
		pass

class AgenticWrestler(Wrestler):
	def __init__(self, x=0, y=0):
		super().__init__(x, y)
		self.network = Network(4, 4 , 4)
		self.opponent: AgenticWrestler = None
		self.thrashold = .5
	
	def control(self):
		x1 = self.pos.x - WINDOW_WIDTH/2
		y1 = self.pos.y - WINDOW_HEIGHT/2
		if self.opponent:
			x2 = self.opponent.pos.x - WINDOW_WIDTH/2
			y2 = self.opponent.pos.y - WINDOW_HEIGHT/2
		else:
			x2 = WINDOW_WIDTH/2
			y2 = WINDOW_HEIGHT/2
		result = self.network.forward(np.array([
			x1, y1, x2, y2
		]))

		self.keys = (result >= self.thrashold).astype(int)

	def mutate(self, copies, diversity):
		agents = []
		for i in range(copies):
			agent = AgenticWrestler()
			agent.network.mutate(diversity)
			agents.append(agent)
		return agents

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

def collision_resolution(w1: Wrestler, w2: Wrestler):
	normal = (w1.pos - w2.pos).unit()
	relative_vel = w1.vel - w2.vel
	# separating velocity - relVel projected onto the collision normal vector
	separating_vel = Vector.dot(relative_vel, normal)
	w1.vel -= normal * separating_vel
	w2.vel += normal * separating_vel
