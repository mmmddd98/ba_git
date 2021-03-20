import numpy as np
import os
import pandas as pd

def average():
    directory = 'paper/images/network_csv/baseline/MobileNetV2/'
    networkname= 'mobileNetV2_baseline_long' # 'ResNet32_strength_e1'2
    #out_directory = 'paper/images/network_csv/baseline/MobileNetV2/'
    newName = 'MobileNetV2_ensemble_distance' 


    tags=[
    'Validation_accuracy'#,
    #'distance0',

 ]

    out_names=[
        directory + newName + '_validation_acuracy.csv'#,
        #directory + newName + '_distance0.csv'
    ]

    for tag, out_name in zip(tags,out_names):
        file_dir = directory + 'run-' + networkname
        filename_1=file_dir + '_1-tag-' + tag + '.csv'
        filename_2=file_dir + '_2-tag-' + tag + '.csv'
        filename_3=file_dir + '_3-tag-' + tag + '.csv'
    
    
        file1 = pd.read_csv(filename_1, delimiter=',')
        file2 = pd.read_csv(filename_2, delimiter=',')
        file3 = pd.read_csv(filename_3, delimiter=',')
        file_sum= file1 + file2 + file3
        file_sum = file_sum/3
        # file_sum['Value'] = file_sum['Value'].ewm(alpha=0.4, axis=0, adjust=False).mean() for smoothing
        file_sum.to_csv(out_name, index=False)
    

average()
    

'''

    directory + newName + '_validation_acuracy.csv',
    directory + newName + '_ensemble_acuracy.csv',
    
    directory + newName + '_distance1.csv',
    directory + newName + '_distance2.csv',
    directory + newName + '_epoch_time.csv'




    'Validation_accuracy',
    'ensemble_accuracy'
    
    'distance1', 
    'distance2',
       'train_epoch_time'
'''