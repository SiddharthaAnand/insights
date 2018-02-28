import boto3, botocore
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
        print(S3_KEY)
        print(S3_SECRET)
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl
            }
        )
    except Exception as e:
        print("Something happend", e)
        return e
    return "Uploaded successfully"


