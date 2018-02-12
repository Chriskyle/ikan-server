from rest_framework.views import APIView

from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.models import Denomination
from ikan.serializers import DenominationSerializer


class DenominationView(APIView):

    @staticmethod
    def get(request):
        denominations = Denomination.objects.all()
        serializer = DenominationSerializer(denominations, many=True)
        return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)