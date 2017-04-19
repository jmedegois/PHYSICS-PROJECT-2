from astropy.io import fits
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
###################################################################################INITIAL CONDITIONS##########################################
csv1 = np.genfromtxt ('/home/jamiedegois/Desktop/Position_dependancy/ALL_LONELY_STARS', delimiter=",")
csv= np.transpose(csv1)
flux=7500
fluxUppr=100000
LwrLimit=10
UpLimit=60
###############################################################################################################################################
multiMap1= fits.open('/home/jamiedegois/Desktop/n4.2.fits')[0].data
multiMap2= fits.open('/home/jamiedegois/Desktop/n5.2.fits')[0].data

def reject_outliers(data, sigma=2):
    return data[abs(data - np.median(data)) < sigma * np.std(data)]

def multiplier(xImage,yImage,Map):
    return 1/(Map[yImage,xImage])

def cubicReg(m3,m2,m1,constant,x):
    firstTerm = np.multiply(x, m1)
    secondTerm = np.multiply(np.multiply(x, m2),x)
    thirdTerm = np.multiply(np.multiply(np.multiply(x, m3),x),x)
    return np.add(np.add(np.add(firstTerm, constant), secondTerm), thirdTerm)



def applyFluxMultilipersToCSV(inCSV,Map,startFlux=4,startX=6,startY=7,cols=6):
    lengthRows=len(inCSV[0,::])
    lengthcols=len(inCSV[::,0])
    count=0
    totFlux=0
    for ii in range(lengthRows):
        ##update all individual fluxs
        for jj in range(startFlux,lengthcols-1,cols):
            if not(np.isnan(inCSV[jj,ii])):
                inCSV[jj,ii]=inCSV[jj,ii]*multiplier(np.int(inCSV[jj+(startX-startFlux),ii])-3,np.int(inCSV[jj+(startY-startFlux),ii])-3,Map)###dont worry about the -3, it is to avoid array index out of bounds issues and does not make a diff
                count=count+1
                totFlux=totFlux+inCSV[jj,ii]
        ##now fix the ave flux
        inCSV[-1,ii]=totFlux/count
        count = 0
        totFlux = 0
    return inCSV

csv=applyFluxMultilipersToCSV(csv,Map=multiMap1)
csv=applyFluxMultilipersToCSV(csv,Map=multiMap2)

hdulist1 = fits.open('/home/jamiedegois/Desktop/n.fits')
pixelScale1= hdulist1[0].data
hdulist2 = fits.open('/home/jamiedegois/Desktop/n1.fits')
pixelScale2= hdulist2[0].data

fitGrad=np.zeros(len(csv[0]))
fitIntercept=np.zeros(len(csv[0]))
count=0
aveSigma=0
xlist=np.zeros(2000000)
ylist=np.zeros(2000000)
countlist=0
for ii in range(len(csv[0])):
    if((csv[-1,ii]>flux)&(csv[-1,ii]<fluxUppr)):
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
        plt.figure(0)
        plt.ylim([0.6, 1.4])
        plt.xlim([35*35, 70*70])
        plt.grid(True)
        # plt.scatter(x, y,s=0.2)
        # print x
        # print '##############'
        # print y
        if ((len(x[~np.isnan(x)])>LwrLimit) & (len(x[~np.isnan(x)])<UpLimit)) :# number of times a source is detected
            # print len(x[~np.isnan(x)])
            fitGrad[count]= np.polyfit(x[~np.isnan(x)],y[~np.isnan(y)],1)[0]
            fitIntercept[count] = np.polyfit(x[~np.isnan(x)], y[~np.isnan(y)], 1)[1]
            count =count +1
            # sigma=4
            # x = x[~np.isnan(x)]
            # y = y[~np.isnan(y)]
            # x = x[abs(y - np.median(y)) < sigma * np.std(y)]
            # y = y[abs(y - np.median(y)) < sigma * np.std(y)]

            aveSigma = aveSigma + np.std(y[~np.isnan(y)])
            xlist[countlist:countlist+len(x[~np.isnan(x)])-6]=x[~np.isnan(x)][3:-3]
            ylist[countlist:countlist+len(y[~np.isnan(y)])-6] = y[~np.isnan(y)][3:-3]
            countlist=countlist+len(x[~np.isnan(x)])-6

print 'number of stars'
print count

print'###############################################'
xlist=xlist[:countlist]
ylist=ylist[:countlist]
print 'number datapoints before crop'
print len(xlist)

