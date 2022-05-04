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


class Menu:
	"""A class to display game menu."""
	def __init__(self):
		self.image = pygame.Surface([300, 400], pygame.SRCALPHA)
		self.rect = self.image.get_rect()
		self.rect.topleft = 250, 50
		self.image.fill((0, 0, 0, 180))

		self.button_restart = pygame.Rect(290, 160, 225, 40)
		self.button_h2p = pygame.Rect(290, 230, 225, 40)
		self.button_exit = pygame.Rect(290, 300, 225, 40)
		self.button_back = pygame.Rect(-100, -100, 225, 40)

		self.default_color = (2, 17, 0)
		self.hover_color = (10, 105, 0)
		self.buttons = [(self.button_restart, self.default_color),
		                (self.button_h2p, self.default_color),
		                (self.button_exit, self.default_color),
		                (self.button_back, self.default_color)]
		self.button_font = pygame.font.SysFont('Comic Sans MS', 24)

	def draw(self):
		self.draw_heading()
		commons.screen.blit(self.image, self.rect)

		pygame.draw.rect(commons.screen, self.buttons[0][1], self.buttons[0][0])
		pygame.draw.rect(commons.screen, self.buttons[1][1], self.buttons[1][0])
		pygame.draw.rect(commons.screen, self.buttons[2][1], self.buttons[2][0])

		button_restart_text = self.button_font.render("Start", False, "white")
		button_h2p_text = self.button_font.render("How To Play", False, "white")
		button_exit_text = self.button_font.render("Exit", False, "white")
		heading2_font = pygame.font.SysFont('Arial Bold', 32)
		continue_text = heading2_font.render("Press ESC to resume", True, "white")
		commons.screen.blit(button_restart_text, (367, 163))
		commons.screen.blit(button_h2p_text, (340, 233))
		commons.screen.blit(button_exit_text, (375, 303))
		commons.screen.blit(continue_text, (290, 390))

	def draw_heading(self):
		heading_font = pygame.font.SysFont('Arial Bold', 48)
		heading_text = heading_font.render("MINI-GOLF", True, "white")
		author_font = pygame.font.SysFont('Arial', 16)
		author_text = author_font.render("by martindustry", True, "white")

		self.image.blit(heading_text, (60, 25))
		self.image.blit(author_text, (100, 55))

	def hover_button(self, mouse_pos):
		"""Handle hover by changing proper button color and mouse cursor."""
		collide = [False for _ in range(len(self.buttons))]

		for index, (rect, color) in enumerate(self.buttons):
			if rect.collidepoint(mouse_pos):
				self.buttons[index] = (rect, self.hover_color)
				collide[index] = True
			else:
				self.buttons[index] = (rect, self.default_color)

		if any(collide):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class HowToPlayMenu(Menu):
	def __init__(self):
		super().__init__()

		self.button_back = pygame.Rect(-100, -100, 225, 40)
		self.buttons = [(self.button_back, self.default_color)]

	def draw(self):
		self.draw_heading()
		commons.screen.blit(self.image, self.rect)

		h2p_menu_font = pygame.font.SysFont('Arial', 24)
		pointer_text = h2p_menu_font.render("Use        to navigate the ball",
		                                    True, "white")
		pointer = pygame.image.load('images/pointer.png').convert_alpha()
		commons.screen.blit(pointer_text, (270, 170))
		commons.screen.blit(pointer, (318, 177))
		lmb_text = h2p_menu_font.render("Hold          to shoot", True,
		                                "white")
		lmb = pygame.image.load('images/mouse.png').convert_alpha()
		commons.screen.blit(lmb_text, (270, 230))
		commons.screen.blit(lmb, (320, 230))
		spacebar_text = h2p_menu_font.render(
			"Press         to reset ball position",
			True, "white")
		spacebar = pygame.image.load('images/spacebar.png').convert_alpha()
		spacebar = pygame.transform.scale(spacebar, (32, 32))
		commons.screen.blit(spacebar_text, (270, 290))
		commons.screen.blit(spacebar, (328, 282))
		button_back_font = pygame.font.SysFont('Comic Sans MS', 24)
		button_back_text = button_back_font.render("<- Back", False,
		                                           "white")

		self.button_back.topleft = 290, 375
		pygame.draw.rect(commons.screen, self.buttons[0][1],
		                 self.buttons[0][0])
		commons.screen.blit(button_back_text, (358, 376))


class EndScreen(Menu):
	"""A class to draw end game menu after finish the last level."""
	def __init__(self):
		super().__init__()

		self.button_restart = pygame.Rect(270, 370, 170, 40)
		self.button_exit = pygame.Rect(455, 370, 80, 40)
		self.buttons = [(self.button_restart, self.default_color),
		                (self.button_exit, self.default_color)]

	def draw(self):
		commons.screen.blit(self.image, self.rect)
		pygame.draw.rect(commons.screen, self.buttons[0][1], self.buttons[0][0])
		pygame.draw.rect(commons.screen, self.buttons[1][1], self.buttons[1][0])

		try_again_text = self.button_font.render("Try again", False, "white")
		exit_text = self.button_font.render("Exit", False, "white")

		commons.screen.blit(try_again_text, (300, 373))
		commons.screen.blit(exit_text, (470, 371))

		stats_font = pygame.font.SysFont('DejaVu Sans Mono', 24)
		stats = [
			('HOLE', '1', '2', '3', '4', '5', '6'),
			('PAR', str(commons.pars[0]), str(commons.pars[1]), str(commons.pars[2]),
			 str(commons.pars[3]), str(commons.pars[4]), str(commons.pars[5])),
			('STROKE', str(commons.level_strokes[0]), str(commons.level_strokes[1]),
			 str(commons.level_strokes[2]), str(commons.level_strokes[3]),
			 str(commons.level_strokes[4]), str(commons.level_strokes[5]))
		]

		# Draw stats table
		width = 6
		y = 80
		for i in range(7):
			stats_table = stats_font.render(
				("{} {} {}".format(stats[0][i].center(width),
				                   stats[1][i].center(width),
				                   stats[2][i].center(width))),
				False, "white")
			commons.screen.blit(stats_table, (255, y))
			y += 32

		divider = pygame.Rect(270, 310, 260, 1)
		pygame.draw.rect(commons.screen, "white", divider)

		points_str = str(int(commons.points))
		score_text = stats_font.render("SCORE: " + points_str, False, "white")

		# Reduce x value so that the number of points fit to the menu border
		commons.screen.blit(score_text, (390 - len(points_str)*5, 320))
