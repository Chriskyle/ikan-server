from jwt import DecodeError, ExpiredSignatureError
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.service.token.util import create_token
from ikan.service.token.util import decode_token


class TokenView(APIView):

    @staticmethod
    def post(request):
        refresh_token = request.META[const.REFRESH_TOKEN]
        try:
            payload = decode_token(refresh_token)
            account_id = payload.get(const.ACCOUNT_ID)
            token_wrapper = {const.TOKEN: create_token(account_id, const.TOKEN_EXPIRE_TIME),
                             const.REFRESH_TOKEN: create_token(account_id,
                                                               const.REFRESH_TOKEN_EXPIRE_TIME)}
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=token_wrapper)
        except (DecodeError, ExpiredSignatureError):
            raise PermissionDenied
