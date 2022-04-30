import pygame
import commons


class Gui:
	"""A class representing the users interface at the bottom of the screen."""
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
