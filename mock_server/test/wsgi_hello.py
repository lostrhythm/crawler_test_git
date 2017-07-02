# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''

# def application(environ, start_response):
#     print environ
#     start_response('200 OK', [('Content-Type', 'text/html')])
#     return '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')

# def application(environ, start_response):
#     method = environ['REQUEST_METHOD']
#     start_response('200 OK', [('Content-Type', 'text/html')])
#     
#     if method=='GET':
#         return '<h1>Hello, get %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
#     if method=='POST':
#         print environ
#         return '<h1>Hello, post %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')

def application(environ, start_response):
    pass