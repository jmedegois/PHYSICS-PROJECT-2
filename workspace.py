string=''
for ii in range(5,743,10):
    string=string+","+"$"+str(ii)
print string[1:]



















#
#
#
#
# catalogue = np.genfromtxt('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/25July/UsingRECalcCentre/RECENTRE-01_2016-01-10_161943_DSC_0700-G.csv', delimiter=",")
# xImage=catalogue[::,2:3:]
# yImage=catalogue[::,3:4:]
#
# catAlpha = catalogue[::, 10:11:]
# catDelta = catalogue[::, 11:12:]
# sexAlpha = catalogue[::, 4:5:]
# sexDelta = catalogue[::, 5:6:]
# alphaDiff = np.subtract(catAlpha, sexAlpha)
# deltaDiff = np.subtract(catDelta, sexDelta)
#
#
# plt.figure(1)
# plt.title('')
# M = np.hypot(3600*alphaDiff,3600*deltaDiff)
# Q = plt.quiver(xImage, yImage, deltaDiff*3600,alphaDiff*3600,M, scale=400, scale_units='inches')
# cb = plt.colorbar(Q)
#
#
#
#
# ####### XY acurate ###############
# import astropy.io.fits as fits
# import astropy.wcs as wcs
# import os
#
# filename = os.path.join(wcs.__path__[0], '/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/25July/UsingRECalcCentre/QUICK01_2016-01-10_161943_DSC_0700-G.fits4100')
# hdulist = fits.open(filename)
# w = wcs.WCS(hdulist[0].header, hdulist)
# hdulist.close()
#
# xCat, yCat = w.all_world2pix(catAlpha, catDelta,1)
#
# xDiff=np.subtract(xCat,xImage)
# yDiff=np.subtract(yCat,yImage)
#
# plt.figure(2)
# plt.title('')
# M = np.hypot(xDiff,yDiff)
# Q = plt.quiver(xImage, yImage, xDiff,yDiff,M, scale=1.5, scale_units='inches')
# cb = plt.colorbar(Q)
#
#
# # M = np.hypot(DECx,RAx)*3600
# # print np.max(M)
# # print np.average(alphaDiff)*3600
# # print np.average(deltaDiff)*3600
#
# plt.show()
#
#
# numDev=12
#
# DECx, RAx = np.meshgrid(np.arange(0,4926.1, 4926/numDev), np.arange(0,4926.1, 4926/numDev))
#
# for ii in range(numDev+1):
#     catalogueTEMP=catalogue[catalogue[:,2]>=(ii*4926/numDev)]
#     catalogueTEMP = catalogueTEMP[catalogueTEMP[:,2] <= ((ii+1) * 4926/numDev)]
#
#
#     for jj in range(numDev+1):
#
#         catalogueTEMP2 = catalogueTEMP[catalogueTEMP[:, 3] >= (jj * 4926/numDev)]
#         catalogueTEMP2 = catalogueTEMP2[catalogueTEMP2[:, 3] <= ((jj + 1) * 4926/numDev)]
#         # print len(catalogueTEMP2)
#
#         catAlpha=catalogueTEMP2[::,10:11:]
#         catDelta = catalogueTEMP2[::, 11:12:]
#         sexAlpha=catalogueTEMP2[::,4:5:]
#         sexDelta = catalogueTEMP2[::, 5:6:]
#
#         alphaDiff = np.subtract(catAlpha, sexAlpha)
#         deltaDiff = np.subtract(catDelta, sexDelta)
#
#
#         if len(sexDelta)>4:
#             DECx[ii,jj]=np.median(deltaDiff)
#             RAx[ii,jj]=np.median(alphaDiff)
#         else:
#             DECx[ii, jj] = 0
#             RAx[ii, jj] = 0
#         # print DECx[ii, jj]
#         # print RAx[ii, jj]
#
#
#
# X, Y = np.meshgrid(np.arange(0,4926.1, 4926/numDev), np.arange(0,4926.1, 4926/numDev))
# plt.figure(3)
# plt.title('')
# M = np.hypot(3600*DECx,3600*RAx)
# Q = plt.quiver(X, Y, 3600*DECx,3600*RAx,M, scale=20, scale_units='inches')
# cb = plt.colorbar(Q)
#
#
# M = np.hypot(DECx,RAx)*3600
# print np.max(M)
# print np.average(DECx)*3600
# print np.average(RAx)*3600
#
#
#
#
#
#
