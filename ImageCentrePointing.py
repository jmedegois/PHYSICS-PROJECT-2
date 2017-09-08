import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time
import matplotlib.pyplot as plt
from astropy.io import fits
import smallPrograms as smalls
import numpy as np

files= smalls.fileInputList('/home/jamiedegois/Desktop/pipeStartQuick/ImageCentrePointing.txt')
arrayALT= [None] * (len(files)-1)
arrayAZ= [None] * (len(files)-1)
arrayra= [None] * (len(files)-1)
arraydec= [None] * (len(files)-1)

ref=fits.open(files[0])

for ii in range(0,len(files)-1,1):
    Fits = fits.open(files[ii])



    ### calc alt az
    Loc = EarthLocation(lat =Fits[0].header.get('SITELAT')*u.deg,
                               lon =Fits[0].header.get('SITELONG') * u.deg
                               , height = Fits[0].header.get('SITEALT')*u.m)
    ImageTime = Time(Fits[0].header.get('DATE-OBS'), format='isot', scale='utc')
    Coordinate = SkyCoord(ra=Fits[0].header.get('CRVAL1')*u.deg,
                                 dec=Fits[0].header.get('CRVAL2')*u.deg,
                                 frame='icrs',
                                 location = Loc
                                 ,obstime = ImageTime )
    alt=Coordinate.altaz.alt*u.deg
    az=Coordinate.altaz.az*u.deg
    arrayAZ[ii]=az.value
    arrayALT[ii] = alt.value


    ### calc Ra Dec for ref image
    refLoc = EarthLocation(lat=ref[0].header.get('SITELAT') * u.deg,
                        lon=ref[0].header.get('SITELONG') * u.deg
                        , height=ref[0].header.get('SITEALT') * u.m)
    refTime = Time(ref[0].header.get('DATE-OBS'), format='isot', scale='utc')
    newCoordinate = SkyCoord(alt=Coordinate.altaz.alt,
                             az=Coordinate.altaz.az,
                             obstime=refTime,
                             frame='altaz',
                             location=refLoc)
    ra = newCoordinate.icrs.ra.degree - 6641.32/60
    dec = newCoordinate.icrs.dec.degree + 1614.9/60
    arrayra[ii] = ra*60
    arraydec[ii] = dec*60

    print ra*60
    print dec * 60

    print ii

# plt.figure(0)
# plt.plot(arrayra,arraydec)
# plt.xlim(-10,10)
# plt.ylim(-10,10)
# plt.show()

plt.figure(0,figsize=(10,10))
for jj in range(31):

    plt.subplot(5,7,jj+1)
    plt.plot(arrayra[jj*70:70+jj*70:1],arraydec[jj*70:70+jj*70:1],)
    plt.title(str(jj+1))
    plt.xlim(-10,10)
    plt.ylim(-10,10)
    plt.xticks(range(-10,11,5),color=(0,0,0,0))
    plt.yticks(range(-10, 11, 5), color=(0, 0, 0, 0))
    plt.grid(True)
plt.suptitle('10x10 arcmin +RECALC CENTRE ONLY')
plt.show()

plt.figure(0,figsize=(10,10))
for jj in range(31):

    plt.subplot(5,7,jj+1)
    plt.plot(arrayra[jj*70:70+jj*70:1],arraydec[jj*70:70+jj*70:1],)
    plt.title(str(jj+1))
    plt.xlim(-2,2)
    plt.ylim(-2,2)
    plt.xticks(range(-2,2,1),color=(0,0,0,0))
    plt.yticks(range(-2,2,1), color=(0, 0, 0, 0))
    plt.grid(True)
plt.suptitle('2x2 arcmin +RECALC CENTRE ONLY')
plt.show()

plt.figure(0,figsize=(10,10))
for jj in range(31):

    plt.subplot(5,7,jj+1)
    plt.plot(arrayra[jj*70:70+jj*70:1],arraydec[jj*70:70+jj*70:1],)
    plt.title(str(jj+1))
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xticks([-0.5,0,0.5],color=(0,0,0,0))
    plt.yticks([-0.5,0,0.5], color=(0, 0, 0, 0))
    plt.grid(True)
plt.suptitle('1x1 arcmin +RECALC CENTRE ONLY')
plt.show()












