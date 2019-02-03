# mp.weixin.qq.com协议分析



## 登陆







#### 留言扫描

Request URL: https://mp.weixin.qq.com/cgi-bin/appmsgotherinfo?appmsgidlist=2247489117,2247489094,2247483674,2247483671,2247483668,2247483651&token=517506600&token=517506600&lang=zh_CN&f=json&ajax=1

可以请求到每一篇推文(appmsg)下面的留言数量

通过数量判断每一篇推文是否有新的留言



#### 消息扫描



##### 伪代码：

- 请求https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&token=517506600&lang=zh_CN&f=json
  - 返回结构体：
    - {
    - base_resp: {err_msg: "", ret: 0}
    - can_search_msg: 1
    - last_fans_msg_id: 438521521
    - latest_msg_id: 438521546
    - msg_items: "balabala"
    - new_user_tag: 1
    - star_msg_cnt: 0
    - total_msg_cnt: 26
    - }
- 判断本次的Head与上次的Head是否相同
  - 如相同则说明
- 如不相同：
- 按照msg_items里面的顺序一个一个往下爬
  - 若爬不到（1s中刷了 超过20条消息）
  - 加参数offset=...
  - 直到找到上一条Head存在为止
- 将Head存下来
- sleep 1s