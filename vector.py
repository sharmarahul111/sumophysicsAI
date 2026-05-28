import math
class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other: Vector) -> Vector:
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other: Vector) -> Vector:
		return Vector(self.x - other.x, self.y - other.y)

	def __iadd__(self, other: Vector) -> Vector:
		self.x += other.x
		self.y += other.y
		return self

	def __isub__(self, other: Vector) -> Vector:
		self.x -= other.x
		self.y -= other.y
		return self

	def mag(self):
		return math.sqrt(self.x**2 + self.y**2)

	def unit(self):
		if self.mag() == 0:
			return Vector(0,0)
		else:
			return Vector(self.x/self.mag(), self.y/self.mag())

	def normal(self):
		return Vector(-self.y, self.x).unit()
	
	def __mul__(self, scalar):
		if isinstance(scalar, (int, float)):
			return Vector(self.x * scalar, self.y * scalar)

		return NotImplemented

	def __imul__(self, scalar):
		if isinstance(scalar, (int, float)):
			self.x *= scalar
			self.y *= scalar
			return self

		return NotImplemented

	def __rmul__(self, scalar):
		return self.__mul__(scalar)

	@staticmethod
	def dot(v1: Vector, v2: Vector) -> float:
		return v1.x * v2.x + v1.y * v2.y