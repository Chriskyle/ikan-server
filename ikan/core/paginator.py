from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ikan.core.const import const
from ikan.core.response import XResponse


def api_paging(objects, request, Serializer):
    try:
        page_size = int(request.GET.get('page_size', const.PAGE_SIZE))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)

    paginator = Paginator(objects, page_size)
    total = paginator.count
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    serializer = Serializer(objects, many=True)
    list_wrapper = {
        'list': serializer.data,
        'page': page,
        'total': total
    }
    return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=list_wrapper)
