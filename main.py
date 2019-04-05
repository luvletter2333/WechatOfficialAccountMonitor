#-*-coding:utf-8-*- 
import session
import login
from config import Config
import logger
import message
import comment
import itchat
import threading
from itchat.content import TEXT
from time import sleep
from PIL import Image
import utils


_config = Config.getConfig()
logger.Init_Logger()


vc_code = ""
wait_vc_code =  False


itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run(blockThread=False)
# Get Wechat Group
itchat_group = itchat.search_chatrooms(name="test_qqq")[0]
# itchat_group = itchat.search_chatrooms(userName="@@0eaaf5d166c7515d6665495ef07bd21390e0307e1e11fa2e024f6bbad7a8cb1c")[0]
NickName = itchat.get_friends(update=False)[0].NickName
logger.logger.debug(itchat_group)
itchat_group.send_msg("itchat login succeed")


@itchat.msg_register(TEXT,isGroupChat=True)
def itchat_text_receiver(msg):
    if msg.isAt:
        logger.logger.debug(msg)
        global vc_code,wait_vc_code,NickName
        if wait_vc_code:
            content = str(msg.Text).encode().decode(encoding="utf-8")
            content = content.replace(NickName,"").replace("@","").replace("\u2005","")
            logger.logger.info("Receive VerifyCode:" + content)
            vc_code = content
            wait_vc_code = False


def qrCallback(qrcode_image):
    qrcode_image.save("mp_login.jpg")
    itchat_group.send_msg("Need VerifyCode")
    itchat_group.send_image("mp_login.jpg")


def callback_verifyCode(vc_image):
    vc_image.save("mp_login_vc.jpg")
    itchat_group.send_msg("Need VerifyCode")
    itchat_group.send_image("mp_login_vc.jpg")
    itchat_group.send_msg("Please At This Account And Reply VerifyCode")
    global vc_code,wait_vc_code
    vc_code = "1234"
    wait_vc_code = True
    for i in range(0,120):
        sleep(1)
        if not wait_vc_code:
            break
    logger.logger.info("Return VerifyCode:"+vc_code)
    return vc_code


def callback_newMessage(message):
    logger.logger.debug(message)
    msg = "【"+custom_time(message["date_time"])+"】【"+message["nick_name"]+"】：" + message["content"]
    logger.logger.info(msg)
    itchat_group.send_msg(msg)


def callback_newComment(comment):
    
    logger.logger.debug(comment)
    msg = "【"+custom_time(comment["post_time"])+"】【"+comment["nick_name"]+"】【"+comment["title"]+"】：" + comment["content"]
    logger.logger.info(msg)
    itchat_group.send_msg(msg)


if session.loadFromFile():
    if session.checklogin():
        logger.logger.info("Read Session Succeed!")
    else:
        logger.logger.info("Read Session Fail")
        session.clear()


if not session.checklogin():
    if login.Login(_config,qrCallback=qrCallback,verifycodeCallback=callback_verifyCode):
        logger.logger.debug("Login Success. Return to main function")
        logger.logger.debug("Start Message Listener")
        session.saveToFile()


message.init(_config,callback_newMessage)
comment.init(_config,callback_newComment)


