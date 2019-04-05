import session
import login
from config import Config
import logger
import message
import comment
import itchat


def qrCallback(qrcode_image):
    qrcode_image.show()


def callback_verifyCode(vc_image):
    vc_image.show()
    logger.logger.info("Please enter verify code")
    code=input()
    logger.logger.info("input verify code:"+code)
    return code


def callback_newMessage(message):
    print()
    print(message)
    print()


def callback_newComment(comment):
    print()
    print(comment)
    print()


_config = Config.getConfig()
logger.Init_Logger()
itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.send_msg("itchat login succeed!","filehelper")

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


input()


