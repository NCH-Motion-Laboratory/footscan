import numpy as np

import pyvista as pv
from footscan import Session


FPEF_BEFORE = '/home/andrey/scratch/footscan_pain/AA/kävely/Anne_Aho_-_Session_11_-_20-12-2022_-_CadCam_'
FPEF_AFTER = '/home/andrey/scratch/footscan_pain/AA/kävely/Anne_Aho_-_Session_21_-_20-12-2022_-_CadCam_'

#FPEF_BEFORE = '/home/andrey/scratch/footscan_pain/MG/kävely/Mari_Gueye_-_Session_10_-_20-12-2022_-_CadCam_'
#FPEF_AFTER = '/home/andrey/scratch/footscan_pain/MG/kävely/Mari_Gueye_-_Session_20_-_20-12-2022_-_CadCam_'

T_SCALE = 0.5
MAX_NSTEPS = 20
X_MARG = 0.2    # relative to the footprint size

s_before = Session(FPEF_BEFORE)
s_after = Session(FPEF_AFTER)

steps_before_left = [s for s in s_before.steps if s.context=='L']
steps_before_right = [s for s in s_before.steps if s.context=='R']
steps_after_left = [s for s in s_after.steps if s.context=='L']
steps_after_right = [s for s in s_after.steps if s.context=='R']

nsteps = min(len(steps_before_left), len(steps_after_left), len(steps_before_right), len(steps_after_right), MAX_NSTEPS)
steps_before_left = steps_before_left[:nsteps]
steps_after_left = steps_after_left[:nsteps]
steps_before_right = steps_before_right[:nsteps]
steps_after_right = steps_after_right[:nsteps]

steps_all = steps_before_left + steps_before_right + steps_after_left + steps_after_right

# Find max dimensions, data value
maxx = max(abs(s.extent[1] - s.extent[0]) for s in steps_all) * (1 + X_MARG)
maxt = max(s.data.shape[2] for s in steps_all)

t_scale = T_SCALE * np.mean((steps_all[0].dx, steps_all[0].dy))


left_tubes_before = pv.MultiBlock()
right_tubes_before = pv.MultiBlock()
left_tubes_after = pv.MultiBlock()
right_tubes_after = pv.MultiBlock()
tubes_t = pv.MultiBlock()

for step in steps_before_left:
    points = np.column_stack((step.cop_x, step.cop_y, t_scale * np.arange(step.data.shape[2])))
    tube = pv.Spline(points, 1000).tube(radius=0.5)
    left_tubes_before.append(tube)

for step in steps_before_right:
    points = np.column_stack((step.cop_x + maxx, step.cop_y, t_scale * np.arange(step.data.shape[2])))
    tube = pv.Spline(points, 1000).tube(radius=0.5)
    right_tubes_before.append(tube)

for step in steps_after_left:
    points = np.column_stack((step.cop_x, step.cop_y, t_scale * np.arange(step.data.shape[2])))
    tube = pv.Spline(points, 1000).tube(radius=0.5)
    left_tubes_after.append(tube)

for step in steps_after_right:
    points = np.column_stack((step.cop_x + maxx, step.cop_y, t_scale * np.arange(step.data.shape[2])))
    tube = pv.Spline(points, 1000).tube(radius=0.5)
    right_tubes_after.append(tube)

points = np.column_stack((0.5*maxx*np.ones(maxt), np.zeros(maxt), t_scale * np.arange(maxt)))
tube = pv.Spline(points, 1000).tube(radius=0.5)
tubes_t.append(tube)

p = pv.Plotter()
p.add_mesh(left_tubes_before, smooth_shading=True, color="r")
p.add_mesh(right_tubes_before, smooth_shading=True, color="g")
p.add_mesh(left_tubes_after, smooth_shading=True, color="b")
p.add_mesh(right_tubes_after, smooth_shading=True, color="b")
p.add_mesh(tubes_t, smooth_shading=True, color="k")
p.set_background([0.7, 0.7, 0.7])
p.show()