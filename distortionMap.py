from astropy.wcs import WCS
import numpy as np
import math
from astropy.io import fits

####note n= x map
####note n1= y map
####note n2= diag map
####note n3= sky area map
####note n4= flux multiplier map
def skyDistance(inRA1,inDec1,inRA2,inDec2):#input in degrees, output in arcseconds...can take np arrays :)
    inRA1=np.multiply(inRA1,(math.pi/180))
    inRA2 = np.multiply(inRA2, (math.pi / 180))
    inDec1 = np.multiply(inDec1, (math.pi / 180))
    inDec2 = np.multiply(inDec2, (math.pi / 180))
    return np.arccos(      np.sin(inDec1)*np.sin(inDec2) +  np.cos(inDec1)*np.cos(inDec2)*np.cos(inRA1-inRA2)   )*(180/math.pi)*3600


w = WCS('/media/jamiedegois/JaimedeGois2TBPortable/swarpOutput/QUICK01_2016-01-10_151153_DSC_0530-G.fitsco-add.fits')
x=6018
y=4863

RA = np.transpose(np.zeros((x,y+1)))
DEC= np.transpose(np.zeros((x,y+1)))
mapX=np.transpose(np.zeros((x,y)))

for ii in range(0,y+1):
    RA[ii], DEC[ii] = w.all_pix2world(range(0,x,1),ii,0)#x then y
    print ii
    if(ii>0):
        mapX[ii-1]=skyDistance(RA[ii-1],DEC[ii-1],RA[ii],DEC[ii])

print RA
print DEC

hdu=fits.PrimaryHDU(mapX)
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/n.fits',overwrite=True)



###########inverse metric ie Y MAP
w = WCS('/media/jamiedegois/JaimedeGois2TBPortable/swarpOutput/QUICK01_2016-01-10_151153_DSC_0530-G.fitsco-add.fits')
x=6018
y=4863

RA = np.transpose(np.zeros((x+1,y)))
DEC= np.transpose(np.zeros((x+1,y)))
mapY=np.transpose(np.zeros((x,y)))

for ii in range(0,x+1):
    RA[::,ii], DEC[::,ii] = w.all_pix2world(ii,range(0,y,1),0)#x then y
    print ii
    if(ii>0):
        mapY[::,ii-1]=skyDistance(RA[::,ii-1],DEC[::,ii-1],RA[::,ii],DEC[::,ii])

print RA
print DEC

hdu=fits.PrimaryHDU(mapY)
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/n1.fits',overwrite=True)
##################diagonal map
hdu=fits.PrimaryHDU(np.divide(np.hypot(mapX,mapY),1.414213562))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/n2.fits',overwrite=True)

################## sky area map (in square arc seconds)
hdu=fits.PrimaryHDU(np.multiply(mapX,mapY))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/n3.fits',overwrite=True)

################## flux multiplier map  see log book page 48 for formula y= -1.5*10^-4(sky area) +1.713025
hdu=fits.PrimaryHDU(np.add(np.multiply(np.multiply(mapX,mapY),-0.00015),+1.713025 ))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/n4.fits',overwrite=True)