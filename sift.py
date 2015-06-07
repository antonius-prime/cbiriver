import os
import numpy as np
import Image

def process_image(imagename, resultname,params="--edge-thresh 10 --peak-thresh 5"):
    """ Process an image and save the results in a file. """
    if imagename[-3:] != 'pgm':
        # create a pgm file
        im = Image.open(imagename).convert('L')
        im.save('tmp.pgm')
        imagename = 'tmp.pgm'

    cmmd = str("sift "+imagename+" --output="+resultname+
               " "+params)
    os.system(cmmd)
    print 'processed', imagename, 'to', resultname

def read_features_from_file(filename):
    """ Read feature properties and return in matrix form. """
    f = np.loadtxt(filename)
    return f[:, :4], f[:, 4:] # feature locations, descriptors

def write_features_to_file(filename,locs,desc):
    """ Save feature location and descriptor to file. """
    np.savetxt(filename, np.hstack((locs, desc)))
