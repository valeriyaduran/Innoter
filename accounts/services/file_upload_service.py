import os

import boto3
from rest_framework.response import Response


class FileUploadService:

    @staticmethod
    def user_picture_upload(request):
        user_picture = request.data.get('file')
        print(user_picture.file)
        return user_picture

    @staticmethod
    def upload_file_to_localstack(request):

        s3 = boto3.resource('s3')
        bucket = s3.Bucket('innotterprofilepictures')

        with open(FileUploadService.user_picture_upload(request).name, 'rb') as data:
            bucket.upload_fileobj(data, 'aws_access_key_id')
        # s3 = boto3.client(
        #     's3',
        #     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        #     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        # )

        # data = s3.put_object(
        #     Body=FileUploadService.user_picture_upload(request),
        #     Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME'),
        #     Key='123'
        # )
