from rest_framework.views import APIView

from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.serializers import UploadImageSerializer


class UploadImageView(APIView):

    @staticmethod
    def post(request):
        serializer = UploadImageSerializer(data=request.data.dict())
        if serializer.is_valid():
            serializer.save()
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
        return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL, data=serializer.error_messages)
