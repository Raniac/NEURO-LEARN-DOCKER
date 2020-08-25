from fastapi import FastAPI
from hdfs.client import InsecureClient

app = FastAPI()

client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")

BASE_URL = "/rest/dmservice"