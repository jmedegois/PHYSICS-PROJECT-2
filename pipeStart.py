import pipeStartQuick_Functions as pip
import Stilts as stilts
import smallPrograms as smalls
import glob2 as glb
import os
import shutil
import numpy as np
import time
import pandas as pd
from IPython import embed
import traceback
from astropy.io.votable import parse
from astropy.io import fits

files= smalls.fileInputList('/home/jamiedegois/Desktop/sextract/stiltsFileList.txt')
pipeStartFiles = smalls.fileInputList('/home/jamiedegois/Desktop/pipeStartQuick/pipeStartFileList.txt')
sextractorFiles= smalls.fileInputList('/home/jamiedegois/Desktop/pipeStartQuick/sexFileList.txt') # fix this

def colomnRemovalString(startIndex,numIterations,numTableColomns,colomnList):
    temp = ''
    for ii in range(0, numIterations, 1):
        for jj in range (0,len(colomnList),1):
            temp = temp + str((startIndex+colomnList[jj]-1) + numTableColomns * (ii)) + ' '
    temp = "'" + temp + "'"
    return temp

def segDate(inlist,startkey,endkey):
    #example of a string "/media/jamiedegois/data1/ASTROSMALL01/2016/02/2016-02-01_ASTROSMALL01_1454314379/01_2016-02-01_211727_DSC_1464-G.fits"
    #program will seperate into a list of lists with all the same date between startkey and end key
    outlist = []
    prevArrayRef=0
    inlist.sort()
    for ii in range(len(inlist)-1):
        if inlist[ii][startkey:endkey]!=inlist[ii+1][startkey:endkey]:
            outlist.append(inlist[prevArrayRef:ii+1])
            prevArrayRef = ii + 1
    outlist.append(inlist[prevArrayRef:])
    return outlist



def joinCatalogues():
    stilts.stiltsTMatchN("60", files, 'ALPHAWIN_J2000', 'DELTAWIN_J2000', "/home/jamiedegois/Desktop/co-adds-10jan-catalogue.fits","ocmd="+'"delcols '+colomnRemovalString(5,len(files)-2,10,[7,8,9,10])+'"')

def runPipeStart(calibrateOnly=False,outPutDir='/home/jamiedegois/Desktop/pipeStartQuick/Output/',calFreq=1):
    masterRefImage='/home/jamiedegois/Desktop/pipeStartQuick/refQuick.fits'
    refImage=''

    for ii in range(0,len(pipeStartFiles)-1,1):
        if ii%calFreq == 0:
            refImage = pip.imageCalibrator(pipeStartFiles[ii], calibrateOnly, False, False, outPutDir, masterRefImage, True)
        else:
            pip.imageCalibrator(pipeStartFiles[ii], calibrateOnly, True, True, outPutDir, refImage, False)


def runSextractor(outputDir='/home/jamiedegois/Desktop/pipeStartQuick/Output'):
    for ii in range(0, len(sextractorFiles) - 1, 1):
        pip.runSextractor(sextractorFiles[ii],outputDir)


