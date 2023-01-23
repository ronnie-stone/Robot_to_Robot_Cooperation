import numpy as np

def add_endpoint(graph, x_array, y_array, pgoal):

		l = len(x_array)

		delta_array = np.zeros(l)

		# Find nearest point in roadmap to desired goal:

		for i in range(len(x_array)):

			delta_array[i] = np.sqrt((x_array[i] - pgoal[0])**2 + (y_array[i] - pgoal[1])**2)

		delta_min = np.argmin(delta_array)

		# Create new point:
		
		x_array = np.append(x_array, pgoal[0])
		y_array = np.append(y_array, pgoal[1])

		# Create new edge:

		graph[l] = dict()

		# Enforce symmetry:

		graph[l][delta_min] = delta_array[delta_min] 
		graph[delta_min][l] = delta_array[delta_min]

		return graph, x_array, y_array
