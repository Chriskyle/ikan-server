from rest_framework.response import Response

from ikan.core.const import const


class XResponse(Response):

    def __init__(self, status_code, msg=None, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(XResponse, self).__init__(data={const.STATUS_CODE: status_code,
                                              const.MSG: msg,
                                              const.DATA: data}, status=status,
                                        template_name=template_name, headers=headers,
                                        exception=exception, content_type=content_type)
