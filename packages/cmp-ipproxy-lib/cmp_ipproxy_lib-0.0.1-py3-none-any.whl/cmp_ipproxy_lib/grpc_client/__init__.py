import logging
import socket

import grpc
from cmp_ipproxy_lib.util import setting_config

from cmp_ipproxy_lib.grpc_generate import AgentFeedBackBucket_pb2_grpc, AgentFetchProxy_pb2_grpc, \
    AgentHeartBeat_pb2_grpc, AgentFetchProxy_pb2, AgentFeedBackBucket_pb2, AgentFeedBack_pb2_grpc, AgentFeedBack_pb2, \
    AgentHeartBeat_pb2
from cmp_ipproxy_lib.util import ReportInfo

import traceback

feedbackBucketLogList = []

def agentFeedBack(reportInfo: ReportInfo):
    try:
        conn = get_insecure_channel()
        client = AgentFeedBack_pb2_grpc.AgentFeedbackServiceStub(channel=conn)
        response = client.feedback(
            AgentFeedBack_pb2.FeedbackLog(costTime=reportInfo.costTime, dep=reportInfo.dep,
                                          serverName=reportInfo.serverName, url=reportInfo.url,
                                          statue=reportInfo.statue, provider=reportInfo.provider,
                                          proxyType=reportInfo.proxyType, exception=reportInfo.exception,
                                          responseSize=reportInfo.responseSize, reportTime=reportInfo.reportTime,
                                          domain=reportInfo.domain))
        logging.info("agentFeedBack received: " + response.message)
    except Exception as e:
        logging.error("agentFeedBack error:", str(e))
        traceback.print_exc()


def agentFeedBackBucket(feedbackBucketLog):
    feedbackBucketLogList.append(feedbackBucketLog)
    logging.info("len(feedbackBucketLogList):" + str(len(feedbackBucketLogList)))
    if len(feedbackBucketLogList) < 5:
        return
    try:
        conn = get_insecure_channel()
        client = AgentFeedBackBucket_pb2_grpc.AgentFeedbackBucketServiceStub(channel=conn)
        response = client.feedbackBucket(
            AgentFeedBackBucket_pb2.FeedbackLogList(logList=feedbackBucketLogList))
        logging.info("agentFeedBackBucket received: " + response.message)
    except Exception as e:
        logging.error("agentFeedBackBucket error ", str(e))
        traceback.print_exc()


def agentHeartBeat(serverName, dep):
    try:
        conn = get_insecure_channel()
        client = AgentHeartBeat_pb2_grpc.AgentHeartBeatServiceStub(channel=conn)
        response = client.sendBeat(
            AgentHeartBeat_pb2.HeartBeat(serverIp=getIP(), serverName=serverName, dep=dep))
        logging.info("agentHeartBeat received: " + str(response.conf[0].confValue))
        return response.conf[0].confValue
    except Exception as e:
        logging.error("agentHeartBeat error: ", str(e))
        traceback.print_exc()


def agentFetchProxy(serverName):
    try:
        conn = get_insecure_channel()
        client = AgentFetchProxy_pb2_grpc.AgentFetchProxyServiceStub(channel=conn)
        response = client.fetch(AgentFetchProxy_pb2.ServerInfo(serverName=serverName))
        logging.info("agentFetchProxy2:" + str(len(response.proxies)))
        return response.proxies
    except Exception as e:
        logging.error("agentFetchProxy error: ", str(e))
        traceback.print_exc()

def get_insecure_channel():
    try:
        conn = grpc.insecure_channel(setting_config.config["grpc"]["ip"] + ':' + setting_config.config["grpc"]["port"])
        return conn
    except Exception as e:
        logging.error("get_insecure_channel error: ", str(e))
        traceback.print_exc()

def getIP():
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            logging.info("ip:" + ip)
            return ip