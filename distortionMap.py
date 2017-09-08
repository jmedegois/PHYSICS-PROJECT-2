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


w = WCS('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalImages/QUICK01_2016-02-01_163824_DSC_0761-G.fitsco-add.fits')
x=6000
y=6000

RA = np.transpose(np.zeros((x,y)))
DEC= np.transpose(np.zeros((x,y)))

mapX=np.transpose(np.zeros((x,y)))#initialise
mapY=np.transpose(np.zeros((x,y)))#initialise

####################X_DIFF MAP##############################################################################3

for ii in range(0,y):
    RA[ii], DEC[ii] = w.all_pix2world(range(0,x,1),ii,0)#x then y
    print ii
    if(ii>0):
        mapX[ii-1]=skyDistance(RA[ii-1],DEC[ii-1],RA[ii],DEC[ii])
mapX[x-1]=mapX[x-2]
print RA
print DEC

hdu=fits.PrimaryHDU(mapX)
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/X_DIFF_MAP.fits',overwrite=True)



###########Y _DIFF MAP MAP##############################################################################################


for ii in range(0,x):
    RA[::,ii], DEC[::,ii] = w.all_pix2world(ii,range(0,y,1),0)#x then y
    print ii
    if(ii>0):
        mapY[::,ii-1]=skyDistance(RA[::,ii-1],DEC[::,ii-1],RA[::,ii],DEC[::,ii])


print RA
print DEC
mapY[::,y-1]=mapY[::,y-2]
hdu=fits.PrimaryHDU(mapY)
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/Y_DIFF_MAP.fits',overwrite=True)
# ##################diagonal map
# hdu=fits.PrimaryHDU(np.divide(np.hypot(mapX,mapY),1.414213562))
# hdulist = fits.HDUList([hdu])
# hdulist.writeto('/home/jamiedegois/Desktop/n2.fits',overwrite=True)
#
# ################## sky area map (in square arc seconds)
# hdu=fits.PrimaryHDU(np.multiply(mapX,mapY))
# hdulist = fits.HDUList([hdu])
# hdulist.writeto('/home/jamiedegois/Desktop/n3.fits',overwrite=True)
#
# ################## flux multiplier map  see log book page 48 for formula y= -1.5*10^-4(sky area) +1.713025
# hdu=fits.PrimaryHDU(np.add(np.multiply(np.multiply(mapX,mapY),-0.00015),+1.713025 ))
# hdulist = fits.HDUList([hdu])
# hdulist.writeto('/home/jamiedegois/Desktop/n4.fits',overwrite=True)
#
# ################## flux multiplier map2  see log book page 54 for formula y= -.27*10^-4(sky area) +1.1283
# hdu=fits.PrimaryHDU(np.add(np.multiply(np.multiply(mapX,mapY),-0.000027),+1.1283 ))
# hdulist = fits.HDUList([hdu])
# hdulist.writeto('/home/jamiedegois/Desktop/n5.fits',overwrite=True)

# ################## flux multiplier map1.1  see log book page 57 for formula y= -1.75*10^-4(sky area) +1.8318625
# hdu=fits.PrimaryHDU(np.add(np.multiply(np.multiply(mapX,mapY),-0.000175),+1.8318625 ))
# hdulist = fits.HDUList([hdu])
# hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/n4.1.fits',overwrite=True)

################## sky pixel area map
hdu=fits.PrimaryHDU(np.multiply(mapX,mapY))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/SKY_PIXEL_AREA_MAP.fits',overwrite=True)

################## flux multiplier map1.2  see log book page 60 for formula y= -1.66141023279*10^-4(sky area) +1.56258808361
hdu=fits.PrimaryHDU(np.add(np.multiply(np.multiply(mapX,mapY),-0.000166141023279),1.56258808361 ))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/FIRST_ORDER_MAP.fits',overwrite=True)

################## flux multiplier map2.2  see log book page 64 for formula
def cubicReg(m3,m2,m1,constant,x):
    firstTerm = np.multiply(x, m1)
    secondTerm = np.multiply(np.multiply(x, m2),x)
    thirdTerm = np.multiply(np.multiply(np.multiply(x, m3),x),x)
    return np.add(np.add(np.add(firstTerm, constant), secondTerm), thirdTerm)

hdu=fits.PrimaryHDU(cubicReg(-1.23018181754e-11,1.22080323835e-07,-0.000383656437,1.38505051602,np.multiply(mapX,mapY)))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/SECOND_ORDER_MAP.fits',overwrite=True)

################## BOTH MAPS IN 1
def cubicReg(m3,m2,m1,constant,x):
    firstTerm = np.multiply(x, m1)
    secondTerm = np.multiply(np.multiply(x, m2),x)
    thirdTerm = np.multiply(np.multiply(np.multiply(x, m3),x),x)
    return np.add(np.add(np.add(firstTerm, constant), secondTerm), thirdTerm)

temp1=cubicReg(-1.23018181754e-11,1.22080323835e-07,-0.000383656437,1.38505051602,np.multiply(mapX,mapY))
temp2=np.add(np.multiply(np.multiply(mapX,mapY),-0.000166141023279),1.56258808361 )
hdu=fits.PrimaryHDU(np.multiply(temp1,temp2))
hdulist = fits.HDUList([hdu])
hdulist.writeto('/home/jamiedegois/Desktop/PHOTO_CORECT_MAPS/Both_MAPS_IN_ONE.fits',overwrite=True)
