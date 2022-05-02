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
	def __init__(self):
		self.image = pygame.Surface([300, 400], pygame.SRCALPHA)
		self.rect = self.image.get_rect()
		self.rect.topleft = 250, 50
		self.image.fill((0, 0, 0, 180))

		self.button_restart = pygame.Rect(290, 160, 225, 40)
		self.button_h2p = pygame.Rect(290, 230, 225, 40)
		self.button_exit = pygame.Rect(290, 300, 225, 40)
		self.button_back = pygame.Rect(-100, -100, 225, 40)

		default_button_color = (2, 17, 0)
		self.button_restart_fill = default_button_color
		self.button_h2p_fill = default_button_color
		self.button_exit_fill = default_button_color
		self.button_back_fill = default_button_color

		self.h2p_menu = False

	def draw(self):
		heading_font = pygame.font.SysFont('Arial Bold', 48)
		heading_text = heading_font.render("MINI-GOLF", True, "white")
		author_font = pygame.font.SysFont('Arial', 16)
		author_text = author_font.render("by martindustry", True, "white")
		heading2_font = pygame.font.SysFont('Arial Bold', 32)
		continue_text = heading2_font.render("Press ESC to resume", True, "white")

		self.image.blit(heading_text, (60, 25))
		self.image.blit(author_text, (100, 55))

		button_font = pygame.font.SysFont('Comic Sans MS', 24)
		button_restart_text = button_font.render("Start", False, "white")
		button_h2p_text = button_font.render("How To Play", False, "white")
		button_exit_text = button_font.render("Exit", False, "white")

		commons.screen.blit(self.image, self.rect)

		if self.h2p_menu:
			self.button_restart.topleft = -100, -100
			self.button_h2p.topleft = -300, -300
			self.button_exit.topleft = -500, -500

			h2p_menu_font = pygame.font.SysFont('Arial', 24)

			pointer_text = h2p_menu_font.render("Use        to navigate the ball",
			                                    True, "white")
			pointer = pygame.image.load('images/pointer.png').convert_alpha()
			commons.screen.blit(pointer_text, (270, 170))
			commons.screen.blit(pointer, (318, 177))

			lmb_text = h2p_menu_font.render("Hold          to shoot", True, "white")
			lmb = pygame.image.load('images/mouse.png').convert_alpha()
			commons.screen.blit(lmb_text, (270, 230))
			commons.screen.blit(lmb, (320, 230))

			spacebar_text = h2p_menu_font.render("Press         to reset ball position",
			                                     True, "white")
			spacebar = pygame.image.load('images/spacebar.png').convert_alpha()
			spacebar = pygame.transform.scale(spacebar, (32, 32))
			commons.screen.blit(spacebar_text, (270, 290))
			commons.screen.blit(spacebar, (328, 282))

			button_back_font = pygame.font.SysFont('Comic Sans MS', 24)
			button_back_text = button_back_font.render("<- Back", False, "white")
			self.button_back.topleft = 290, 375
			pygame.draw.rect(commons.screen, self.button_back_fill, self.button_back)
			commons.screen.blit(button_back_text, (358, 376))

		else:
			self.button_restart.topleft = 290, 160
			self.button_h2p.topleft = 290, 230
			self.button_exit.topleft = 290, 300

			pygame.draw.rect(commons.screen, self.button_restart_fill,
			                 self.button_restart)
			pygame.draw.rect(commons.screen, self.button_h2p_fill, self.button_h2p)
			pygame.draw.rect(commons.screen, self.button_exit_fill, self.button_exit)
			commons.screen.blit(button_restart_text, (367, 163))
			commons.screen.blit(button_h2p_text, (340, 233))
			commons.screen.blit(button_exit_text, (375, 303))
			commons.screen.blit(continue_text, (290, 390))
			self.button_back.topleft = -100, -100

	def hover_button(self, mouse_pos):
		default_color = (2, 17, 0)
		hover_color = (10, 105, 0)
		if self.button_restart.collidepoint(mouse_pos):
			self.button_restart_fill = hover_color
		else:
			self.button_restart_fill = default_color

		if self.button_h2p.collidepoint(mouse_pos):
			self.button_h2p_fill = hover_color
		else:
			self.button_h2p_fill = default_color

		if self.button_exit.collidepoint(mouse_pos):
			self.button_exit_fill = hover_color
		else:
			self.button_exit_fill = default_color

		if self.button_back.collidepoint(mouse_pos):
			self.button_back_fill = hover_color
		else:
			self.button_back_fill = default_color

		if self.button_restart_fill == hover_color or self.button_h2p_fill == \
				hover_color or self.button_exit_fill == hover_color or \
				self.button_back_fill == hover_color:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

	def handle_button_clicks(self, mouse_pos, restart_game_func):
		if self.button_restart.collidepoint(mouse_pos):
			restart_game_func()
		if self.button_h2p.collidepoint(mouse_pos):
			self.h2p_menu = True
		if self.button_exit.collidepoint(mouse_pos):
			return True
		if self.button_back.collidepoint(mouse_pos):
			self.h2p_menu = False
