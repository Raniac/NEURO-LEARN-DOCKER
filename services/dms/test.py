from hdfs.client import Client

client = Client("http://hdfs.neurolearn.com:50070")

print(client.status("/"))
