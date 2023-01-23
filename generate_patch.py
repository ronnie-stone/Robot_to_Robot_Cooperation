from matplotlib.path import Path
import matplotlib.patches as patches


def generate_patch(obstacle, facecolor="blue", lw=1, alpha=0.8):

	n_points_polygon = len(obstacle)-1

	move_sequence = [Path.MOVETO]

	for i in range(n_points_polygon-1):
		move_sequence.append(Path.LINETO)

	move_sequence.append(Path.CLOSEPOLY)

	patch_path = Path(obstacle, move_sequence)

	patch = patches.PathPatch(patch_path, facecolor=facecolor, lw=lw, alpha=alpha)

	return patch