from rest_framework import status

from ikan.core.const import const
from ikan.core.response import XResponse


class Error(Exception):

    def __init__(self, message=u'服务器异常', status_code=const.CODE_10010):
        self.message = message
        self.status_code = status_code

    def __unicode__(self):
        return u'[Error] %d: %s' % (self.status_code, self.message)

    def get_response(self):
        return error_response(self.message, self.status_code)


def error_response(message=u'服务器异常', status_code=const.CODE_10010):
    http_status = status.HTTP_200_OK

    if status_code == const.CODE_10001:
        http_status = status.HTTP_401_UNAUTHORIZED

    if status_code == const.CODE_10002:
        http_status = status.HTTP_403_FORBIDDEN

    return XResponse(status_code=status_code, msg=message, status=http_status)
