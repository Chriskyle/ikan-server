from rest_framework.views import APIView

from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.models import Version
from ikan.serializers import VersionSerializer


class VersionUpdateView(APIView):

    @staticmethod
    def get(request):
        version = Version.objects.last()
        serializer = VersionSerializer(version, many=False)
        return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
