import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.spatial import distance
from functools import partial

def make_factory_grid(n=10, m=10):

	pass

if __name__ == "__main__":

	n = 10
	m = 20

	make_factory_grid(n, m)

	# Plotting:

	fig, ax = plt.subplots(1,1,tight_layout=False)
	plt.xlim([0, m])
	plt.ylim([0, n])
	plt.tick_params(left=False,bottom=False)
	plt.xticks(color='w')
	plt.yticks(color='w')
	plt.title("Continuous Representation")
	ax.set_aspect(1)

	plt.show()