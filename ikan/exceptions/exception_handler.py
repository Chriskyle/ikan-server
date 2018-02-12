from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import set_rollback

from ikan.core.const import const
from ikan.exceptions.common.exception import Error, error_response


def exception_handler(exc, context):
    if isinstance(exc, Error):
        set_rollback()
        return error_response(exc.message, exc.status_code)

    if isinstance(exc, KeyError):
        set_rollback()
        return error_response(u'参数错误', const.CODE_10007)

    if isinstance(exc, AuthenticationFailed):
        return error_response(u'token已过期', const.CODE_10001)

    if isinstance(exc, PermissionDenied):
        return error_response(u'refresh token已过期', const.CODE_10002)

