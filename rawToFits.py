import rawpy
import numpy as np
import matplotlib.pyplot as plt

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

raw = rawpy.imread("/home/jamiedegois/Desktop/cammera exp/part 3/DSC_1066.NEF")
temp=raw.raw_image

greenPixels1=np.reshape(temp[:4928:2,1:7380:2],9092160)
greenPixels2=np.reshape(temp[1:4928:2,0:7380:2],9092160)
greenPixels=np.concatenate((greenPixels1,greenPixels2))
greenPixelsNoOutliers=reject_outliers(greenPixels,3)

print "Std dev is:"+str(np.std(greenPixels))
print "Min is    :"+str(np.amin(greenPixels))
print "Max is    :"+str(np.amax(greenPixels))
print "Mean is   :"+str(np.mean(greenPixels))
print "Median is :"+str(np.median(greenPixels))

plt.hist(greenPixels, bins=400,log=True)
plt.show()

