from astropy.io import fits
import smallPrograms as smalls
import numpy as np
import matplotlib.pyplot as plt

files= smalls.fileInputList('/home/jamiedegois/Desktop/pipeStartQuick/NumSexDetects.txt')
array= [None] * (len(files)-1)

for ii in range(len(array)):
    cat = fits.open(files[ii])
    array[ii] = len(cat[2].data)
    print ii


plt.figure(0)
plt.plot(range(len(array)), array)
plt.grid(True)
plt.xticks(np.arange(0,len(array),70))
plt.show()
