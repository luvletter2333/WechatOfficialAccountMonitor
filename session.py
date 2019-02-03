import requests
import pickle

_session = None
_UrlToken = None
_isLogin = None


def getSession():
    global _session
    if not _session:
        _session = requests.Session()
    return _session


def setUrlToken(urlToken):
    global _UrlToken
    _UrlToken = urlToken


def getUrlToken():
    global _UrlToken
    return _UrlToken


def saveToFile():
    raise NotImplementedError()
    # s = MpWechat.getSession()
    # with open('mp.weixin.qq.com.session', 'wb') as f:
    #     pickle.dump(s.cookies, f)


def loadFromFile():
    raise NotImplementedError()



if __name__ == '__main__':
    s1 = MpWechat.getSession()
    s2 = MpWechat.getSession()
    print(id(s1))
    print(id(s2))
