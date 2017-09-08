from astropy.io import fits
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd


########################################################################################################
#This program takes a csv and then make it a 2 dimentional array and then allows you to plot stuff with it
########################################################################################################
flux=0
fluxUpper=30000000000
LwrLimit=100
UpLimit=5000


def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

print "here0"
csv1 = np.genfromtxt ('/home/jamiedegois/Desktop/ALLLONELYSTARSWITHMAP1AND2', delimiter=",")
print type(csv1)
print "here-1"
csv= np.transpose(csv1)
print "here-2"
####################################################################
# # ##as a function of distance from middle x
# # for ii in range(len(csv[0])):
# #     if(csv[-1,ii]>25000):
# #         y=csv[4:-1:6,ii]
# #         x=csv[6::6,ii]
# #         x=abs(runningMeanFast(x,1)-3000)
# #         y=y*(1/csv[-1,ii])
# #         y=runningMeanFast(y,1)
# #         plt.ylim([0.5, 1.5])
# #         plt.xlim([0, 3000])
# #         plt.grid(True)
# #         plt.scatter(x, y,s=15)
# #
# plt.show()
##############################################################################
###as a function of distance from center
print "here"
fitGrad=np.zeros(len(csv[0]))
print "here1"
fitIntercept=np.zeros(len(csv[0]))
print "here2"
count=0
print csv
for ii in range(len(csv[0])):
    print ii
    if(csv[-2,ii]>flux):
        y=csv[4:3489:7,ii]
        x=np.hypot(csv[6:3489:7,ii]-3000,csv[7:3489:7,ii]-3000)
        y=y*(1/csv[-2,ii])
        x = runningMeanFast(x, 1)
        y = runningMeanFast(y, 1)
        plt.ylim([0.5, 2])
        plt.xlim([0, 3200])
        plt.yscale('log')
        plt.grid(True)
        if ((len(x[~np.isnan(x)])>LwrLimit) & (len(x[~np.isnan(x)])<UpLimit)) :# number of times a source is detected
            print len(x[~np.isnan(x)])
            fitGrad[count]= np.polyfit(x[~np.isnan(x)],y[~np.isnan(y)],1)[0]
            fitIntercept[count] = np.polyfit(x[~np.isnan(x)], y[~np.isnan(y)], 1)[1]
            count =count +1
            plt.scatter(x[20:-20], y[20:-20], s=0.03)
        print ii/(len(csv[0])+1.0)
plt.show()

arr=fitGrad[:count:]
plt.figure(1)
plt.hist(arr, normed=True,bins=count/5)
plt.xlim((min(arr), max(arr)))

mean = np.median(arr)
variance = np.var(arr)
sigma = np.sqrt(variance)
x = np.linspace(min(arr), max(arr), 100)
plt.plot(x, mlab.normpdf(x, mean, sigma))
print mean *10000
print sigma*10000
print len(arr)


arr=arr[~(np.abs(mean-arr)>1.58*sigma)]
plt.figure(2)
plt.hist(arr, normed=True,bins=count/10)
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


#######as a function of diagonal pixel scale
# from astropy.io import fits
#
# hdulist = fits.open('/home/jamiedegois/Desktop/n2.fits')
# pixelScale= hdulist[0].data
# count=0
# fitGrad=np.zeros(len(csv[0]))
# fitIntercept=np.zeros(len(csv[0]))
# for ii in range(len(csv[0])):
#     if(csv[-1,ii]>flux):
#         y=csv[4:-1:6,ii]
#         x= np.round(csv[6:-1:6,ii])
#         x1=np.round(csv[6:-1:6,ii])
#         x2=np.round(csv[7::6,ii])
#         y=y*(1/csv[-1,ii])
#         for jj in range(len(x1)):
#             if np.isnan(x1[jj]):
#                 x1[jj]=0
#             else:
#                 # print np.int(x1[jj])
#                 # print np.int(x2[jj])
#                 x[jj]=pixelScale[(np.int(x2[jj]-2)),(np.int(x1[jj]-2))]###    why2 ? close enough and stoped index errors (pixel scale wont change over 2 pixels)
#                 # print x[jj]
#         plt.ylim([0.5, 1.5])
#         plt.xlim([35, 70])
#         plt.grid(True)
#         if ((len(x[~np.isnan(x)])>LwrLimit) & (len(x[~np.isnan(x)])<UpLimit)) :# number of times a source is detected
#             print len(x[~np.isnan(x)])
#             fitGrad[count]= np.polyfit(x[~np.isnan(x)],y[~np.isnan(y)],1)[0]
#             fitIntercept[count] = np.polyfit(x[~np.isnan(x)], y[~np.isnan(y)], 1)[1]
#             count =count +1
#             plt.scatter(x, y, s=0.002)
#
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
# arr=arr[~(np.abs(mean-arr)>1.565*sigma)]
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

##############################################################
#######as a function of pixel sky area
from astropy.io import fits

hdulist1 = fits.open('/home/jamiedegois/Desktop/n.fits')
pixelScale1= hdulist1[0].data
hdulist2 = fits.open('/home/jamiedegois/Desktop/n1.fits')
pixelScale2= hdulist2[0].data

fitGrad=np.zeros(len(csv[0]))
fitIntercept=np.zeros(len(csv[0]))

count=0
aveSigma=0
for ii in range(len(csv[0])):
    if(csv[-1,ii]>flux)&(csv[-1,ii]<fluxUpper):
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
        plt.ylim([0.5, 2])
        plt.xlim([35*35, 70*70])
        plt.grid(True)
        plt.yscale("log")
        # plt.scatter(x, y,s=0.2)
        # print x
        # print '##############'
        # print y
        if ((len(x[~np.isnan(x)])>LwrLimit) & (len(x[~np.isnan(x)])<UpLimit)) :# number of times a source is detected
            print len(x[~np.isnan(x)])
            fitGrad[count]= np.polyfit(x[~np.isnan(x)],y[~np.isnan(y)],1)[0]
            fitIntercept[count] = np.polyfit(x[~np.isnan(x)], y[~np.isnan(y)], 1)[1]
            count =count +1
            plt.scatter(x, y, s=0.003)
            aveSigma=aveSigma+np.std(y[~np.isnan(y)])
            # if (np.amax(x[~np.isnan(x)])>4200)&(np.amax(x[~np.isnan(x)])<4500):
            #     plt.plot(x,y)
            #     plt.scatter(x[0:20:1],y[0:20:1])
            #     plt.show()

print aveSigma/count
# plt.plot(np.arange(5000),np.add(np.multiply(np.arange(5000),-0.000175),1.58))
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






# ######################x-y positions of stars star treks see page 41 log book ####################
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