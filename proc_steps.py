import numpy as np

import matplotlib.pylab as plt

from footscan import Session

FPEF_BEFORE = '/home/andrey/scratch/footscan_pain/AA/kävely/Anne_Aho_-_Session_11_-_20-12-2022_-_CadCam_'
FPEF_AFTER = '/home/andrey/scratch/footscan_pain/AA/kävely/Anne_Aho_-_Session_21_-_20-12-2022_-_CadCam_'
OUT_FNAME_TEMPL = '/home/andrey/scratch/footscan_pain/AA/kävely/out/frame_%07i.png'

#FPEF_BEFORE = '/home/andrey/scratch/footscan_pain/MG/kävely/Mari_Gueye_-_Session_10_-_20-12-2022_-_CadCam_'
#FPEF_AFTER = '/home/andrey/scratch/footscan_pain/MG/kävely/Mari_Gueye_-_Session_20_-_20-12-2022_-_CadCam_'
#OUT_FNAME_TEMPL = '/home/andrey/scratch/footscan_pain/MG/kävely/out/frame_%07i.png'

MAX_NSTEPS = 20
X_MARG = 0.1    # relative to the footprint size
Y_MARG = 0.1    # relative to the footprint size
CMAP = 'Wistia'
DPI = 300

def plot_block(steps, offset, dx, maxdata, cmap, t):
    for step, i in zip(steps, range(len(steps))):
        # if past the last frame, redraw the last frame
        # if you want to normalize all the steps to the same cycle length,
        # you'll need to change the line below
        nt = min(t, step.data.shape[2] - 1)

        ext = np.array(step.extent).copy()
        ext[:2] += (offset[0] + (i * dx))
        ext[2:] += offset[1]

        # Plot the backgound
        backgr = step.data.max(axis=2)
        backgr[backgr > -1] = 0
        plt.imshow(backgr, vmin=-1, vmax=6, cmap='binary', extent=list(ext), origin=step.origin)

        # Plot the pressure map
        step_data = (step.data[:, :, nt]).copy()
        step_data[step_data == -1] = np.nan
        plt.imshow(step_data, vmin=0, vmax=maxdata, cmap=cmap, extent=list(ext), origin=step.origin)

        plt.plot(step.cop_x + (offset[0] + (i * dx)), step.cop_y + offset[1], color='b', linewidth=1)
        plt.plot(step.cop_x[nt] + (offset[0] + (i * dx)), step.cop_y[nt] + offset[1], color='b', marker='o', markersize=2)


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
maxy = max(abs(s.extent[2] - s.extent[3]) for s in steps_all) * (1 + Y_MARG)
maxf = max(s.data.shape[2] for s in steps_all)
maxdata = max(s.data.max() for s in steps_all)

plt.figure()

for t in range(maxf):
    plt.clf()
    plot_block(steps_before_left, (0, 0), maxx, maxdata, CMAP, t)
    plot_block(steps_before_right, (maxx * nsteps, 0), maxx, maxdata, CMAP, t)
    plot_block(steps_after_left, (0, maxy), maxx, maxdata, CMAP, t)
    plot_block(steps_after_right, (maxx * nsteps, maxy), maxx, maxdata, CMAP, t)

    plt.axis('off')
    plt.savefig(OUT_FNAME_TEMPL % t, format='png', dpi=DPI,  bbox_inches='tight')
