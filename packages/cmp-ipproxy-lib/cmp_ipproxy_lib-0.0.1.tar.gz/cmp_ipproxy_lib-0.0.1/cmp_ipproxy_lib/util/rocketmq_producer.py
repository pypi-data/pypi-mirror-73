# #!/usr/bin/env python
# # coding=utf8
# import sys
#
# from mq_http_sdk.mq_exception import MQExceptionBase
# from mq_http_sdk.mq_producer import *
# from mq_http_sdk.mq_client import *
# import time
#
# # 初始化 client
# mq_client = MQClient(
#     # 设置HTTP接入域名（此处以公共云生产环境为例）
#     # "http://MQ_INST_1264942389759895_BcNYhXZ8.cn-hangzhou.mq-internal.aliyuncs.com:8080",
#     "http://1264942389759895.mqrest.cn-qingdao-public.aliyuncs.com",
#     # AccessKey 阿里云身份验证，在阿里云服务器管理控制台创建
#     "LTAIH9iVXSXohX1J",
#     # SecretKey 阿里云身份验证，在阿里云服务器管理控制台创建
#     "JumfT3R8iW4NvZjQOXFtRSS9kKfX57"
# )
# # 所属的 Topic
# topic_name = "cmp-proxy-api-log-test"
# # Topic所属实例ID，默认实例为空None
# instance_id = ""
#
# producer = mq_client.get_producer(instance_id, topic_name)
#
#
# def send_mq(content):
#     try:
#         msg = TopicMessage(
#             # 消息内容
#             content,
#             # 消息标签
#             "error_log"
#         )
#         # 设置属性
#         # msg.put_property("a", "i")
#         # 设置KEY
#         # msg.set_message_key("131231223")
#         re_msg = producer.publish_message(msg)
#         print("Publish Message Succeed. MessageID:%s, BodyMD5:%s" % (re_msg.message_id, re_msg.message_body_md5))
#
#     except MQExceptionBase as e:
#         if e.type == "TopicNotExist":
#             print("Topic not exist, please create it.")
#             # sys.exit(1)
#         print("Publish Message Fail. Exception:%s" % e)
