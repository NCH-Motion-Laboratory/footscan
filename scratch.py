import numpy as np

import matplotlib.pylab as plt

from footscan import Session

FPEF_BEFORE = '/home/andrey/scratch/footscan_pain/AA/kävely/Anne_Aho_-_Session_11_-_20-12-2022_-_CadCam_'
FPEF_AFTER = '/home/andrey/scratch/footscan_pain/AA/kävely/Anne_Aho_-_Session_21_-_20-12-2022_-_CadCam_'
OUT_FNAME_TEMPL = '/home/andrey/scratch/footscan_pain/AA/kävely/out/frame_%07i.png'
OUT_FNAME_MAX = '/home/andrey/scratch/footscan_pain/AA/kävely/out/max.png'

NSTEPS = 6
NPAD_ROW = 10
NPAD_COL = 10
CMAP = 'Wistia'
DPI = 300

s_before = Session(FPEF_BEFORE)
s_after = Session(FPEF_AFTER)


step = s_before.steps[0]

plt.matshow(step.data[:,:,100], extent=step.extent, origin=step.origin)
plt.plot(step.cop_x, step.cop_y)
plt.show()