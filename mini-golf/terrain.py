import pygame
import commons


class Hole:
	def __init__(self):
		self.image = pygame.image.load("images/hole.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect()
		self.rect.center = commons.initial_hole_pos

	def draw(self):
		commons.screen.blit(self.image, self.rect)
