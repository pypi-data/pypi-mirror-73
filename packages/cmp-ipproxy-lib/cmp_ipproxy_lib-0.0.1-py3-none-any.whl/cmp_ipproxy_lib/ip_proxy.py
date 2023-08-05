import sys
from threading import Timer

from cmp_ipproxy_lib import grpc_client, http_plugins
from cmp_ipproxy_lib.util import global_dict
from cmp_ipproxy_lib.util import setting_config
import os

import yaml
import logging.config

def start(server_name):
    init_logging()
    init_global_dict(server_name)
    init_setting_config()
    start_heart_timer(server_name, "default")
    http_plugins.install()

def start_heart_timer(serverName, dep):
    grpc_client.agentHeartBeat(serverName, dep)
    Timer(1, start_heart_timer, (serverName, dep)).start()

def init_logging():
    # with open('logging_config.yaml', 'r', encoding='utf-8') as lf:
    file = os.path.dirname(os.path.abspath(__file__))
    with open(file + '/logging_config.yaml', 'r', encoding='utf-8') as lf:
        config = yaml.load(lf, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)

def init_global_dict(server_name):
    global_dict._init()
    global_dict.set_value("server_name", server_name)

def init_setting_config():
    env = "dev"
    file = os.path.dirname(os.path.abspath(__file__))
    with open(file + '/config.yaml', 'r', encoding='utf-8') as f:
        if len(sys.argv) > 1 and 'prd' in sys.argv:
            env = 'prd'
        elif len(sys.argv) > 1 and 'stg' in sys.argv:
            env = 'stg'
        elif len(sys.argv) > 1 and 'sit' in sys.argv:
            env = 'sit'
        else:
            env = env
        logging.info(f"app init: {env}")
        setting_config.config = yaml.load(f, Loader=yaml.FullLoader)[env]

# if __name__ == '__main__':
#     # start("gdc-sinaspider")
#     # os.system('python /Users/songzhipeng/PycharmProjects/http_test/http_test.py')
#     fp = open('/Users/songzhipeng/PycharmProjects/http_test/http_test.py')
#     lines = []
#     for line in fp:  # 内置的迭代器, 效率很高
#         lines.append(line)
#     fp.close()
#
#     lines.insert(9, "    print('a new line')")  # 在第 LINE+1 行插入
#     s = '\n'.join(lines)
#     fp = open('/Users/songzhipeng/PycharmProjects/http_test/http_test2.py', 'w')
#     fp.write(s)
#     fp.close()
#
#     os.system('python /Users/songzhipeng/PycharmProjects/http_test/http_test2.py')