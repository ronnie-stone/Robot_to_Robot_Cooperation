# Test 2 is concerned with testing a new and more flexible animation framework.
# It also makes extensive use our own plotting and animation functions to visualize the results.

# Python standard libraries:

import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import os

# Our implementations of common path-planning algorithms:

from rrt import rrt
from prm import prm
from djikstra import djikstra

# Plotting functions:

from plot_obstacles import plot_obstacles
from plot_graph import plot_graph
from plot_path import plot_path

# Auxiliary functions:

from pick_endpoints import pick_endpoints
from make_video import make_video
from remove_nodes import remove_nodes
from restore_nodes import restore_nodes
from add_endpoint import add_endpoint

if __name__ == "__main__":

	# Cleans directory:

	CURR_DIR = os.path.dirname(os.path.realpath(__file__))
	for filename in glob.glob(CURR_DIR + "/debug/*.png"):
		 os.remove(filename)

	converged = False

	# Define environment:

	static_obstacles = [[1, 1, 2.5, 2.5], [4, 7, 1, 1], [8, 3, 1, 5]]
	# dynamic_obstacles = [[5, 7, 0.5, 1]]
	dynamic_obstacles = [[5, 7, 0.5, 1], [1, 9, 1, 1], [4, 4, 1, 1], [7, 5, 1, 1], [5, 0, 1, 1], [3, 7, 1, 1]]

	# Calculate roadmap and add endpoint: 

	graph_prm, x_array_prm, y_array_prm = prm(static_obstacles, N=3000, k=12)
	graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (0.5,9.5))
	graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (9.5,9.5))
	qgoal1 = len(x_array_prm) - 2
	qgoal2 = len(x_array_prm) - 1
	qinit1 = qgoal2 + 1
	qinit2 = qinit1 + 1

	# Testing "optimal":

	graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (0.5, 0.5))
	graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (9.5, 0.5))

	path_prm_1, total_cost_1 = djikstra(qinit1, qgoal1, graph_prm, x_array_prm, y_array_prm)
	path_prm_2, total_cost_2 = djikstra(qinit2, qgoal2, graph_prm, x_array_prm, y_array_prm)

	min_idx = list(graph_prm[qinit1].items())[0][0]
	graph_prm[min_idx].pop(qinit1)
	graph_prm.pop(qinit1)
	x_array_prm = np.delete(x_array_prm, -1)
	y_array_prm = np.delete(y_array_prm, -1)

	min_idx = list(graph_prm[qinit2].items())[0][0]
	graph_prm[min_idx].pop(qinit2)
	graph_prm.pop(qinit2)
	x_array_prm = np.delete(x_array_prm, -1)
	y_array_prm = np.delete(y_array_prm, -1)

	print(len(x_array_prm))

	# Define speeds:

	speed = 0.3
	speed_obs = 0.04

	# Define roboot dimensions:

	x_robot_len = 0.5
	y_robot_len = 0.5

	# Define start of trajectory:

	x_trajectory = [0.5]
	y_trajectory = [0.5]

	x_trajectory_2 = [9.5]
	y_trajectory_2 = [0.5]

	i = 0

	while not converged:

		fig, ax = plt.subplots(1,1)
		plt.cla()

		for d_obs in dynamic_obstacles:
			static_obstacles.append(d_obs)

		x_cur = x_trajectory[i]
		y_cur = y_trajectory[i]

		x_cur_2 = x_trajectory_2[i]
		y_cur_2 = y_trajectory_2[i]

		graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (x_cur, y_cur))
		graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (x_cur_2, y_cur_2))

		# Calculate path for Agent 1:

		dynamic_obstacles.append([x_cur_2, y_cur_2, x_robot_len, y_robot_len])

		remove_nodes(graph_prm, x_array_prm, y_array_prm, dynamic_obstacles, eps=0.25)

		path_1, total_cost = djikstra(qinit1, qgoal2, graph_prm, x_array_prm, y_array_prm, astar=True)

		dynamic_obstacles.pop()

		restore_nodes(graph_prm, x_array_prm, y_array_prm)

		# Calculate path for Agent 2:

		dynamic_obstacles.append([x_cur, y_cur, x_robot_len, y_robot_len])

		remove_nodes(graph_prm, x_array_prm, y_array_prm, dynamic_obstacles, eps=0.25)

		path_2, total_cost = djikstra(qinit2, qgoal1, graph_prm, x_array_prm, y_array_prm, astar=True)

		restore_nodes(graph_prm, x_array_prm, y_array_prm)

		dynamic_obstacles.pop()

		if not path_1:
			print("Path 1 not found!")
			break
		if not path_2:
			print("Path 2 not found!")
			break
			
		# Calculate diretion in which to march in time (look into this):

		x0 = (x_array_prm[path_1[1]], y_array_prm[path_1[1]])
		x1 = (x_array_prm[path_1[2]], y_array_prm[path_1[2]])

		x2 = (x_array_prm[path_2[1]], y_array_prm[path_2[1]])
		x3 = (x_array_prm[path_2[2]], y_array_prm[path_2[2]])

		theta = np.arctan2(x1[1] - x0[1], x1[0] - x0[0])
		dx = speed*np.cos(theta)
		dy = speed*np.sin(theta)

		theta_2 = np.arctan2(x3[1] - x2[1], x3[0] - x2[0])
		dx_2 = speed*np.cos(theta_2)
		dy_2 = speed*np.sin(theta_2)

		ax.add_patch(plt.Rectangle((x_cur - x_robot_len/2, y_cur - y_robot_len/2), x_robot_len, y_robot_len, 
		edgecolor = "black", facecolor = "red", zorder=1))

		ax.add_patch(plt.Rectangle((x_cur_2 - x_robot_len/2, y_cur_2 - y_robot_len/2), x_robot_len, y_robot_len, 
		edgecolor = "black", facecolor = "yellow", zorder=1))

		x_cur += dx
		y_cur += dy
		x_trajectory.append(x_cur)
		y_trajectory.append(y_cur)

		x_cur_2 += dx_2
		y_cur_2 += dy_2
		x_trajectory_2.append(x_cur_2)
		y_trajectory_2.append(y_cur_2)

		# Move dynamic obstacle:

		dynamic_obstacles[0][0] += speed_obs
		dynamic_obstacles[1][1] -= speed_obs
		dynamic_obstacles[2][0] += speed_obs
		dynamic_obstacles[3][0] -= speed_obs
		dynamic_obstacles[4][0] -= speed_obs
		dynamic_obstacles[5][1] -= speed_obs

		if dynamic_obstacles[0][0] + dynamic_obstacles[0][2] + speed_obs > 8 or dynamic_obstacles[0][0] + speed_obs < 5:
			speed_obs *= -1

		plot_obstacles(static_obstacles, dynamic_obstacles, ax)
		plt.plot(x_trajectory, y_trajectory, color="b", label="True Path" ,lw=3.0)
		plot_path(path_1, x_array_prm, y_array_prm, "g", ax, legend=False)
		plot_path(path_2, x_array_prm, y_array_prm, "y", ax, legend=False)

		step = '{:03d}'.format(i)

		plt.savefig("debug/Step" + step)
		plt.close()
		print(i)
		ax.patches.pop()
		ax.patches.pop()
		i += 1

		if np.sqrt((x_cur-9.5)**2 + (y_cur-9.5)**2) < 0.1:
			print("Script terminated!")
			break 

		for j in range(len(dynamic_obstacles)):
			static_obstacles.pop()

		# Remove beginning endpoint:

		min_idx = list(graph_prm[qinit1].items())[0][0]
		graph_prm[min_idx].pop(qinit1)
		graph_prm.pop(qinit1)
		x_array_prm = np.delete(x_array_prm, -1)
		y_array_prm = np.delete(y_array_prm, -1)

		min_idx = list(graph_prm[qinit2].items())[0][0]
		graph_prm[min_idx].pop(qinit2)
		graph_prm.pop(qinit2)
		x_array_prm = np.delete(x_array_prm, -1)
		y_array_prm = np.delete(y_array_prm, -1)

	make_video("/debug/*.png", "debug")