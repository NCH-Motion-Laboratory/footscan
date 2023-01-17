import matplotlib.pylab as plt
from footscan import Step

FNAME = '/home/andrey/storage/Data/Gait_Lab/footscan_export_test/test_test_-_Session_3_-_12-1-2023_-_CadCam_L1.apd'

sc = Step(FNAME)

plt.figure()
plt.imshow(sc.dti)



plt.figure()
plt.imshow(sc.dtis.max(axis=2))



plt.figure()
frame = sc.dtis[:,:,700]
frame[frame==-1] = 0
plt.imshow(frame)

print(frame.sum() * 0.762 * 0.508)


plt.show()
