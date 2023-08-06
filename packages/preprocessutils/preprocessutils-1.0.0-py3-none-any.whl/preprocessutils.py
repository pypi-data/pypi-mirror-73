import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler

def fix_imbalance(data, target, threshold=10.0, oversample=True, smote=False):
    """
    Method Name: fix_imbalance
    Description: This method will be used to handle unbalanced datasets(rare classes) through oversampling/ undersampling 
                 techniques
    Input Description: data: the input dataframe with target column.
                       threshold: the threshold of mismatch between the target values to perform balancing.

    Output: A balanced dataframe.
    On Failure: Raise Exception

    Written By: Punit Nanda
    Version: 1.0
    Revisions: None

    """
    #self.logger_object.log(#self.file_object,'Entered the fix_imbalance method of the DataPreprocessor class') # Logging entry to the method
    try:
        #data= pd.read_csv(#self.training_file) # reading the data file
        ##self.logger_object.log(#self.file_object,'DataFrame Load Successful of the fix_imbalance method of the DataPreprocessor class')
        #return #self.data # return the read data to the calling method
        
        ##self.logger_object.log(#self.file_object,'X y created in the fix_imbalance method of the DataPreprocessor class')
        X = data.drop(target, axis=1)
        y = data[target]
        
        ##self.logger_object.log(#self.file_object,'Class Imbalance Process Starts in the fix_imbalance method of the DataPreprocessor class')
        
        no_of_classes = data[target].nunique()
        
        if no_of_classes == 2:
            
            
            ##self.logger_object.log(#self.file_object,'No of Classes is 2 in the fix_imbalance method of the DataPreprocessor class')
            thresh_satisfied = ((data[target].value_counts()/float(len(data[target]))*100).any() < threshold)
            if thresh_satisfied:
                #self.logger_object.log(#self.file_object,'Threshold satisfied in the fix_imbalance method of the DataPreprocessor class')
                if smote:
                    #self.logger_object.log(#self.file_object,'OverSampling using SMOTE having 2 classes in the fix_imbalance method of the DataPreprocessor class')
                    smote = SMOTE()
                    X, y = smote.fit_resample(X, y)
                elif oversample:
                    #self.logger_object.log(#self.file_object,'OverSampling minority classes data having 2 classes in the fix_imbalance method of the DataPreprocessor class')
                    ROS = RandomOverSampler(sampling_strategy='auto', random_state=42)
                    X, y = ROS.fit_sample(X, y)
                else:
                    #self.logger_object.log(#self.file_object,'UnderSampling majority classes data having 2 classes in the fix_imbalance method of the DataPreprocessor class')
                    ROS = RandomUnderSampler(sampling_strategy='auto', random_state=42)
                    X, y = ROS.fit_sample(X, y)
        else:
            
            high = (data[target].value_counts()/float(len(data[target]))*100).ravel().max()
            low = (data[target].value_counts()/float(len(data[target]))*100).ravel().min()
            
            thresh_satisfied = ( high-low > 100.0 - threshold )
            
            if thresh_satisfied:
                #self.logger_object.log(#self.file_object,'Threshold satisfied in the fix_imbalance method of the DataPreprocessor class')
                if smote:
                    #self.logger_object.log(#self.file_object,'OverSampling using SMOTE having more than 2 classes in the fix_imbalance method of the DataPreprocessor class')
                    for i in range(no_of_classes-2):
                        smote = SMOTE()
                        X, y = smote.fit_resample(X, y)
                elif oversample:
                    #self.logger_object.log(#self.file_object,'OverSampling minority classes data having more than 2 classes in the fix_imbalance method of the DataPreprocessor class')
                    for i in range(no_of_classes-2):
                        ROS = RandomOverSampler(sampling_strategy='auto', random_state=42)
                        X, y = ROS.fit_sample(X, y)
                else:
                    #self.logger_object.log(#self.file_object,'UnderSampling majority classes data having more than 2 classes in the fix_imbalance method of the DataPreprocessor class')
                    for i in range(no_of_classes-2):
                        ROS = RandomUnderSampler(sampling_strategy='auto', random_state=42)
                        X, y = ROS.fit_sample(X, y)                    
                                                 
        
        y.to_frame(name=target)
        dfBalanced = pd.concat([X, y], axis=1)
        #self.logger_object.log(#self.file_object,'Class Imbalance Process Ends in the fix_imbalance method of the DataPreprocessor class')
        return dfBalanced
        
    except Exception as e:
        #self.logger_object.log(#self.file_object,'Exception occured in fix_imbalance method of the DataPreprocessor class. Exception message: '+str(e)) # Logging the exception message
        #self.logger_object.log(#self.file_object,'DataFrame Load Unsuccessful.Exited the fix_imbalance method of the DataPreprocessor class') # Logging unsuccessful load of data
        raise Exception() # raising exception and exiting
