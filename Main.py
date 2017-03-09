import PipeStartQuick as pip
import Stilts as stilts
import smallPrograms as smalls
import time




files= smalls.fileInputList('/home/jamiedegois/Desktop/sextract/stiltsFileList.txt')
########### remove all the unnecasarry infomation from catalogues
###########  remove ext 1
################################################################################
# for ii in range(0,len(files),1):
#     stilts.removeColomn(files[ii]+"#2",files[ii],"'9 10 11 12'")


# pip.pipeStartQuick("01_2016-01-07_163141_DSC_0730-G.fits")
#################################################################################


##########Join all the catalogues together
#add a new adress colomn
stilts.stiltsColomnAdd(files[0],files[0]+"2","1","ADRESS_ALPHA","ALPHAWIN_J2000")
stilts.stiltsColomnAdd(files[0]+"2",files[0]+"2","2","ADRESS_DELTA","DELTAWIN_J2000")
stilts.stiltsColomnAdd(files[0]+"2",files[0]+"2","3","NumDetects","1")
stilts.stitlsORJoin("120","ALPHAWIN_J2000","DELTAWIN_J2000","ALPHAWIN_J2000","DELTAWIN_J2000",files[0]+"2",files[1],files[0]+"2")
smalls.addAdress(files[0]+"2",20,16,17)

# for ii in range(2,len(files),1):
for ii in range(2,22,1):
    start = time.time()

    stilts.stitlsORJoin("120","ADRESS_ALPHA","ADRESS_DELTA","ALPHAWIN_J2000","DELTAWIN_J2000",files[0]+"2",files[ii],files[0]+"2")
    smalls.addAdress(files[0]+"2",20+((ii-1)*9),16+((ii-1)*9),17+((ii-1)*9))
    print ii

    print (time.time()-start)


