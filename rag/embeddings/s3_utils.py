import boto3

def read_file(bucket_name, file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket = bucket_name, Key = file_key)
    return obj["Body"].read().decode('utf-8').split("\n\n")

# BUCKET_NAME = "mhai-clinical-reports"
# s3 = boto3.client('s3')
# response = s3.list_objects_v2(Bucket=BUCKET_NAME)
# for obj in response.get('Contents', []):
#     print(obj['Key'])    