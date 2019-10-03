# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.CharField(max_length=32, unique=True)
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user_id

class Projects(models.Model):
    proj_id = models.CharField(max_length=32, unique=True)
    label = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=128)
    introduction = models.CharField(max_length=4096)
    methods = models.CharField(max_length=4096)
    flowchart_url = models.CharField(max_length=128)
    workflows_url = models.CharField(max_length=128)
    templates_url = models.CharField(max_length=128)

    def __unicode__(self):
        return self.proj_id

class User_Proj_Auth(models.Model):
    user_id = models.CharField(max_length=32)
    proj_id = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user_id

class Datasets(models.Model):
    data_id = models.CharField(max_length=32, unique=True)
    proj_id = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
    data_name = models.CharField(max_length=64, unique=True)
    data_cont = models.TextField(max_length=4294967295)

    def __unicode__(self):
        return self.data_id

class Submissions(models.Model):
    task_id = models.CharField(max_length=32, unique=True)
    proj_id = models.CharField(max_length=32)
    task_name = models.CharField(max_length=64)
    task_type = models.CharField(max_length=16)
    task_config = models.CharField(max_length=4096)
    task_status = models.CharField(max_length=16)
    task_result = models.TextField(max_length=4294967295)

    def __unicode__(self):
        return self.task_id