
def pipeStartQuick(newFileName):
    import subprocess
    from shutil import copyfile
    import astropy.units as u
    from astropy.io import fits
    from astropy.coordinates import SkyCoord, EarthLocation
    from astropy.time import Time
    import re

    ###1 importing both images
    refFits = fits.open('/home/jamiedegois/Desktop/pipeStartQuick/refQuick.fits')
    newFits = fits.open('/home/jamiedegois/Desktop/pipeStartQuick/Input/'+ newFileName)


    ###2 Croping newFits
    newFitsMid = fits.PrimaryHDU()
    newFitsMid.data = newFits[0].data[1:4927,1227:6153]
    newFitsMid.header = newFits[0].header
    newFitsMid.writeto('/home/jamiedegois/Desktop/pipeStartQuick/Output/QUICK' + newFileName, clobber=True)
    newFits = fits.open('/home/jamiedegois/Desktop/pipeStartQuick/Output/QUICK' + newFileName)##may be redundant


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





    newFits.writeto('/home/jamiedegois/Desktop/pipeStartQuick/Output/QUICK' + newFileName, clobber=True)
    print("###############   all done :)   #############")

###########################################do SEXTRACTOR AND SCAMP##############################

    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/Output/QUICK' + newFileName,
             '/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits')

    def subprocess_cmd(command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print proc_stdout


    subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits;scamp test.cat -c scamp3.conf')

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

    for ii in range (96):
        try:
            header[keys[ii]] = int(values[ii])
        except ValueError:
            try:
                header[keys[ii]] = float(values[ii])
            except ValueError:
                pass #it is a string and can be done manually
    header['CTYPE1'] = 'RA---TPV'
    header['CTYPE2'] = 'DEC--TPV'
    header['CUNIT1'] = 'deg'
    header['CUNIT2'] = 'deg'
    header['RADESYS'] = 'ICRS'


    fits.writeto("/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits",data, header, clobber=True)
    subprocess_cmd('cd /home/jamiedegois/Desktop/pipeStartQuick/sextractorStart; sextractor test.fits -c default2.sex')

    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.fits','/home/jamiedegois/Desktop/pipeStartQuick/Output/QUICK' + newFileName)
    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/better_astr_referror2d_1.svg','/home/jamiedegois/Desktop/pipeStartQuick/Output/CHECKPLOT-' + newFileName.replace(".fits",".svg"))
    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/full_1.cat','/home/jamiedegois/Desktop/pipeStartQuick/Output/FULL-' + newFileName.replace(".fits",".catalogue"))
    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/merged_1.cat','/home/jamiedegois/Desktop/pipeStartQuick/Output/MERGED-' + newFileName.replace(".fits",".catalogue"))
    copyfile('/home/jamiedegois/Desktop/pipeStartQuick/sextractorStart/test.cat','/home/jamiedegois/Desktop/pipeStartQuick/Output/sextractor-' + newFileName.replace(".fits",".cat"))





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

