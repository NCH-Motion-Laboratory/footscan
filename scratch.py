import numpy as np

import matplotlib.pylab as plt

from footscan import Session

FPEF_BEFORE = '/home/andrey/storage/Data/Gait_Lab/footscan_export_test/test_test_-_Session_6_-_12-1-2023_-_CadCam_'
FPEF_AFTER = '/home/andrey/storage/Data/Gait_Lab/footscan_export_test/test_test_-_Session_6_-_12-1-2023_-_CadCam_'
NSTEPS = 4
OUT_FNAME_TEMPL = '/home/andrey/scratch/out/frame_%07i.png'
NPAD_ROW = 10
NPAD_COL = 10

def zeropad(nr, nc, nf, inp):
    """
    Pad the input sides so that the new size is nr * nc * nf. For the nr and nc
    dimensions split the padding approximately evenly before/after, for the nf
    dimension add all the padding after.
    """
    r, c, f = inp.shape
    dr = nr - r
    dc = nc - c

    r_before = dr // 2
    c_before = dc // 2

    r_after = dr - r_before
    c_after = dc - c_before

    return np.pad(inp, ((r_before, r_after), (c_before, c_after), (0, nf-f)))

s_before = Session(FPEF_BEFORE)
s_after = Session(FPEF_AFTER)

steps_before_left = [s for s in s_before.steps if s.context=='L'][:NSTEPS]
steps_before_right = [s for s in s_before.steps if s.context=='R'][:NSTEPS]
steps_after_left = [s for s in s_after.steps if s.context=='L'][:NSTEPS]
steps_after_right = [s for s in s_after.steps if s.context=='R'][:NSTEPS]

steps_all = steps_before_left + steps_before_right + steps_after_left + steps_after_right

# Find max dimensions, data value
maxr = max(s.data.shape[0] for s in steps_all) + NPAD_ROW
maxc = max(s.data.shape[1] for s in steps_all) + NPAD_COL
maxf = max(s.data.shape[2] for s in steps_all)
maxdata = max(s.data.max() for s in steps_all)

# Pad the data
data_before_left_padded = [zeropad(maxr, maxc, maxf, s.data) for s in steps_before_left]
data_before_right_padded = [zeropad(maxr, maxc, maxf, s.data) for s in steps_before_right]
data_after_left_padded = [zeropad(maxr, maxc, maxf, s.data) for s in steps_after_left]
data_after_right_padded = [zeropad(maxr, maxc, maxf, s.data) for s in steps_after_right]

all_before = np.concatenate(data_before_left_padded + data_before_right_padded, axis=1)
all_after = np.concatenate(data_after_left_padded + data_after_right_padded, axis=1)

all = np.concatenate((all_before, all_after), axis=0)

plt.figure()

for i in range(maxf):
    plt.matshow(all[:, :, i], fignum=0, aspect=s_before.steps[0].dx / s_before.steps[0].dy, vmin=0, vmax=maxdata)
    plt.savefig(OUT_FNAME_TEMPL % i, format='png')
