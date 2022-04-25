import pygame
import commons
import sys
import vectors

from ball import Ball, Pointer


def calc_velocity(mouse_pos):
	"""Set initial ball speed using math functions."""
	initial_pos = ball.rect.center
	diff = vectors.calc_difference(initial_pos, mouse_pos)
	normalized_direction = vectors.normalize_vector(diff)

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


def update():
	check_screen_collisions()


def draw():
	commons.screen.fill(commons.bg_color)

	handle_pointer_movement()
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
pointer = Pointer(ball)
move = False
force = 0
increase_force = False
angle = 0

# The main loop for the game.
while app_running:

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
	# print(force)

	update()
	draw()

	clock.tick(commons.fps)

pygame.quit()
sys.exit()
