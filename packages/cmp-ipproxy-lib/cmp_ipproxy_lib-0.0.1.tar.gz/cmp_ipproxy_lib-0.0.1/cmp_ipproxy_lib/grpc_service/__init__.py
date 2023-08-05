from cmp_ipproxy_lib.util import global_dict
import logging
from cmp_ipproxy_lib import grpc_client


def get_proxies():
    ip_infos = grpc_client.agentFetchProxy(global_dict.get("server_name"))
    logging.info("ip_infos.proxies: " + str(len(ip_infos)))
    ip_info = ip_infos[0]
    if not ip_info is None and ip_info != "":
        logging.info("ip_info: " + str(ip_info.ip))
        ip = ip_info.ip
        port = ip_info.port
        proxies = {
            "http": "http://" + ip + ":" + str(port),
            "https": "https://" + ip + ":" + str(port)
        }
        logging.info(proxies)
        return proxies