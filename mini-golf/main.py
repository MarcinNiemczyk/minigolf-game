import pygame
import commons
import sys
import vectors
import levels

from ball import Ball, Pointer, Indicator
from terrain import Hole
from screen import Gui, Menu, EndScreen, HowToPlayMenu


def calc_velocity(mouse_pos):
	"""Set initial ball speed using math functions."""
	initial_pos = ball.rect.center
	diff = vectors.calc_difference(initial_pos, mouse_pos)
	normalized_direction = vectors.normalize_vector(diff)

	ball.velocity_x = normalized_direction[0] * force
	ball.velocity_y = normalized_direction[1] * force


def check_screen_collisions():
	if ball.velocity_x < 0 and ball.rect.left <= 0:
		handle_bounce_sounds(ball.velocity_x)
		ball.velocity_x = -ball.velocity_x
	if ball.velocity_y < 0 and ball.rect.top <= 0:
		handle_bounce_sounds(ball.velocity_y)
		ball.velocity_y = -ball.velocity_y
	if ball.velocity_x > 0 and ball.rect.right >= commons.screen_width:
		handle_bounce_sounds(ball.velocity_x)
		ball.velocity_x = -ball.velocity_x
	if ball.velocity_y > 0 and ball.rect.bottom >= commons.screen_height - 75:
		handle_bounce_sounds(ball.velocity_y)
		ball.velocity_y = -ball.velocity_y


def check_hole_collision():
	"""Check if the ball collide with the hole field and simulate a fall."""
	global win
	global move
	global play_hole_sound

	# Number 4 is a margin from the hole center that allows to indicate collision.
	if (hole.rect.centerx - 4 < ball.rect.centerx < hole.rect.centerx + 4 and
		  hole.rect.centery - 4 < ball.rect.centery < hole.rect.centery + 4):

		if play_hole_sound:
			hole_pop_sound.play()
			play_hole_sound = False

		# Move the ball towards the center of the hole.
		diff = vectors.calc_difference(ball.rect.center, hole.rect.center)
		move = True
		ball.velocity_x = diff[0]
		ball.velocity_y = diff[1]
		ball.x += ball.velocity_x * 0.4
		ball.y += ball.velocity_y * 0.4
		if ball.rect.center == hole.rect.center:
			ball.velocity_x = 0
			ball.velocity_y = 0

		# Ball falling simulation.
		ball.image = pygame.transform.smoothscale(ball.image,
		                                          (ball.initial_size_x,
		                                           ball.initial_size_y))
		ball.rect = ball.image.get_rect()
		ball.rect.center = hole.rect.centerx - diff[0], hole.rect.centery - diff[1]
		if ball.initial_size_x >= 3 and ball.initial_size_y >= 3:
			ball.initial_size_x -= 0.3
			ball.initial_size_y -= 0.3

	if ball.image.get_size() == (3, 3):
		win = True


def check_block_collision():
	"""Check if terrain blocks collide with the ball."""
	collide_object = pygame.sprite.spritecollide(ball, blocks, False)
	if collide_object:
		# Add 25 pixels margin in case of high velocity
		if (abs(ball.rect.left - collide_object[0].rect.right) < 25 and
			  ball.velocity_x < 0):
			ball.velocity_x = -ball.velocity_x
			handle_bounce_sounds(ball.velocity_x)
		elif (abs(ball.rect.top - collide_object[0].rect.bottom) < 25 and
		      ball.velocity_y < 0):
			ball.velocity_y = -ball.velocity_y
			handle_bounce_sounds(ball.velocity_y)
		elif (abs(ball.rect.right - collide_object[0].rect.left) < 25 and
		      ball.velocity_x > 0):
			ball.velocity_x = -ball.velocity_x
			handle_bounce_sounds(ball.velocity_x)
		elif (abs(ball.rect.bottom - collide_object[0].rect.top) < 25 and
		      ball.velocity_y > 0):
			ball.velocity_y = -ball.velocity_y
			handle_bounce_sounds(ball.velocity_y)


