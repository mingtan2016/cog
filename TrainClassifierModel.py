import sys
import pickle
from sklearn import svm

class ClassifierModel:
    def __init__(self, omodelclassifier, omodelreg, feature_size):
        self.omodelclassifier = omodelclassifier
        self.omodelreg = omodelreg
        self.feature_size = feature_size



    def train_classifier(self, trainfile):
        print 'Feature Size', self.feature_size
        
        fi = open(trainfile, 'r')
        X = []
        Y = []
        for line in fi:
            line = line.strip()
            (control, targetb, _, featurestr) = line.split('\t')
            Y.append(int(targetb))
            xx = [0.0 for i in range(self.feature_size)]
            featpairs = featurestr.split()
            for feat in featpairs:            
                (fidx, vv) = feat.split(':')
                xx[int(fidx)] = float(vv)
            X.append(xx)
        print 'Training start'
        '''
        Training start
        '''
        class_weights = {0:0.1, 1:0.9} #for unbalanced data, label-0 is much more than label-1. 
        clf = svm.LinearSVC(class_weight=class_weights)
        clf.fit(X, Y)
        '''
        Training End
        '''
        print 'Classifier Training End'
        pickle.dump(clf, open(self.omodelclassifier, 'wb'))
        self.clf = clf

    def train_predict(self, trainfile):
        print 'Feature Size', self.feature_size
        
        fi = open(trainfile, 'r')
        X = []
        Y = []
        for line in fi:
            line = line.strip()
            (control, targetb, targetd, featurestr) = line.split('\t')
            if(int(targetb) == 0):
                continue
            Y.append(float(targetd))
            xx = [0.0 for i in range(feature_size)]
            featpairs = featurestr.split()
            for feat in featpairs:            
                (fidx, vv) = feat.split(':')
                xx[int(fidx)] = float(vv)
            X.append(xx)
        print 'Regression Training start'
        
        '''
        Training start
        '''
        reg = svm.LinearSVR()
        reg.fit(X, Y)
        '''
        Training End
        '''
        print 'Regression Training End'
        pickle.dump(reg, open(self.omodelreg, 'wb'))
        self.reg = reg
        
    def readCmodel(self):
        pkl_file = open(self.omodelclassifier, 'rb')
        self.clf = pickle.load(pkl_file)
        pkl_file.close()
        
    def readRmodel(self): 
        pkl_file = open(self.omodelreg, 'rb')
        self.reg = pickle.load(pkl_file)
        pkl_file.close()
    
    '''
	inference function for binary classification
    ''' 
    def classify(self, X):    
        ytest = self.clf.predict(X)
        return ytest
    '''
	inference function for regression. 
    '''
    def predict(self, X):
        ytest = self.reg.predict(X)
        return ytest         
        
if __name__ == '__main__':
    if(len(sys.argv)!=5):
        print 'Usage: train_feature_file, output_model_for_classifier, output_model_for_predict, feature_size'
        sys.exit()
    trainfile = sys.argv[1]
    modelclassifier = sys.argv[2]
    modelreg = sys.argv[3]
    feature_size = int(sys.argv[4])
    cm = ClassifierModel(modelclassifier, modelreg, feature_size)
    cm.train_classifier(trainfile)
    cm.train_predict(trainfile)
