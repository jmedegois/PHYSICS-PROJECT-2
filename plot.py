from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import math
import numpy as np
import matplotlib.pyplot as plt
########################################################################################################
#This program takes a csv and then make it a 2 dimentional array and then allows you to plot stuff with it
########################################################################################################


def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]


csv1 = np.genfromtxt ('/home/jamiedegois/Desktop/Huge', delimiter=",")
csv= np.transpose(csv1)

for ii in range(len(csv[0])):
    if(csv[-1,ii]>25000):
        y=csv[4:-1:6,ii]
        x=csv[6::6,ii]
        x=abs(runningMeanFast(x,1)-3000)
        y=y*(1/csv[-1,ii])
        y=runningMeanFast(y,1)
        plt.ylim([0.5, 1.5])
        plt.xlim([0, 3000])
        plt.grid(True)
        plt.scatter(x, y,s=15)

plt.show()

for ii in range(len(csv[0])):
    if(csv[-1,ii]>25000):
        y=csv[4:-1:6,ii]
        x=np.hypot(csv[6:-1:6,ii]-3000,csv[7::6,ii]-2400)
        y=y*(1/csv[-1,ii])
        x = runningMeanFast(x, 1)
        y = runningMeanFast(y, 1)
        plt.ylim([0.5, 1.5])
        plt.xlim([0, 3200])
        plt.grid(True)
        plt.scatter(x, y,s=15)

plt.show()

######################x-y positions of stars####################
# for ii in range(len(csv[0])):
#     if(csv[-1,ii]>10000):
#         x=csv[6:-1:6,ii]
#         y=csv[7::6,ii]
#         plt.ylim([0,5000])
#         plt.xlim([0, 7000])
#         plt.grid(True)
#         plt.scatter(x, y,s=5)
#
# plt.show()



