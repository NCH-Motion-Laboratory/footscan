import numpy as np
import pyvista as pv
import matplotlib.pylab as plt

from footscan import Session

FNAME = '/home/andrey/storage/Data/Gait_Lab/footscan_export_test/test_test_-_Session_6_-_12-1-2023_-_CadCam_'

s = Session(FNAME)

step = s.steps[0]
ny, nx = step.data.shape[:2]
x = np.arange(nx) * step.dx
y = np.arange(ny) * step.dy

x, y = np.meshgrid(x, y)

grid = pv.StructuredGrid(x, y, step.data.max(axis=2))
grid.plot()