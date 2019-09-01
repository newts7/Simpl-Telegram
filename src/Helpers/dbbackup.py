import boto3
import os
from datetime import datetime
client = boto3.client(
    's3',
)

def initiate_backup():
    bucketName = "simpldbbackup"
    os.system("mongodump -d cclub -c profiles")
    Key = "dump/cclub/profiles.bson"
    outPutname = str(datetime.now())
    client.upload_file(Key, bucketName, outPutname)
    os.system("rm -rf dump")