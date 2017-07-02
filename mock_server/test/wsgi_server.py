# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''

# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from db_opedb_operations.mock_server.test.wsgi_hellot application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print "Serving HTTP on port 8000..."
# 开始监听HTTP请求:
httpd.serve_forever()