def pipeStart(outputDir,startDirectory='',n=20,p=40,k=1500,TychoCatalogueDir='/home/jamiedegois/Desktop/pipeStartQuick/TyIDRef.fits'):

    ################################# Make default Directories ####################################
    try:
        os.mkdir(outputDir+'/Logs',)
    except:
        pass
    try:
        os.mkdir(outputDir + '/FinalImages')
    except:
        pass
    try:
        os.mkdir(outputDir + '/FinalImages/Catalogues')
    except:
        pass
    try:
        os.mkdir(outputDir + '/Temp')
    except:
        pass
    try:
        os.mkdir(outputDir + '/FinalCatalogues')
    except:
        pass
    try:
        os.mkdir(outputDir + '/DiagnosticPlots')
    except:
        pass
    try:
        os.mkdir(outputDir + '/Testing')
    except:
        pass





    ################################# Sort and Break up Images into days ##########################
    filelist= glb.glob(startDirectory+'/**/*.fits')
    filelist.sort()
    masterList=segDate(filelist,-33,-23)

    ################################# Calibrate refImages and Create refList  #####################
    refTable=pd.DataFrame(columns=['Date' ,'Image_Number','Original_Dir','Ref_Dir','Cloud_Flag'])
    for ii in range (len(masterList)):

        if len(masterList[ii])<(2*p+1):
            try:
                file = open(outputDir+"/Logs/Error.txt", 'a')
            except:
                file = open(outputDir+"/Logs/Error.txt", 'w')
            file.write(
                'Error 03 :Too few images in day a day (numImages<2*P)')
            file.write('    date affected:  ' + masterList[ii][0][-33:-23] + '\n')
            file.close()

        else:#enough images in the day, continue with calibrating ref images
            currList= masterList[ii][p:-p:n]
            for jj in range(len(currList)):
                refImageDir=pip.imageCalibrator(currList[jj], False, False, False, outputDir + '/Temp/', True,k)
                if refImageDir!=None:
                    Date=pd.to_datetime(currList[jj][-33:-23]+' '+currList[jj][-22:-16])
                    Image_Number=currList[jj][-11:-7]
                    Original_Dir=currList[jj]
                    Cloud_Flag=False # for now, If we may want to exclude a ref image for any other reason besides clouds flag, we will edit this.
                    row = pd.DataFrame([[Date, Image_Number, Original_Dir, refImageDir, Cloud_Flag]],
                                       columns=['Date', 'Image_Number', 'Original_Dir', 'Ref_Dir', 'Cloud_Flag'], )
                    refTable=refTable.append(row, ignore_index=True)
                else:
                    Date = pd.to_datetime(currList[jj][-33: -23] + ' ' + currList[jj][-22: -16])
                    Image_Number = currList[jj][-11:-7]
                    Original_Dir = currList[jj]
                    Cloud_Flag = True  # for now, If we may want to exclude a ref image for any other reason besides clouds flag, we will edit this.
                    refImageDir=''
                    row = pd.DataFrame([[Date, Image_Number, Original_Dir, refImageDir, Cloud_Flag]],
                                       columns=['Date', 'Image_Number', 'Original_Dir', 'Ref_Dir', 'Cloud_Flag'], )
                    refTable=refTable.append(row, ignore_index=True)
    refTable.to_csv(outputDir+'/Logs/masterRefList.csv')#save ref Table to log files

################################# Make Diagnostic Plot:Num Scources detected v time  #####################
##########################################################################################################





##### initialising stuff for the Day centered aproach ###################
    calibratedList = masterList
    coAddRefDir = []
    catRefDir = []
