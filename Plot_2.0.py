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

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

def cubicReg(m3,m2,m1,constant,x,m4=0,m5=0):
    firstTerm = np.multiply(x, m1)
    secondTerm = np.multiply(np.multiply(x, m2),x)
    thirdTerm = np.multiply(np.multiply(np.multiply(x, m3),x),x)
    fourthTerm = np.multiply(np.multiply(np.multiply(np.multiply(x,m4), x), x), x)
    fithTerm = np.multiply(np.multiply(np.multiply(np.multiply(np.multiply(x,m5), x), x), x), x)
    return np.add(np.add(np.add(np.add(np.add(firstTerm, constant), secondTerm), thirdTerm),fourthTerm),fithTerm)

Pixel_AREA=fits.open('/home/jamiedegois/Desktop/pipeStartQuick/PHOTO_CORECT_MAPS/SKY_PIXEL_AREA_MAP.fits')[0].data
Map1=fits.open('/home/jamiedegois/Desktop/pipeStartQuick/PHOTO_CORECT_MAPS/Both_MAPS_IN_ONE.fits')[0].data
dat = Table.read('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/2016-02-08._corected_FLAT_with8Feb_.fits', format='fits')
df = dat.to_pandas()
array=df.as_matrix()


mags=array[:,2]
mags=np.asfarray(mags,dtype='float')
y=array[:,5::7]
y=np.asfarray(y,dtype='float')
instrumentMags=np.log10(np.power(y,-2.5))
MagZeroPoint=mags[:,None]-instrumentMags

dx=np.subtract(array[:,7::7], 3000.0)
dx=np.asfarray(dx,dtype='float')
dy=np.subtract(array[:,8::7], 3000.0)
dy=np.asfarray(dy,dtype='float')
#######################subset parameters####################
fluxLwr=3000
fluxUpr=30000000000
LwrLimit=2
UprLimit=2000
ratiolimits=2.0
num_detects=np.count_nonzero(~np.isnan(y),axis=1)
ymean=(np.nanmean(y,axis=1))
selection= np.logical_and(np.logical_and((num_detects>LwrLimit),(num_detects<UprLimit)),np.logical_and((ymean>fluxLwr),(ymean<fluxUpr)))
y=y[selection ,:]
print len(y)
dx=dx[selection ,:]
dy=dy[selection ,:]
MagZeroPoint=MagZeroPoint[selection ,:]
instrumentMags=instrumentMags[selection ,:]

# #####Plot xy of stars in catalogues###############################################################
# plt.xlim([-3000,3000])
# plt.ylim([-3000,3000])
# plt.scatter(dx,dy,s=0.001)
# plt.show()
# ##################################################################################################

# #####Plot flux ratio as fuction center distance ##################################################
# plt.xlim([0,4000])
# plt.grid(True, which='both')
# plt.ylim([1/ratiolimits,1*ratiolimits])
# plt.yscale('log')
# dc=np.sqrt(np.add(np.square(dx),np.square(dy)))
# ymean=(1.0/np.nanmean(y,axis=1))
# yratio=y*ymean[:,np.newaxis]
# plt.scatter(dc,yratio,s=0.0001)
# plt.xlabel("Distance from center(pixels)")
# plt.ylabel("Flux_Instantaneous/Flux_Mean (Log scale)")
# plt.yticks(np.arange(0.5,2,0.1))
# plt.show()
#
#
# plt.figure(1)
# dclist=dc.flatten()
# yratiolist=yratio.flatten()
# dclist=dclist[~np.isnan(dclist)]
# yratiolist=yratiolist[~np.isnan(yratiolist)]
# xlist=dclist
# ylist=yratiolist
# ###################################################################################################

######Plot flux ratio as fuction sky pixel distance##################################################

y1=y[~np.isnan(y)]
nonNegFluxBool=y1>0
y1=y1[nonNegFluxBool]
instrumentMags1=instrumentMags[~np.isnan(instrumentMags)]
MagZeroPoint1=MagZeroPoint[~np.isnan(MagZeroPoint)]
dx1=dx[~np.isnan(dx)]
dx1=dx1[nonNegFluxBool]
dy1=dy[~np.isnan(dy)]
dy1=dy1[nonNegFluxBool]
dx1=dx1.astype(int)
dy1=dy1.astype(int)
skyPixelArea=Pixel_AREA[dx1,dy1]
correction_ratio=Map1[dx1,dy1]
plt.xlim([min(skyPixelArea),max(skyPixelArea)])
plt.grid(True, which='both')
plt.ylim([1/ratiolimits,1*ratiolimits])
plt.yscale('log')
# newBoolSelector=np.nanmin(y,axis=1)>0
# y=y[newBoolSelector]
ymean=(1.0/np.nanmean(y,axis=1))
yratio=y*ymean[:,np.newaxis]
yratio1=yratio.flatten()
yratio1=yratio1[~np.isnan(yratio1)]
yratio1=yratio1[yratio1>0]
plt.scatter(skyPixelArea,yratio1,s=0.0001)
plt.xlabel("Distance from center(pixels)")
plt.ylabel("Flux_Instantaneous/Flux_Mean (Log scale)")
plt.yticks(np.arange(0.5,2,0.1))
plt.show()
###################################################################################################
dc1=np.sqrt(np.add(np.square(dx1),np.square(dy1)))
plt.figure(1)
xlist=skyPixelArea
ylist=y1
###################################################################################################

