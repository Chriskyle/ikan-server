from rest_framework.views import APIView

from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.models import Bill
from ikan.serializers import BillSerializer
from ikan.service.token.util import decode_token


class AssetsView(APIView):

    @staticmethod
    def get(request):
        try:
            token = request.META.get(const.META_TOKEN, const.UNKNOWN)
            payload = decode_token(token)
            account_id = payload.get(const.ACCOUNT_ID)
            bill = Bill.objects.get(account=account_id)
            serializer = BillSerializer(bill)
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
        except Bill.DoesNotExist:
            return XResponse(status_code=const.CODE_10006, msg=const.MSG_FAIL)
