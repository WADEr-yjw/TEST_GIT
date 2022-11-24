# -*- coding: utf-8 -*-
import json
import time
import sys
f = open("result.json")
result = json.load(f)
mac_th = result['MAC']['Throughput']
mac_delay = result['MAC']['Delay']
mac_rate = result['MAC']['deli_rate']
route_th = result['Route']['Throughput']
route_delay = result['Route']['Delay']
f.close()
f = open("./python_script/time_save.txt","r")
time_t = f.readline()
f.close()
mint, maxt = [int(ii) for ii in sys.argv[1].split(',')]
print (time_t, '\t',end='')
print ('[',mint,',',maxt,']',sep='',end='')
print ('\t','\t',mac_th, '\t', '\t',route_th, '\t', '\t',mac_delay, '\t', '\t',route_delay, '\t', '\t',mac_rate)
