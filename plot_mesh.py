"""
Example for PyVista plots with the following features:
    - Selection of the camera/zoom.
    - 3D plot (field pattern and geometry).
    - 2D plot (slice of the 3D geometry).

The EM problem solution has been obtained with PyPEEC (https://pypeec.otvam.ch).
PyPEEC is a 3D quasi-magnetostatic PEEC solver (voxel-based and FFT-accelerated).
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "Mozilla Public License Version 2.0"

import os
import pyvista as pv
import utils_pv

# ###########################################################
# Plot global parameters
# ###########################################################

# set global parameters
utils_pv.set_global()

# create the output folder
os.makedirs("render", exist_ok=True)

# ###########################################################
# Load the 3D objects
# ###########################################################

# load the EM solution (VTK file)
solution = pv.read("mesh_data/solution.vtk")

# load the STL geometry
coil = pv.read("mesh_data/coil.stl")
core = pv.read("mesh_data/core.stl")

# scale the units
coil = coil.scale(0.001)
core = core.scale(0.001)

# extract the winding potential
potential = solution.threshold(scalars="potential")

# extract the core field
field = solution.threshold(scalars="field")

# define the colormap
cmap_potential = "viridis"
cmap_field = "magma"

# get the colormap ticks
clim_potential = (0.35, 0.65)
clim_field = (0.0, 2.0)

# ###########################################################
# Find the camera angle
# ###########################################################

# create a plotter
pl = pv.Plotter(window_size=(1024, 768))

# add the geometry
pl.add_mesh(coil, color="orange")
pl.add_mesh(core, color="gray")

# plot and get the final camera angle
cpos = pl.show(return_cpos=True)

# ###########################################################
# Plot the winding potential / 3D
# ###########################################################

# create a plotter
pl = pv.Plotter(window_size=(1024, 768))

# add the geometry
pl.add_mesh(potential, scalars="potential", cmap=cmap_potential, clim=clim_potential)
pl.add_mesh(core, color="gray")

# plot, save, and crop margin
pl.show(screenshot="render/mesh_winding_3D.png", cpos=cpos)
utils_pv.get_crop("render/mesh_winding_3D.png", margin=25)

# ###########################################################
# Plot the core field / 3D
# ###########################################################

# create a plotter
pl = pv.Plotter(window_size=(1024, 768))

# add the geometry
pl.add_mesh(field, scalars="field", cmap=cmap_field, clim=clim_field)
pl.add_mesh(coil, color="orange")

# plot, save, and crop margin
pl.show(screenshot="render/mesh_core_3D.png", cpos=cpos)
utils_pv.get_crop("render/mesh_core_3D.png", margin=25)

# ###########################################################
# Plot the winding potential / 2D
# ###########################################################

# create a plotter
pl = pv.Plotter(window_size=(1024, 768), lighting="none")

# create a 2D slice of the 3D solution
potential = potential.slice(normal=(0.0, 1.0, 0.0), origin=(0.0, 0.0, 0.0))
core = core.clip(normal=(0.0, 1.0, 0.0), origin=(0.0, 0.0, 0.0))

# add the geometry
pl.add_mesh(potential, scalars="potential", cmap=cmap_potential, clim=clim_potential)
pl.add_mesh(core, color="gray")

# plot, save, and crop margin
pl.enable_2d_style()
pl.enable_parallel_projection()
pl.show(screenshot="render/mesh_winding_2D.png", cpos="xz")
utils_pv.get_crop("render/mesh_winding_2D.png", margin=25)

# ###########################################################
# Plot the core field / 2D
# ###########################################################

# create a plotter
pl = pv.Plotter(window_size=(1024, 768), lighting="none")

# create a 2D slice of the 3D solution
field = field.slice(normal=(0.0, 1.0, 0.0), origin=(0.0, 0.0, 0.0))
coil = coil.clip(normal=(0.0, 1.0, 0.0), origin=(0.0, 0.0, 0.0))

# add the geometry
pl.add_mesh(field, scalars="field", cmap=cmap_field, clim=clim_field)
pl.add_mesh(coil, color="orange")

# plot, save, and crop margin
# pl.enable_2d_style()
pl.enable_parallel_projection()
pl.show(screenshot="render/mesh_core_2D.png", cpos="xz")
utils_pv.get_crop("render/mesh_core_2D.png", margin=25)
