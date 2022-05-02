import pygame
from terrain import Block


class Level1:
	def __init__(self):
		self.ball_pos = 100, 260
		self.hole_pos = 700, 260
		self.blocks = pygame.sprite.Group()


class Level2(Level1):
	def __init__(self):
		super().__init__()
		block1 = Block(150, 225, 75, 75)
		block2 = Block(350, 225, 75, 75)
		block3 = Block(550, 225, 75, 75)
		self.blocks.add(block1, block2, block3)


class Level3(Level1):
	def __init__(self):
		super().__init__()
		block1 = Block(350, 25, 75, 75)
		block2 = Block(350, 425, 75, 75)
		block3 = Block(500, 225, 75, 75)
		self.blocks.add(block1, block2, block3)


class Level4(Level1):
	def __init__(self):
		super().__init__()
		self.ball_pos = 50, 475
		self.hole_pos = 720, 475
		block1 = Block(350, 25, 75, 75)
		block2 = Block(550, 425, 100, 100)
		block3 = Block(150, 150, 50, 50)
		block4 = Block(550, 75, 50, 50)
		block5 = Block(675, 200, 50, 50)
		block6 = Block(650, 325, 50, 50)
		block7 = Block(200, 425, 50, 50)
		self.blocks.add(block1, block2, block3, block4, block5, block6, block7)


class Level5(Level1):
	def __init__(self):
		super().__init__()
		self.ball_pos = 50, 50
		self.hole_pos = 750, 50
		block1 = Block(100, 0, 100, 425)
		block2 = Block(350, 100, 100, 425)
		block3 = Block(600, 0, 100, 425)
		self.blocks.add(block1, block2, block3)


class Level6(Level1):
	def __init__(self):
		super().__init__()
		self.ball_pos = 50, 50
		self.hole_pos = 700, 50
		block1 = Block(500, 0, 100, 425)
		block2 = Block(150, 150, 75, 75)
		block3 = Block(85, 400, 50, 50)
		block4 = Block(375, 100, 50, 50)
		block5 = Block(625, 350, 50, 50)
		block6 = Block(725, 225, 50, 50)
		block7 = Block(625, 125, 50, 50)
		self.blocks.add(block1, block2, block3, block4, block5, block6, block7)


def generate_level():
	yield Level1()
	yield Level2()
	yield Level3()
	yield Level4()
	yield Level5()
	yield Level6()
