import threading
from time import sleep
import session
import logger
import json

_config = None
_newMessageCallback = None
_listen_thread = None
_stop_flag = False


def init(__config,__newMessageCallback):
    global _config
    global _newMessageCallback
    _config = __config
    if not callable(__newMessageCallback):
        raise TypeError("parma `__newMessageCallback` should be a function")
    _newMessageCallback = __newMessageCallback
    _listen_thread = threading.Thread(target=__run__)
    _listen_thread.setDaemon(True)
    _listen_thread.start()


def close():
    if _listen_thread:
        _stop_flag = True


def __run__():
    global _stop_flag
    global _listen_thread
    global _newMessageCallback
    # Request Head Message
    items = json.loads(__request_message__()["msg_items"])["msg_item"]
    # print(items)
    head = items[0]["id"]
    logger.logger.info("get head message. id:"+str(head))
    while True:
        if _stop_flag:
            break
        sleep(3)
        # Polling Start
        _found_head = False
        _page = 0
        new_message = list()
        while not _found_head:
            #   Todo
            items = json.loads(__request_message__(_page)["msg_items"])["msg_item"]
            if _page == 0:
                _new_head = items[0]["id"]
            for i in range(0,19):
                if items[i]["id"] == head:
                    _found_head = True
                    break
                new_message.append(items[i])
            _page = _page + 1
        logger.logger.debug("set new head id"+str(_new_head))
        head = _new_head
        # Polling end, handle new messages
        for msg in new_message:
            logger.logger.warning("Receive New Message. id:"+ str(msg["id"]))
            #logger.logger.warning(str(json.dumps(msg)))
            _newMessageCallback(msg)
        new_message.clear()
    _stop_flag = True
    _listen_thread = None


def __request_message__(offset=0):
    ret = session.getSession().get("https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token="+session.getUrlToken()+"&lang=zh_CN&f=json&offset="+str(offset))
    # logger.logger.debug(ret.text)
    # it's toooooooo big
    ret_json = ret.json()
    if not ret_json["base_resp"]["ret"] == 0:
        # Todo Exception Handling
        #      :block this thread and wait login status back
        raise NotImplementedError()
    return ret.json()


