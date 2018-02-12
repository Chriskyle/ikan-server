from rest_framework.views import APIView

from ikan.core import paginator
from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.models import Notification
from ikan.serializers import NotificationSerializer


class NotificationView(APIView):

    @staticmethod
    def get(request):
        notifications = Notification.objects.all()
        return paginator.api_paging(notifications, request, NotificationSerializer)

    @staticmethod
    def delete(request, pk):
        notification = Notification.objects.get(pk=pk)
        serializer = NotificationSerializer(notification, data=request.data)
        notification.delete()
        return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
