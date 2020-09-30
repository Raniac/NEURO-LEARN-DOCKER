import os
import pandas as pd
from .Components import *

def test_sa_task(task_id, task_type, test_var_data_x, group_var_data_y):
    print(task_id, task_type)

    if task_type.startswith('sa_da'):
        GROUP_VAR = 'LABEL_GROUP'

        data_columns = test_var_data_x[0].columns
        columns_to_drop = []
        for column in data_columns:
            if column == 'ID':
                columns_to_drop.append(column)
            elif column[:6] == 'LABEL_':
                columns_to_drop.append(column)
            else:
                break

        test_variables = test_var_data_x[0].drop(columns_to_drop, axis=1)
        group_variables = test_var_data_x[0][GROUP_VAR]

        if len(test_var_data_x) > 0:
            for i in range(1, len(test_var_data_x)):
                test_variables_temp = pd.read_csv(test_var_data_x[i], encoding='gbk').drop(columns_to_drop, axis=1)
                group_variables_temp = pd.read_csv(test_var_data_x[i], encoding='gbk')[GROUP_VAR]
                test_variables = pd.concat([test_variables, test_variables_temp], axis=0)
                group_variables = pd.concat([group_variables, group_variables_temp], axis=0)

        if task_type[6:] == 'ttest':
            return integrated_ttest(test_variables, group_variables)
        elif task_type[6:] == 'anova':
            return integrated_anova(test_variables, group_variables)
    
    elif task_type.startswith('sa_ca'):
        DATA_X_PATH = test_var_data_x[0]
        DATA_Y_PATH = group_var_data_y[0]

        data_columns = test_var_data_x[0].columns
        columns_to_drop = []
        for column in data_columns:
            if column == 'ID':
                columns_to_drop.append(column)
            elif column[:6] == 'LABEL_':
                columns_to_drop.append(column)
            else:
                break

        data_x = test_var_data_x[0].drop(columns_to_drop, axis=1)
        data_y = group_var_data_y[0].drop(columns_to_drop, axis=1)

        if len(test_var_data_x) > 0:
            for i in range(1, len(test_var_data_x)):
                data_x_temp = pd.read_csv(test_var_data_x[i], encoding='gbk').drop(columns_to_drop, axis=1)
                data_x = pd.concat([data_x, data_x_temp], axis=0)

        if len(group_var_data_y) > 0:
            for i in range(1, len(group_var_data_y)):
                data_y_temp = pd.read_csv(group_var_data_y[i], encoding='gbk').drop(columns_to_drop, axis=1)
                data_y = pd.concat([data_y, data_y_temp], axis=0)

        if task_type[6:] == 'prson':
            return integrated_pearson(data_x, data_y)
        elif task_type[6:] == 'spman':
            return integrated_spearman(data_x, data_y)