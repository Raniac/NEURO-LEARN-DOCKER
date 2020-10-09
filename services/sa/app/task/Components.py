import numpy as np
import pandas as pd
import time
import decimal
import seaborn as sns
import csv
import scipy
import statsmodels.stats.weightstats as st

def integrated_ttest(test_variables, group_variables):
    feature_list = test_variables.columns
    ttest_results = pd.DataFrame({'Feature Name': [],'t value': [], 'p value': []})
    sig_features = []
    t_value_list = []
    p_value_list = []

    group0_var = test_variables[group_variables == 0]
    group1_var = test_variables[group_variables == 1]

    for feature_name in feature_list:
        t_value, p_value, df = st.ttest_ind(group0_var[feature_name], group1_var[feature_name], usevar='unequal')
        if p_value <= 0.05:
            sig_features.append(feature_name)
            t_value_list.append(t_value)
            p_value_list.append(p_value)

    ttest_results['Feature Name'] = sig_features
    ttest_results['t value'] = t_value_list
    ttest_results['p value'] = p_value_list

    return ttest_results.to_dict('records')

def integrated_anova(test_variables, group_variables):
    
    feature_list = test_variables.columns
    anova_results = pd.DataFrame({'Feature Name': [],'f value': [], 'p value': []})
    groups = group_variables.unique()
    num_groups = len(groups)
    test_var_groups = []
    sig_features = []
    f_value_list = []
    p_value_list = []

    for i in range(num_groups):
        test_var_groups.append(test_variables[group_variables == groups[i]])

    for feature_name in feature_list:
        test_var = []
        for i in range(num_groups):
            test_var.append(test_var_groups[i][feature_name])
        f_value, p_value = scipy.stats.f_oneway(*test_var)
        if p_value <= 0.05:
            sig_features.append(feature_name)
            f_value_list.append(f_value)
            p_value_list.append(p_value)

    anova_results['Feature Name'] = sig_features
    anova_results['f value'] = f_value_list
    anova_results['p value'] = p_value_list

    return anova_results.to_dict('records')

def integrated_pearson(data_x, data_y):
    ## TODO reduce storage cost using correlation matrix
    # x_feature_list = data_x.columns
    # num_x_features = len(x_feature_list)
    # y_feature_list = data_y.columns
    # num_y_features = len(y_feature_list)
    # r_value_table = pd.DataFrame(np.zeros((num_x_features, num_y_features)),
    #                              columns=y_feature_list,
    #                              index=x_feature_list)
    # p_value_table = pd.DataFrame(np.zeros((num_x_features, num_y_features)),
    #                              columns=y_feature_list,
    #                              index=x_feature_list)

    # for x_feature_name in x_feature_list:
    #     for y_feature_name in y_feature_list:
    #         r_value, p_value = scipy.stats.pearsonr(data_x[x_feature_name], data_y[y_feature_name])
    #         if p_value <= 0.05:
    #             r_value_table[x_feature_name][y_feature_name] = r_value
    #             p_value_table[x_feature_name][y_feature_name] = p_value

    x_feature_list = data_x.columns
    y_feature_list = data_y.columns
    pearson_results = pd.DataFrame({'X Feature Name': [], 'Y Feature Name': [], 'r value': [], 'p value': []})
    x_feature_names = []
    y_feature_names = []
    r_value_list = []
    p_value_list = []

    for x_feature_name in x_feature_list:
        for y_feature_name in y_feature_list:
            r_value, p_value = scipy.stats.pearsonr(data_x[x_feature_name], data_y[y_feature_name])
            if p_value <= 0.05:
                x_feature_names.append(x_feature_name)
                y_feature_names.append(y_feature_name)
                r_value_list.append(r_value)
                p_value_list.append(p_value)

    pearson_results['X Feature Name'] = x_feature_names
    pearson_results['Y Feature Name'] = y_feature_names
    pearson_results['r value'] = r_value_list
    pearson_results['p value'] = p_value_list
    
    return pearson_results.to_dict('records')

def integrated_spearman(data_x, data_y):
    x_feature_list = data_x.columns
    y_feature_list = data_y.columns
    spearman_results = pd.DataFrame({'X Feature Name': [], 'Y Feature Name': [], 'r value': [], 'p value': []})
    x_feature_names = []
    y_feature_names = []
    r_value_list = []
    p_value_list = []

    for x_feature_name in x_feature_list:
        for y_feature_name in y_feature_list:
            r_value, p_value = scipy.stats.spearmanr(data_x[x_feature_name], data_y[y_feature_name])
            if p_value <= 0.05:
                x_feature_names.append(x_feature_name)
                y_feature_names.append(y_feature_name)
                r_value_list.append(r_value)
                p_value_list.append(p_value)

    spearman_results['X Feature Name'] = x_feature_names
    spearman_results['Y Feature Name'] = y_feature_names
    spearman_results['r value'] = r_value_list
    spearman_results['p value'] = p_value_list
    
    return spearman_results.to_dict('records')