def handle_ball_movement():
	ball.x += ball.velocity_x * commons.delta_time
	ball.y += ball.velocity_y * commons.delta_time

	ball.velocity_x *= commons.friction
	ball.velocity_y *= commons.friction

	# Stop the barely moving ball.
	if 10 > ball.velocity_x >= 0:
		ball.velocity_x = 0
	if -10 < ball.velocity_x <= 0:
		ball.velocity_x = 0
	if 10 > ball.velocity_y >= 0:
		ball.velocity_y = 0
	if -10 < ball.velocity_y <= 0:
		ball.velocity_y = 0


def handle_hit_sounds():
	if 0 < force <= 300:
		hit_sound_4.play()
	elif 300 < force <= 700:
		hit_sound_3.play()
	elif 600 < force <= 1000:
		hit_sound_2.play()
	else:
		hit_sound_1.play()


def handle_bounce_sounds(velocity):
	velocity = abs(velocity)

	if 10 < velocity <= 200:
		hit_sound_4.play()
	elif 200 < velocity <= 500:
		hit_sound_3.play()
	elif 500 < velocity <= 800:
		hit_sound_2.play()
	else:
		hit_sound_1.play()


def handle_pointer_movement():
	"""Rotate the pointer image correct to follow the mouse cursor."""
	if move:
		pointer.rect = 0, 0
	else:
		pointer.rect = ball.rect.center
		mouse_pos = pygame.mouse.get_pos()
		diff = vectors.calc_difference(pointer.rect, mouse_pos)
		angle = vectors.calc_angle(diff) - 45  # Image is drawn in 45 degrees

		w, h = pointer.image.get_size()
		# List elements represent the 4 corner points of the image bounding box.
		box = [(0, 0), (w, 0), (w, -h), (0, -h)]
		box_rotate = [vectors.rotate(p, angle) for p in box]
		min_x = (min(box_rotate, key=lambda p: p[0])[0])
		max_y = (max(box_rotate, key=lambda p: p[1])[1])
		# Move the origin point by difference before and after rotation.
		origin = (pointer.rect[0] + min_x, pointer.rect[1] - max_y)

		rotated_image = pygame.transform.rotate(pointer.image, angle)
		commons.screen.blit(rotated_image, origin)


def handle_button_clicks(mouse_pos):
	global menu
	global game_active
	global sub_menu

	if menu:
		if menu.button_restart.collidepoint(mouse_pos):
			restart_game()
		elif menu.button_exit.collidepoint(mouse_pos):
			game_active = False
		elif menu.button_h2p.collidepoint(mouse_pos):
			sub_menu = HowToPlayMenu()
			menu = None
	if sub_menu:
		if sub_menu.button_back.collidepoint(mouse_pos):
			menu = Menu()
			sub_menu = None
	if end_screen:
		if end_screen.button_restart.collidepoint(mouse_pos):
			restart_game()
		elif end_screen.button_exit.collidepoint(mouse_pos):
			game_active = False


def restart_game():
	global menu
	global end_screen

	reset_stats()
	menu = None
	end_screen = None
	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

	initiate_game_levels()

	reset_ball_position()
	reset_hole_position()


def initiate_game_levels():
	global levels_iter
	global level
	global blocks

	levels_iter = levels.generate_level()
	level = next(levels_iter)
	commons.initial_ball_pos = level.ball_pos
	commons.initial_hole_pos = level.hole_pos
	blocks = level.blocks


def reset_stats():
	commons.level = 1
	commons.strokes = 0
	commons.level_strokes = [0 * i for i in range(6)]
	commons.points = 0


def reset_ball_position():
	global ball
	ball = Ball()


def reset_hole_position():
	global hole
	hole = Hole()


def update():
	check_screen_collisions()
	check_hole_collision()
	check_block_collision()
	if menu:
		menu.hover_button(mouse_xy)
	if sub_menu:
		sub_menu.hover_button(mouse_xy)
	if end_screen:
		end_screen.hover_button(mouse_xy)


