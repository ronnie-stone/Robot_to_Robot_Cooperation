import numpy as np


def fetch_agent(path):

	agent = []

	with open("Agents/" + path + ".txt", "r") as f:

		for line in f:

			raw_data = line.strip().split(" ")

			for i in range(len(raw_data)):

				coords = raw_data[i][1:-1].split(",")
				vertex = [float(coords[0]), float(coords[1])]
				agent.append(vertex)

	return np.asarray(agent, dtype="float")