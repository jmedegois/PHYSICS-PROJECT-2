from astropy.io import fits
import math

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








