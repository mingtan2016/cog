'''
Created on Jul 31, 2016

@author: mingtan
'''

import sys
from DataHandler import DataHandler
from operator import itemgetter
class FeatureProcesser:    

    def __init__(self, datafile, orifeaturelist, newfeaturelist):
        self.datafile = datafile
        self.orifeaturelist = orifeaturelist
        self.newfeaturelist = newfeaturelist
    '''
	Go through the training data, and generate the feature vocabulary list
    '''
    def GetFeatureVocabs(self):
        self.ReadOriFeatureList()
        self.dataHandler = DataHandler(self.datafile)
        self.featVocabs = dict()
        ind = 0
        for feature_list in self.dataHandler:
            if(feature_list == None):
                break
            for idx, feat in enumerate(feature_list):
                feat = feat.strip()
                if(self.dataHandler.featidx2name[idx]=='ZIP'):
                    continue
                if(self.dataHandler.featidx2name[idx]=='MDMAUD'):
                    for ii in range(4):
                        if('MDMAUD_POS'+feat[ii] not in  self.featVocabs):
                            self.featVocabs['MDMAUD_POS'+feat[ii] ]=ind
                            ind += 1
                        
                elif(self.dataHandler.featidx2name[idx]=='DOMAIN'):
                    if(feat != ''):
                        for ii in range(2):
                            if( 'DOMAIN_POS'+feat[ii]  not in  self.featVocabs):
                                self.featVocabs['DOMAIN_POS'+feat[ii]]=ind
                                ind += 1
                        
                        
                elif(self.dataHandler.featidx2name[idx]=='TCODE'):
                    code1 = feat[:3]
                    if('TCODE_PART1_'+code1 not in  self.featVocabs):
                        self.featVocabs['TCODE_PART1_'+code1]=ind
                        ind += 1
                    code2 = feat[3:]
                    if(code2 != ''):
                        if( 'TCODE_PART2_'+code2 not in  self.featVocabs):
                            self.featVocabs['TCODE_PART2_'+code2]=ind
                            ind += 1
                elif(self.dataHandler.featidx2name[idx]=='CONTROLN'):
                    pass        
                elif(self.dataHandler.featidx2name[idx]=='TARGET_B'):
                    pass
                elif(self.dataHandler.featidx2name[idx]=='TARGET_D'):
                    pass
                elif(self.mapOriFeatureType[ self.dataHandler.featidx2name[idx] ] == 'Num'):
                    if( self.dataHandler.featidx2name[idx] not in  self.featVocabs):
                        self.featVocabs[self.dataHandler.featidx2name[idx]] = ind
                        ind += 1
                elif(self.mapOriFeatureType[ self.dataHandler.featidx2name[idx] ] == 'Date'):
                    if(feat == '' or len(feat)!=4):
                        if( self.dataHandler.featidx2name[idx] + '_EMPTY' not in  self.featVocabs):
                            self.featVocabs[self.dataHandler.featidx2name[idx] + '_EMPTY'] = ind
                            ind += 1
                    elif( self.dataHandler.featidx2name[idx] not in  self.featVocabs):
                        self.featVocabs[self.dataHandler.featidx2name[idx]] = ind
                        ind += 1

                elif(self.mapOriFeatureType[ self.dataHandler.featidx2name[idx] ] == 'Char'):
                    if(feat == ''):
                        if( self.dataHandler.featidx2name[idx] + "_EMPTY" not in  self.featVocabs):
                            self.featVocabs[self.dataHandler.featidx2name[idx] + "_EMPTY" ] = ind
                            ind += 1
                    else:
                        if( self.dataHandler.featidx2name[idx] + "_" + feat not in  self.featVocabs):
                            self.featVocabs[self.dataHandler.featidx2name[idx] + "_"+ feat ] = ind
                            ind += 1
        self.featsize = len(self.featVocabs )
        
        fo = open(self.newfeaturelist, 'w')
        featVocabs_sortd = sorted(self.featVocabs.items(), key=itemgetter(1))
        for ll in featVocabs_sortd:
            fo.write(str(ll[0])+'\t'+str(ll[1])+'\n')
        fo.close()
    '''
	Generate feature vectors according to feature vocabularies for each dataset.
    '''
    def GetFeatureFile(self, infile, outfile):
        self.dataHandler = DataHandler(infile)
        fo = open(outfile, 'w')        
        for feature_list in self.dataHandler:
            targetb = 0
            targetd = 0.0
            control = 0
            ofeatures = [0.0 for i in range(self.featsize)]
            if(feature_list == None):
                break
            for idx, feat in enumerate(feature_list):
                feat = feat.strip()
                
                if(self.dataHandler.featidx2name[idx]=='MDMAUD'):
                    for ii in range(4):
                        if('MDMAUD_POS'+feat[ii] in  self.featVocabs):
                            ofeatures[self.featVocabs['MDMAUD_POS'+feat[ii] ] ] +=1.
                        
                elif(self.dataHandler.featidx2name[idx]=='DOMAIN'):
                    if(feat != ''):
                        for ii in range(2):
                            if( 'DOMAIN_POS'+feat[ii]  in  self.featVocabs):
                                ofeatures[self.featVocabs['DOMAIN_POS'+feat[ii]] ] +=1.
                        
                        
                elif(self.dataHandler.featidx2name[idx]=='TCODE'):
                    code1 = feat[:3]
                    if('TCODE_PART1_'+code1 in  self.featVocabs):
                        ofeatures[self.featVocabs['TCODE_PART1_'+code1]] +=1.
                    code2 = feat[3:]
                    if(code2 != ''):
                        if( 'TCODE_PART2_'+code2 in  self.featVocabs):
                            ofeatures[ self.featVocabs['TCODE_PART2_'+code2] ] += 1.
                        
                elif(self.dataHandler.featidx2name[idx]=='TARGET_B'):
                    targetb = int(feat)
                elif(self.dataHandler.featidx2name[idx]=='TARGET_D'):
                    targetd = float(feat)
                elif(self.dataHandler.featidx2name[idx]=='CONTROLN'):
                    control = int(feat)                       
                elif(self.mapOriFeatureType[ self.dataHandler.featidx2name[idx] ] == 'Num'):
                    if( self.dataHandler.featidx2name[idx] in  self.featVocabs):
                        vv = 0.0
                        if(feat != ''):
                            vv = float(feat)
                        ofeatures[self.featVocabs[self.dataHandler.featidx2name[idx]] ] += float(vv)

                elif(self.mapOriFeatureType[ self.dataHandler.featidx2name[idx] ] == 'Date'):
                    if(feat == '' or len(feat)!=4):
                        if(self.dataHandler.featidx2name[idx]+ '_EMPTY' in self.featVocabs):
                            ofeatures[ self.featVocabs[self.dataHandler.featidx2name[idx] + '_EMPTY'] ] += 1
                    elif( self.dataHandler.featidx2name[idx] in  self.featVocabs):
                        yy = float(feat[:2])
                        mm = float(feat[2:]) / 12.0
                        ofeatures[ self.featVocabs[self.dataHandler.featidx2name[idx]] ] += yy + mm

                elif(self.mapOriFeatureType[ self.dataHandler.featidx2name[idx] ] == 'Char'):
                    if(feat == ''):
                        if( self.dataHandler.featidx2name[idx] + "_EMPTY" in  self.featVocabs):
                            ofeatures[ self.featVocabs[self.dataHandler.featidx2name[idx] + "_EMPTY" ] ] = 1.
                    else:
                        if( self.dataHandler.featidx2name[idx] + '_' + feat in  self.featVocabs):
                            ofeatures[ self.featVocabs[self.dataHandler.featidx2name[idx] + '_' + feat ] ]= 1.
            #fo.write(str(targetb)+ '\t'+ str(targetd)+'\t'+' '.join(map(str, ofeatures)) + '\n')
            fo.write(str(control) + '\t' + str(targetb)+ '\t'+ str(targetd)+'\t')
            for oo in range(len(ofeatures)):
                if(ofeatures[oo] != 0.0):
                    fo.write(str(oo)+':'+str(ofeatures[oo])+ ' ')
            fo.write('\n')
            fo.flush()
        fo.close()
    '''
	Read a list of original input variables, in order to get their type: Date, Num and Char. I added Date manually for special take-care of Date variables. 
    '''    
    def ReadOriFeatureList(self):
        fi = open(self.orifeaturelist, 'r')
        
        self.mapOriFeatureType = dict()
        for line in fi:
            (dname,dtype) = line.strip().split()
            self.mapOriFeatureType[dname.strip()] =  dtype.strip()
        fi.close()
        
        
if __name__ in '__main__':
    
    if(len(sys.argv)!=7):
        print 'Usage: train_file_name, test_file_name, original_feature_list_file_name, output_generated_feature_list_file_name, output_train_feature_file_name, output_test_feature_file_name'
        sys.exit()
    trainfile=sys.argv[1]
    devfile = sys.argv[2]
    orifeaturelist=sys.argv[3]
    newfeaturelist = sys.argv[4]
    otrainFeatureFile=sys.argv[5]
    odevFeatureFile = sys.argv[6]
    fp = FeatureProcesser(trainfile, orifeaturelist, newfeaturelist)
    fp.GetFeatureVocabs()
    print 'fp.GetFeatureVocabs() finish'
    fp.GetFeatureFile(trainfile, otrainFeatureFile)
    print 'fp.GetFeatureFile(trainfile, otrainFeatureFile) finish'
    fp.GetFeatureFile(devfile, odevFeatureFile)
    print 'fp.GetFeatureFile(devfile, odevFeatureFile) finish'
    
