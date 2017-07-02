# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
'''
thesse methods are out of box methods should not be organized in a class and uses loggers,
if one do want to add logger, should write new methods in the core modules, and wrap these methods up,

really basic method, even without catch exceptions and retrys
'''
import urllib
import urllib2
import json
import cookielib
import traceback


def http_get(url = '', headers = {}, cookieuse = False, timeout = 2):
    req = urllib2.Request(url, headers = headers)
    
    if cookieuse:
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    else:
        opener = urllib2.build_opener()
        
    response = opener.open(req, timeout = timeout)

    return response.read(), response.headers
                
        
        
    
def http_post(url = '', params = {}, headers = {}, serialization = 'Json', cookieuse = False, timeout = 2):
    if serialization == 'Json':
        data = json.dumps(params) # inner network communication
    elif serialization == 'UrlEncode':
        data = urllib.urlencode(params)
        
    req = urllib2.Request(url, data, headers)
    
    if cookieuse:
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    else:
        opener = urllib2.build_opener()
        
    response = opener.open(req, timeout = timeout)
    return response.read(), response.headers
    
    
    
    
    
    
if __name__ == '__main__':    
    
    try:
        params = {'strategy_id' : 'TEST_1', 'tasks_batchsize' : 10}
        resp, headers = http_post(url = 'http://localhost:5000/task', params = params)
    except Exception as e:
        print traceback.format_exc(e)
    else:
        print resp