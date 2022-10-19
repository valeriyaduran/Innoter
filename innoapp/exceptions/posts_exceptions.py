from rest_framework.exceptions import APIException


class PostNotFound(APIException):
    status_code = 404
    default_detail = 'Post does not exist!'
    default_code = 'post_not_found'
