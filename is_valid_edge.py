import random as rd
import numpy as np
import matplotlib.pyplot as plt


def is_valid_edge(obstacles, edge):

	def triangle_signed_area(p1, p2, p3):

		ax, ay = p1
		bx, by = p2
		cx, cy = p3

		return ax*by - ay*bx + ay*cx - ax*cy + bx*cy - cx*by

	# Fetch points defining edge.

	p1 = edge[0]
	p2 = edge[1]

	# For each obstacle, check intersection.

	for obs in obstacles:

		n_points_polygon = len(obs) - 1

		# For each edge defining the obstacle, check intersection.

		for i in range(n_points_polygon):

			# Fetch points defining current edge.

			p3 = (obs[i][0], obs[i][1])
			p4 = (obs[i+1][0], obs[i+1][1])

			# Calculate orientation for different triangle combinations.

			orientation_1 = triangle_signed_area(p1, p2, p3)
			orientation_2 = triangle_signed_area(p1, p2, p4)
			orientation_3 = triangle_signed_area(p3, p4, p1)
			orientation_4 = triangle_signed_area(p3, p4, p2)

			# If the orientations are the same, the edge is valid.

			if orientation_1 * orientation_2 < 0 and orientation_3 * orientation_4 < 0:

				return False

	return True

if __name__ == "__main__":

	# Function testing

	# Note that the points that define the obstacle must be ordered counter-clockwise.
	# Also note that the initial and final points are the same and must be included.

	xlim = (0, 10)
	ylim = (0, 10)

	random_polygon = [(1,2), (0,1), (1,0), (3,1), (2,1), (2,2), (1,2)] 
	square = [(3,3), (3,4), (4,4), (4,3), (3,3)]
	hourglass = [(1,3), (2,3), (1.6, 4), (2,5), (1,5), (1.4,4), (1,3)]
	hexagon = [(3.5, 1), (3.75, 0), (4.75, 0), (5,1), (4.75, 2), (3.75, 2), (3.5,1)]

	south_wall = np.array([[ylim[0], xlim[0]], [ylim[0], xlim[1]]], dtype="float")
	east_wall = np.array([[ylim[0], xlim[1]], [ylim[1], xlim[1]]], dtype="float")
	north_wall = np.array([[ylim[1], xlim[1]], [ylim[1], xlim[0]]], dtype="float")
	west_wall = np.array([[ylim[1], xlim[0]], [ylim[0], xlim[0]]], dtype="float")

	obstacles = [random_polygon, square, hourglass, hexagon, south_wall, east_wall, west_wall, north_wall]

	# Plot obstacles.

	fig, ax = plt.subplots(1,1)

	for obs in obstacles:

		i = 0

		while i < len(obs)-2:

			plt.plot([obs[i][0], obs[i+1][0]], [obs[i][1], obs[i+1][1]], color="b")
			i += 1

		plt.plot([obs[i][0], obs[0][0]], [obs[i][1], obs[0][1]], color="b")

	for i in range(5000):

		x1_random = 11*rd.random()
		y1_random = 11*rd.random()

		x2_random = 11*rd.random()
		y2_random = 11*rd.random()

		edge = [(x1_random, y1_random), (x2_random, y2_random)]

		if is_valid_edge(obstacles, edge):

			plt.plot([x1_random, x2_random], [y1_random, y2_random], color="green", alpha=0.5)

		else:

			continue

			plt.plot([x1_random, x2_random], [y1_random, y2_random], color="red")

	plt.show()

