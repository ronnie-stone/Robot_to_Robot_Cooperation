import random as rd
import numpy as np
import matplotlib.pyplot as plt


def is_valid_point(obstacles, point):

	x = point[0]
	y = point[1]

	for obs in obstacles:

		n_points_polygon = len(obs)
		n_intersections = 0

		for i in range(n_points_polygon-1):

			point_A = (obs[i][0], obs[i][1])
			point_B = (obs[i+1][0], obs[i+1][1])

			x1 = point_A[0]
			y1 = point_A[1]

			x2 = point_B[0]
			y2 = point_B[1]

			if ((y < y1) != (y < y2)) and x < (((x2-x1)*(y-y1))/(y2-y1) + x1):

				n_intersections += 1

		intersection = False if n_intersections % 2 == 0 else True

		if intersection: return False

	return True

if __name__ == "__main__":

	# Function testing

	obstacles = [[(1,2), (0,1), (1,0), (3,1), (2,1), (2,2)]]

	fig, ax = plt.subplots(1,1)

	for obs in obstacles:

		i = 0

		while i < len(obs)-1:

			plt.plot([obs[i][0], obs[i+1][0]], [obs[i][1], obs[i+1][1]], color="b")
			i += 1

		plt.plot([obs[i][0], obs[0][0]], [obs[i][1], obs[0][1]], color="b")

	for i in range(5000):

		x_random = 5*rd.random()
		y_random = 5*rd.random()

		point = (x_random, y_random)

		if is_valid_point(obstacles, point):

			plt.plot(x_random, y_random, marker="o", markersize=2, color="green")

		else:

			plt.plot(x_random, y_random, marker="o", markersize=2, color="red")

	plt.show()

