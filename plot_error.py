"""
Example for a Matplotlib plot with the following features:
    - Error bar plot
    - Error fill plot
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
y = 2 + 2 * x ** 2
e = 0.1 + 0.1 * y

# get the axis ticks
xticks = np.linspace(0.0, 2.0, 4)
yticks = np.linspace(2.0, 11.0, 5)

# ###########################################################
# Definition of the line plot
# ###########################################################

# create a figure with a determined size
(fig, ax) = utils_mpl.get_fig(size=(3.5, 3.0), dpi=200)

# add the plot curves
plt.fill_between(x, y-e, y+e, color="g", alpha=0.2)
plt.errorbar(x, y, yerr=e, lw=1.5, marker='o', ms=3.0, capsize=3.0, ecolor="r", color="g")

# set the x-axis limit and format
utils_mpl.set_x_axis(bnd=xticks, add_offset=0.1)
utils_mpl.set_format(ax.xaxis, ticks=xticks, fmt="${x:.2f}$")

# set the y-axis limit and format
utils_mpl.set_y_axis(bnd=yticks, add_offset=1.0)
utils_mpl.set_format(ax.yaxis, ticks=yticks, fmt="${x:.2f}$")

# set the legend and labels
ax.set_xlabel("x-axis (unit)")
ax.set_ylabel("y-axis (unit)")
ax.set_title("Plot Title")

# set the grid
utils_mpl.set_grid(ax)

# save the plot for Inkscape
utils_mpl.save_svg(fig, "render/error.svg")

# ###########################################################
# Show the plots
# ###########################################################

# show the plot for inspection
plt.show()
