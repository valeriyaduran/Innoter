from rest_framework.exceptions import APIException


class PageNotFound(APIException):
    status_code = 404
    default_detail = 'Current user does not have a page. Please, create a page before'
    default_code = 'current_user_page_not_found_error'


class PageToFollowNotFound(APIException):
    status_code = 404
    default_detail = 'Requested user does not have a page.'
    default_code = 'page_to_follow_not_found_error'