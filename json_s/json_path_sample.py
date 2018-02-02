# -*- coding:utf-8 -*-
# 演示Json Path
import  jsonpath_rw_ext

sample_json2 = {"network": {"udp": [{
    "src": "172.16.1.1",
    "dst": "172.16.1.102",
    "offset": 2102,
    "time": 0.17747807502746582,
    "dport": 68,
    "sport": 67
},
    {
        "src": "172.16.1.101",
        "dst": "172.16.1.102",
        "offset": 3255,
        "time": 0.3072469234466553,
        "dport": 137,
        "sport": 137
    }, ]}}



# 检查选择
json_path = "network.udp[*].dst"
# 条件过滤
json_path2 = "network.udp[?(@.offset==3255)].dst"
jsonpath_expr = jsonpath_rw_ext.parse(json_path)
jsonpath_exp2 = jsonpath_rw_ext.parse(json_path2)
print [match.value for match in jsonpath_expr.find(sample_json2)]
print [match.value for match in jsonpath_exp2.find(sample_json2)]