#########################################################################

    for ii in range(len(masterList)):
        try:
            ################################# apply Ref image Solutions to all other images in day ii #####################
            for jj in range(len(masterList[ii])):
                ####FIND nearest ref Image
                currImageDate=pd.to_datetime(masterList[ii][jj][-33: -23]+' '+masterList[ii][jj][-22:-16])
                cloudlessTable=refTable.query('Cloud_Flag==False')#get rid of cloud affected
                index=np.argmin(np.abs(cloudlessTable.Date - currImageDate))#find index for nearest image

                if np.min(np.abs(cloudlessTable.Date - currImageDate)).seconds>3600:#if ref image taken too long ago, note on a log file
                    file = open(outputDir + '/Logs/' + 'ERRORLOG_REFIMAGES.txt', 'a')
                    file.write('Error @ day:' + str(ii)  +'\n'+'    ImageNumber:'+str(jj)+'     Time to(sec):'+str(np.min(np.abs(cloudlessTable.Date - currImageDate)).seconds)+'\n')
                    file.close()

                refDIR= refTable.iloc[index].Ref_Dir
                ####
                pip.imageCalibrator(masterList[ii][jj],True,False,True,outputDir+'/Temp/',False,k,refDIR)

             ################################# co-add images using SWARP of day ii ########################################

            for kk in range(len(masterList[ii])):
                calibratedList[ii][kk]=outputDir+'/Temp/QUICK'+masterList[ii][kk].split('/')[-1]

            temp=pip.runSwarp(calibratedList[ii],n,outputDir+'/FinalImages/',True)
            coAddRefDir.append(temp)


            ################################# Make Catalougues of co-added images of day ii ###############################
            temp=[]
            temper=''
            for jj in range(len(coAddRefDir[ii])):
                    temper=pip.runSextractor(coAddRefDir[ii][jj],outputDir+'/FinalImages/Catalogues')
                    temp.append(temper)
            catRefDir.append(temp)



            ################################# Make Final catalogue of day ii #######################################
            catRefDir[ii].insert(0, TychoCatalogueDir)#add the TychoRef catalogue to the front of list so stilts knows what to match image catalogues to
            stilts.stiltsTMatchN("120",catRefDir[ii],'ALPHAWIN_J2000', 'DELTAWIN_J2000',outputDir+'/FinalCatalogues/'+catRefDir[ii][1].split('/')[-1][19:29]+'.fits','',outFormat='fits')

            ################################ Delete all temp image #################################################
            for fl in glb.glob(outputDir+'/FinalImages/**/*co-add.weight.fits'):
                os.remove(fl)
            for fl in glb.glob(outputDir+'/FinalImages/**/*.coaddhead'):
                os.remove(fl)
            for kk in range(len(calibratedList[ii])):
                if refTable['Ref_Dir'].str.contains(calibratedList[ii][kk]).any():
                    pass# do not delete if a ref image
                else:
                    os.remove(calibratedList[ii][kk])





        except Exception, e:# if anything goes wrong, just move on to next night
            print "###############################ERORR####################################################"
            print str(e)
            formatted_lines = traceback.format_exc().splitlines()
            print formatted_lines


            file = open(outputDir+'/Logs/'+'ERRORLOG.txt', 'a')
            file.write('\n'+'Error @ day:'+str(ii)+'\n')
            for kk in range(len(formatted_lines)):
                file.write(formatted_lines[kk]+'\n')
            file.write('\n#################################################################################################################################')
            file.close()
            coAddRefDir.append('placeHolder')
            catRefDir.append('Placeholder')














# except Exception, e:
#     print "###############################ERORR####################################################"
#     print str(e)
#     traceback.print_exc()
#     print "########################################################################################"
#     embed()


