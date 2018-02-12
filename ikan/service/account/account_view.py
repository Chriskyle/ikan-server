from rest_framework.views import APIView

from ikan.core.const import const
from ikan.core.response import XResponse
from ikan.models import Account, Bill
from ikan.models import ThirdParty
from ikan.serializers import AccountSerializer, CreateAccountSerializer
from ikan.service.token.util import create_token


class AccountView(APIView):

    @staticmethod
    def get(request, pk):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account)
            return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
        except Account.DoesNotExist:
            return XResponse(status_code=const.CODE_10006, msg=const.MSG_FAIL)

    @staticmethod
    def post(request):
        openid = request.data[const.OPENID]

        if openid is not None:
            try:
                third_party = ThirdParty.objects.get(openid=openid)
                account_serializer = AccountSerializer(third_party.account)

                data_wrapper = {const.TOKEN: create_token(third_party.account.id, const.TOKEN_EXPIRE_TIME),
                                const.REFRESH_TOKEN: create_token(third_party.account.id,
                                                                  const.REFRESH_TOKEN_EXPIRE_TIME),
                                const.ACCOUNT: account_serializer.data}
                return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=data_wrapper)
            except ThirdParty.DoesNotExist:
                account = {const.NICKNAME: request.data[const.NICKNAME],
                           const.AVATAR: request.data[const.AVATAR]}
                create_account_serializer = CreateAccountSerializer(data=account)

                if create_account_serializer.is_valid():
                    account_instance = create_account_serializer.save()
                    third_party = ThirdParty(openid=openid,
                                             bind_type=request.data[const.BIND_TYPE],
                                             account=account_instance)
                    third_party.save(force_insert=True)

                    bill = Bill(account=account_instance)
                    bill.total = 10
                    bill.balance = 10
                    bill.save(force_insert=True)

                    data_wrapper = {const.TOKEN: create_token(account_instance.id, const.TOKEN_EXPIRE_TIME),
                                    const.REFRESH_TOKEN: create_token(third_party.account.id,
                                                                      const.REFRESH_TOKEN_EXPIRE_TIME),
                                    const.ACCOUNT: AccountSerializer(account_instance).data}
                    return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=data_wrapper)
                else:
                    return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL,
                                     data=create_account_serializer.error_messages)
        else:
            return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL)

    @staticmethod
    def patch(request, pk):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return XResponse(status_code=const.CODE_10000, msg=const.MSG_SUCCESS, data=serializer.data)
            else:
                return XResponse(status_code=const.CODE_10007, msg=const.MSG_FAIL, data=serializer.error_messages)
        except Account.DoesNotExist:
            return XResponse(status_code=const.CODE_10006, msg=const.MSG_FAIL)
