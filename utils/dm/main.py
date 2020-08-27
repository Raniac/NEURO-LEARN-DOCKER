import argparse
import logging

from hdfs import InsecureClient

client = InsecureClient("http://hdfs.neurolearn.com:50070", user="hadoop")

def parse_args():
    parser = argparse.ArgumentParser(description='hdfs-utils-main')
    
    parser.add_argument('--host', dest='host', default='http://hdfs.neurolearn.com')
    parser.add_argument('--port', dest='port', default='50070')
    parser.add_argument('--user', dest='user', default='hadoop')
    
    parser.add_argument('--action', dest='action', default='explore')
    parser.add_argument('--local-path', dest='local_path', required=False)
    parser.add_argument('--remote-path', dest='remote_path', required=True)
    
    args = parser.parse_args()
    return args

def explorer(remote_path):
    print(client.list(remote_path))

def uploader(remote_path, local_path):
    client.upload(remote_path, local_path)

def downloader(remote_path, local_path):
    client.download(remote_path, local_path)

if __name__ == "__main__":
    args = parse_args()
    client = InsecureClient(args.host + ':' + args.port, user=args.user)
    
    if args.action == 'explore':
        explorer(args.remote_path)
    elif args.action == 'upload':
        uploader(args.remote_path, args.local_path)
    elif args.action == 'download':
        downloader(args.remote_path, args.local_path)
