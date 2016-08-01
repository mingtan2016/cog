'''
Created on Jul 31, 2016

@author: mingtan
'''
import sys

class DataHandler:
    def __init__(self, fname):
        self.fi = open(fname, 'r')
        headerline = self.fi.readline().strip()
        featurenames = headerline.split(',')
        self.featidx2name = dict()
        self.featname2idx = dict()
        for ind,fn in enumerate(featurenames):
            self.featidx2name[ind] = fn
            self.featname2idx[fn] = ind
        self.ii = 0
    def __iter__(self):
        return self

    def next(self):
        line = self.fi.readline()
        if(not line):
            return None
        else:
            self.ii += 1
            print self.ii
            return line.strip().split(',')
    
    def __del__(self):
        print 'close file'
        self.fi.close()

if __name__ == '__main__':
    fname = sys.argv[1]
    dhandler = DataHandler(fname)
    for featlist in dhandler:
        if(featlist == None):
            break
