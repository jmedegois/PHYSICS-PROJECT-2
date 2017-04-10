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


csv1 = np.genfromtxt ('/home/jamiedegois/Desktop/Position_dependancy/allsmall', delimiter=",")
csv= np.transpose(csv1)
#
# ##as a function of distance from middle x
# for ii in range(len(csv[0])):
#     if(csv[-1,ii]>25000):
#         y=csv[4:-1:6,ii]
#         x=csv[6::6,ii]
#         x=abs(runningMeanFast(x,1)-3000)
#         y=y*(1/csv[-1,ii])
#         y=runningMeanFast(y,1)
#         plt.ylim([0.5, 1.5])
#         plt.xlim([0, 3000])
#         plt.grid(True)
#         plt.scatter(x, y,s=15)
#
plt.show()

##as a function of distance from center
for ii in range(len(csv[0])):
    if(csv[-1,ii]>7500):
        y=csv[4:-1:6,ii]
        x=np.hypot(csv[6:-1:6,ii]-3000,csv[7::6,ii]-2400)
        y=y*(1/csv[-1,ii])
        x = runningMeanFast(x, 1)
        y = runningMeanFast(y, 1)
        plt.ylim([0.5, 1.5])
        plt.xlim([0, 3200])
        plt.grid(True)
        plt.scatter(x, y,s=0.2)
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

#######as a function of pixel scale
from astropy.io import fits

hdulist = fits.open('/home/jamiedegois/Desktop/n2.fits')
pixelScale= hdulist[0].data

for ii in range(len(csv[0])):
    if(csv[-1,ii]>7500):
        y=csv[4:-1:6,ii]
        x= np.round(csv[6:-1:6,ii])
        x1=np.round(csv[6:-1:6,ii])
        x2=np.round(csv[7::6,ii])
        y=y*(1/csv[-1,ii])
        for jj in range(len(x1)):
            if np.isnan(x1[jj]):
                x1[jj]=0
            else:
                # print np.int(x1[jj])
                # print np.int(x2[jj])
                x[jj]=pixelScale[(np.int(x2[jj]-2)),(np.int(x1[jj]-2))]###    why2 ? close enough and stoped index errors (pixel scale wont change over 2 pixels)
                # print x[jj]
        plt.ylim([0.5, 1.5])
        plt.xlim([35, 70])
        plt.grid(True)
        plt.scatter(x, y,s=0.2)

plt.show()

#######as a function of pixel scale
from astropy.io import fits

hdulist1 = fits.open('/home/jamiedegois/Desktop/n.fits')
pixelScale1= hdulist1[0].data
hdulist2 = fits.open('/home/jamiedegois/Desktop/n1.fits')
pixelScale2= hdulist2[0].data

for ii in range(len(csv[0])):
    if(csv[-1,ii]>7500):
        y=csv[4:-1:6,ii]
        x= np.round(csv[6:-1:6,ii])
        x1=np.round(csv[6:-1:6,ii])
        x2=np.round(csv[7::6,ii])
        y=y*(1/csv[-1,ii])
        for jj in range(len(x1)):
            if np.isnan(x1[jj]):
                x1[jj]=0
            else:
                # print np.int(x1[jj])
                # print np.int(x2[jj])
                x[jj]=pixelScale1[(np.int(x2[jj]-2)),(np.int(x1[jj]-2))]*pixelScale2[(np.int(x2[jj]-2)),(np.int(x1[jj]-2))]###    why2 ? close enough and stoped index errors (pixel scale wont change over 2 pixels)
                # print x[jj]
        plt.ylim([0.5, 1.5])
        plt.xlim([35*35, 70*70])
        plt.grid(True)
        plt.scatter(x, y,s=0.2)

plt.show()


