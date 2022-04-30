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


class Gui:
	def __init__(self):
		self.image = pygame.image.load('images/gui.png').convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = 0, commons.screen_height - 75

	def draw(self):
		self.image = pygame.image.load('images/gui.png').convert()
		bigger_font = pygame.font.SysFont('Comic Sans MS', 32)
		level_text = bigger_font.render("Level: " + str(commons.level) + "/6",
		                                False, "white")

		smaller_font = pygame.font.SysFont('Comic Sans MS', 24)
		strokes_text = smaller_font.render("Strokes: " + str(commons.strokes),
		                                   False, "white")
		points_text = smaller_font.render("Points: " + str(round(commons.points)),
		                                  False, "white")

		self.image.blit(points_text, (600, 20))
		self.image.blit(strokes_text, (50, 20))
		self.image.blit(level_text, (self.rect.centerx - 100, 15))
		commons.screen.blit(self.image, self.rect)
