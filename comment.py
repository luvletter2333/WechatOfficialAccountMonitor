import threading
from time import sleep
import session
import logger
import json

_config = None
_newCommentCallback = None
_listen_thread = None
_stop_flag = False


def init(__config,__newCommentCallback):
    global _config
    global _newCommentCallback
    _config = __config
    if not callable(__newCommentCallback):
        raise TypeError("parma `__newCommentCallback` should be a function")
    _newCommentCallback = __newCommentCallback
    _listen_thread = threading.Thread(target=__run__)
    _listen_thread.setDaemon(True)
    _listen_thread.start()


def close():
    if _listen_thread:
        _stop_flag = True


def __run__():
    global _stop_flag
    global _listen_thread
    global _newCommentCallback
    # Request Head Message
    counts = __request_comment_count__()
    while True:
        if _stop_flag:
            break
        sleep(3)
        new_comments = list()
        # Polling Start
        new_counts = __request_comment_count__()
        for comment in new_counts.keys():
            # Compare New Count and Old Count
            if comment in new_counts: # comment is Tweet ID
                # Old Tweet
                if(new_counts[comment] > counts[comment]):
                    logger.logger.info("Tweet"+str(comment)+" Has new comments.")
                    # Get Comments
                    comments = __request_comment__(comment)
                    for i in range(0,new_counts[comment] - counts[comment]):
                        new_comments.append(comments["comment"][i])
            else:
                # New Tweet
                if(new_counts[comment]>0):
                    # Get Comments
                    comments = __request_comment__(comment)
                    for i in range(0,new_counts[comment]):
                        new_comments.append(comments["comment"][i])
        counts = new_counts
        # Polling end, handle new messages
        for msg in new_comments:
            logger.logger.warning("Receive New Comment. id:"+ str(msg["id"]))
            #logger.logger.warning(str(json.dumps(msg)))
            _newCommentCallback(msg)
        new_comments.clear()
    _stop_flag = True
    _listen_thread = None


def __request_comment_count__(count=5):
    ret = session.getSession().get("https://mp.weixin.qq.com/misc/appmsgcomment?action=get_unread_appmsg_comment&begin=0&count="+str(count)+"&token="+session.getUrlToken()+"&lang=zh_CN&f=json&ajax=1")
    # logger.logger.debug(ret.text)
    # it's toooooooo big
    ret_json = ret.json()
    if not ret_json["base_resp"]["ret"] == 0:
        # Todo Exception Handling
        #      :block this thread and wait login status back
        raise NotImplementedError()
    count_dic = dict()
    for item in ret_json["item"]:
        count_dic[item["comment_id"]] = item["total_count"]
    return count_dic


def __request_comment__(comment_id): # comment_id is Tweet ID
    ret = session.getSession().get("https://mp.weixin.qq.com/misc/appmsgcomment?action=list_comment&begin=0&count=20&comment_id="+str(comment_id)+"&filtertype=0&day=0&type=2&max_id=0&token="+str(session.getUrlToken())+"&lang=zh_CN&f=json&ajax=1")
    # logger.logger.debug(ret.text)
    ret_json = ret.json()
    if not ret_json["base_resp"]["ret"] == 0:
        # Todo Exception Handling
        #      :block this thread and wait login status back
        raise NotImplementedError()
    return json.loads(ret_json["comment_list"])

