import boto3
import logging
import os
import time

logging.basicConfig(level=logging.INFO)

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def create_bucket(bucket_name, region):
    unique_bucket_name = f"{bucket_name}-{int(time.time())}"
    try:
        if region == "us-east-1":
            # us-east-1 doesn't accept LocationConstraint
            s3_client.create_bucket(Bucket=unique_bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=unique_bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        logging.info(f"Bucket '{unique_bucket_name}' created successfully.")
        return unique_bucket_name
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logging.info(f"Bucket '{unique_bucket_name}' already exists.")
        return unique_bucket_name

def upload_file(local_file, bucket_name, key):
    s3_client.upload_file(local_file, bucket_name, key)
    logging.info(f"Uploaded {local_file} to s3://{bucket_name}/{key}")

def read_file(bucket_name, file_key):
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return obj["Body"].read().decode('utf-8')

def save_to_s3(content, bucket_name, file_key):
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=content.encode('utf-8'))
    logging.info(f"Saved file to s3://{bucket_name}/{file_key}")

def download_file(bucket_name, file_key, local_folder="outputs"):
    os.makedirs(local_folder, exist_ok=True)
    local_path = os.path.join(local_folder, os.path.basename(file_key))
    s3_client.download_file(bucket_name, file_key, local_path)
    logging.info(f"Downloaded s3://{bucket_name}/{file_key} to {local_path}")
    return local_path

def delete_bucket(bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
    logging.info(f"Deleted bucket '{bucket_name}' and all contents.")
