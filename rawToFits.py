# The script is a massive mess, but here is the relevant part:
# -------------------------
#
#
#     rawHeader = rawHDU.header
#     # read image size in header
#     width = rawHeader['NAXIS1']
#     height = rawHeader['NAXIS2']
#     rawIMG = rawHDU.data
#
# colIMG_G = np.zeros((height, width), dtype="uint16")
#         colIMG_G[1::2, ::2] = rawIMG[1::2, ::2]     # GREEN 2
#         colIMG_G[::2, 1::2] = rawIMG[::2, 1::2]     # GREEN 1
#         colIMG_G[2::2, 2::2] = (rawIMG[2::2, 1:width - 2:2] +
#                                 rawIMG[2::2, 3::2] +
#                                 rawIMG[1:height - 2:2, 2::2] +
#                                 rawIMG[3::2, 2::2]) / 4    # RED -> GREEN
#         colIMG_G[1:height - 2:2, 1:width - 2:2] = (rawIMG[:height - 2:2, 1:width - 2:2] +
#                                                    rawIMG[2:height:2, 1:width - 2:2] +
#                                                    rawIMG[1:height - 2:2, :width - 2:2] +
#                                                    rawIMG[1:height - 2:2, 2:width:2]) / 4     # BLUE -> GREEN
# # flip picture to follow fits standard and write
# pyfits.writeto(outG, np.flipud(colIMG_G), rawHDU.header)
# -------------------------
# - rawHDU is the non de-Bayered fits object coming straight from the raw file.
# - colIMG_G is the interpolated picture (half of the pixels are interpolated, the other half are unmodified raw)
# So I think if you reverse the process, you should be able to get to the actual raw green pixels, namely colIMG_G[1::2, ::2] and colIMG_G[::2, 1::2].
# Don't forget to flip the picture once imported (flipud), otherwise those coordinates won't match the actual raw green pixels.
#
# import sys
# sys.path.append("/home/jamiedegois/.local/lib/python2.7/site-packages/")
# import os
# os.environ["LD_LIBRARY_PATH"] = "/home/jamiedegois/LibRaw-0.18.1/lib" #+ os.environ["LD_LIBRARY_PATH"]


import rawpy



from PIL import Image
raw = rawpy.imread('/home/jamiedegois/Desktop/sources/Dark images/DSC_1038.NEF')
rgb = raw.raw_image()
print (rgb[10])
