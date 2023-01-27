import numpy as np

import matplotlib.pylab as plt

from footscan import Session, zeropad

FPEF_BEFORE = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\kävely\\Anne_Aho_-_Session_11_-_20-12-2022_-_CadCam_'
FPEF_AFTER = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\kävely\\Anne_Aho_-_Session_21_-_20-12-2022_-_CadCam_'
OUT_FNAME_TEMPL = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\kävely\\out\\frame_%07i.png'
OUT_FNAME_MAX = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\kävely\\out\\max.png'

NSTEPS = 6
NPAD_ROW = 10
NPAD_COL = 10
CMAP = 'Wistia'
DPI = 300

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
all_max = all.max(axis=2)
backgr = all_max.copy()
all_max[all_max==-1] = np.nan
backgr[backgr>-1] = 0
all[all==-1] = np.nan

plt.figure()

for i in range(maxf):
    plt.clf()
    plt.matshow(backgr, vmin=-1, vmax=6, cmap='binary')
    plt.matshow(all[:, :, i], fignum=0, aspect=s_before.steps[0].dx / s_before.steps[0].dy, vmin=0, vmax=maxdata, cmap=CMAP)
    plt.savefig(OUT_FNAME_TEMPL % i, format='png', dpi=DPI)

plt.clf()
plt.matshow(all_max, fignum=0, aspect=s_before.steps[0].dx / s_before.steps[0].dy, vmin=0, vmax=maxdata, cmap=CMAP)
plt.savefig(OUT_FNAME_MAX, format='png', dpi=DPI)