###############new selection criteria#######
criteria=np.logical_and(np.abs(dx1)<3000,np.abs(dy1)<3000)#  star is in image of 6000x6000
dx1=dx1[criteria]
dy1=dy1[criteria]
xlist=xlist[criteria]
ylist=ylist[criteria]
yratio1=yratio1[criteria]
MagZeroPoint1=MagZeroPoint1[criteria]
instrumentMags1=instrumentMags1[criteria]
###########################################
#############################Flat field map########################################################
dx1=np.add(dx1,3000)
dy1=np.add(dy1,3000)
xbins=60
ybins=60
imageXSize=6000
imageYSize=6000
xBinlen=imageXSize/xbins
yBinlen=imageXSize/ybins
undersampled_map=np.zeros([xbins,ybins])
count=0
for ii in range(ybins):
    for kk in range(xbins):
        selectorX=np.logical_and(dx1>(xBinlen*ii),dx1<=(xBinlen*(ii+1)))#carfull here with the >= vs >
        selectorY =np.logical_and(dy1 > (yBinlen * kk), dy1 <= (yBinlen * (kk + 1)))#carfull here with the >= vs >
        selector= np.logical_and(selectorX,selectorY)
        num_starsInBox=np.count_nonzero(selector)

        # print xBinlen*ii
        # print yBinlen * kk
        # print num_starsInBox
        count=count+num_starsInBox
        if num_starsInBox>5:
            undersampled_map[(xbins-1)-kk,ii]=np.median(yratio1[selector])
        else:
            undersampled_map[(xbins - 1) - kk, ii] =0
        print undersampled_map[(xbins-1)-kk,ii]
    print xBinlen * ii
print len(xlist)
print count
fig, ax = plt.subplots()
cax = ax.imshow(undersampled_map,interpolation="gaussian",cmap=cm.afmhot)
cbar = fig.colorbar(cax)
plt.show()
# # If you want flat as field uncomment below 2 lines
# hdu=fits.PrimaryHDU(undersampled_map)
# hdu.writeto('/home/jamiedegois/Desktop/CorrectionMaplessMag7_2Feb_COMPLETETRANSIT',overwrite=True)
######Now to crop image to nice region#####################
x_1,x_2,y_1,y_2,undersampled_map1=smalls.giveCropingCo_ords(undersampled_map,1)
fig, ax = plt.subplots()
cax = ax.imshow(undersampled_map1,interpolation="gaussian",cmap=cm.afmhot)
cbar = fig.colorbar(cax)
plt.show()
CORRECTIONMAP=imresize(undersampled_map1,np.multiply(undersampled_map1.shape,6000/xbins),interp='bicubic',mode='F')
hdu=fits.PrimaryHDU(CORRECTIONMAP[::-1,::])#np and fits have a different way of arranging images
hdu.header["Xbegin  "]=x_1*6000/xbins
hdu.header["XEND    "]=x_2*6000/xbins
hdu.header["Ybegin  "]=y_1*6000/ybins
hdu.header["YEND    "]=y_2*6000/ybins
# hdu.writeto('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/CorrectionMap8Feb_ALMostCompTransitMoreMag9_SecondIteration.fits',overwrite=True)
embed()





###### getting cubic reg ##########################################################################
# gradient5=np.polyfit(xlist,ylist,4)[0]
# gradient4=np.polyfit(xlist,ylist,3)[0]
gradient3=np.polyfit(xlist,ylist,3)[0]
gradient2=np.polyfit(xlist,ylist,3)[1]
gradient1=np.polyfit(xlist,ylist,3)[2]
intercept=np.polyfit(xlist,ylist,3)[3]
print 'm^1:'
print gradient1
print 'm^2:'
print gradient2
print 'm^3:'
print gradient3
# print 'm^4:'
# print gradient4
# print 'm^5:'
# print gradient5
print 'c:'
print intercept
plt.plot(np.arange(0,4800),cubicReg(gradient3,gradient2,gradient1,intercept,np.arange(0,4800),m4=0,m5=0))
plt.yscale('log')
# extraticks=[1.74, 1.51, 1.32, 1.15, 1, 0.87, 0.76, 0.66, 0.57]
# plt.yticks(extraticks)
plt.ylim([.25, 4])
plt.scatter(xlist, ylist,s=0.0001)
plt.grid(True, which='major')
plt.xlabel("Distance from center(pixels)")
plt.ylabel("Flux_Instantaneous/Flux_Mean (Log scale)")
plt.show()
###################################################################################################

