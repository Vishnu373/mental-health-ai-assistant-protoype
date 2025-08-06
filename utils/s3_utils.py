import boto3
import logging
import os
import time
import json

logging.basicConfig(level=logging.INFO)

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def create_bucket(bucket_name, region, unique=True):
    """
    unique=True, appends a timestamp to the bucket name for uniqueness (ephemeral).
    unique=False, uses the exact bucket_name (persistent).
    """
    final_name = f"{bucket_name}-{int(time.time())}" if unique else bucket_name

    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=final_name)
        else:
            s3_client.create_bucket(
                Bucket=final_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        logging.info(f"Bucket '{final_name}' created successfully.")
        return final_name
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logging.info(f"Bucket '{final_name}' already exists.")
        return final_name
    
# Uploading local to s3
def upload_file(local_file, bucket_name, key):
    s3_client.upload_file(local_file, bucket_name, key)
    logging.info(f"Uploaded {local_file} to s3://{bucket_name}/{key}")

# Reading file from S3
def read_file(bucket_name, file_key):
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return obj["Body"].read().decode('utf-8')

# File saving in S3 (output file)
def save_to_s3(content, bucket_name, file_key):
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=content.encode('utf-8'))
    logging.info(f"Saved file to s3://{bucket_name}/{file_key}")

# S3 -> local (output file)
def download_file(bucket_name, file_key, local_folder="outputs"):
    os.makedirs(local_folder, exist_ok=True)
    local_path = os.path.join(local_folder, os.path.basename(file_key))
    s3_client.download_file(bucket_name, file_key, local_path)
    logging.info(f"Downloaded s3://{bucket_name}/{file_key} to {local_path}")
    return local_path

# Deleting bucket
def delete_bucket(bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
    logging.info(f"Deleted bucket '{bucket_name}' and all contents.")

# Getting embeddings from S3 for opensearch
def load_embeddings(bucket_name, key):
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    data = obj['Body'].read().decode('utf-8')
    return json.loads(data)
