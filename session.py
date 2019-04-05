import requests
import pickle

_session = None
_UrlToken = None


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
    #raise NotImplementedError()
    s = dict()
    s["session"] = _session
    s["UrlToken"] = _UrlToken
    with open('mp.weixin.qq.com.session', 'wb') as f:
        pickle.dump(s, f)


def loadFromFile():
    global _session
    global _UrlToken
    try:
        with open('mp.weixin.qq.com.session', 'rb') as f:
            s = pickle.load(f)
    except:
        return False
    _session = s["session"]
    _UrlToken = s["UrlToken"]
    return True


def checklogin():
    if _UrlToken is None:
        return False
    ret = _session.get("https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token="+str(_UrlToken)+"&lang=zh_CN&f=json")
    ret_json = ret.json()
    if not ret_json["base_resp"]["ret"] == 0:
        return False
    return True


def clear():
    global _session,_UrlToken
    _session = requests.session()
    _UrlToken = None
