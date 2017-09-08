from astropy.io import fits
import numpy as np
import math
from IPython import embed

def fileInputList(txtFileDirectory):
    f = open(txtFileDirectory)
    data= f.read()
    data= data.split("\n")
    return data

def addAdress(inFitsDirectory,seperationColNumber,alphaColNumber,deltaColNumber):
    fitsTable = fits.open(inFitsDirectory)
    for ii in range(0,len(fitsTable[1].data),1):
        if math.isnan(fitsTable[1].data[ii][seperationColNumber-1]):
            if math.isnan(fitsTable[1].data[ii][0]):
                fitsTable[1].data[ii][0]=fitsTable[1].data[ii][alphaColNumber-1]
                fitsTable[1].data[ii][1] = fitsTable[1].data[ii][deltaColNumber-1]
                fitsTable[1].data[ii][2] = 1
        else:
            fitsTable[1].data[ii][2] = fitsTable[1].data[ii][2]+1
    fitsTable.writeto(inFitsDirectory,clobber=True)

def giveCropingCo_ords(undersampled_map,min__zeros_to_crop=3):
    x_1=0
    y_1=0
    x_2=len(undersampled_map)
    y_2=len(undersampled_map)
    keepdoing=True
    undersampled_map1=undersampled_map
    while keepdoing==True:
        max_numx_1=np.count_nonzero(np.less(undersampled_map1[::,0],0.001))
        max_numx_2=np.count_nonzero(np.less(undersampled_map1[::,-1],0.001))
        max_numy_1=np.count_nonzero(np.less(undersampled_map1[0,::],0.001))
        max_numy_2=np.count_nonzero(np.less(undersampled_map1[-1,::],0.001))
        maxNumZeros=max(max_numx_1,max_numx_2,max_numy_1,max_numy_2)
        if maxNumZeros>=min__zeros_to_crop:
            if max_numx_1==maxNumZeros:
                x_1=x_1+1
            if max_numx_2==maxNumZeros:
                x_2=x_2-1
            if max_numy_1==maxNumZeros:
                y_1=y_1+1
            if max_numy_2==maxNumZeros:
                y_2=y_2-1
        else:
            keepdoing=False
        undersampled_map1=undersampled_map[y_1:y_2,x_1:x_2]
    return x_1,x_2,y_1,y_2,undersampled_map1







