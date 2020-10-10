from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django import forms
from django.middleware.csrf import get_token, rotate_token

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import permissions

import uuid

from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import os
import io
import time
import zipfile
import traceback

from hdfs import InsecureClient

# from .models import Book, Projects_Demo, Submissions_Demo, Submissions_SA_Demo, Data_Demo, User_Demo

from .models import Users, Projects, User_Proj_Auth, Datasets, Submissions


@require_http_methods(["GET"])
def healthcheck(request):
    response = HttpResponse()
    response.write("success")

    return response

# Create your views here.
# ==================================================
# Universal APIs
# ==================================================
@require_http_methods(["GET", "POST"])
def user_register(request):
    response_content = {}
    response = HttpResponse()
    try:
        postBody = json.loads(request.body.decode('utf-8'))
        user_id = 'USER' + time.strftime('%Y%m%d%H%M%S')
        username=postBody.get('username')
        password=postBody.get('password')

        user = Users(
            user_id=user_id,
            username=username,
            password=password
        )
        user.save()
        
        response_content['post_body'] = postBody
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1
    
    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def user_login(request):
    response_content = {}
    response = HttpResponse()
    try:
        username = request.GET.get('username')
        password = request.GET.get('password')
        userobj = Users.objects.filter(username=username, password=password).first()

        if userobj:
            response_content['msg'] = 'Correct password!'
            response_content['username'] = username
            response_content['user_id'] = userobj.user_id

            sessionid = str(uuid.uuid3(uuid.NAMESPACE_URL, username))
            response.set_cookie('sessionid', sessionid, expires=60000, path='/', httponly=False)
            response.set_cookie('username', username, expires=60000, path='/', httponly=False)
            response.set_cookie('user_id', userobj.user_id, expires=60000, path='/', httponly=False)
            response_content['sessionid'] = sessionid

            print(sessionid)
            
            response_content['error_num'] = 0
        else:
            response_content['msg'] = 'Wrong password!'
            response_content['error_num'] = 1
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

