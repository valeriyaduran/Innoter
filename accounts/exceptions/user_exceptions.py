from rest_framework.exceptions import APIException


class CurrentUserNotFound(APIException):
    status_code = 404
    default_detail = 'User not found'
    default_code = 'user_not_found_error'


class UsernameNotFound(APIException):
    status_code = 404
    default_detail = 'No user found by username provided'
    default_code = 'username_not_found_error'


class UnableToFollow(APIException):
    status_code = 404
    default_detail = 'You are not able to follow or accept yourself as a follower of your own page'
    default_code = 'unable_to_follow_error'