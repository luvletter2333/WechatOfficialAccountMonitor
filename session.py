import requests
import pickle

_session = None
_UrlToken = None
_isLogin = None

class MpWechat:

    @staticmethod
    def getSession():
        global _session
        if not _session:
            _session = requests.Session()
        return _session

    @staticmethod
    def setUrlToken(urlToken):
        _UrlToken = urlToken

    @staticmethod
    def getUrlToken():
        return _UrlToken

    @staticmethod
    def setisLogin(isLogin):
        _isLogin = isLogin

    @staticmethod
    def getisLogin():
        return _isLogin

    @staticmethod
    def saveToFile():
        raise NotImplementedError()
        # s = MpWechat.getSession()
        # with open('mp.weixin.qq.com.session', 'wb') as f:
        #     pickle.dump(s.cookies, f)

    @staticmethod
    def loadFromFile():
        raise NotImplementedError()



if __name__ == '__main__':
    s1 = MpWechat.getSession()
    s2 = MpWechat.getSession()
    print(id(s1))
    print(id(s2))
