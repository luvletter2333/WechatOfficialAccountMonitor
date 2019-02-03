from session import MpWechat
import login
from config import Config
import logger

logger.Init_Logger()

def qrCallback(qrcode_image):
    qrcode_image.show()

def callback_verifyCode(vc_image):
    vc_image.show()
    logger.logger.info("Please enter verify code")
    code=input()
    logger.logger.info("input verify code:"+code)
    return code

_config = Config.getConfig()
if login.Login(_config,qrCallback=qrCallback,verifycodeCallback=callback_verifyCode):
    logger.logger.debug("Login Success. Return to main function")

input()


