'''
Created on Jul 31, 2016

@author: mingtan
'''
import sys

minvaluemap = dict()
maxvaluemap = dict()

'''
	compute the min and max value for every column (features). 
'''
def MinMaxValues(oriTrainData):

    fi = open(oriTrainData, 'r')
    ind = 0
    for line in fi:
        line = line.strip()
        (control, targetb, targetd, featurestr) = line.split('\t')
        featpairs = featurestr.strip().split()
        for fpair in featpairs:
            fn, fv = fpair.split(':')
            fv = float(fv)
            if(fn not in minvaluemap):
                minvaluemap[fn] = fv
            else:
                if(minvaluemap[fn] > fv):
                    minvaluemap[fn] = fv
            if(fn not in maxvaluemap):
                maxvaluemap[fn] = fv
            else:
                if(maxvaluemap[fn] < fv):
                    maxvaluemap[fn] = fv    
        print ind
        ind += 1
    fi.close()

'''
	rescale the feature values by (feature-min)/(max-min)
'''
def Normalize(oriData, newData):
    fi = open(oriData, 'r')
    fo = open(newData,'w')
    for line in fi:
        line = line.strip()
        (control, targetb, targetd, featurestr) = line.split('\t')
        featpairs = featurestr.strip().split()
        fo.write(control + '\t' +targetb+'\t'+targetd+'\t')
        for fpair in featpairs:
            fn, fv = fpair.split(':')
            fv = float(fv)
            minfv = minvaluemap[fn]
            maxfv = maxvaluemap[fn]
            if(maxfv == minfv):
                fv = fv/maxfv
            elif(maxfv > minfv):
                fv = (fv-minfv)/(maxfv-minfv)
            else:
                print 'ERROR'
            fo.write(fn+':'+str(round(fv,4))+' ')
        fo.write('\n')
    fi.close()
    fo.close()
    
if __name__ == '__main__':
    oriTrainData = sys.argv[1]
    oriDevData = sys.argv[2]
    newTrainData = sys.argv[3]
    newDevData = sys.argv[4]
    
    MinMaxValues(oriTrainData)
    print 'MinMax Value Computation Finished.'
    Normalize(oriTrainData, newTrainData)
    print 'Normalized train set finished.'
    Normalize(oriDevData, newDevData)
    print 'Noramal validation set finished.'
