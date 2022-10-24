import boto3
from rest_framework.exceptions import ValidationError

from innotter import settings


class AvatarUploadService:

    @staticmethod
    def get_avatar(request):
        user_picture = request.data['file']
        return user_picture

    @staticmethod
    def get_avatar_name(request):
        avatar = AvatarUploadService.get_avatar(request)
        avatar_name = avatar.name.split('.')[0]
        return avatar_name

    @staticmethod
    def upload_avatar_to_localstack(request):
        AvatarUploadService.check_avatar_extension(request)
        s3 = boto3.client(
            's3',
            endpoint_url='http://host.docker.internal:4566/innotter-profile-pictures/'
        )

        s3.upload_fileobj(
            AvatarUploadService.get_avatar(request),
            settings.AWS_STORAGE_BUCKET_NAME,
            AvatarUploadService.get_avatar_name(request)
        )

        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                     'Key': AvatarUploadService.get_avatar_name(request)}
                                             )
        return response

    @staticmethod
    def check_avatar_extension(request):
        try:
            avatar_extension = AvatarUploadService.get_avatar(request).name.split('.')[1]
        except IndexError:
            raise ValidationError("File has no extension!")
        if avatar_extension not in ('jpeg', 'jpg', 'png'):
            raise ValidationError("Incorrect file extension!")
