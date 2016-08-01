'''
Created on Jul 31, 2016

@author: mingtan
'''
import sys

from TrainClassifierModel import ClassifierModel


def prediction(cm, feature_size, testdata, outputfile):
    fi = open(testdata, 'r')
    fo = open(outputfile, 'w')
    fo.write('CONTROLN,TARGET_D\n')
    sumrev = 0.0
    ind = 0
    for line in fi:
        (control, _,targetd,featurestr) = line.strip().split('\t')
        featvec = [0.0 for i in range(feature_size)]
        featpairs = featurestr.split()
        for feat in featpairs:            
            (fidx, vv) = feat.split(':')
            featvec[int(fidx)] = float(vv)
        X = [featvec]
        clf_pred = cm.clf.predict(X)[0]
        oo = 0.0
        if(clf_pred <=0.01):
            oo = 0.0
        else:
            oo = cm.reg.predict(X)[0]
        if(oo<0.0):
            oo = 0.0
        fo.write(control+','+str(oo)+'\n')
        fo.flush()
        if(oo>0.68):
            sumrev = sumrev + float(targetd) - 0.68
        ind += 1
        print "index {0}, targetd {1}, pred_label {2}, pred_amount {3}".format(ind, targetd, clf_pred, oo)
    fi.close()
    fo.close()
    print "final total revenue:", sumrev
    
if __name__ == '__main__':
    if(len(sys.argv)!=6):
	print 'usage: classifier_model_location, regression_model_location, feature_vector_size, test_feature_file, output_submission_file'
	sys.exit()
    clf_model = sys.argv[1]
    reg_model = sys.argv[2]
    feature_size = int(sys.argv[3])
    testdata = sys.argv[4]
    outputfile = sys.argv[5]
    
    cm = ClassifierModel(clf_model, reg_model, feature_size)
    cm.readCmodel()
    cm.readRmodel()
    
    prediction(cm, feature_size, testdata, outputfile)
    
