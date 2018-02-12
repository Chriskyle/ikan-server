class _Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


const = _Const()

const.STATUS_CODE = "status_code"
const.MSG = "msg"
const.DATA = "data"

const.UNKNOWN = "unknown"

const.MSG_SUCCESS = "success"
const.MSG_FAIL = "fail"

const.CODE_10000 = 10000  # success
const.CODE_10001 = 10001  # token expired
const.CODE_10002 = 10002  # refreshToken expired
const.CODE_10003 = 10003  #
const.CODE_10004 = 10004  #
const.CODE_10005 = 10005  # feed does not exist
const.CODE_10006 = 10006  # account does not exist
const.CODE_10007 = 10007  # http bad request
const.CODE_10008 = 10008  #
const.CODE_10009 = 10008  #
const.CODE_10010 = 10010  # internal server error
const.CODE_10011 = 10011  # login required
const.CODE_10012 = 10012  # feed like fail
const.CODE_10013 = 10013  # feed buy fail
const.CODE_10014 = 10014  # balance is not enough


const.MSG_LOGIN_REQUIRED = "未登录状态下不能进行该操作"

const.PAGE_SIZE = 10

const.SEARCH_KEYWORD = "keyword"

const.OPENID = "openid"
const.NICKNAME = "nickname"
const.AVATAR = "avatar"
const.BIND_TYPE = "bind_type"

const.FEED_TYPE_HOME = 0
const.FEED_TYPE_TRENDING = 1
const.FEED_TYPE_DISCOVER = 2
const.FEED_TYPE_RECOMMEND = 3

const.META_TOKEN = "HTTP_TOKEN"
const.META_SKT = "HTTP_SKT"

const.VERSION_CODE = "version_code"

const.TOKEN = "token"
const.REFRESH_TOKEN = "refresh_token"
const.ACCOUNT = "account"
const.ACCOUNT_ID = "account_id"
const.FEED = "feed"
const.FEED_ID = "feed_id"
const.SEGMENT = "segment"
const.COMMENT_CONTENT = "content"
const.CATEGORY = "category"
const.BILL = "bill"
const.EXPIRE_TIME = "exp"
const.TOKEN_EXPIRE_TIME = 60 * 60 * 60 * 2
const.REFRESH_TOKEN_EXPIRE_TIME = 60 * 60 * 60 * 24 * 15

const.ALGORITHM = "HS256"
const.SECRET = b"MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKEoj9rdb6hbH3oSLylUwody/ZH7X384asnJZIAa65YO/OkMFR2mF3rCLwWNCfqKv5OtIfSCPajJ82oR7KzDI0p27NPhDBeI35POEYOnmRnDsgZiUirFDEccOwgzP7KCR9k5NzAGqacJsXMCyqW6LRnOadjK+YeQQcdqpsElWETnAgMBAAECgYBtmOEj7b2Wl8mzQZSTHhJg/QGW+oV6RkrRScWwHR6j4TN75XyiuiZzlIVX2A+2NA+PBYn292+pTxXbx67V2qsvT0P7ltIe9s8uSRfTpd2PeJ8Wtce5+Bdf8RsPfMfF5jujGDxaT5cU7qXr9Y7qNfkrmdafORuwR9wcevoUfm9CUQJBANYlAR4Jl2X2kzxdCMJYrpaZAOyNpQ4ayDZJoQbWT28OdxUZqlhc9UZNtb9NBC7oKVY6QU/DhegkanqFo1HqKpkCQQDAqFSOz5OKJ+6Pecjb+Vponlu+5YLQo7wLh/P6/ViWMYv6+wzFo/tCDhO2XSCrMRRRLvuGPtmPpLdVxS7Bhxt/AkEAxtAyOl3zRsHnLnq9gBnvdXf1yKk03WR2DxjKvFtKAjRu0JM0eLdNLIlHPKVXRelbP2f0bQZ9EuqERN4/o/SAuQJAPegZO8ahzzwjoUDt9Rl8Hq/8JSxUy7xBWac3FAjCpYiIRX7UTNHzk/c4CFqGe9wKfkfNlQavHEQ+kTYKXy+N+wJAVMU11hZMlECqjMkSkMpiHbaQSiF+YCJw+3LQgre6ndXhuS3F0bU+oWGJnZmhybqecLC0a6Y9YnRaRUKDYap+rg"
