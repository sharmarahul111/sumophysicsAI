from save import load_agents
from settings import *
from circle import Circle
from wrestler import *
from random import random
ARENA_RADIUS = int(min(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)*.96)
class Game(Circle):
	def __init__(self):
		# setting up the playground
		x = WINDOW_WIDTH/2
		y = WINDOW_HEIGHT/2
		radius = ARENA_RADIUS
		super().__init__(x, y, radius, BLUE)

		self.agent: Wrestler = load_agents()
		self.human = Wrestler(self.pos.x, self.pos.y)
		self.human_score = 0
		self.agent_score = 0
		self.human.accelaration = .8
		self.agent.accelaration = .7
		self.human.color = GREEN


	def next_match(self):
		angle = random() * math.pi * 2
		offset = Vector(math.cos(angle), math.sin(angle)) * 100
		self.agent.pos = self.pos - offset
		self.human.pos = self.pos + offset
		self.agent.vel = Vector(0,0)
		self.agent.acc = Vector(0,0)

		self.human.vel = Vector(0,0)
		self.human.acc = Vector(0,0)

			


	def update(self):
		self.agent.opponent = self.human
		self.agent.update()
		self.human.update()
		if self.check_gameover():
			self.next_match()
		if check_collision(self.agent, self.human):
			resolve_penetration(self.agent, self.human)
			collision_resolution(self.agent, self.human)
		

	def check_gameover(self):
		agent_out = (self.pos - self.agent.pos).mag() > self.radius-self.border - self.agent.radius
		human_out = (self.pos - self.human.pos).mag() > self.radius-self.border - self.human.radius
		if agent_out or human_out:
			if agent_out and not human_out:
				self.human_score += 1
			if human_out and not agent_out:
				self.agent_score += 1	
			return True
		else:
			return False

	def draw(self):
		super().draw()
		self.agent.draw("AI")
		self.human.draw("Human")

	def draw_status(self):
		draw_text(f"SCORE", 40, 40, 35, WHITE)
		draw_text(f"HUMAN: {self.human_score}", 40, 80, 25, GREEN)
		draw_text(f"AI: {self.agent_score}", 40, 120, 25, YELLOW)
		draw_fps(20,200)


init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sumo Physics AI VS Human")
set_target_fps(60)

game = Game()

while not window_should_close():
	# updating
	game.update()

	# drawing
	begin_drawing()
	clear_background((55, 55, 55))
	game.draw()
	game.draw_status()
	end_drawing()

close_window()