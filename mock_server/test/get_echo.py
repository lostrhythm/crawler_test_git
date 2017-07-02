# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''
import urllib
import urllib2
import json


def get_echo(data_dict = {},echo_server_url = 'http://localhost:5000/echo'):
    # post
    request = urllib2.Request(echo_server_url)
    data = urllib.urlencode(data_dict)
    response = urllib2.urlopen(request, data)    
    return response.read() # json

if __name__ == '__main__':    
    data_dict = {'taskId':'123', 'taskParams':'{"taskParam_1": ["111"], "taskparam_2": ["222"]}'}
    print repr(get_echo(data_dict))
    print type(get_echo(data_dict))