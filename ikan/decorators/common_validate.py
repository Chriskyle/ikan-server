from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.models import Feed
from ikan.service.token.util import decode_token


def account_personal(f):
    def wrapped_f(self, request, pk):
        token = request.META.get(const.META_TOKEN, const.UNKNOWN)
        try:
            payload = decode_token(token)
            account_id = payload.get(const.ACCOUNT_ID)
            feed = Feed.objects.get(pk=pk)
            if account_id == feed.account_id:
                return f(self, request, pk)
            else:
                return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)
        except Feed.DoesNotExist:
            return XResponse(status_code=const.CODE_10004, msg=const.MSG_FAIL)

    return wrapped_f


def login_required(f):
    def wrapped_f(self, request, pk):
        token = request.META.get(const.META_TOKEN, const.UNKNOWN)
        if token.strip() == const.UNKNOWN:
            return XResponse(status_code=const.CODE_10011, msg=const.MSG_LOGIN_REQUIRED)
        else:
            return f(self, request, pk)

    return wrapped_f
