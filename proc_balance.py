import numpy as np

import matplotlib.pylab as plt

from footscan import Step, zeropad

"""
FNAME_BEFORE = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_seisominen - vasen\\Anne_Aho_-_Session_8_-_20-12-2022_-_CadCam_L1.apd'
FNAME_AFTER = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_seisominen - vasen\\Anne_Aho_-_Session_18_-_20-12-2022_-_CadCam_L1'
OUT_FNAME_TEMPL = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_seisominen - vasen\\out\\frame_%07i.png'
OUT_FNAME_MAX = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_seisominen - vasen\\out\\max.png'
"""

FNAME_BEFORE = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_päkiälle_nosto - vasen\\Anne_Aho_-_Session_10_-_20-12-2022_-_CadCam_L1.apd'
FNAME_AFTER = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_päkiälle_nosto - vasen\\Anne_Aho_-_Session_20_-_20-12-2022_-_CadCam_R1.apd'
OUT_FNAME_TEMPL = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_päkiälle_nosto - vasen\\out\\frame_%07i.png'
OUT_FNAME_MAX = 'C:\\Users\\HUS86357138\\scratch\\footscan_pain\\AA\\yhden_jalan_päkiälle_nosto - vasen\\out\\max.png'

NPAD_ROW = 10
NPAD_COL = 10
CMAP = 'Wistia'
DPI = 300
ROT = 1
# ROT = -1

s_before = Step(FNAME_BEFORE)
s_after = Step(FNAME_AFTER)

# Find max dimensions, data value
maxr = max(s_before.data.shape[0], s_after.data.shape[0]) + NPAD_ROW
maxc = max(s_before.data.shape[1], s_after.data.shape[1]) + NPAD_COL
maxf = max(s_before.data.shape[2], s_after.data.shape[2])
maxdata = max(s_before.data.max(), s_after.data.max())

# Pad the data
data_before = zeropad(maxr, maxc, maxf, s_before.data)
data_after = zeropad(maxr, maxc, maxf, s_after.data)

all = np.concatenate((data_before, data_after), axis=1)
all = np.rot90(all, ROT)

all_max = all.max(axis=2)
backgr = all_max.copy()
all_max[all_max==-1] = np.nan
backgr[backgr>-1] = 0
all[all==-1] = np.nan

plt.figure()

for i in range(maxf):
    plt.clf()
    plt.matshow(backgr, vmin=-1, vmax=6, cmap='binary')
    plt.matshow(all[:, :, i], fignum=0, aspect=s_before.dy / s_before.dx, vmin=0, vmax=maxdata, cmap=CMAP)
    plt.savefig(OUT_FNAME_TEMPL % i, format='png', dpi=DPI)

plt.clf()
plt.matshow(all_max, fignum=0, aspect=s_before.dy / s_before.dx, vmin=0, vmax=maxdata, cmap=CMAP)
plt.savefig(OUT_FNAME_MAX, format='png', dpi=DPI)