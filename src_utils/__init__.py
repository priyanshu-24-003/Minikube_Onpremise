import pandas as pd
import os
import boto3
from io import StringIO
import pickle





class Credentials():
    aws_access_key = os.getenv("AWS_ACCESS_KEY")
    aws_secret_key = os.getenv("AWS_SECRET_KEY")
    s3_bucket = os.getenv("BUCKET")

    INGEST_SERVICE_URL = os.getenv("INGEST_SERVICE_URL")
    TRAINER_SERVICE_URL = os.getenv("TRAINER_SERVICE_URL")
    PUSHER_SERVICE_URL = os.getenv("PUSHER_SERVICE_URL")

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

    def fetch_df(self, data):
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=data)
        df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
        return df

    def push_data(self, datafile, destination_folder):
        self.s3_client.upload_file(
            Filename=datafile,     # Local path
            Bucket=self.bucket_name,     # Target bucket name
            Key=f'{destination_folder}/{datafile}'     # S3 object key/path
        )

    def fetch_model_typ(self, fileurl):
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=fileurl)
        byt = response["Body"].read()

        return pickle.loads(byt)




def save_data(data:pd.DataFrame, path):
    data.to_csv(path, index=False)
    pass

def remove_data(path):
    os.remove(path)
    pass

def save_model_typ(typ, path):
    with open(path, "wb") as f:
        t = pickle.dump(typ, f)



    