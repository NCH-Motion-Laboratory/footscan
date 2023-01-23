import matplotlib.pylab as plt
from footscan import Step

FNAME = '/home/andrey/storage/Data/Gait_Lab/footscan_export_test/test_test_-_Session_3_-_12-1-2023_-_CadCam_L1.apd'

sc = Step(FNAME)


plt.figure()
plt.imshow(sc.dtis[:,:,700])





plt.show()
