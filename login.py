from session import MpWechat
from PIL import Image
from io import BytesIO
import time
import threading
import logger
import regex

_isLogining = False


def Login(config,qrCallback,verifycodeCallback,verifycode=None,failCallback=None):
    if callable(qrCallback) is False:
        raise TypeError("parma `qrCallback` should be a function")
    if callable(verifycodeCallback) is False:
        raise TypeError("parma `verifycodeCallback` should be a function")
    global _isLogining
    if _isLogining:
        logger.logger.warning("Logining!")
        return False
    _isLogining = True
    # First Send Username And MD5(Password)
    r = MpWechat.getSession().post("https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin",
                                        data={
                                            "username": config["username"],
                                            "pwd": config["password_md5"],
                                            "imgcode": "" if (verifycode is None) else verifycode,
                                            "f": "json",
                                            "userlang": "zh_CN",
                                            "redirect_url": "",
                                            "token": "",
                                            "lang": "zh_CN",
                                            "ajax": "1"},
                                        headers={"Referer": "https://mp.weixin.qq.com/"})
    logger.logger.debug(r.text)
    r_json = r.json()
    ret_code = r_json["base_resp"]["ret"]
    # Return 0 means your Username and Password is right
    # and you can go straight to the next step
    if ret_code == 0:
        logger.logger.info("Login First-Step Succeed")
        if __WaitForScan(config,qrCallback):
            logger.logger.info("Login Success!")
            r = MpWechat.getSession().post("https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login",
                                           data={
                                               "userlang": "zh_CN",
                                               "redirect_url": "",
                                               "token": "",
                                               "lang": "zh_CN",
                                               "f": "json",
                                               "ajax": "1"
                                           },
                                           headers={"Referer":"https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account="+config["username_urlencode"]+"&token="})
            logger.logger.debug(r.text)
            if r.json()["base_resp"]["ret"] != 0:
                logger.logger.critical("Login Third-Step Fail")
                _isLogining = False
                return False
            redirect_url = r.json()["redirect_url"]
            url_token=regex.compile("token=[0-9]*").findall(redirect_url)[0].replace("token=","")
            logger.logger.info("Get Url_Token: "+url_token)
            MpWechat.setUrlToken(url_token)
        else:
            # Timeout in scanning qrcode
            MpWechat.getSession().cookies.clear()
            _isLogining = False
            return Login(config,qrCallback,verifycode,failCallback)
        _isLogining = False
        return True

    # Return 200008 OR 200027 means it need VerifyCode Or bad VerifyCode
    elif ret_code == 200008 or ret_code == 200027:
        logger.logger.warning("Need verify code or wrong verify code")
        ret = MpWechat.getSession().get("https://mp.weixin.qq.com/cgi-bin/verifycode?username=" + config["username"] + "&r=1549177766480")
        vc_img = Image.open(BytesIO(ret.content))
        _isLogining = False
        return Login(config,qrCallback,verifycodeCallback,verifycodeCallback(vc_img),failCallback)

    # Login Fail in First Step
    # Return 200023 means wrong Username or wrong Password
    elif ret_code == 200023:
        hint = "Cannot login because of wrong username or password. Please check your setting."
        logger.logger.critical(hint)
        if callable(failCallback):
            failCallback(hint)
        _isLogining = False
        return False
    else:
        hint = "Login First-Step Fail - " + str(r.json()["base_resp"])
        logger.logger.critical(hint)
        if callable(failCallback):
            failCallback(hint)
        _isLogining = False
        return False


def __WaitForScan(config,qrCallback):
    _referer = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account=" + config["username_urlencode"] + "&token="

    # First `ask for loginqrcode` Request Will Respond ret:1 with msg:default
    r = MpWechat.getSession().get("https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1",
            headers={"Referer":_referer})
    logger.logger.debug(r.text)

    # Then Request QRCode Image
    r_img = MpWechat.getSession().get("https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=36",headers={"Referer":_referer})
    i = Image.open(BytesIO(r_img.content))

    # Call `qrCallback` Async to inform you of scanning qrcode or you can customize your action
    threading.Thread(target=qrCallback,args=(i,)).start()

    # Check Scan Status
    while True:
        time.sleep(1.0)
        r = MpWechat.getSession().get(
            "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1",
            headers={"Referer": _referer})
        logger.logger.debug(r.text)
        ret_status = r.json()["status"]
        # Response List:
        # {"base_resp":{"err_msg":"ok","ret":0},"status":0,"user_category":0}    Not Scan
        # {"base_resp":{"err_msg":"ok","ret":0},"status":1,"user_category":3}    Confirm Login
        # {"base_resp":{"err_msg":"ok","ret":0},"status":3,"user_category":3}    Timeout
        # {"base_resp":{"err_msg":"ok","ret":0},"status":4,"user_category":0}    Scanned
        if ret_status == 0:
            logger.logger.info("Waiting For Scan")
        elif ret_status == 4:
            logger.logger.info("Scanned!")
        elif ret_status == 1:
            logger.logger.info("Scan Confirmed!")
            return True
        elif ret_status == 3:
            logger.logger.error("Timeout in scanning qrCode")
            return False
