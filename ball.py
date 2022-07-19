import pygame
import commons

from pygame.sprite import Sprite


class Ball(Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("images/ball.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = commons.initial_ball_pos
		self.velocity_x = 0.0
		self.velocity_y = 0.0
		self.initial_size_x, self.initial_size_y = self.image.get_size()

		# Float values of a ball position vector are needed to handle movement.
		self.x = float(self.rect.centerx)
		self.y = float(self.rect.centery)

	def draw(self):
		commons.screen.blit(self.image, self.rect)


class Pointer:
	def __init__(self, ball):
		self.image = pygame.image.load("images/pointer.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect = ball.rect.center


class Indicator:
	def __init__(self):
		self.image = pygame.image.load("images/indicator.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect = -100, -100
		self.image = pygame.transform.scale(self.image, (32, 32))

	def draw(self):
		commons.screen.blit(self.image, self.rect)

	def increase(self, force):
		fill_pos = 30 - (force // 100) * 2
		fill_size = 0 + (force // 100) * 2
		color = (236, 255, 0)

		pigment = pygame.rect.Rect(14, fill_pos, 6, fill_size)
		pygame.draw.rect(self.image, color, pigment)

		if force < 100:
			self.image = pygame.image.load("images/indicator.png").convert_alpha()
			self.image = pygame.transform.scale(self.image, (32, 32))
