import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def stitlsORJoin(inputError, alpha1,delta1,alpha2,delta2,inFile1,inFile2,outFile):
    #takes in two fits catalogues, OR joins them
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tskymatch2 ifmt1=fits ifmt2=fits omode=out out='+
                   outFile+' ofmt=fits ra1='+alpha1+' dec1='+delta1+' ra2='+alpha2+' dec2='+delta2+' error='+
                   inputError+' join=1or2 find=best in1='+inFile1+' in2='+inFile2)

def stitlsANDJoinCSV(inputError, alpha1,delta1,alpha2,delta2,inFile1,inFile2,outFile):
    #takes in two fits catalogues, AND joins them
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tskymatch2 ifmt1=fits ifmt2=fits omode=out out='+
                   outFile+' ofmt=csv-noheader ra1='+alpha1+' dec1='+delta1+' ra2='+alpha2+' dec2='+delta2+' error='+
                   inputError+' join=1and2 find=best in1='+inFile1+' in2='+inFile2)

def stiltsTMatchN(inputError,inDirectoryList, inAlphaCol, inDeltaCol,outfile,outCommands,inFormat='fits',outFormat='votable-binary-inline',HDUNum='2' ):
    inNString =  'in' + str(1) + '=' + inDirectoryList[0] +' '
    ifmtNString =  'ifmt' + str(1) + '=' + inFormat+' '
    valuesNString =  'values' + str(1) + '="' + inAlphaCol + ' ' + inDeltaCol + '" '
    for ii in range(1,len(inDirectoryList)-1,1):
        inNString=inNString+'in'+str(ii+1)+'='+inDirectoryList[ii]+"#"+HDUNum+' '
        ifmtNString=ifmtNString+'ifmt'+str(ii+1)+'='+inFormat+' '
        valuesNString=valuesNString+'values'+str(ii+1)+'="'+inAlphaCol+' '+inDeltaCol+'" '
    print inNString
    print ifmtNString
    print valuesNString
    subprocess_cmd('java -jar /home/jamiedegois/bin/topcat/stilts.jar tmatchn'+' nin='+str(len(inDirectoryList)-1)+' '+ifmtNString+' matcher=sky'+' '+inNString+' omode=out out='+outfile+' ofmt='+outFormat+'  multimode=pairs'+' params='+inputError+' '+valuesNString+' '+outCommands)



def removeColomn(inFile,outFile,inColomnNumber):
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tpipe in='+inFile+' omode=out out='+outFile+' ofmt=fits cmd="delcols '+inColomnNumber+'"')

def stiltsColomnAdd(inFile,outFile,inBeforeColNum,inNewColName,colExpression):
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tpipe in='+inFile+' omode=out out='+outFile+' ofmt=fits cmd="addcol -before '+inBeforeColNum+' '+inNewColName+' '+colExpression+'"')
