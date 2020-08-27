import json
import os
import requests
import time
import traceback

from fastapi import File, UploadFile

from config.settings import app
from config.settings import BASE_URL
from config.settings import client

@app.get("/")
def hello():
    return "I'm healthy!"

## User Management

@app.get("/v0/user/login")
def login():
    pass

@app.post("/v0/user/register")
def register():
    pass

## Project Management

@app.post("/v0/proj/new")
def newProject():
    pass

@app.get("/v0/proj/delete")
def deleteProject():
    pass

@app.get("/v0/proj/overview")
def overviewProjects():
    pass

@app.get("/v0/proj/all")
def showAllProjects():
    pass

@app.get("/v0/proj/join")
def joinProject():
    pass

@app.get("/v0/proj/quit")
def quitProject():
    pass

## Data Management

@app.post("/v0/data/upload")
def uploadData():
    pass

@app.get("/v0/data/show")
def showData():
    pass

@app.get("/v0/data/delete")
def deleteData():
    pass

## Task Management

@app.post("/v0/task/new")
def newTask():
    pass

@app.get("/v0/task/overview")
def overviewTasks():
    pass

@app.get("/v0/task/show")
def showTasks():
    pass

@app.get("/v0/task/result")
def getTaskResult():
    pass

@app.get("/v0/task/image")
def getTaskImage():
    pass

@app.get("/v0/task/supplementary")
def getTaskSupplementary():
    pass
