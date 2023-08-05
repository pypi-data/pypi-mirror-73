# import time
# import traceback
#
# import json
# from agent.util import grpc_client
# from agent.util.ReportInfo import ReportInfo
#
# dep = "cmp"
# serverName = "gdc-sinaspider"
# ips = []
#
#
# def handle_response(fn):
#     def wrapper(*args):
#         exception = ""
#         start_time = int(round(time.time() * 1000))
#         response = ""
#         print("start_time===========>" + str(start_time))
#         try:
#             response = fn(*args)
#         except Exception as e:
#             exception = str(e)
#             print("str(e)=======>" + exception)
#             traceback.print_exc()
#
#         end_time = int(round(time.time() * 1000))
#         print("end_time=========>" + str(end_time))
#
#         # requests.Response.content
#         reportInfo = ReportInfo()
#         reportInfo.dep = dep
#         reportInfo.serverName = serverName
#         reportInfo.costTime = end_time - start_time
#         reportInfo.reportTime = int(time.time() * 1000)
#         reportInfo.exception = exception
#         reportInfo.statue = 2000
#         if not response is None  and response != "":
#             print("response========================>" + str(response))
#             print("response.status_code========================>" + str(response.status_code))
#             print("response.url========================>" + str(response.url))
#             print("response.content========================>" + str(len(response.content)))
#             reportInfo.statue = response.status_code
#             reportInfo.url = response.url
#             reportInfo.responseSize = len(response.content)
#         else:
#             if "Connection refuse" in exception:
#                 reportInfo.statue = 2001
#             elif "connect timeout" in exception:
#                 reportInfo.statue = 2002
#             elif "No route to host" in exception:
#                 reportInfo.statue = 2003
#             elif "Timeout waiting for connection from pool" in exception:
#                 reportInfo.statue = 4001
#             elif "Read timed out" in exception:
#                 reportInfo.statue = 4002
#
#         reportInfoJson = json.dumps(reportInfo.__dict__)
#
#         print("reportInfoJson===================>" + reportInfoJson)
#
#         grpc_client.agentFeedBack(reportInfo)
#
#         print("goodby=========================》, %s" % fn.__name__)
#         return response
#
#     return wrapper
#
# def get_proxies():
#     # if len(ips) == 0:
#     #     result = requests.get("http://10.64.56.235:8080/proxy/agent/fetch/ip?serverName=foot-tm-spr&provider")
#     #     print("requests.get===============》" + result.text)
#     #     new_ips = json.loads(result.text)
#     #     for ip in new_ips:
#     #         ips.append(ip)
#     #
#     # print(ips)
#     # print(len(ips))
#     #
#     # ip_info = ips.pop()
#
#     ip_infos = grpc_client.agentFetchProxy(serverName)
#     print("ip_infos.proxies====>" + str(len(ip_infos)))
#     ip_info = ip_infos[0]
#     if not ip_info is None and ip_info != "":
#         print("ip_info======>" + str(ip_info.ip))
#         ip = ip_info.ip
#         port = ip_info.port
#         proxies = {
#             # "http": "http://" + ip_data + ":" + port_data
#             "http": "http://" + ip + ":" + str(port),
#             "https": "https://" + ip + ":" + str(port)
#         }
#         print(proxies)
#         return proxies
#
# # print(json.loads("{\"1\":\"2\"}"))
# # ips.count(ips, json.loads("[{\"1\":\"2\"}]"))
# # print(ips)
# # get_proxies()
# #
# # proxies = {
# #         # "http": "http://" + ip_data + ":" + port_data
# #         "http": "http://175.147.96.120:40230"
# #     }
# #
# # for i in range(0, 5):
# #     data = requests.get('http://httpbin.org/get', proxies = proxies)
# #     print(data.text)
