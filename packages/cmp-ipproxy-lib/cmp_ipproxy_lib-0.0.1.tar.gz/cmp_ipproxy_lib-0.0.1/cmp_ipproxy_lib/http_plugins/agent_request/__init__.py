import logging
import time

from cmp_ipproxy_lib import grpc_client
from cmp_ipproxy_lib.grpc_generate import AgentFeedBackBucket_pb2

from cmp_ipproxy_lib.util import global_dict

logger = logging.getLogger(__name__)

_SERVER_NAME = global_dict.get_value("server_name")
ips = []


def install():
    # noinspection PyBroadException
    try:
        from requests import Session

        _request = Session.request

        def _agent_request(this: Session, method, url,
                           params=None, data=None, headers=None, cookies=None, files=None,
                           auth=None, timeout=None, allow_redirects=True, proxies=None,
                           hooks=None, stream=None, verify=None, cert=None, json=None):

            from urllib.parse import urlparse

            start_time = int(round(time.time() * 1000))
            response = ""
            exception = ""

            try:

                # proxies = grpc_client.get_proxies()

                response = _request(this, method, url, params, data, headers, cookies, files, auth, timeout,
                                    allow_redirects,
                                    proxies,
                                    hooks, stream, verify, cert, json)
            except Exception as e:
                exception = str(e)
                logger.error("_agent_request exception:" + exception)
                raise e
            finally:
                reportInfo(start_time, exception, response)

            return response

        Session.request = _agent_request
    except Exception:
        logger.error('failed to install plugin %s', __name__)


def reportInfo(start_time, exception, response):
    try:
        end_time = int(round(time.time() * 1000))
        feedbackBucketLog = AgentFeedBackBucket_pb2.FeedbackBucketLog()
        feedbackBucketLog.serverName = _SERVER_NAME
        feedbackBucketLog.costTime = end_time - start_time
        feedbackBucketLog.reportTime = int(time.time() * 1000)
        feedbackBucketLog.exception = exception
        feedbackBucketLog.statue = 2000
        if not response is None and response != "":
            feedbackBucketLog.statue = response.status_code
            feedbackBucketLog.url = response.url
            feedbackBucketLog.responseSize = len(response.content)
        else:
            if "Connection refuse" in exception:
                feedbackBucketLog.statue = 2001
            elif "connect timeout" in exception:
                feedbackBucketLog.statue = 2002
            elif "No route to host" in exception:
                feedbackBucketLog.statue = 2003
            elif "Timeout waiting for connection from pool" in exception:
                feedbackBucketLog.statue = 4001
            elif "Read timed out" in exception:
                feedbackBucketLog.statue = 4002

        logger.info("feedbackBucketLogJson: " + str(feedbackBucketLog))

        grpc_client.agentFeedBackBucket(feedbackBucketLog)
    except Exception as e:
        logging.error(str(e))
