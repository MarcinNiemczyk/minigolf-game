import math


def calc_difference(initial_pos, target_pos):
	"""Return a vector that is difference between target and initial position."""
	return target_pos[0] - initial_pos[0], target_pos[1] - initial_pos[1]


def calc_magnitude(vec):
	"""Return length of a vector, indispensable to normalize vector."""
	return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def normalize_vector(vec):
	"""Return a normalized vector with proper x, y ratio and set direction."""
	vec_length = calc_magnitude(vec)

	if vec_length < 0.00001:
		return 0, 1

	return (vec[0] / vec_length), (vec[1] / vec_length)


def calc_angle(vec):
	"""Calculate the vector angle and transform from radian value to degrees."""
	return (math.atan2(*vec) * 180) / math.pi


def rotate(vec, angle):
	"""Rotate a vector by x degrees."""
	angle = math.radians(angle)
	return math.cos(angle) * vec[0] - math.sin(angle) * vec[1], \
	       math.sin(angle) * vec[0] + math.cos(angle) * vec[1]
