Training Process:
==================

Generally, I build two models to solve this prediction problem. One is binary classification, which is used to determined whether there is a response. If it labels the testing data as 0, the PREDICT_D value is set to 0. If the testing data is labeled as 1, another model for regression is used to predict the PREDICT_D. 

For the binary classification step, all training examples are used. For the prediction step, only the examples with responses are used for training. 


The code is built on PYTHON, using the Scikit-Learn package. The classifier is based on Linear SVM classifier, and the regressor is based on Linear SVM regressor. 

There are following steps to complete the training and testing. 

1) Feature creation. 

Since there are many categorical variables, I used one-hot vectors to represent those categorical features. For example, each different value X in the input variable A, there is a binary feature call A_X. There is an additional feature named 'A_Empty' in case there is no value for the input variable A. 

There is only one single feature for numerical valuables.

There are several special cases. 
a) ZIP: Although ZIP is a categorical variable, there are too many different values. Considering reducing the memory usage, I did not use this variable. b) MDMAUD: four bytes respectively have their own meanings. So for each byte, I regard it as independent categorical variable. c) DOMAIN: two bytes respectively have their own meanings. So for each byte, I regard it as independent categorical variable. d) All DATE vaiables: The last two digit 'mm' is month, the final value is yy + mm/12

The command is:

python FeatureProcessor.py  original_train_file original_validation_file, feature_type_list_file, output_feature_vocab_list_file, output_train_feature_file, output_validation_feature_file


original_train_file:                    cup98LRN.txt
<br>
original_validation_file:               cup98VAL.txt
<br>
feature_type_list_file :                It is manually transfered from feature_types.txt. 
<br>
For example: 	                        ODATEDW  Date = manually change Char to Date
                                        OSOURCE     Char
                                        TCODE       Num
                                        .....
<br>
output_feature_vocab_list_file    	the list of generated features as well as their indices. 
<br>
output_train_feature_file		the output feature files for training set. 
<br>
output_validation_feature_file	the output feature files for validation set.


2) Normalization

Since the values of features are in different scale, I did a simple feature normalization to rescale all values to [0,1] in the training set, ie. 
<br>
newvalue = (oldvalue-minvalue)/(maxvalue-minvalue)
<br>
where maxvalue and minvalue is the maxminum and mininum of each column (feature)

The command is:
python NormalizeData.py original_output_train_feature_file original_output_validation_feature_file normalized_output_train_feature_file normalized_output_validation_feature_file

original_output_train_feature_file: output_train_feature_file from Step 1
original_output_validation_feature_file:  output_validation_feature_file from Step 1
normalized_output_train_feature_file: The normalized train features. 
normalized_output_validation_feature_file: The normalized dev features.



3) Train the model
python TrainClassifierModel.py normalized_train_feature_file  output_classifier_model  output_regression_model  feature_size
<br>
normalized_train_feature_file: from Step 2
<br>
output_classifier_model: the output classification model by pickle. 
<br>
output_regression_model: the output regression model by pickle
<br>
feature_size: the total size of the features generated from Step 1. 



4) Generate Test Model
python ~/workspace/cognitive/TestModel.py  classifier_model regression_model feature_size normalized_output_validation_feature_file  submission_file

<br>
classifier_model: output_classifier_model from step 3
<br>
regression_model: output_regression_model from step 3
<br>
feature_size : Line # of output_feature_vocab_list_file from step 1. 
<br>
normalized_output_validation_feature_file: normalized_output_validation_feature_file from Step 2.  
<br>
submission_file: The output submission files for the validation data. 


5) Hyper-parameter tuning
<br>
Here are two hyperparameters tuned in this experiments. 
<br>
The two regularization factor Cs  of the classifier model and the regression model.
<br>
The class weights between label=0 and label=1 in the classifier model.  
<br>
I split randomly the training feature files in two parts: around 90000 examples for testing, and 5000 examples for validation in order to tune the hyperparameters. 






