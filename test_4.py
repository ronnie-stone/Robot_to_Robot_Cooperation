# Test 4 adds more dynamic and static obstacles to test validity of our PRM approach.
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
from prm_3D import prm_3D
from djikstra import djikstra

# Plotting functions:

from plot_obstacles import plot_obstacles
from plot_graph import plot_graph
from plot_path import plot_path

# Auxiliary functions:

from pick_endpoints import pick_endpoints
from remove_nodes import remove_nodes
from restore_nodes import restore_nodes
from make_video import make_video
from fetch_agent import fetch_agent
from fetch_static_obstacles import fetch_static_obstacles
from rigid_body_motion import rigid_body_motion

if __name__ == "__main__":

	CURR_DIR = os.path.dirname(os.path.realpath(__file__))
	for filename in glob.glob(CURR_DIR + "/test4/*.png"):
		 os.remove(filename)

	# Select obstacles type:

	converged = False
	static_obstacles, dilated_static_obstacles = fetch_static_obstacles("Polygons", eps=0.1)
	dynamic_obstacles = []

	# Select agent type:

	agent = fetch_agent("LongRectangle")
	#agent = fetch_agent("UnitOctagon")/1.5

	goal = (7,9)
	start = (2, 0.5)

	t0 = time.time()

	graph_prm, x_array_prm, y_array_prm, t_array_prm = prm_3D(dilated_static_obstacles, agent, N=3000, k=6)
	# graph_prm, x_array_prm, y_array_prm = prm(dilated_static_obstacles, agent, N=1000, k=6)

	t1 = time.time()

	print(t1-t0)
	qinit, qgoal = pick_endpoints((start[0], start[1]), (goal[0], goal[1]), x_array_prm, y_array_prm) 
	path_prm, total_cost = djikstra(qinit, qgoal, graph_prm, x_array_prm, y_array_prm)

	# Given the path, plot the sequence of poses:

	fig1, ax1 = plt.subplots(1,1)
	plot_graph(graph_prm, x_array_prm, y_array_prm, ax1)
	plot_obstacles(static_obstacles, dilated_static_obstacles, ax1)
	# plot_path(path_prm, x_array_prm, y_array_prm, "r", ax1, agent=agent, t_array=t_array_prm)
	# plot_path(path_prm, x_array_prm, y_array_prm, "r", ax1, agent=agent)
	plt.show()
	#print("Continuing")

	speed = 0.2
	i = 0

	x_trajectory = [start[0]]
	y_trajectory = [start[1]]

	'''

	while not converged:

		fig, ax = plt.subplots(1,1)
		plt.cla()

		x_cur = x_trajectory[i]
		y_cur = y_trajectory[i]

		qinit, qgoal = pick_endpoints((x_cur, y_cur), (goal[0], goal[1]), x_array_prm, y_array_prm)
		path, total_cost = djikstra(qinit, qgoal, graph_prm, x_array_prm, y_array_prm, astar=True)

		if not path:
			print("Path not found!")
			break

		# Calculate direction in which to march in time:

		x0 = (x_array_prm[path[0]], y_array_prm[path[0]])
		x1 = (x_array_prm[path[1]], y_array_prm[path[1]])

		theta = np.arctan2(x1[1] - x0[1], x1[0] - x0[0])
		dx = speed*np.cos(theta)
		dy = speed*np.sin(theta)
		plot_obstacles([], [rigid_body_motion(agent, (x_cur, y_cur), 0)], ax)
		x_cur += dx
		y_cur += dy
		x_trajectory.append(x_cur)
		y_trajectory.append(y_cur)

		plot_obstacles(static_obstacles, dynamic_obstacles, ax)
		plt.plot(x_trajectory, y_trajectory, color="b", label="True Path", lw=3.0)
		plot_path(path, x_array_prm, y_array_prm, "g", ax, legend=False)
		plot_path(path_prm, x_array_prm, y_array_prm, "r", ax)

		step = '{:03d}'.format(i)

		plt.savefig("test4/Step" + step)
		plt.close()
		print(i)
		i += 1

		if np.sqrt((x_cur-goal[0])**2 + (y_cur-goal[1])**2) < 0.5:
			print("Script terminated!")
			break 

	make_video("/test4/*.png", "test4")

	'''
