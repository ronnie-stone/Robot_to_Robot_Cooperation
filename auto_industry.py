import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def make_factory_grid(n=10, m=10):

	l_safe = 5

	raw_data =  np.ones((m,n))

	raw_data[:, 0:l_safe] = 2
	raw_data[4:6, -2:] = 3
	raw_data[1:9:2,1] = 5
	raw_data[6:8, 3:5] = 4

	fig, ax = plt.subplots(1,1,tight_layout=False)

	my_cmap = {1: np.array([255, 0, 0, 0.2]),
             	2: np.array([0, 255, 0, 0.2]),
             	3: np.array([0, 0, 255, 0.2]),
             	4: np.array([0, 255, 255, 1]),
             	5: np.array([0, 0, 0, 1])}  	

	ax.axvline(0, lw=3, color='k', zorder=5)

	for i in range(1, n):
		ax.axvline(i, lw=1.5, color='k', zorder=5)

	ax.axvline(n, lw=3, color='k', zorder=5)

	ax.axhline(0, lw=3, color='k', zorder=5)

	for j in range(1, m+1):
		ax.axhline(j, lw=2, color='k', zorder=5)

	ax.axis("off")

	print(raw_data)

	color_data = np.ndarray(shape=(raw_data.shape[0], raw_data.shape[1], 4), dtype=float)
	for i in range(0, raw_data.shape[0]):
		for j in range(0, raw_data.shape[1]):
			color_data[i][j] = my_cmap[raw_data[i][j]]

	ax.imshow(color_data, extent=[0, n, 0, m], zorder=0)
	ax.set_title("Factory Floor")

if __name__ == "__main__":

	make_factory_grid(20, 10)

	plt.show()





