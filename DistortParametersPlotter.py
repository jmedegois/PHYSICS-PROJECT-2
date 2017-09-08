import matplotlib.pyplot as plt
import numpy as np
import smallPrograms as smalls
import astropy.io.fits as fits
import astropy.wcs as wcs
import os


ImageFiles = smalls.fileInputList('/home/jamiedegois/Desktop/pipeStartQuick/Quiver/ImageFiles.txt')
y=np.zeros((len(ImageFiles),137))
for ii in range(0, len(ImageFiles)-1, 1):



    ####### XY acurate ###############
    filename = os.path.join(wcs.__path__[0], ImageFiles[ii])
    hdulist = fits.open(filename)
    w = wcs.WCS(hdulist[0].header, hdulist)
    hdulist.close()


    for jj in range(0,140,1):

        OBSTIME = hdulist[0].header[jj]
        if isinstance(OBSTIME, float):
            y[ii,jj]=OBSTIME
            print "ii:" +str(ii) +" jj:"+str(jj)

count=1
for kk in range(0,137,1):
    if (y[-14:-13,kk])>0.000000001:
        plt.subplot(6,6,count)
        plt.plot(range(10,135,1),y[10:-3,kk-1])
        plt.title(str(kk))
        count=count+1
plt.show()


    # xDiff=np.subtract(xCat,xImage)
    # yDiff=np.subtract(yCat,yImage)
    #
    # plt.subplot(4, 5, np.mod(ii,20)+1)
    # plt.title('')
    # M = np.hypot(xDiff,yDiff)
    # Q = plt.quiver(xImage, yImage, xDiff,yDiff,M, scale=8, scale_units='inches')
    # cb = plt.colorbar(Q)
    # plt.xticks(range(-10, 11, 5), color=(0, 0, 0, 0))
    # plt.yticks(range(-10, 11, 5), color=(0, 0, 0, 0))
    # plt.title(str(ii + 3))
#
# plt.subplots_adjust(left=0.08, bottom=0.01, right=0.94, top=0.97, wspace=0.00, hspace=0.00)
# plt.show()