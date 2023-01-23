import random as rd
import numpy as np
import matplotlib.pyplot as plt
from is_valid_point import is_valid_point
from is_valid_edge import is_valid_edge


def is_valid_pose(obstacles, agent, xlim, ylim): 

	# Check if any points defining the agent intersect the obstacles:

	n_points_polygon = len(agent) - 1

	for i in range(n_points_polygon):

		if is_valid_point(obstacles, agent[i]):

			continue

		else:

			return False

	# Add wall conditions to obstacles.

	south_wall = np.array([[ylim[0], xlim[0]], [ylim[0], xlim[1]]], dtype="float")
	east_wall = np.array([[ylim[0], xlim[1]], [ylim[1], xlim[1]]], dtype="float")
	north_wall = np.array([[ylim[1], xlim[1]], [ylim[1], xlim[0]]], dtype="float")
	west_wall = np.array([[ylim[1], xlim[0]], [ylim[0], xlim[0]]], dtype="float")
	walls = [south_wall, east_wall, north_wall, west_wall]

	for j in range(n_points_polygon):

		if is_valid_edge(walls, [agent[j], agent[j+1]]) and is_valid_edge(obstacles, [agent[j], agent[j+1]]):

			continue

		else:

			return False

	return True

if __name__ == "__main__":

	# Function testing

	# Note that the points that define the obstacle must be ordered counter-clockwise.
	# Also note that the initial and final points are the same and must be included.

	random_polygon = [(1,2), (0,1), (1,0), (3,1), (2,1), (2,2), (1,2)] 
	random_polygon = [(3,1), (3.5, 1), (3.25, 1.5), (3,1)] 
	square = [(3,3), (3,4), (4,4), (4,3), (3,3)]
	hourglass = [(1,3), (2,3), (1.6, 4), (2,5), (1,5), (1.4,4), (1,3)]
	hexagon = [(3.5, 1), (3.75, 0), (4.75, 0), (5,1), (4.75, 2), (3.75, 2), (3.5,1)]

	obstacles = [square, hourglass, hexagon]

	# Plot obstacles.

	fig, ax = plt.subplots(1,1)

	for obs in obstacles:

		i = 0

		while i < len(obs)-2:

			plt.plot([obs[i][0], obs[i+1][0]], [obs[i][1], obs[i+1][1]], color="b")
			i += 1

		plt.plot([obs[i][0], obs[0][0]], [obs[i][1], obs[0][1]], color="b")

	agent = random_polygon

	if is_valid_pose(obstacles, agent):

		color = "green"

	else:

		color = "red"

	i = 0

	while i < len(agent)-2:

		plt.plot([agent[i][0], agent[i+1][0]], [agent[i][1], agent[i+1][1]], color=color)

		i += 1

	plt.plot([agent[i][0], agent[0][0]], [agent[i][1], agent[0][1]], color=color)

	plt.show()