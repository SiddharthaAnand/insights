import boto3
import botocore
from config import S3_KEY, S3_SECRET

s3 = boto3.resource('s3')
s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl='public-read'):
    """

    :param file:
    :param bucket_name:
    :param acl:
    :return:
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl
            }
        )
    except Exception as e:
        print("Something", e)
        return e
    return "Uploaded successfully"


def download_from_s3(bucket_name, filename):
    try:
        if s3 is not None:
            response = s3.download_file(bucket_name, filename, 'my_local_file.txt')
            print("I am here", response)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    return True


def calculate_average(file_obj):
    rows = file_obj.readlines()
    rows = [line.decode('utf-8').strip() for line in rows]
    rows = [int(val) for val in rows if val != '']
    total = 0
    average = None
    if len(rows) != 0:
        for val in rows:
            total += val
        average = total / len(rows)

    return average
