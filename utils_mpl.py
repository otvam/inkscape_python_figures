"""
Collection of small utils to create figures with Matplotlib:
    - Step nice default parameters (fonts, sizes, etc.).
    - Create and save figures as PDFs and PNGs.
    - Set the grid, axis limit, and axis ticks.
    - Clone the exact size of an axes in a new figure.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "Mozilla Public License Version 2.0"

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np


def set_global():
    """
    Set the global Matplotlib options.
    """

    # set the font family
    plt.rcParams["font.size"] = 9.0
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.default"] = "regular"

    # set the axes parameters
    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.linewidth"] = 1.0
    plt.rcParams["axes.labelsize"] = 9.0
    plt.rcParams["axes.titlesize"] = 10.0
    plt.rcParams["axes.labelpad"] = 8.0
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.titleweight"] = "bold"

    # set the legend parameters
    plt.rcParams["legend.edgecolor"] = "k"
    plt.rcParams["legend.fancybox"] = False
    plt.rcParams["legend.framealpha"] = 1.0
    plt.rcParams["legend.fontsize"] = 9.0


def set_grid(major=True, minor=True):
    """
    Set the grid for a plot.
    """

    if major:
        plt.grid(which="major", linewidth=0.75)
    if minor:
        plt.grid(which="minor", linewidth=0.25)


def get_bnd(bnd=None, add_offset=0.0, add_fact=0.0):
    """
    Get bound limits with specified tolerances.
        - bnd: vector containing the bounds
        - add_offset: offset added to the bounds (useful for linear scales)
        - add_fact: factor added to the bounds (useful for log scales)
    """

    # set the bounds
    v_min = (np.min(bnd) - add_offset) / (1 + add_fact)
    v_max = (np.max(bnd) + add_offset) * (1 + add_fact)

    return v_min, v_max


def set_cbar(bnd=None, add_offset=0.0, add_fact=0.0):
    """
    Create a colorbar and set the bounds (with tolerances).
    """

    # create the colorbar
    cb = plt.colorbar()

    # set the bounds
    if bnd is not None:
        (v_min, v_max) = get_bnd(bnd=bnd, add_offset=add_offset, add_fact=add_fact)
        plt.clim(v_min, v_max)

    return cb


def set_x_axis(bnd=None, add_offset=0.0, add_fact=0.0):
    """
    Set the bounds for the x-axis (with tolerances).
    """

    if bnd is not None:
        (v_min, v_max) = get_bnd(bnd=bnd, add_offset=add_offset, add_fact=add_fact)
        plt.xlim(v_min, v_max)


def set_y_axis(bnd=None, add_offset=0.0, add_fact=0.0):
    """
    Set the bounds for the y-axis (with tolerances).
    """

    if bnd is not None:
        (v_min, v_max) = get_bnd(bnd=bnd, add_offset=add_offset, add_fact=add_fact)
        plt.ylim(v_min, v_max)


def set_format(axis, ticks=None, fmt=None):
    """
    Set the tick locations and formats with the following options:
        - A Matplotlib formatter can be provided.
        - If a string is provided, StrMethodFormatter is used.
        - If a calltable is provided, FuncFormatter is used.
    """

    # set the ticks
    if ticks is not None:
        axis.set_ticks(ticks)

    # set the format
    if fmt is not None:
        if isinstance(fmt, tkr.Formatter):
            axis.set_major_formatter(fmt)
        elif isinstance(fmt, str):
            axis.set_major_formatter(tkr.StrMethodFormatter(fmt))
        elif callable(fmt):
            axis.set_major_formatter(tkr.FuncFormatter(fmt))
        else:
            raise ValueError("invalid tick format")


def get_fig(size=(6, 4), dpi=100):
    """
    Create a figure for a vector plot:
        - The figure size can be specified (print size).
        - The resolution can be specified (screen size)
    """

    # create the figure
    fig = plt.figure(figsize=size, dpi=dpi)
    ax = fig.gca()

    # dummy plot in order to get a colormap
    plt.scatter(np.nan, np.nan)

    return fig, ax


def get_fig_clone(fig, ax):
    """
    Find the exact dimension (width and height) of the axes.
    Find the bounds of the axes (x-axis, y-axis, and colorbar).

    This function is used to split large plots in two parts:
        - A vector plot with the axes, labels, ticks, legend, etc.
        - A raster plot with the large payload (contour, scatter, etc.)
    """

    # get the size of the axis of the vector figure
    bbox = ax.get_window_extent()
    width = bbox.width / fig.dpi
    height = bbox.height / fig.dpi

    size = (width, height)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    clim = plt.gci().get_clim()

    return size, xlim, ylim, clim


def set_fig_clone(size, xlim, ylim, clim):
    """
    Resize a figure to the specified dimensions.
    The axes are occupied the complete figure.
    The axes and grid are hidden.

    This function is used to split large plots in two parts:
        - A vector plot with the axes, labels, ticks, legend, etc.
        - A raster plot with the large payload (e.g., contour, scatter, or image).
    """

    plt.gca().set_position([0.0, 0.0, 1.0, 1.0])
    plt.gcf().set_size_inches(size)

    # set the extent
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.clim(clim)
    plt.grid(False)
    plt.axis(False)


def save_svg(fig, filename):
    """
    Save a plot to a SVG file (for Inkscape).
    """

    # compact and fix the plot layout
    fig.tight_layout()

    # save the plot for Inkscape
    fig.savefig(filename, transparent=True)


def save_png(fig, filename, dpi=100):
    """
    Save a plot to a PNG file (for Inkscape).
    The resolution can be specified.
    """

    # save the plot for Inkscape
    fig.savefig(filename, dpi=dpi, transparent=True)
