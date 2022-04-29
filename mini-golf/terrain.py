import pygame
import commons

from pygame.sprite import Sprite


class Hole:
	def __init__(self):
		self.image = pygame.image.load("images/hole.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect()
		self.rect.center = commons.initial_hole_pos

	def draw(self):
		commons.screen.blit(self.image, self.rect)


class Block(Sprite):
	def __init__(self, pos_x, pos_y, width, height, color="white"):
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.rect = self.image.get_rect()
		self.rect.topleft = pos_x, pos_y
		pygame.draw.rect(self.image, color, (3, 3, width-6, height-6),
		                 border_radius=8)
