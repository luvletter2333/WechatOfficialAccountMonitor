import logging
import config

logger = None

def Init_Logger():
    global logger
    if logger:
        return
    if config.Config.getConfig()["debug"]:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"

    logger = logging.getLogger()  # 不加名称设置root logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT,datefmt='%Y-%m-%d %H:%M:%S')
    # 使用FileHandler输出到文件
    fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.info('this is info message')
    logger.warning('this is warn message')