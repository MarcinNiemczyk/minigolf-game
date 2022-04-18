import pygame


class Ball:
	def __init__(self, main):
		self.screen = main.screen
		self.settings = main.settings
		self.screen_rect = self.screen.get_rect()

		self.image = pygame.image.load('images/ball.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,
		                                    (self.settings.ball_size,
		                                     self.settings.ball_size))
		self.pos = self.image.get_rect()
		self.pos.center = self.screen_rect.center
		self.y = float(self.pos.y)

	def update(self, end_x, end_y):
		end_x = end_x - self.settings.ball_size // 2
		end_y = end_y - self.settings.ball_size // 2
		if self.pos.x > end_x:
			self.pos.x -= 1
		elif self.pos.x < end_x:
			self.pos.x += 1

		if self.pos.y > end_y:
			self.pos.y -= 1
		elif self.pos.y < end_y:
			self.pos.y += 1


	def draw(self):
		self.screen.blit(self.image, self.pos)
