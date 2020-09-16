import os
import sys
import time

from hdfs import InsecureClient
import pandas as pd

from task.Acquisition import Data
from task.Models import *
from task.Integrated import *

def handleHdfsUpload(file_path, proj_id, task_id):
    try:
        client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")
        hdfs_path = "/neurolearn/files/" + proj_id + "/results/" + task_id
        client.makedirs(hdfs_path)
        client.upload(hdfs_path, file_path)
        print('Uploaded Images to HDFS.')
    except Exception as e:
        print(e)
        hdfs_path = ''
    return hdfs_path

def ml_task(task_id, proj_id, task_type, train_data, enable_test, test_data, label, feat_sel, estimator, cv_type):
    print(task_id, task_type, enable_test, label, feat_sel, estimator, cv_type)
    
    data_columns = train_data[0].columns
    columns_to_drop = []
    for column in data_columns:
        if column == 'ID':
            columns_to_drop.append(column)
        elif column[:6] == 'LABEL_':
            columns_to_drop.append(column)
        else:
            break

    # Instantiate training dataset
    train_X = train_data[0].drop(columns_to_drop, axis=1) # load data file
    train_y = train_data[0]['LABEL_' + label] # load label file

    if len(train_data) > 0:
        for i in range(1, len(train_data)):
            train_X_temp = train_data[i].drop(columns_to_drop, axis=1) # load data file
            train_y_temp = train_data[i]['LABEL_' + label] # load label file
            train_X = pd.concat([train_X, train_X_temp], axis=0)
            train_y = pd.concat([train_y, train_y_temp], axis=0)
    
    my_train_data = Data(train_X, train_y) # instantiate data class
    my_train_data.data_preprocessing()
    (train_n_samples, train_n_features) = train_X.shape

    if enable_test:
        # Instantiate testing dataset
        test_X = test_data[0].drop(columns_to_drop, axis=1) # load data file
        test_y = test_data[0]['LABEL_' + label] # load label file
        
        if len(test_data) > 0:
            for i in range(1, len(test_data)):
                test_X_temp = test_data[i].drop(columns_to_drop, axis=1) # load data file
                test_y_temp = test_data[i]['LABEL_' + label] # load label file
                test_X = pd.concat([test_X, test_X_temp], axis=0)
                test_y = pd.concat([test_y, test_y_temp], axis=0)
        
        my_test_data = Data(test_X, test_y) # instantiate data class
        my_test_data.data_preprocessing()
        (test_n_samples, test_n_features) = test_X.shape
    
    if cv_type == '10-fold':
        cv = 10
    elif cv_type == '5-fold':
        cv = 5
    elif cv_type == '3-fold':
        cv = 3
    else:
        from sklearn.model_selection import LeaveOneOut
        cv = LeaveOneOut()

    if task_type == "ml_clf":
        if feat_sel == "Principal Component Analysis":
            my_feat_sel = PCA_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "Analysis of Variance":
            my_feat_sel = ANOVA_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "Recursive Feature Elimination":
            my_feat_sel = RFE_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "None":
            my_feat_sel = None
        
        if estimator == "Support Vector Machine":
            my_model = SVM_CLF()
        elif estimator == "Random Forest":
            my_model = RF_CLF()
        elif estimator == "Linear Discriminative Analysis":
            my_model = LDA_CLF()
        elif estimator == "Logistic Regression":
            my_model = LR_CLF()
        elif estimator == "K Nearest Neighbor":
            my_model = KNN_CLF()

        if enable_test:
            results = integrated_clf_model(my_feat_sel, my_model, my_train_data, my_test_data, cv, task_id) # run integrated classification model
        else:
            results = integrated_clf_model_notest(my_feat_sel, my_model, my_train_data, cv, task_id)
    
        if my_feat_sel:
            opt_hdfs_path = handleHdfsUpload(task_id + 'optimization_curve.png', proj_id, task_id)
            results['Opt HDFS Path'] = opt_hdfs_path
        if enable_test:
            roc_hdfs_path = handleHdfsUpload(task_id + 'ROC_curve.png', proj_id, task_id)
            results['ROC HDFS Path'] = roc_hdfs_path

    elif task_type == "ml_rgs":
        if feat_sel == "Analysis of Variance":
            my_feat_sel = ANOVA_Feat_Sel(train_n_samples, train_n_features)
        elif feat_sel == "None":
            my_feat_sel = None
        
        if estimator == "Support Vector Regression":
            my_model = SVR_RGS()
        elif estimator == "Elastic Net":
            my_model = EN_RGS()
        elif estimator == "Ordinary Least Square":
            my_model = OLS_RGS()
        elif estimator == "Lasso Regression":
            my_model = L1_RGS()
        elif estimator == "Ridge Regression":
            my_model = L2_RGS()
    
        if enable_test:
            results = integrated_rgs_model(my_feat_sel, my_model, my_train_data, my_test_data, cv) # run integrated classification model
        else:
            results = integrated_rgs_model_notest(my_feat_sel, my_model, my_train_data, cv)

    return results
