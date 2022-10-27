import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.spatial import distance
from functools import partial

def make_factory_grid(n=10, m=10):

	pass

def update_mobile(x_robot, y_robot, path, i, speed=0.1):

	x_center = x_robot[0] + 0.5
	y_center = y_robot[0] + 0.5

	# idx = distance.cdist([(x_center, y_center)], path).argmin()

	# dx = path[0][1] - path[0][0]
	
	#slope = (path[idx+1][1] - path[idx][1])/dx

	#x_new = 

	return path[i][0], path[i][1], np.pi

def interpolate():

	xp = np.array([1.5, 10, 18])
	yp = np.array([1.5, 2, 8])

	params = np.polyfit(xp, yp, deg=2)


	return params

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
	# plt.grid()
	ax.set_aspect(1)
	tx = ax.text(1, -1, "Mobile Robot X-Pos: 1")
	ty = ax.text(1, -2, "Mobile Robot Y-Pos: 1")

	# Initial positions:

	ax.add_patch(plt.Rectangle((8.75, 3.75), 2.5, 2.5, edgecolor = "black", facecolor = "blue"))

	# Mobile robot:

	x_robot = np.array([1])
	y_robot = np.array([1])

	ax.add_patch(plt.Rectangle((x_robot, y_robot), 1, 1, edgecolor = "black", facecolor = "red", zorder=1))
	#ax.add_patch(plt.Rectangle((1.5, 1.25), 0.5, 0.5, edgecolor = "black", facecolor = "red", zorder=1))

	draw_circle = plt.Circle((10, 5), 0, facecolor = "blue", edgecolor = "black")
	ax.add_artist(draw_circle)

	plt.scatter(18, 8, color = "r", marker="x", s=100)

	circle_radii = np.linspace(0, 0.5, 25)
	speed = 0.1

	x_path = np.linspace(1.5, 18, 125)
	params = interpolate()
	y_path = params[0]*x_path**2 + params[1]*x_path + params[2]
	plt.plot(x_path, y_path, zorder=0)

	path = np.array(list(zip(x_path, y_path)))

	def update_plot(i, x_robot, y_robot):

		r = 0.5

		# Update circle position: 

		ax.patches.pop()
		ax.patches.pop()

		if i < 25:

			# Increase radius

			draw_circle = plt.Circle((7.5, 5), circle_radii[i], facecolor = "blue", edgecolor = "black")

		elif i < 50:

			# Decrease radius
			draw_circle = plt.Circle((7.5, 5), 2*r - i/50, facecolor = "blue", edgecolor = "black")

		elif i < 75:

			draw_circle = plt.Circle((7.5, 5), 0, facecolor = "blue", edgecolor = "black")

		elif i < 100:

			draw_circle = plt.Circle((12.5, 5), circle_radii[i-100], facecolor = "blue", edgecolor = "black")

		else:

			draw_circle = plt.Circle((12.5, 5), circle_radii[-1] - circle_radii[i-125], facecolor = "blue", edgecolor = "black")

		# Update mobile robot:

		dx, dy, theta = update_mobile(x_robot, y_robot, path, i)

		# print(dx, dy)

		ax.add_patch(plt.Rectangle((dx - 0.5, dy - 0.5), 1, 1, edgecolor = "black", facecolor = "red", zorder=1))

		ax.add_artist(draw_circle)

		tx.set_text("Mobile Robot X-Pos: " + "{:.2f}".format(dx))
		ty.set_text("Mobile Robot Y-Pos: " + "{:.2f}".format(dy))

		return ax, tx, ty

	anim = FuncAnimation(fig, func=partial(update_plot, x_robot=x_robot, y_robot=y_robot),
	repeat=True, frames=np.arange(1,125), interval=50)

	#anim.save("python_simulator.gif", dpi=300, writer=PillowWriter(fps=25))

	plt.show()