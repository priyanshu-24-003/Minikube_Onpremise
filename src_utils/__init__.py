import pandas as pd
import os
import boto3
from io import StringIO



class Credentials():
    aws_access_key = os.getenv("AWS_ACCESS_KEY")
    aws_secret_key = os.getenv("AWS_SECRET_KEY")
    s3_bucket = os.getenv("BUCKET")
    pass


class connect_s3():

    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region_name="us-east-1"):
        
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

    def fetch_data(self, data):
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=data)
        df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
        return df

    def push_data(self, datafile, destination_folder):
        self.s3_client.upload_file(
            Filename=datafile,     # Local path
            Bucket=self.bucket_name,     # Target bucket name
            Key=f'{destination_folder}/{datafile}'     # S3 object key/path
        )


def save_data(data:pd.DataFrame, path):
    data.to_csv(path,)
    pass

def remove_data(path):
    os.remove(path)
    pass



    