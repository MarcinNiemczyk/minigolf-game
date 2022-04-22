import pygame
import commons


class Ball:
	def __init__(self):
		self.image = pygame.image.load("images/ball.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = commons.initial_ball_pos
		self.velocity_x = 0.0
		self.velocity_y = 0.0

		# Float values of a ball position vector are needed to handle movement.
		self.x = float(self.rect.centerx)
		self.y = float(self.rect.centery)

	def draw(self):
		commons.screen.blit(self.image, self.rect)
