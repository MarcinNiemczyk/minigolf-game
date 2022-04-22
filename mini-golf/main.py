import pygame
import commons
import math
import sys

from ball import Ball


def calc_difference(ball_pos, mouse_pos):
	"""Return a vector that is difference between target and initial position."""
	return mouse_pos[0] - ball_pos[0], mouse_pos[1] - ball_pos[1]


def calc_magnitude(vec):
	"""Return length of a vector, indispensable to normalize vector."""
	return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def normalize_vector(vec):
	"""Return a normalized vector with proper x, y ratio and set direction."""
	vec_length = calc_magnitude(vec)

	if vec_length < 0.00001:
		return 0, 1

	return (vec[0] / vec_length), (vec[1] / vec_length)


def calc_velocity(mouse_pos):
	"""Set initial ball speed using math functions."""
	initial_pos = ball.rect.center
	diff = calc_difference(initial_pos, mouse_pos)
	normalized_direction = normalize_vector(diff)

	ball.velocity_x = normalized_direction[0] * force
	ball.velocity_y = normalized_direction[1] * force


def check_screen_collisions():
	if ball.rect.right >= commons.screen_width or ball.rect.left <= 0:
		ball.velocity_x = -ball.velocity_x
	if ball.rect.bottom >= commons.screen_height or ball.rect.top <= 0:
		ball.velocity_y = -ball.velocity_y


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


def update():
	check_screen_collisions()


def draw():
	commons.screen.fill(commons.bg_color)
	if not move:
		pygame.draw.line(commons.screen, "black", ball.rect.center,
		                 mouse_position, 2)

	ball.draw()
	pygame.display.update()


pygame.init()
app_running = True

clock = pygame.time.Clock()
commons.screen = pygame.display.set_mode((commons.screen_width,
                                          commons.screen_height))
pygame.display.set_caption("Mini-Golf")
icon_image = pygame.image.load("images/ball.png").convert_alpha()
pygame.display.set_icon(icon_image)

ball = Ball()
move = False
force = 0
increase_force = False

# The main loop for the game.
while app_running:
	# Create a line that connects user's cursor with the ball.
	mouse_position = pygame.mouse.get_pos()
	line = [ball.rect.center, mouse_position]

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			app_running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == pygame.BUTTON_LEFT:
				force = 0
				if not move:
					increase_force = True

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == pygame.BUTTON_LEFT:
				if not move:
					calc_velocity(pygame.mouse.get_pos())
					move = True
					increase_force = False

	if increase_force:
		force += 10
		if force >= 400:
			force += 10
		if force >= 1500:
			increase_force = False

	if move:
		handle_ball_movement()
	if ball.velocity_x == 0 and ball.velocity_y == 0:
		move = False
	# Position of the ball needs to be updated with float x, y values.
	ball.rect.centerx = ball.x
	ball.rect.centery = ball.y

	# FIXME: Temporary force print.
	print(force)

	update()
	draw()
	clock.tick(commons.fps)

pygame.quit()
sys.exit()
