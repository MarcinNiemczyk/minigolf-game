import pygame
import commons
import sys
import vectors

from ball import Ball, Pointer, Indicator
from terrain import Hole, Block, Gui


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
	if ball.rect.bottom >= commons.screen_height - 75 or ball.rect.top <= 0:
		ball.velocity_y = -ball.velocity_y


def check_hole_collision():
	"""Check if the ball collide with the hole field and simulate a fall."""
	global win
	global move

	# Number 4 is a margin from the hole center that allows to indicate collision.
	if hole.rect.centerx - 4 < ball.rect.centerx < hole.rect.centerx + 4 and \
			hole.rect.centery - 4 < ball.rect.centery < hole.rect.centery + 4:

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
	collide_object = pygame.sprite.spritecollide(ball, blocks, False)
	if collide_object:
		if collide_object[0].rect.collidepoint(ball.rect.midleft):
			ball.velocity_x = -ball.velocity_x
		if collide_object[0].rect.collidepoint(ball.rect.midright):
			ball.velocity_x = -ball.velocity_x
		if collide_object[0].rect.collidepoint(ball.rect.midtop):
			ball.velocity_y = -ball.velocity_y
		if collide_object[0].rect.collidepoint(ball.rect.midbottom):
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
	check_hole_collision()
	check_block_collision()


def draw():
	commons.screen.fill(commons.bg_color)

	hole.draw()
	ball.draw()
	blocks.draw(commons.screen)
	indicator.draw()
	handle_pointer_movement()
	gui.draw()

	pygame.display.update()


pygame.init()
app_running = True

clock = pygame.time.Clock()
commons.screen = pygame.display.set_mode((commons.screen_width,
                                          commons.screen_height))
pygame.display.set_caption("Mini-Golf")
icon_image = pygame.image.load("images/ball.png").convert_alpha()
pygame.display.set_icon(icon_image)

blocks = pygame.sprite.Group()

ball = Ball()
hole = Hole()
pointer = Pointer(ball)
indicator = Indicator()
gui = Gui()

move = False
force = 0
increase_force = False
win = False

# The main loop for the game.
while app_running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			app_running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == pygame.BUTTON_LEFT:
				if not move:
					increase_force = True
					indicator.rect = (ball.rect.right + 5, ball.rect.top - 5)

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == pygame.BUTTON_LEFT:
				if not move:
					calc_velocity(pygame.mouse.get_pos())
					move = True
					increase_force = False
					commons.strokes += 1
					commons.level_strokes[commons.level-1] += 1

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				ball = Ball()

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

	if win:
		commons.points += (1000 * (commons.level**2)) / (
				commons.level_strokes[commons.level-1] + 1)
		move = False
		if commons.level < 6:
			commons.level += 1
		else:
			commons.level = 1
			commons.strokes = 0
			commons.level_strokes = [0 * i for i in range(6)]
			commons.points = 0

		if commons.level == 1:
			blocks.empty()
			commons.initial_ball_pos = 100, 260
			commons.initial_hole_pos = 700, 260
		if commons.level == 2:
			block1 = Block(150, 225, 75, 75, "white")
			block2 = Block(350, 225, 75, 75, "white")
			block3 = Block(550, 225, 75, 75, "white")
			blocks.add(block1, block2, block3)
		if commons.level == 3:
			blocks.empty()
			block1 = Block(350, 25, 75, 75, "white")
			block2 = Block(350, 425, 75, 75, "white")
			block3 = Block(500, 225, 75, 75, "white")
			blocks.add(block1, block2, block3)
		if commons.level == 4:
			blocks.empty()
			commons.initial_ball_pos = 50, 475
			commons.initial_hole_pos = 720, 475
			block1 = Block(350, 25, 75, 75)
			block2 = Block(550, 425, 100, 100)
			block3 = Block(150, 150, 50, 50)
			block4 = Block(550, 75, 50, 50)
			block5 = Block(675, 200, 50, 50)
			block6 = Block(650, 325, 50, 50)
			block7 = Block(200, 425, 50, 50)
			blocks.add(block1, block2, block3, block4, block5, block6, block7)
		if commons.level == 5:
			blocks.empty()
			commons.initial_ball_pos = 50, 50
			commons.initial_hole_pos = 750, 50
			block1 = Block(100, 0, 100, 425)
			block2 = Block(350, 100, 100, 425)
			block3 = Block(600, 0, 100, 425)
			blocks.add(block1, block2, block3)
		if commons.level == 6:
			blocks.empty()
			commons.initial_ball_pos = 50, 50
			commons.initial_hole_pos = 700, 50
			block1 = Block(500, 0, 100, 425)
			block2 = Block(150, 150, 75, 75)
			block3 = Block(85, 400, 50, 50)
			block4 = Block(375, 100, 50, 50)
			block5 = Block(625, 350, 50, 50)
			block6 = Block(725, 225, 50, 50)
			block7 = Block(625, 125, 50, 50)
			blocks.add(block1, block2, block3, block4, block5, block6, block7)

		ball = Ball()
		hole = Hole()
		ball.initial_size_x, ball.initial_size_y = ball.image.get_size()
		win = False

	update()
	draw()

	clock.tick(commons.fps)

pygame.quit()
sys.exit()
