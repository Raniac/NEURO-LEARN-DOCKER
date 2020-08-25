from fastapi import FastAPI
from hdfs.client import Client

app = FastAPI()

client = Client("http://hdfs.neurolearn.com:50070")

BASE_URL = "/rest/dmservice"