###### linear reg ##########################################################################
# gradient5=np.polyfit(xlist,ylist,4)[0]
# gradient4=np.polyfit(xlist,ylist,3)[0]
# gradient3=np.polyfit(xlist,ylist,3)[0]
# gradient2=np.polyfit(xlist,ylist,3)[1]
# gradient1=np.polyfit(xlist,ylist,1)[2]
# intercept=np.polyfit(xlist,ylist,1)[3]
gradient1=np.polyfit(xlist,ylist,1)[0]
intercept=np.polyfit(xlist,ylist,1)[1]
print 'm^1:'
print gradient1
print 'm^2:'
# print gradient2
# print 'm^3:'
# print gradient3
# print 'm^4:'
# print gradient4
# print 'm^5:'
# print gradient5
print 'c:'
print intercept
# plt.plot(np.arange(0,4800),cubicReg(gradient3,gradient2,gradient1,intercept,np.arange(0,4800),m4=0,m5=0))
plt.plot(np.arange(0,4800),cubicReg(0,0,gradient1,intercept,np.arange(0,4800),m4=0,m5=0))
plt.yscale('log')
# extraticks=[1.74, 1.51, 1.32, 1.15, 1, 0.87, 0.76, 0.66, 0.57]
# plt.yticks(extraticks)
plt.ylim([.25, 4])
plt.scatter(xlist, ylist,s=0.0001)
plt.grid(True, which='major')
plt.xlabel("Distance from center(pixels)")
plt.ylabel("Flux_Instantaneous/Flux_Mean (Log scale)")
plt.show()
###################################################################################################









































for ii in range(len(array)):
    y=np.array(array[ii][5::7])
    x=np.array(np.hypot(np.subtract(array[ii][7::7],3000.0),np.subtract(array[ii][8::7],3000.0)))
    y=y[~np.isnan(y)]
    x=x[~np.isnan(x)]
    y=np.multiply(y,(1.0/np.mean(y)))
    plt.scatter(x[3:-3], y[3:-3], s=0.03)
    print str(ii / (len(array) + 1.0))

plt.show()



# print "here"
# fitGrad=np.zeros(len(array[0]))
# print "here1"
# fitIntercept=np.zeros(len(array[0]))
# print "here2"
# count=0
# array=np.array(array)
#
# for ii in range(len(array[0])):
#     print ii
#     if(array[ii][-2]>flux):
#         y=array[ii][5:3489:7]
#         x=np.hypot(array[ii][7:3489:7]-3000,array[ii][8:3489:7]-3000)
#         y=y*(1/array[ii][-2])
#         x = runningMeanFast(x, 1)
#         y = runningMeanFast(y, 1)
#         plt.ylim([0.5, 2])
#         plt.xlim([0, 3200])
#         plt.yscale('log')
#         plt.grid(True)
#         if ((len(x[~np.isnan(x)])>LwrLimit) & (len(x[~np.isnan(x)])<UpLimit)) :# number of times a source is detected
#             print len(x[~np.isnan(x)])
#             fitGrad[count]= np.polyfit(x[~np.isnan(x)],y[~np.isnan(y)],1)[0]
#             fitIntercept[count] = np.polyfit(x[~np.isnan(x)], y[~np.isnan(y)], 1)[1]
#             count =count +1
#             plt.scatter(x[20:-20], y[20:-20], s=0.03)
#             # print str(ii/(len(array[0])+1.0))
# plt.show()
#
# arr=fitGrad[:count:]
# plt.figure(1)
# plt.hist(arr, normed=True,bins=count/5)
# plt.xlim((min(arr), max(arr)))
#
# mean = np.median(arr)
# variance = np.var(arr)
# sigma = np.sqrt(variance)
# x = np.linspace(min(arr), max(arr), 100)
# plt.plot(x, mlab.normpdf(x, mean, sigma))
# print mean *10000
# print sigma*10000
# print len(arr)
#
#
# arr=arr[~(np.abs(mean-arr)>1.58*sigma)]
# plt.figure(2)
# plt.hist(arr, normed=True,bins=count/10)
# plt.xlim((min(arr), max(arr)))
#
# mean = np.median(arr)
# variance = np.var(arr)
# sigma = np.sqrt(variance)
# x = np.linspace(min(arr), max(arr), 100)
# plt.plot(x, mlab.normpdf(x, mean, sigma))
# print mean *10000
# print sigma*10000
# print len(arr)
# plt.show()


