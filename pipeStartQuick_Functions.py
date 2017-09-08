def imageCalibrator(newFileName, calibrateOnly=False, recalcCentreOnly=False, applyRefImageOnly=False, outPutLocation='/home/jamiedegois/Desktop/pipeStartQuick/Output/',
                    returnRefImageDIR = False, minSources=1500, inRefFits='/home/jamiedegois/Desktop/pipeStartQuick/refQuick.fits'):
    import subprocess
    import Stilts
    from shutil import copyfile
    import astropy.units as u
    from astropy.io import fits
    from astropy.coordinates import SkyCoord, EarthLocation
    from astropy.time import Time
    import re
    import numpy as np


    def subprocess_cmd(command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print proc_stdout
    lenCat=0

    ###1 importing both images
    refFits = fits.open(inRefFits)
    newFits = fits.open(newFileName)

    newFileName=newFileName.split("/")[-1]

    ###2 Croping newFits
    newFitsMid = fits.PrimaryHDU()
    newFitsMid.data = newFits[0].data[1:4927,1227:6153]
    newFitsMid.header = newFits[0].header
    newFitsMid.writeto('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits', clobber=True)
    newFits = fits.open('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits')##may be redundant


    ###3 calculate new center coordinates
    ##First calulate AZALT -wof CRPIX in REFERENCE IMAGE
    refLoc = EarthLocation(lat =refFits[0].header.get('SITELAT')*u.deg,
                           lon =refFits[0].header.get('SITELONG') * u.deg
                           , height = refFits[0].header.get('SITEALT')*u.m)
    refTime = Time(refFits[0].header.get('DATE-OBS'), format='isot', scale='utc')
    refCoordinate = SkyCoord(ra=refFits[0].header.get('CRVAL1')*u.deg,
                             dec=refFits[0].header.get('CRVAL2')*u.deg,
                             frame='icrs',
                             location = refLoc
                             ,obstime = refTime )
    print refCoordinate.altaz
    ##second calculate RADEC of CRPIX in NEW IMAGE
    # newLoc = EarthLocation(lat =refFits[0].header.get('SITELAT')*u.deg,
    #                        lon =refFits[0].header.get('SITELONG') * u.deg
    #                        , height = refFits[0].header.get('SITEALT')*u.m)
    newTime = Time(newFits[0].header.get('DATE-OBS'), format='isot', scale='utc')
    newCoordinate = SkyCoord(alt = refCoordinate.altaz.alt,
                             az =refCoordinate.altaz.az ,
                             obstime = newTime ,
                             frame = 'altaz',
                             location = refLoc)
    #print newCoordinate.icrs

    newCenterCoord1= newCoordinate.icrs.ra.degree
    newCenterCoord2= newCoordinate.icrs.dec.degree

    print 'New (CRVAL1,CRVAL2):'
    print newCenterCoord1
    print newCenterCoord2


####################### Write Initial Astrometric solution ####################
    OBSTIME = newFits[0].header['OBSTIME']
    DATEOBS= newFits[0].header['DATE-OBS']
    SITELAT= newFits[0].header['SITELAT']
    SITELONG= newFits[0].header['SITELONG']
    SITEALT= newFits[0].header['SITEALT']
    DATE= newFits[0].header['DATE']

    newFits[0].header = refFits[0].header

    newFits[0].header['OBSTIME'] =OBSTIME
    newFits[0].header['DATE-OBS']= DATEOBS
    newFits[0].header['SITELAT'] = SITELAT
    newFits[0].header['SITELONG'] = SITELONG
    newFits[0].header['SITEALT'] = SITEALT
    newFits[0].header['DATE'] = DATE
    newFits[0].header['CRVAL1'] = newCenterCoord1
    newFits[0].header['CRVAL2'] = newCenterCoord2

    newFits.writeto('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits', clobber=True)
    print("###############   all done :)   #############")

    if applyRefImageOnly:

        # subprocess_cmd(
        #     'cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits -c default_12_SIGMA.sex')
        #
        # Stilts.stitlsANDJoinCSV('300', 'ALPHAWIN_J2000', 'DELTAWIN_J2000', 'X_WORLD', 'Y_WORLD',
        #                         "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat#2",
        #                         "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCalcCentre.fits",
        #                         '/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv')
        # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv',
        #          outPutLocation + 'RECENTRE-' + newFileName.replace(".fits", ".csv"))
        # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat',
        #          outPutLocation + 'sextractor-' + newFileName.replace(".fits", ".cat"))
        copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits',
                 outPutLocation + 'QUICK' + newFileName)

        return

    if (recalcCentreOnly == False):
    ###########################################do SEXTRACTOR AND SCAMP (PLUS CHECK IF >minSources) ##############################





        subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits')
        cat = fits.open('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat')
        lenCat=len(cat[2].data)


        if(lenCat>minSources): #if more than minSources  detected, proceed with calibration
            subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; scamp test.cat -c scamp3.conf')


        ############################################# Write refined Astrometric solution to header and run SExtractor again ##########################


            f = open('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.head')
            data= f.read()

            data= data.replace(" / ","#")
            data= data.replace(" ","")
            data= data.split("\n",3)[3]

            data= re.split('=|#|\n',data)

            keys = data[0:287:3]


            values = data[1:287:3]

            from astropy.io import fits
            data, header = fits.getdata("/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits", header=True)

            if len(keys)>95:
                for ii in range (96):
                    try:
                        header[keys[ii]] = int(values[ii])
                    except ValueError:
                        try:
                            header[keys[ii]] = float(values[ii])
                        except ValueError:
                            pass #it is a string and can be done manually
            else:
                file = open('/home/jamiedegois/Desktop/pipeStartQuick/ERRORLOG.txt', 'a')
                file.write('Error 01:Test.head too short, output file may not have the correct photometric calibration solution\n')
                file.write('    File affected:'+newFileName+'\n')
                file.close()

            header['CTYPE1'] = 'RA---TPV'
            header['CTYPE2'] = 'DEC--TPV'
            header['CUNIT1'] = 'deg'
            header['CUNIT2'] = 'deg'
            header['RADESYS'] = 'ICRS'


            fits.writeto("/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits",data, header, clobber=True)
            if ((calibrateOnly)):
                pass
            else:
                subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits')

            ########CREATE CSV#####
            subprocess_cmd(
                'cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits -c default_12_SIGMA.sex')
            Stilts.stitlsANDJoinCSV('600', 'ALPHAWIN_J2000', 'DELTAWIN_J2000', 'X_WORLD', 'Y_WORLD',
                                    "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat#2",
                                    "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCalcCentre.fits",
                                    '/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv')
            #########################

            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits',outPutLocation+'QUICK' + newFileName)
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/better_astr_referror2d_1.svg',outPutLocation+'CHECKPLOT-' + newFileName.replace(".fits",".svg"))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/full_1.cat',outPutLocation+'FULL-' + newFileName.replace(".fits",".catalogue"))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/merged_1.cat',outPutLocation+'MERGED-' + newFileName.replace(".fits",".catalogue"))
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat',outPutLocation+'sextractor-' + newFileName.replace(".fits",".cat"))
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv',
                     outPutLocation + 'RECENTRE-' + newFileName.replace(".fits", ".csv"))


        else: #(less than minSources sources)
            file = open('/home/jamiedegois/Desktop/pipeStartQuick/ERRORLOG.txt', 'a')
            file.write(
                'Error 02:Less Than '+str(minSources)+ ' Sources detected- only ref image calibration applied to image\n')
            file.write('    File affected:' + newFileName + '\n')
            file.close()

            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits',outPutLocation + 'QUICK' + newFileName)
            #copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/better_astr_referror2d_1.svg',outPutLocation + 'CHECKPLOT-' + newFileName.replace(".fits", ".svg"))
            #copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/full_1.cat',outPutLocation + 'FULL-' + newFileName.replace(".fits", ".catalogue"))
            #copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/merged_1.cat',outPutLocation + 'MERGED-' + newFileName.replace(".fits", ".catalogue"))
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat',outPutLocation + 'sextractor-' + newFileName.replace(".fits", ".cat"))

    else: # only want to recalculate centre
        subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits -c default_12_SIGMA.sex')

        Stilts.stitlsANDJoinCSV('600', 'ALPHAWIN_J2000', 'DELTAWIN_J2000','X_WORLD' , 'Y_WORLD',
                             "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat#2",
                             "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCalcCentre.fits",
                             '/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv')

        catalogue = np.genfromtxt('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv', delimiter=",")

        if (len(catalogue) > minSources  and catalogue.ndim>1) :  # if more than minSources sources detected and crossMatched, proceed with calibration
            catAlpha = catalogue[::, 10:11:]
            catDelta = catalogue[::, 11:12:]
            sexAlpha = catalogue[::, 4:5:]
            sexDelta = catalogue[::, 5:6:]

            alphaDiff=np.subtract(catAlpha,sexAlpha)
            deltaDiff = np.subtract(catDelta,sexDelta)

            print np.median(alphaDiff)*3600
            print np.median(deltaDiff)*3600

            newFits[0].header['CRVAL1'] = newCenterCoord1+np.median(alphaDiff)
            newFits[0].header['CRVAL2'] = newCenterCoord2+np.median(deltaDiff)

            newFits.writeto('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits', clobber=True)



            if (calibrateOnly==False):
                subprocess_cmd(
                    'cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits -c default_12_SIGMA.sex')

                Stilts.stitlsANDJoinCSV('180', 'ALPHAWIN_J2000', 'DELTAWIN_J2000', 'X_WORLD', 'Y_WORLD',
                                        "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat#2",
                                        "/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCalcCentre.fits",
                                        '/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv')


            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits',
                     outPutLocation + 'QUICK' + newFileName +str(len(catalogue)))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/better_astr_referror2d_1.svg',outPutLocation + 'CHECKPLOT-' + newFileName.replace(".fits", ".svg"))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/full_1.cat',outPutLocation + 'FULL-' + newFileName.replace(".fits", ".catalogue"))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/merged_1.cat',outPutLocation + 'MERGED-' + newFileName.replace(".fits", ".catalogue"))
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat',
                     outPutLocation + 'sextractor-' + newFileName.replace(".fits", ".cat"))
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/reCenterOutputCat.csv',
                     outPutLocation + 'RECENTRE-' + newFileName.replace(".fits", ".csv"))




        else:  # (less than minSources sources)
            print"###########warning#############"
            file = open('/home/jamiedegois/Desktop/pipeStartQuick/ERRORLOG.txt', 'a')
            file.write(
                'Error 02CENTRE:Less Than '+minSources+' Sources detected- only ref image calibration applied to image\n')
            file.write('    File affected:' + newFileName + '\n')
            file.close()

            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits',
                     outPutLocation + 'QUICK' + newFileName+'-WARNING')
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/better_astr_referror2d_1.svg',outPutLocation + 'CHECKPLOT-' + newFileName.replace(".fits", ".svg"))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/full_1.cat',outPutLocation + 'FULL-' + newFileName.replace(".fits", ".catalogue"))
            # copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/merged_1.cat',outPutLocation + 'MERGED-' + newFileName.replace(".fits", ".catalogue"))
            copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat',
                     outPutLocation + 'sextractor-' + newFileName.replace(".fits", ".cat")+'-WARNING')
    print "lenCAt:"+str(lenCat)
    print minSources

    if returnRefImageDIR:
        if lenCat>minSources:
            return outPutLocation + 'QUICK' + newFileName
        else:
            return None







