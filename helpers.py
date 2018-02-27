import boto3, botocore
from config import S3_KEY, S3_BUCKET, S3_SECRET, S3_LOCATION

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
                "ACL": acl,
                "Content-type": file.content_type
            }
        )
    except Exception as e:
        print("Something happend", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)