def Join_AND_correct(outPutCatDIR,TychoCatalogueDir='/home/jamiedegois/Desktop/pipeStartQuick/TyIDRef.fits',
                     FlatfieldDIR='/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/CorrectionMap8Feb_ALMostCompTransitMoreMag9_SecondIteration.fits'):
    # this functions joins all the day catalogues, applys correction maps and only keep columns of intrest
    #####First add time to all co-add catalogues and apply correction maps
    List = smalls.fileInputList('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/SexDirList')[:-1]
    for ii in range(len(List)):
        refFits = fits.open(List[ii])
        #/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalImages/Catalogues/sextractor-QUICK01_2016-02-15_183022_DSC_1061-G.catco-add.cat
        time = List[ii][-42:-32]+' '+List[ii][-31:-25]
        arrayTime = np.array([time] * len(refFits[2].data))
        c1=fits.Column(name="DateTime", format="A17",array=arrayTime)
        newColumns=refFits[2].columns[:6] + c1
        fitsFlat=fits.open(FlatfieldDIR)
        Map1 = fitsFlat[0].data
        xBegin=fitsFlat[0].header['XBEGIN  ']
        xEnd = fitsFlat[0].header['XEnd    ']
        yBegin=fitsFlat[0].header['YBEGIN  ']
        yEnd = fitsFlat[0].header['YEnd    ']
        hdu = fits.BinTableHDU.from_columns(newColumns)

        #####remove all entries not in flat field region#####
        selectionBoolx=np.logical_and(hdu.data['XWIN_IMAGE']>(xBegin+1),hdu.data['XWIN_IMAGE']<(xEnd-1))
        selectionBooly=np.logical_and(hdu.data['YWIN_IMAGE']>(yBegin+1),hdu.data['YWIN_IMAGE']<(yEnd-1))
        selectionBool=np.logical_and(selectionBoolx,selectionBooly)
        hdu.data=hdu.data[selectionBool]
        ###########apply flat field##########################
        hdu.data['FLUX_AUTO']=np.divide(hdu.data['FLUX_AUTO'],Map1[np.int_(hdu.data['YWIN_IMAGE'])-yBegin,np.int_(hdu.data['XWIN_IMAGE'])-xBegin])
        hdu.data['FLUXERR_AUTO'] = np.divide(hdu.data['FLUXERR_AUTO'], Map1[
            np.int_(hdu.data['YWIN_IMAGE']) - yBegin, np.int_(hdu.data['XWIN_IMAGE']) - xBegin])
        hdu.writeto(List[ii] + ".fits", overwrite=True)
        # newColumns[0].array=np.divide(newColumns[0].array,Map1[np.int_(newColumns[3].array)%6000,np.int_(newColumns[2].array)% 6000])#applying correction maps to flux and flux err.....
        #                                                                                                                             # mod 6000 cos some ximages are outside image????
        # newColumns[1].array = np.divide(newColumns[1].array,Map1[np.int_(newColumns[3].array) % 6000, np.int_(newColumns[2].array)% 6000] )
        #hdu = fits.BinTableHDU.from_columns(newColumns)
        print ii/(len(List)+1.0)

    for ii in range(len(List)):
        List[ii]=List[ii]+".fits"
        print ii / (len(List) + 1.0)
    # /media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalImages/Catalogues/sextractor-QUICK01_2016-02-15_190932_DSC_1161-G.catco-add.cat.fits
    print List[0][-47:-37]
    DaySeperatedList=segDate(List,-47,-37)
    for ii in range(len(DaySeperatedList)):
        DaySeperatedList[ii].insert(0,TychoCatalogueDir)  # add the TychoRef catalogue to the front of list so stilts knows what to match image catalogues to
        print str(DaySeperatedList[ii][1][-47:-37])
        stilts.stiltsTMatchN("120", DaySeperatedList[ii], 'ALPHAWIN_J2000', 'DELTAWIN_J2000',outPutCatDIR+str(DaySeperatedList[ii][1][-47:-37])+"._corected_FLAT_with8Feb_.fits",'',HDUNum='1',outFormat="fits")




    # stilts.stiltsTMatchN(60,DIRLIST,"$1","2",
    #                      '/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/OUTPUT.vot',"ocmd="+'"delcols '+colomnRemovalString(5,len(files)-2,10,[7,8,9,10])+'"')




##################################  Commands Here  ###########################################
#
# pipeStart('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIP_300','/media/jamiedegois/data1/ASTROSMALL01/2016/02/2016-02-01_ASTROSMALL01_1454314379',k=1000,n=300,p=120)

Join_AND_correct('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/')


# DIRLIST=smalls.fileInputList('/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/TestPIPE/FinalCatalogues/dir list')
#
# print colomnRemovalString(5,len(DIRLIST),10,[5,6,7,8,9,10])[0:-1]
# embed()






# stilts.removeColomn("/home/jamiedegois/Desktop/some.fits","//home/jamiedegois/Desktop/some_short.fits",colomnRemovalString(5,130,6,[2,3,4,5,6]))
#runPipeStart(False,"/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/31July/",7)
# pip.runSwarp(10,'/media/jamiedegois/JaimedeGois2TBPortable/Sem_2/26_June/swarpOutput/')
# runSextractor('/media/jamiedegois/JaimedeGois2TBPortable/swarpOutputCataloguesBright')
# joinCatalogues()




##############################################################################################
# string=''
# for ii in range(6,337,6):
#     string=string+","+"$"+str(ii)
# print string

















