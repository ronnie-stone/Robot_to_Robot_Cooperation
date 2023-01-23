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
	dynamic_obstacles = [[5, 7, 0.5, 1]]

	# Calculate roadmap and add endpoint: 

	graph_prm, x_array_prm, y_array_prm = prm(static_obstacles, N=2500, k=6)
	graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (9.5,9.5))
	qgoal = len(x_array_prm) - 1
	qinit = qgoal + 1

	# Testing "optimal":

	graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (0.5, 0.5))
	path_prm, total_cost = djikstra(qinit, qgoal, graph_prm, x_array_prm, y_array_prm)

	min_idx = list(graph_prm[qinit].items())[0][0]
	graph_prm[min_idx].pop(qinit)
	graph_prm.pop(qinit)
	x_array_prm = np.delete(x_array_prm, -1)
	y_array_prm = np.delete(y_array_prm, -1)

	#print(graph_prm)

	# Define speeds:

	speed = 0.3
	speed_obs = 0.05

	# Define roboot dimensions:

	x_robot_len = 0.5
	y_robot_len = 0.5

	# Define start of trajectory:

	x_trajectory = [0.5]
	y_trajectory = [0.5]

	i = 0

	while not converged:

		fig, ax = plt.subplots(1,1)
		plt.cla()
		static_obstacles.append(dynamic_obstacles[0])

		remove_nodes(graph_prm, x_array_prm, y_array_prm, dynamic_obstacles, eps=0.2)

		x_cur = x_trajectory[i]
		y_cur = y_trajectory[i]

		#print(x_cur, y_cur)

		graph_prm, x_array_prm, y_array_prm = add_endpoint(graph_prm, x_array_prm, y_array_prm, (x_cur, y_cur))
		path, total_cost = djikstra(qinit, qgoal, graph_prm, x_array_prm, y_array_prm, astar=True)
		#plot_graph(graph_prm, x_array_prm, y_array_prm, ax)
		#plt.show()

		if not path:
			print("Path not found!")
			break
			
		# Calculate diretion in which to march in time:

		#print(path[0])

		x0 = (x_array_prm[path[1]], y_array_prm[path[1]])
		x1 = (x_array_prm[path[2]], y_array_prm[path[2]])

		theta = np.arctan2(x1[1] - y_cur, x1[0] - x_cur)
		dx = speed*np.cos(theta)
		dy = speed*np.sin(theta)
		ax.add_patch(plt.Rectangle((x_cur - x_robot_len/2, y_cur - y_robot_len/2), x_robot_len, y_robot_len, 
		edgecolor = "black", facecolor = "red", zorder=1))
		x_cur += dx
		y_cur += dy
		x_trajectory.append(x_cur)
		y_trajectory.append(y_cur)

		# Move dynamic obstacle:

		quad_rep = dynamic_obstacles[0][0] - 6.5

		if speed_obs > 0:
			speed_obs = -0.02*(quad_rep)**2 + 0.2
		else:
			speed_obs = 0.02*(quad_rep)**2 - 0.2

		if dynamic_obstacles[0][0] + dynamic_obstacles[0][2] > 8 or dynamic_obstacles[0][0] < 5:
			speed_obs *= -1

		dynamic_obstacles[0][0] += speed_obs

		plot_obstacles(static_obstacles, dynamic_obstacles, ax)
		plt.plot(x_trajectory, y_trajectory, color="b", label="True Path" ,lw=3.0)
		plot_path(path, x_array_prm, y_array_prm, "g", ax, legend=False)
		#plot_graph(graph_prm, x_array_prm, y_array_prm, ax)
		#plot_path(path_prm, x_array_prm, y_array_prm, "r", ax)

		step = '{:03d}'.format(i)

		plt.savefig("debug/Step" + step)
		plt.close()
		print(i)
		ax.patches.pop()
		i += 1

		if np.sqrt((x_cur-9.5)**2 + (y_cur-9.5)**2) < 0.5:
			print("Script terminated!")
			break 

		static_obstacles.pop()

		# Remove beginning endpoint:

		min_idx = list(graph_prm[qinit].items())[0][0]
		graph_prm[min_idx].pop(qinit)
		graph_prm.pop(qinit)
		x_array_prm = np.delete(x_array_prm, -1)
		y_array_prm = np.delete(y_array_prm, -1)
		restore_nodes(graph_prm, x_array_prm, y_array_prm)

	make_video("/debug/*.png", "debug")