def draw():
	commons.screen.fill(commons.bg_color)

	hole.draw()
	ball.draw()
	blocks.draw(commons.screen)
	indicator.draw()
	gui.draw()
	if menu:
		menu.draw()
	if end_screen:
		end_screen.draw()
	if sub_menu:
		sub_menu.draw()
	if not menu and not sub_menu and not end_screen:
		handle_pointer_movement()

	pygame.display.update()


pygame.init()
game_active = True

clock = pygame.time.Clock()
commons.screen = pygame.display.set_mode((commons.screen_width,
                                          commons.screen_height))
pygame.display.set_caption("Mini-Golf")
icon_image = pygame.image.load("images/ball.png").convert_alpha()
pygame.display.set_icon(icon_image)

levels_iter = levels.generate_level()
initiate_game_levels()
ball = Ball()
hole = Hole()
pointer = Pointer(ball)
indicator = Indicator()
gui = Gui()

move = False
force = 0
increase_force = False
win = False
menu = Menu()
end_screen = None
sub_menu = None

hit_sound_1 = pygame.mixer.Sound('sounds/ball_hit_1.ogg')
hit_sound_2 = pygame.mixer.Sound('sounds/ball_hit_2.ogg')
hit_sound_3 = pygame.mixer.Sound('sounds/ball_hit_3.ogg')
hit_sound_4 = pygame.mixer.Sound('sounds/ball_hit_4.ogg')
bounce_sound = pygame.mixer.Sound('sounds/ball_bounce.ogg')
end_sound = pygame.mixer.Sound('sounds/end_sound.ogg')
hole_pop_sound = pygame.mixer.Sound('sounds/hole_pop.ogg')
play_hole_sound = True

# The main loop for the game.
while game_active:
	mouse_xy = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_active = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == pygame.BUTTON_LEFT:
				if not menu and not end_screen and not sub_menu:
					if not move:
						increase_force = True
						indicator.rect = ball.rect.right + 5, ball.rect.top - 5

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == pygame.BUTTON_LEFT:
				if not menu and not end_screen and not sub_menu:
					if not move:
						increase_force = False
						calc_velocity(mouse_xy)
						move = True
						if force > 10:
							commons.level_strokes[commons.level - 1] += 1
							commons.strokes += 1
							handle_hit_sounds()
				else:
					handle_button_clicks(mouse_xy)

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if not menu:
					reset_ball_position()
			if event.key == pygame.K_ESCAPE:
				if not end_screen and not sub_menu:
					if menu:
						menu = None
						pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
					else:
						menu = Menu()

	if increase_force:
		force += 10
		if force >= 50:
			force += 10
		if force >= 500:
			force += 20
		if force >= 1400:
			increase_force = False
	indicator.increase(force)

	if move:
		handle_ball_movement()
		indicator.rect = -100, -100
		force = 0
	if ball.velocity_x == 0 and ball.velocity_y == 0:
		move = False
	# Position of the ball needs to be updated with float x, y values.
	ball.rect.centerx = ball.x
	ball.rect.centery = ball.y

	# Level increments handling
	if win:
		commons.points += (1000 * (commons.level ** 2)) / (
				commons.level_strokes[commons.level - 1] + 1)
		move = False
		try:
			level = next(levels_iter)
			commons.initial_ball_pos = level.ball_pos
			commons.initial_hole_pos = level.hole_pos
			blocks = level.blocks
			commons.level += 1
		except StopIteration:
			menu = None
			sub_menu = None
			end_screen = EndScreen()
			end_sound.play()

		reset_ball_position()
		reset_hole_position()
		ball.initial_size_x, ball.initial_size_y = ball.image.get_size()
		win = False
		play_hole_sound = True

	update()
	draw()
	clock.tick(commons.fps)

pygame.quit()
sys.exit()
