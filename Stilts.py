import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def stitlsORJoin(inputError, alpha1,delta1,alpha2,delta2,inFile1,inFile2,outFile):
    #takes in two fits catalogues, AND joins them
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tskymatch2 ifmt1=fits ifmt2=fits omode=out out='+outFile+' ofmt=fits ra1='+alpha1+' dec1='+delta1+' ra2='+alpha2+' dec2='+delta2+' error='+inputError+' join=1or2 find=best in1='+inFile1+' in2='+inFile2)

def removeColomn(inFile,outFile,inColomnNumber):
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tpipe in='+inFile+' omode=out out='+outFile+' ofmt=fits cmd="delcols '+inColomnNumber+'"')

def stiltsColomnAdd(inFile,outFile,inBeforeColNum,inNewColName,colExpression):
    subprocess_cmd('cd /home/jamiedegois/bin/topcat/; java -jar stilts.jar tpipe in='+inFile+' omode=out out='+outFile+' ofmt=fits cmd="addcol -before '+inBeforeColNum+' '+inNewColName+' '+colExpression+'"')
