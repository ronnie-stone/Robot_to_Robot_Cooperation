import numpy as np 
import matplotlib.pyplot as plt
import random as rd
from is_valid_pose import is_valid_pose
from is_valid_point import is_valid_point
from is_valid_edge import is_valid_edge
from rigid_body_motion import rigid_body_motion

def prm_3D(obstacles, agent, N=200, xlim=(0, 10), ylim=(0, 10), tlim=(-np.pi, np.pi), k=6, eps=0.25):
	"""
	A simple implementation of PRM.

		Parameters:

			obstacles (list of lists): Shape of obstacles.
			N (int): Number of samples.
			xlim (float 2-tuple): Enviroment x bounds.
			ylim (float 2-tuple): Enviroment y bounds.
			k (int): Maximum number of neighbors for each node.
			eps (float): Tolerance to obstacles.

		Returns:

			edges (int-list dictionary): Nodes' IDs and connectivities.
			x_array (N x 1 float array): Nodes' x coordinates.
			y_array (N x 1 float array): Nodes' y coordinates.

	"""

	def shortest_k_neighbors(cur_idx, k, x_array, y_array, t_array):
		"""
		Finds the nearest k-neighbors to the current index.

			Parameters:

				cur_idx (int): ID of current node being connected
				k (int): maximum number of nearest neighbors to be connected
				x_array (N x 1 float array): Nodes' x coordinates.
				y_array (N x 1 float array): Nodes' y coordinates.

			Returns:

				True or False (bool).

		"""

		# This requires a future overhaul (to ensure completeness and symmetry).

		p = (x_array[cur_idx],y_array[cur_idx], t_array[cur_idx])

		delta_array = np.zeros(len(x_array))

		for i in range(len(x_array)):

			delta_array[i] = np.sqrt((x_array[i] - p[0])**2 + (y_array[i] - p[1])**2 + (t_array[i] - p[2])**2)

		min_idx = []
		min_dis = []

		j = 0

		while j < k:

			delta_min = np.argmin(delta_array)
			edge = [p, (x_array[delta_min], y_array[delta_min], t_array[delta_min])]

			if delta_min != cur_idx:

				min_idx.append(delta_min)
				min_dis.append(delta_array[delta_min])
				j += 1

			delta_array[delta_min] = float("Inf")

		return min_idx, min_dis

	# Define data structures:

	x_array = np.zeros(N)
	y_array = np.zeros(N)
	t_array = np.zeros(N)
	edges = dict()

	i = 0

	while i < N:

		# Sample random point in configuration space:

		x = rd.uniform(xlim[0], xlim[1])
		y = rd.uniform(ylim[0], ylim[1])
		t = rd.uniform(tlim[0], tlim[1])
		p = (x,y,t)
		translated_agent = rigid_body_motion(agent, (x,y), t)

		# Check if point is valid:

		if is_valid_pose(obstacles, translated_agent, xlim, ylim):

			# Store point's coordinates:

			x_array[i] = x
			y_array[i] = y
			t_array[i] = t
			i += 1

	# Add k closest neighbors to each node:

	for i in range(N):

		min_idx, min_dis = shortest_k_neighbors(i, k, x_array, y_array, t_array)
		edges[i] = dict()

		for j in range(k):

			edges[i][min_idx[j]] = min_dis[j]

	# Enforce symmetry:

	for i in range(N):

		edge = edges[i]

		for idx in edge:

			if i not in edges[idx]:

				edges[idx][i] = edge[idx]

	return edges, x_array, y_array, t_array