#########cubic reg below
gradient3=np.polyfit(xlist,ylist,3)[0]
gradient2=np.polyfit(xlist,ylist,3)[1]
gradient1=np.polyfit(xlist,ylist,3)[2]
intercept=np.polyfit(xlist,ylist,3)[3]

# ########linear reg below
# gradient3=0
# gradient2=0
# gradient1=np.polyfit(xlist,ylist,1)[0]
# intercept=np.polyfit(xlist,ylist,1)[1]

print 'm^1:'
print gradient1
print 'm^2:'
print gradient2
print 'm^3:'
print gradient3
print 'c:'
print intercept


plt.plot(np.arange(1750,4750),cubicReg(gradient3,gradient2,gradient1,intercept,np.arange(1750,4750)))
plt.scatter(xlist, ylist,s=0.03)

print'###############################################'
plt.figure(1)
plt.ylim([0.6, 1.4])
plt.xlim([35 * 35, 70 * 70])
plt.grid(True)
resid= np.subtract(ylist,    cubicReg(gradient3,gradient2,gradient1,intercept,xlist)   )  #actual-trendline
residSTD= np.std(resid)
print "residual std deviation is before crop:"
print residSTD
#################### residual plots
# plt.figure(0)
# plt.scatter(xlist,resid)
#
#
# plt.figure(1)
# plt.scatter(xlist[~np.greater(np.abs(resid),3*residSTD)],resid[~np.greater(np.abs(resid),3*residSTD)])
# plt.show()
xlist=xlist[~np.greater(np.abs(resid),3*residSTD)]
ylist=ylist[~np.greater(np.abs(resid),3*residSTD)]
#########cubic reg below
gradient3=np.polyfit(xlist,ylist,3)[0]
gradient2=np.polyfit(xlist,ylist,3)[1]
gradient1=np.polyfit(xlist,ylist,3)[2]
intercept=np.polyfit(xlist,ylist,3)[3]

# #########linear reg below
# gradient3=0
# gradient2=0
# gradient1=np.polyfit(xlist,ylist,1)[0]
# intercept=np.polyfit(xlist,ylist,1)[1]

print 'm^1:'
print gradient1
print 'm^2:'
print gradient2
print 'm^3:'
print gradient3
print 'c:'
print intercept

resid= np.subtract(ylist,    cubicReg(gradient3,gradient2,gradient1,intercept,xlist)   )  #actual-trendline
residSTD= np.std(resid)
print "residual std deviation is after crop:"
print residSTD
print 'number datapoints after crop'
print len(xlist)
print 'cropped m^1:'
print gradient1
print 'cropped m^2:'
print gradient2
print 'cropped m^3:'
print gradient3
print 'c:'
print intercept
plt.plot(np.arange(1750,4750),cubicReg(gradient3,gradient2,gradient1,intercept,np.arange(1750,4750)))
plt.scatter(xlist, ylist,s=0.03)
plt.show()



print aveSigma/count
arr=fitGrad[:count:]
plt.figure(1)
plt.hist(arr, normed=True,bins=1+count/5)
plt.xlim((min(arr), max(arr)))

mean = np.median(arr)
variance = np.var(arr)
sigma = np.sqrt(variance)
x = np.linspace(min(arr), max(arr), 100)
plt.plot(x, mlab.normpdf(x, mean, sigma))
print mean *10000
print sigma*10000
print len(arr)


arr=arr[~(np.abs(mean-arr)>1.5*sigma)]
plt.figure(2)
plt.hist(arr, normed=True,bins=1+count/10)
plt.xlim((min(arr), max(arr)))

mean = np.median(arr)
variance = np.var(arr)
sigma = np.sqrt(variance)
x = np.linspace(min(arr), max(arr), 100)
plt.plot(x, mlab.normpdf(x, mean, sigma))
print mean *10000
print sigma*10000
print len(arr)
plt.show()

##########show plot of radial responce
# y=np.zeros(6000)
# x=np.arange(6000)
# hdulist = fits.open('/home/jamiedegois/Desktop/n3.fits')
# pixelScale= hdulist[0].data
# for ii in range(6000):
#     x[ii]=pixelScale[2400,ii]
#     y[ii]=multiplier(ii,2400,multiMap1)*multiplier(ii,2400,multiMap2)
#
#
# plt.plot(x,y)
# plt.show()