# ==================================================
# Data Management APIs
# ==================================================
@require_http_methods(["GET"])
def show_project_overview(request):
    response_content = {}
    response = HttpResponse()
    try:
        user_id = request.GET.get('user_id')
        proj_ids = User_Proj_Auth.objects.filter(user_id=user_id).values('proj_id')
        proj_id_list = []
        for itm in proj_ids:
            proj_id_list.append(itm['proj_id'])
        projects = Projects.objects.filter(proj_id__in = proj_id_list)
        response_content['list']  = json.loads(serializers.serialize("json", projects))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_all_projects(request):
    response_content = {}
    response = HttpResponse()
    try:
        projects = Projects.objects.filter()
        response_content['list']  = json.loads(serializers.serialize("json", projects))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def join_project(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        user_id = request.GET.get('user_id')
        if len(User_Proj_Auth.objects.filter(proj_id=proj_id, user_id=user_id)) == 0:
            auth_rec = User_Proj_Auth(
                user_id=user_id,
                proj_id=proj_id
            )
            auth_rec.save()
        else:
            raise Exception('Already joined!')
        
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def quit_project(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        user_id = request.GET.get('user_id')
        if len(User_Proj_Auth.objects.filter(proj_id=proj_id, user_id=user_id)) == 1:
            User_Proj_Auth.objects.filter(proj_id=proj_id, user_id=user_id).delete()
        else:
            raise Exception('Something went wrong!')
        
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(['POST'])
def upload_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        user_id = request.GET.get('user_id')
        proj_id = request.GET.get('proj_id')
        data_file = request.FILES.get('datafile')
        data_id = 'DATA' + time.strftime('%Y%m%d%H%M%S')
        data_name = data_file.name
        if data_name[-4:] == '.csv':
            data_cont, hdfs_path = handle_uploaded_file(data_file, data_id, proj_id)
        else:
            data_cont, hdfs_path = '', ''

        dataset = Datasets(
            data_id=data_id,
            proj_id=proj_id,
            user_id=user_id,
            data_name=data_name,
            data_cont=data_cont,
            hdfs_path=hdfs_path
        )
        dataset.save()
        
        response_content['msg'] = 'success'
        response_content['dataid'] = data_id
    
    except Exception as e:
        traceback.print_exc()
        response_content['msg'] = 'existed'
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

def handle_uploaded_file(f, data_id, proj_id):
    file_name = str(f.name)
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    data_content = pd.read_csv(file_name, encoding='utf-8')
    data_json = data_content.to_json()

    try:
        client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")
        hdfs_path = "/neurolearn/files/" + proj_id + "/datasets/" + data_id
        client.makedirs(hdfs_path)
        client.upload(hdfs_path, file_name)
    except:
        hdfs_path = ''
    
    return data_json, hdfs_path

@require_http_methods(["GET"])
def show_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        data = Datasets.objects.filter(proj_id=proj_id).order_by('-id').only('data_id', 'data_name', 'proj_id')
        response_content['list']  = json.loads(serializers.serialize("json", data, fields=('data_id', 'data_name', 'proj_id')))
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def delete_data(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        data_id = request.GET.get('data_id')
        user_id = request.GET.get('user_id')
        fetched = Datasets.objects.filter(proj_id=proj_id, data_id=data_id, user_id=user_id).values('hdfs_path')
        if len(fetched) == 0:
            raise Exception('Oops! No access!')
        if list(fetched)[0]['hdfs_path']:
            client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")
            client.delete(list(fetched)[0]['hdfs_path'], recursive=True)
        Datasets.objects.filter(proj_id=proj_id, data_id=data_id, user_id=user_id).delete()

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def download_data(request):
    try:
        data_id = request.GET.get('data_id')
        user_id = request.GET.get('user_id')
        data_path = data_id + '.csv'

        fetched = Datasets.objects.filter(data_id=data_id, user_id=user_id).values('hdfs_path', 'data_name')
        if len(fetched) == 0:
            raise Exception('Oops! No access!')
        if list(fetched)[0]['hdfs_path']:
            client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")
            client.download(list(fetched)[0]['hdfs_path'] + '/' + list(fetched)[0]['data_name'], data_path, overwrite=True)
        else:
            data_cont_query = Datasets.objects.filter(data_id=data_id, user_id=user_id).values('data_cont')
            if len(data_cont_query) == 0:
                raise Exception('Oops! No access!')
            data_cont = list(data_cont_query)[0]['data_cont']
            pd.read_json(data_cont).to_csv(data_path, index=False)
        
        data_file = open(data_path, 'rb')
        
        response = FileResponse(data_file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename=\"' + data_id + '.csv\"'
    except Exception as e:
        traceback.print_exc()
        response_content = {}
        response = HttpResponse()
        response_content['msg'] = str(e)
        response_content['error_num'] = 1
        response.write(json.dumps(response_content))

    return response

@require_http_methods(["POST"])
def new_project(request):
    response = HttpResponse()
    response_content = {}
    try:
        postBody = json.loads(request.body.decode("utf-8"))
        user_id = request.GET.get('user_id')
        proj_id = 'PROJ' + time.strftime('%Y%m%d%H%M%S')
        label = postBody.get('label')
        title = postBody.get('title')
        intro = postBody.get('introduction')
        methd = postBody.get('methods')
        flowchart_url = postBody.get('flowchart_url')
        workflows_url = postBody.get('workflows_url')
        templates_url = postBody.get('templates_url')

        proj = Projects(
            proj_id=proj_id,
            admin_id=user_id,
            label=label,
            title=title,
            introduction=intro,
            methods=methd,
            flowchart_url=flowchart_url,
            workflows_url=workflows_url,
            templates_url=templates_url
        )
        proj.save()

        response_content['post_body'] = postBody
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def delete_project(request):
    response_content = {}
    response = HttpResponse()
    try:
        proj_id = request.GET.get('proj_id')
        user_id = request.GET.get('user_id')
        if len(Projects.objects.filter(proj_id=proj_id, admin_id=user_id)) == 0:
            raise Exception('Oops! No access!')
        Projects.objects.filter(proj_id=proj_id, admin_id=user_id).delete()
        User_Proj_Auth.objects.filter(proj_id=proj_id).delete()

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["POST"])
def new_task(request):
    response = HttpResponse()
    try:
        res = requests.post(
            url="http://ml.neurolearn.com:4701/rest/mlservice/v0/task/insert",
            data=request.body.decode("utf-8")
        )
        response.write(json.dumps(res.json()))
        return response
    except Exception as e:
        response.write(e)
        return response

@require_http_methods(["POST"])
def new_sa_task(request):
    response = HttpResponse()
    try:
        res = requests.post(
            url="http://sa.neurolearn.com:7410/rest/saservice/v0/task/insert",
            data=request.body.decode("utf-8")
        )
        response.write(json.dumps(res.json()))
        return response
    except Exception as e:
        response.write(e)
        return response

@require_http_methods(["POST"])
def new_sgn_task(request):
    response = HttpResponse()
    try:
        res = requests.post(
            url="http://sgn.neurolearn.com:7014/rest/sgnservice/v0/task/insert",
            data=request.body.decode("utf-8")
        )
        response.write(json.dumps(res.json()))
        return response
    except Exception as e:
        response.write(e)
        return response

@require_http_methods(["GET"])
def overview_submissions(request):
    response_content = {}
    response = HttpResponse()
    try:
        user_id = request.GET.get('user_id')
        proj_ids = User_Proj_Auth.objects.filter(user_id=user_id).values('proj_id')
        proj_id_list = []
        for itm in proj_ids:
            proj_id_list.append(itm['proj_id'])
        
        submissions = Submissions.objects.filter(proj_id__in = proj_id_list).order_by('-id')[:8]
        response_content['list']  = json.loads(
            serializers.serialize(
                "json", submissions, 
                fields=('task_id', 'proj_id', 'task_name', 'task_type', 'task_config', 'task_status')
            )
        )

        total = Submissions.objects.filter(proj_id__in = proj_id_list).count()
        response_content['total_num'] = total
        submitted = Submissions.objects.filter(task_status='Submitted', proj_id__in = proj_id_list).count()
        response_content['submitted_num'] = submitted
        running = Submissions.objects.filter(task_status='Running', proj_id__in = proj_id_list).count()
        response_content['running_num'] = running
        finished = Submissions.objects.filter(task_status='Finished', proj_id__in = proj_id_list).count()
        response_content['finished_num'] = finished
        failed = Submissions.objects.filter(task_status='Failed', proj_id__in = proj_id_list).count()
        response_content['failed_num'] = failed

        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_submissions(request):
    response_content = {}
    response = HttpResponse()
    try:
        analysis_type = request.GET.get('analysis_type')
        page_num = int(request.GET.get('page_num'))
        page_size = int(request.GET.get('page_size'))
        user_id = request.GET.get('user_id')
        search = request.GET.get('search')
        status = request.GET.get('status')
        proj_ids = User_Proj_Auth.objects.filter(user_id=user_id).values('proj_id')
        proj_id_list = []
        for itm in proj_ids:
            proj_id_list.append(itm['proj_id'])
        if analysis_type == 'Machine Learning':
            submissions = Submissions.objects.filter(task_type__in = ['ml_clf', 'ml_rgs'], proj_id__in = proj_id_list, task_name__icontains = search, task_status__icontains = status).order_by('-id')[(page_num-1)*page_size:page_num*page_size]
            response_content['list']  = json.loads(
                serializers.serialize(
                    "json", submissions, 
                    fields=('task_id', 'proj_id', 'task_name', 'task_type', 'task_config', 'task_status')
                )
            )
            response_content['total_size'] = Submissions.objects.filter(task_type__in = ['ml_clf', 'ml_rgs'], proj_id__in = proj_id_list).count()
        elif analysis_type == "Statistical Analysis":
            submissions = Submissions.objects.filter(task_type__in = ['sa_da_ttest', 'sa_da_anova', 'sa_ca_prson', 'sa_ca_spman'], proj_id__in = proj_id_list, task_name__icontains = search, task_status__icontains = status).order_by('-id')[(page_num-1)*page_size:page_num*page_size]
            response_content['list']  = json.loads(
                serializers.serialize(
                    "json", submissions, 
                    fields=('task_id', 'proj_id', 'task_name', 'task_type', 'task_config', 'task_status')
                )
            )
            response_content['total_size'] = Submissions.objects.filter(task_type__in = ['sa_da_ttest', 'sa_da_anova', 'sa_ca_prson', 'sa_ca_spman'], proj_id__in = proj_id_list).count()
        elif analysis_type == "SchizoGraphNet":
            submissions = Submissions.objects.filter(task_type__in = ['dl_ts', 'dl_ft'], proj_id__in = proj_id_list, task_name__icontains = search, task_status__icontains = status).order_by('-id')[(page_num-1)*page_size:page_num*page_size]
            response_content['list']  = json.loads(
                serializers.serialize(
                    "json", submissions, 
                    fields=('task_id', 'proj_id', 'task_name', 'task_type', 'task_config', 'task_status')
                )
            )
            response_content['total_size'] = Submissions.objects.filter(task_type__in = ['dl_ts', 'dl_ft'], proj_id__in = proj_id_list).count()
        response_content['msg'] = 'success'
        response_content['error_num'] = 0
    except Exception as e:
        response_content['msg'] = str(e)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

@require_http_methods(["GET"])
def show_results(request):
    response_content = {}
    response = HttpResponse()
    try:
        task_id = request.GET.get('task_id')
        analysis_type = request.GET.get('analysis_type')
        
        task_info_query = Submissions.objects.filter(task_id=task_id).values('task_id', 'proj_id', 'task_name', 'task_type', 'task_config', 'task_status', 'task_result')
        task_info = list(task_info_query)[0]
        proj_id = task_info['proj_id']
        if task_info['task_status'] == 'Failed':
            raise Exception('Task Failed! No Valid Result.')
        
        if analysis_type == 'Machine Learning':
            # response with task configuration list
            task_config = task_info['task_config']
            task_info_dict = json.loads(task_config)
            task_info_dict['task_name'] = task_info['task_name']
            task_info_dict['task_type'] = task_info['task_type']
            response_content['info'] = task_info_dict

            # response with task result table
            task_result_json = task_info['task_result']
            task_result_dict = json.loads(task_result_json)
            result_table_dict = task_result_dict.copy()
            if 'Predictions' in result_table_dict.keys():
                del(result_table_dict['Predictions'])
            if 'Feature Weights' in result_table_dict.keys():
                del(result_table_dict['Feature Weights'])
            if 'Optimization' in result_table_dict.keys():
                del(result_table_dict['Optimization'])
            if 'ROC fpr' in result_table_dict.keys():
                del(result_table_dict['ROC fpr'])
            if 'ROC tpr' in result_table_dict.keys():
                del(result_table_dict['ROC tpr'])
            if 'Opt HDFS Path' in result_table_dict.keys():
                del(result_table_dict['Opt HDFS Path'])
            if 'ROC HDFS Path' in result_table_dict.keys():
                del(result_table_dict['ROC HDFS Path'])
            if 'Cor HDFS Path' in result_table_dict.keys():
                del(result_table_dict['Cor HDFS Path'])
            result_table_dict['Optimal Parameters'] = str(result_table_dict['Optimal Parameters'])
            result_table = []
            for idx in range(len(list(result_table_dict.keys()))):
                result_table.append({'Item': list(result_table_dict.keys())[idx], 'Value': list(result_table_dict.values())[idx]})
            response_content['list'] = result_table

            # response with supplementary including feature weights list if exists
            response_content['got_weights'] = 0
            if 'Predictions' in task_result_dict.keys():
                predictions_list = pd.DataFrame.from_records(task_result_dict['Predictions'])
                predictions_list.to_csv(path_or_buf='supplementary.csv', index=False)
                response_content['got_weights'] = 1
            if 'Feature Weights' in task_result_dict.keys():
                feature_weights_list = pd.DataFrame.from_records(task_result_dict['Feature Weights'])
                if 'Predictions' in task_result_dict.keys():
                    feature_weights_list.to_csv(path_or_buf='supplementary.csv', index=False, mode='a+')
                else:
                    feature_weights_list.to_csv(path_or_buf='supplementary.csv', index=False)
                response_content['got_weights'] = 1

            # response with image data if exists
            response_content['img_list'] = []
            if 'Opt HDFS Path' in task_result_dict.keys():
                opt_file_path = 'optimization_curve_' + task_id + '.png'
                if task_result_dict['Opt HDFS Path']:
                    opt_hdfs_path = task_result_dict['Opt HDFS Path'] + '/' + task_id + '_optimization_curve.png'
                    opt_file_path = handleHdfsDownload(opt_hdfs_path, opt_file_path)
                else:
                    plt.figure()
                    best_clfs = pd.DataFrame.from_records(task_result_dict['Optimization'])
                    components_col_dict = {
                        'Principal Component Analysis': 'param_pca__n_components',
                        'Analysis of Variance': 'param_anova__percentile',
                        'Recursive Feature Elimination': 'param_rfe__n_features_to_select'
                    }
                    components_col = components_col_dict[task_info_dict['feat_sel']]
                    best_clfs.plot(x=components_col, y='mean_test_score', yerr='std_test_score')
                    plt.ylabel('Classification Accuracy')
                    plt.xlabel('Features Selected')
                    plt.title('Optimization Curve')
                    plt.savefig(opt_file_path, dpi=300)
                    plt.close()
                response_content['img_list'].append(opt_file_path)
            
            if 'ROC HDFS Path' in task_result_dict.keys():
                roc_file_path = 'ROC_curve_' + task_id + '.png'
                if task_result_dict['ROC HDFS Path']:
                    roc_hdfs_path = task_result_dict['ROC HDFS Path'] + '/' + task_id + '_ROC_curve.png'
                    roc_file_path = handleHdfsDownload(roc_hdfs_path, roc_file_path)
                else:
                    plt.figure()
                    mean_fpr = np.linspace(0, 1, 100)
                    fpr = np.array(task_result_dict['ROC fpr'])
                    tpr = np.array(task_result_dict['ROC tpr'])
                    roc_auc = task_result_dict['Area Under Curve']
                    plt.plot(fpr, tpr,
                            label='AUC = %0.2f' % (roc_auc))
                    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                            label='Chance', alpha=.8)
                    plt.xlim([-0.05, 1.05])
                    plt.ylim([-0.05, 1.05])
                    plt.xlabel('False Positive Rate')
                    plt.ylabel('True Positive Rate')
                    plt.title('Receiver Operating Characteristic')
                    plt.legend(loc="lower right")
                    plt.savefig(roc_file_path, dpi=300)
                    plt.close()
                response_content['img_list'].append(roc_file_path)
            
            if 'Cor HDFS Path' in task_result_dict.keys():
                opt_file_path = 'Original_Predicted_Correlation_' + task_id + '.png'
                if task_result_dict['Cor HDFS Path']:
                    opt_hdfs_path = task_result_dict['Cor HDFS Path'] + '/' + task_id + '_Original_Predicted_Correlation.png'
                    opt_file_path = handleHdfsDownload(opt_hdfs_path, opt_file_path)
                    response_content['img_list'].append(opt_file_path)

        elif analysis_type == 'Statistical Analysis':
            # response with task configuration list
            task_config = task_info['task_config']
            task_info_dict = json.loads(task_config)
            task_info_dict['task_name'] = task_info['task_name']
            task_info_dict['task_type'] = task_info['task_type']
            response_content['info'] = task_info_dict

            # response with task result table
            task_result_json = task_info['task_result']
            significance = pd.DataFrame.from_dict(json.loads(task_result_json), orient='index')
            significance.to_csv(path_or_buf='significance.csv')

        response_content['msg'] = 'success'
        response_content['error_num'] = 0

    except Exception as e:
        traceback.print_exc()
        if analysis_type == 'Machine Learning':
            response_content['msg'] = json.dumps(Submissions.objects.get(task_id=task_id).task_result)
        elif analysis_type == 'Statistical Analysis':
            response_content['msg'] = json.dumps(Submissions.objects.get(task_id=task_id).task_result)
        response_content['error_num'] = 1

    response.write(json.dumps(response_content))

    return response

def handleHdfsDownload(hdfs_path, local_path):
    client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")
    client.download(hdfs_path, local_path, overwrite=True)
    print('Downloaded Images from HDFS.')
    return local_path

@require_http_methods(["GET"])
def show_img(request):
    response = {}
    img_name = request.GET.get('img_name')

    buf = io.BytesIO()
    img = Image.open(img_name)
    img.save(buf, 'png')

    return HttpResponse(buf.getvalue(), 'image/png')

@require_http_methods(["GET"])
def download_feature_weights(request):
    task_id = request.GET.get('task_id')
    feature_weights_file = open('supplementary.csv', 'rb')

    task_info_query = Submissions.objects.filter(task_id=task_id).values('task_name')
    task_info = list(task_info_query)[0]
    
    response = FileResponse(feature_weights_file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=\"' + task_info['task_name'] + '_supplementary.csv\"'
    return response

@require_http_methods(["GET"])
def download_significance_values(request):
    task_id = request.GET.get('task_id')
    significance_file = open('significance.csv', 'rb')

    task_info_query = Submissions.objects.filter(task_id=task_id).values('task_name')
    task_info = list(task_info_query)[0]
    
    response = FileResponse(significance_file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=\"' + task_info['task_name'] + '_significance.csv\"'
    return response
