import numpy as np
import matplotlib.pyplot as plt
from plot_obstacles import plot_obstacles


def fetch_static_obstacles(path, eps=0.1):

	static_obstacles = []
	dilated_static_obstacles = []

	with open("Scenarios/" + path + ".txt", "r") as f:

		for line in f:

			vertices = []
			dilated_vertices = []

			raw_data = line.strip().split(" ")
			translation = np.asarray(raw_data[-1][1:-1].split(","), dtype=float)

			for i in range(len(raw_data)-1):

				coords = raw_data[i][1:-1].split(",")
				coords = np.asarray(coords, dtype=float)

				vertex = [coords[0]+translation[0], coords[1]+translation[1]]
				vertices.append(vertex)

				#theta = np.arctan2(coords[1], coords[0])
				#coords[0] += eps*np.cos(theta)
				#coords[1] += eps*np.sin(theta)

				

				d = 1

				if coords[0] == 0:
					d = np.sqrt(2)

				if coords[1] > 0:
					coords[1] += d*eps
				elif coords[1] < 0:
					coords[1] -= d*eps

				d = 1

				if coords[1] == 0: 
					d = np.sqrt(2)

				if coords[0] > 0:
					coords[0] += d*eps
				elif coords[0] < 0:
					coords[0] -= d*eps

				

				dilated_vertex = [coords[0]+translation[0], coords[1]+translation[1]]
				dilated_vertices.append(dilated_vertex)

			static_obstacles.append(vertices)
			dilated_static_obstacles.append(dilated_vertices)

	return static_obstacles, dilated_static_obstacles

if __name__ == "__main__":

	obs, dobs = fetch_static_obstacles("Rectangles")

	fig, ax = plt.subplots(1,1)
	
	plot_obstacles(obs, [], ax)

	plt.show()

