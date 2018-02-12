import datetime

import jwt

from ikan.core.const import const


def create_token(account_id, time):
    token = jwt.encode({
        const.EXPIRE_TIME: datetime.datetime.utcnow() + datetime.timedelta(
            seconds=time),
        const.ACCOUNT_ID: account_id},
        const.SECRET, algorithm=const.ALGORITHM)
    return token


def decode_token(token):
    return jwt.decode(token, const.SECRET, algorithms=const.ALGORITHM)
