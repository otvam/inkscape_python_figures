"""
Example for a Matplotlib plot with the following features:
    - Logarithmic axis.
    - Custom axis ticks.

The EM problem solution has been obtained with PyPEEC (https://pypeec.otvam.ch).
PyPEEC is a 3D quasi-magnetostatic PEEC solver (voxel-based and FFT-accelerated).
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "Mozilla Public License Version 2.0"

import os
import numpy as np
import matplotlib.pyplot as plt
import utils_mpl

# ###########################################################
# Plot global parameters and define dummy data
# ###########################################################

# set global parameters
utils_mpl.set_global()

# create the output folder
os.makedirs("render", exist_ok=True)

# define dummy data
x = np.linspace(0, 2, 11)
y_1 = 1e4 + 0.5e6 * x ** 2
y_2 = 1e4 + 0.5e6 * x ** 4

# get the axis ticks
xticks = np.linspace(0.0, 2.0, 4)
yticks = np.power(10.0, np.linspace(4, 7, 4))

# ###########################################################
# Definition of the line plot
# ###########################################################

# create a figure with a determined size
(fig, ax) = utils_mpl.get_fig(size=(3.5, 3.0), dpi=200)

# add reference curves
plt.plot([-1, +3], [1e6, 1e6], "-k", lw=1.0)
plt.plot([-1, +3], [1e5, 1e5], "-k", lw=1.0)
plt.axhspan(1e5, 1e6, facecolor="orange", alpha=0.2)

# add the data curves
plt.plot(x, y_1, "-or", ms=3.0, lw=1.5, label="label 1")
plt.plot(x, y_2, "-ob", ms=3.0, lw=1.5, label="label 2")

# get the axes transformations
plt.xscale("linear")
plt.yscale("log")

# custom format for y-axis
def custom_format(x, _):
    out = f"10^{abs(np.log10(x)):.0f}"
    if np.any(np.isclose(x, [1e5, 1e6])):
        return f"bnd / ${out}$"
    else:
        return f"out / ${out}$"

# set the x-axis limit and format
utils_mpl.set_x_axis(bnd=xticks, add_offset=0.1)
utils_mpl.set_format(ax.xaxis, ticks=xticks, fmt="${x:.2f}$")

# set the y-axis limit and format
utils_mpl.set_y_axis(bnd=yticks, add_fact=1.0)
utils_mpl.set_format(ax.yaxis, ticks=yticks, fmt=custom_format)

# set the legend and labels
ax.legend(loc="upper left")
ax.set_xlabel("x-axis (unit)")
ax.set_ylabel("y-axis (unit)")
ax.set_title("Plot Title")

# set the grid
utils_mpl.set_grid(ax)

# save the plot for Inkscape
utils_mpl.save_svg(fig, "render/line.svg")

# ###########################################################
# Show the plots
# ###########################################################

# show the plot for inspection
plt.show()
