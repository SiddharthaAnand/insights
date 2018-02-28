import os

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
S3_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
S3_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://s3.ap-south-1.amazonaws.com/' + S3_BUCKET + "/"

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000
