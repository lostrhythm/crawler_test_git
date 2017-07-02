# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''


from flask import Flask
from flask import request
import json
import logging
from log.log import get_logger
logger = get_logger('echo_server')

app = Flask(__name__)

@app.route('/echo', methods=['GET'])
def echo_get():
    return 'using method GET'


@app.route('/echo', methods=['POST'])
def echo_post():
    data = dict(request.form)
    logger.debug(repr(data))
    return json.dumps(data,'utf-8')


if __name__ == '__main__':
    app.run()