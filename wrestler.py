from settings import *
from circle import Circle
from vector import Vector
from network import Network
import numpy as np
import math


class Wrestler(Circle):
	def __init__(self, x, y, radius=50):
		super().__init__(x, y, radius, YELLOW)
		self.vel = Vector(0, 0)
		self.acc = Vector(0, 0)
		self.border = .1 # drawing border
		self.score = 0
		self.accelaration = 2
		self.friction = .018
		self.keys = [0,0,0,0] # left/right/up/down

	def control(self):
		if is_key_down(KEY_LEFT):
			self.keys[0] = 1
		else:
			self.keys[0] = 0

		if is_key_down(KEY_RIGHT):
			self.keys[1] = 1
		else:
			self.keys[1] = 0

		if is_key_down(KEY_UP):
			self.keys[2] = 1
		else:
			self.keys[2] = 0

		if is_key_down(KEY_DOWN):
			self.keys[3] = 1
		else:
			self.keys[3] = 0


	def update(self):
		self.control() # get controls
		self.acc.x = (self.keys[1] - self.keys[0])*self.accelaration
		self.acc.y = (self.keys[3] - self.keys[2])*self.accelaration
		self.vel += self.acc
		self.vel *= 1-self.friction
		self.pos += self.vel

class DummyWrestler(Wrestler):
	def control(self):
		pass

class AgenticWrestler(Wrestler):
	def __init__(self, x=0, y=0):
		super().__init__(x, y)
		self.network = Network(8, 10 , 2)
		self.opponent: AgenticWrestler = None
		self.past_champion = False
	
	def control(self):
		noise = np.random.normal(0, 0.01, 8)
		x1 = self.pos.x - WINDOW_WIDTH/2
		y1 = self.pos.y - WINDOW_HEIGHT/2
		if self.opponent:
			x2 = self.opponent.pos.x - WINDOW_WIDTH/2
			y2 = self.opponent.pos.y - WINDOW_HEIGHT/2
			vx = self.opponent.vel.x
			vy = self.opponent.vel.y
		else:
			x2 = WINDOW_WIDTH/2
			y2 = WINDOW_HEIGHT/2
			vx, vy = 0, 0

		result = self.network.forward(np.array([
			x1/WINDOW_WIDTH,
			y1/WINDOW_HEIGHT,
			(x2-x1)/WINDOW_WIDTH,
			(y2-y1)/WINDOW_HEIGHT,
			self.vel.x/15,
			self.vel.y/15,
			vx/15,
			vy/15
		] + noise))

		# reward self being closer to center and punish for opponent being closer to center
		center = Vector(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
		self_dist = (self.pos - center).mag()
		opp_dist = (self.opponent.pos - center).mag()
		self.score += (opp_dist - self_dist) * 0.03

		# reward forward pressure
		to_opp = (self.opponent.pos - self.pos).unit()
		pressure = Vector.dot(self.vel, to_opp)
		self.score += pressure * 0.05

		# penalty for spiraling
		tangent = to_opp.normal()
		orbiting = abs(Vector.dot(self.vel, tangent))
		self.score -= orbiting * 0.03
		
		# penalty for idling
		if self.vel.mag() < 0.2:
			self.score -= 0.05

		# penalty for going away from both opponent and center
		

		return result # [ax, ay]

	def update(self):
		[ax, ay] = self.control() # get controls
		self.acc.x = ax * self.accelaration
		self.acc.y = ay * self.accelaration
		self.vel += self.acc
		self.vel *= 1-self.friction
		self.pos += self.vel

		MAX_SPEED = 15

		if self.vel.mag() > MAX_SPEED:
			self.vel = self.vel.unit() * MAX_SPEED

	def mutate(self, copies, diversity):
		agents = []
		for i in range(copies):
			agent = AgenticWrestler()
			agent.network = self.network.mutate(diversity)
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
	impulse = normal * separating_vel

	w1.vel -= impulse
	w2.vel += impulse
