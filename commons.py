"""A file that store commonly used variables in one place."""

screen_width = 800
screen_height = 600
fps = 60
delta_time = 1 / fps
friction = 0.981

level = 1
strokes = 0
level_strokes = [0 * i for i in range(6)]
points = 0
pars = [1, 2, 2, 3, 6, 4]

bg_color = (143, 248, 75)
screen = None

initial_ball_pos = None
initial_hole_pos = None
