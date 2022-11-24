# -*- coding: utf-8 -*-
# 文件名: test.py
import sys
#sys.path.append('/home/maoss/stackUIproject/performance_analysis')
#sys.path.append('/home/maoss/anaconda3/lib/python36.zip')
#sys.path.append('/home/maoss/anaconda3/lib/python3.6')
#sys.path.append('/home/maoss/anaconda3/lib/python3.6/lib-dynload')
#sys.path.append('/home/maoss/anaconda3/lib/python3.6/site-packages')
print('命令行参数如下:')
for i in sys.argv:
   print(i)
print('\n\nPython 路径为：', sys.path, '\n')

