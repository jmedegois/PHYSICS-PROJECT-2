from astropy.io import fits
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.mlab as mlab
import pandas as pd
from IPython import embed
import pandas
from astropy.table import Table
import smallPrograms as smalls
from scipy.misc import imresize
from astropy.time import Time as Time

catFiles = smalls.fileInputList(
    '/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/LightcurveTextFiles/CatsDir')[:-1]
recnosFiles = smalls.fileInputList(
    '/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/LightcurveTextFiles/RecnosList')[:-1]
recnos = np.asarray(recnosFiles)
recnos = recnos.astype(np.int)


dat = Table.read(catFiles[0], format='fits')
df = dat.to_pandas()
df['recno']=df['recno'].astype(int)
df=df[df['recno'].isin(recnos)]#select only rows that have recnos in recnos list
joinedCat=df
count=len(joinedCat.columns)

for ii in range(1,len(catFiles)):
    dat = Table.read(catFiles[ii], format='fits')
    df = dat.to_pandas()
    df['recno'] = df['recno'].astype(int)
    df = df[df['recno'].isin(recnos)]  # select only rows that have recnos in recnos list
    joinedCat = joinedCat.merge(df, left_on='recno', right_on='recno', how='outer')
    joinedCat=joinedCat.drop(joinedCat.columns[count:count+4],axis=1)
    count=len(joinedCat.columns)
    print ii/(len(catFiles)+0.0001)
joinedCat.drop_duplicates(subset='recno', inplace=True)
array=joinedCat.as_matrix()

fluxes = array[:, 5::7]
fluxes = np.asfarray(fluxes, dtype='float')
catNum = array[:, 4]
catNum = np.asarray(catNum, dtype='int')
obsTime = array[:, 11::7]
obsTime = np.asarray(obsTime, dtype='string')
Mag = array[:, 2]
Mag = np.asfarray(Mag, dtype='float')



containsMesurement = ~np.isnan(fluxes)
fluxesLists = [None] * len(containsMesurement)
obsTimeLists = [None] * len(containsMesurement)
for ii in range(len(containsMesurement)):
    fluxesLists[ii] = fluxes[ii][containsMesurement[ii]]
    obsTimeLists[ii] = obsTime[ii][containsMesurement[ii]]
    obsTimeLists[ii] = pd.to_datetime(obsTimeLists[ii])
    obsTimeLists[ii] = obsTimeLists[ii].to_julian_date()
    np.array(obsTimeLists[ii])
    times=np.array(obsTimeLists[ii])
    for kk in range(1,len(times)):
        difference=times[kk]-times[kk-1]
        if difference>0.2:
            times[kk:]=np.subtract(times[kk:],0.6)
    plt.figure(ii)
    plt.scatter(times, fluxesLists[ii])
    plt.ylim(0,max(fluxesLists[ii]))
    plt.title(str(Mag[ii]))
plt.show()
embed()