########### remove all the unnecasarry infomation from catalogues
###########  remove ext 1
################################################################################
# for ii in range(0,len(files),1):
#     stilts.removeColomn(files[ii]+"#2",files[ii],"'9 10 11 12'")


# pip.pipeStartQuick("01_2016-01-07_163141_DSC_0730-G.fits")
#################################################################################


#stilts.stiltsTMatchN("60",files,'ALPHAWIN_J2000','DELTAWIN_J2000',files[0]+"2")

##########Join all the catalogues together
#add a new adress colomn
# stilts.stiltsColomnAdd(files[0],files[0]+"2","1","ADRESS_ALPHA","ALPHAWIN_J2000")
# stilts.stiltsColomnAdd(files[0]+"2",files[0]+"2","2","ADRESS_DELTA","DELTAWIN_J2000")
# stilts.stiltsColomnAdd(files[0]+"2",files[0]+"2","3","NumDetects","1")
# stilts.stitlsORJoin("120","ALPHAWIN_J2000","DELTAWIN_J2000","ALPHAWIN_J2000","DELTAWIN_J2000",files[0]+"2",files[1],files[0]+"2")
# smalls.addAdress(files[0]+"2",20,16,17)

# for ii in range(2,len(files),1):
# for ii in range(2,22,1):
#     start = time.time()
#
#     stilts.stitlsORJoin("120","ADRESS_ALPHA","ADRESS_DELTA","ALPHAWIN_J2000","DELTAWIN_J2000",files[0]+"2",files[ii],files[0]+"2")
#     smalls.addAdress(files[0]+"2",20+((ii-1)*9),16+((ii-1)*9),17+((ii-1)*9))
#     print ii
#
#     print (time.time()-start)

#

















































########################################TASK Centered approach##########################
#
#
# ################################# apply Ref image Solutions to all other images ###############
# for ii in range(len(masterList)):
#     for jj in range(len(masterList[ii])):
#         ####FIND nearest ref Image
#         currImageDate = pd.to_datetime(masterList[ii][jj][-33: -23] + ' ' + masterList[ii][jj][-22:-16])
#         cloudlessTable = refTable.query('Cloud_Flag==False')  # get rid of cloud affected
#         index = np.argmin(np.abs(cloudlessTable.Date - currImageDate))  # find index for nearest image
#         refDIR = refTable.iloc[index].Ref_Dir
#         ####
#         pip.imageCalibrator(masterList[ii][jj], True, False, True, outputDir + '/Temp/', False, k, refDIR)
#
# ################################# co-add images using SWARP ###################################
# calibratedList = masterList
# for ii in range(len(masterList)):
#     for kk in range(len(masterList[ii])):
#         calibratedList[ii][kk] = outputDir + '/Temp/QUICK' + masterList[ii][kk].split('/')[-1]
#
# coAddRefDir = []
# for ii in range(len(masterList)):
#     try:
#         temp = pip.runSwarp(calibratedList[ii], n, outputDir + '/FinalImages/', True)
#         coAddRefDir.append(temp)
#     except:
#         print "here 101"
#         embed()
#
# ################################# Make Catalougues of co-added images #########################
# catRefDir = []
# for ii in range(len(masterList)):
#     temp = []
#     temper = ''
#     for jj in range(len(coAddRefDir[ii])):
#         temper = pip.runSextractor(coAddRefDir[ii][jj], outputDir + '/FinalImages/Catalogues')
#         temp.append(temper)
#     catRefDir.append(temp)
#
# ################################# Make Final catalogues #######################################
# for ii in range(len(catRefDir)):
#     catRefDir[ii].insert(0, TychoCatalogueDir)
#     stilts.stiltsTMatchN("120", catRefDir[ii], 'ALPHAWIN_J2000', 'DELTAWIN_J2000',
#                          outputDir + '/FinalCatalogues/' + catRefDir[ii][1].split('/')[-1][19:29] + '.vot', '')
#
#
#
#
