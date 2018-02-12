from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import DecodeError
from jwt import ExpiredSignatureError
from rest_framework import status

from ikan.core.const import const
from ikan.service.token.util import decode_token


class RequestInterceptMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        token = request.META.get(const.META_TOKEN, const.UNKNOWN)
        if token.strip() != const.UNKNOWN:
            try:
                decode_token(token)
            except (DecodeError, ExpiredSignatureError):
                error = {const.STATUS_CODE: const.CODE_10001,
                         const.MSG: const.MSG_FAIL}
                return JsonResponse(error, status=status.HTTP_401_UNAUTHORIZED)
        return None