def runSwarp(inDIRlist,numImagesPerStack=20,outPutDir='/home/jamiedegois/Desktop/pipeStartQuick/swarp',doRunt=False):
    import subprocess
    import shutil
    def subprocess_cmd(command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print proc_stdout


    swarpFileList = inDIRlist
    jj=0
    swarpString=''
    refDirList=[]
    for ii in range (0,(len(swarpFileList))/numImagesPerStack,1):
        outputName=swarpFileList[jj].split("/")[-1]
        try:
            shutil.copy('/home/jamiedegois/Desktop/pipeStartQuick/coadd.coaddhead',
                        outPutDir + '/' + outputName + 'co-add.coaddhead')
        except:
            pass
        for kk in range (0,numImagesPerStack,1):
            swarpString=swarpString +' '+swarpFileList[jj]
            jj=jj+1
        subprocess_cmd('cd '+outPutDir+';/home/jamiedegois/bin/SWARP/bin/swarp'+swarpString+' -c /home/jamiedegois/Desktop/pipeStartQuick/default.swarp -IMAGEOUT_NAME '+outputName+'co-add.fits'+
                       ' -WEIGHTOUT_NAME '+outputName+'co-add.weight.fits')
        swarpString = ''
        refDirList.append(outPutDir+outputName+'co-add.fits')

    if (doRunt==True and ((len(swarpFileList)%numImagesPerStack)>1)):# if want to do final set of images, and the final list is not an empty list (or a single image)
        swarpFileList=swarpFileList[jj::]
        outputName = swarpFileList[0].split("/")[-1]
        try:
            shutil.copy('/home/jamiedegois/Desktop/pipeStartQuick/coadd.coaddhead',
                        outPutDir + '/' + outputName + 'co-add.coaddhead')
        except:
            pass
        for ll in range(len(swarpFileList)):
            swarpString = swarpString + ' ' + swarpFileList[ll]
        subprocess_cmd(
            'cd ' + outPutDir + ';/home/jamiedegois/bin/SWARP/bin/swarp' + swarpString + ' -c /home/jamiedegois/Desktop/pipeStartQuick/default.swarp -IMAGEOUT_NAME ' + outputName + 'co-add.fits' +
            ' -WEIGHTOUT_NAME ' + outputName + 'co-add.weight.fits')
        refDirList.append(outPutDir + outputName + 'co-add.fits')
    return refDirList




def runSextractor(newFileName,outputDir='/home/jamiedegois/Desktop/pipeStartQuick/Output'):
    import subprocess
    from shutil import copyfile
    def subprocess_cmd(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print proc_stdout

    copyfile(newFileName, '/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits')
    subprocess_cmd(
        'cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits -c default2.sex')
    newFileName = newFileName.split("/")[-1]
    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat',
             outputDir+'/sextractor-' + newFileName.replace(".fits", ".cat"))
    return outputDir+'/sextractor-' + newFileName.replace(".fits", ".cat")


def numSexDetects():
    pass



#
# import subprocess
#
#
# def subprocess_cmd(command):
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
#     proc_stdout = process.communicate()[0].strip()
#     print proc_stdout
#
# subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick;scamp *.cat -c scamp3.conf')


# scamp sextractor-01_2015-09-22_180033_DSC_1117-G.cat sextractor-01_2015-09-22_181742_DSC_1161-G.cat sextractor-01_2015-09-22_184741_DSC_1238-G.cat sextractor-01_2015-09-22_191453_DSC_1308-G.cat sextractor-01_2015-09-22_193936_DSC_1370-G.cat -c scamp3.conf

