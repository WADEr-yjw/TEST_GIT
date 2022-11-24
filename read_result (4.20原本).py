# -*- coding: utf-8 -*-
import json
import time
f = open("result.json")
result = json.load(f)
mac_th = result['MAC']['Throughput']
mac_delay = result['MAC']['Delay']
mac_rate = result['MAC']['deli_rate']
route_th = result['Route']['Throughput']
route_delay = result['Route']['Delay']
print (time.strftime("%Y-%m-%d_%X", time.localtime()), '\t',mac_th, '\t', route_th, '\t', mac_delay, '\t', route_delay, '\t', mac_rate)
