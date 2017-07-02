# -*- coding:utf-8 -*-
'''
Created on 2017年6月23日

@author: Thinkpad
'''
import json
import base64
import os
import time
from flask import Flask
from flask import request
from log.log import get_logger
logger = get_logger('server_service')

app = Flask(__name__)




def StrategyGenerator():
    # initial strategies
    TEST_1_1_json = '{"RetryTime": 2, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_1", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    TEST_2_1_json = '{"RetryTime": 2, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_2", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    StrategyGroup_1_dict = {'TEST_1' : TEST_1_1_json, 'TEST_2' : TEST_2_1_json}
    StrategyGroupJson_1 = json.dumps(StrategyGroup_1_dict)  
    
    # new strategies
    TEST_1_2_json = '{"RetryTime": 3, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_1", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    TEST_2_2_json = '{"RetryTime": 3, "WaitTime": 1, "CookieUse":false, "StrategyID": "TEST_2", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 3, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "ContentException":[]}'
    StrategyGroup_2_dict = {'TEST_1' : TEST_1_2_json, 'TEST_2' : TEST_2_2_json}
    StrategyGroupJson_2 = json.dumps(StrategyGroup_2_dict)    
    
    looplist = [StrategyGroupJson_1, StrategyGroupJson_2]
    
    while True:
        for StrategyGroupJson in looplist:
            yield StrategyGroupJson



StrategyGenerator_Ins = StrategyGenerator()



@app.route('/strategy', methods=['GET'])
def strategy_server():
    return next(StrategyGenerator_Ins)



@app.route('/task', methods=['POST'])
def task_server():
    TasksGroupJson = ''
    data = json.loads( request.get_data() ) # decode Json
    logger.debug(repr(data)) # {'strategy_id': [u'TEST_1'], 'tasks_batchsize': [u'10']}
    
    # 'TEST_1'
    Task_1_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 1, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "data+science"}'
    Task_2_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 2, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "computer+science"}'
    Task_3_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 3, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "spider"}'
    Task_4_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 4, "TaskType": 0, "StrategyID": "TEST_1", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "queue"}'
    TaskGroup_1_dict = {1 : Task_1_json, 2 : Task_2_json, 3 : Task_3_json, 4 : Task_4_json}
    TaskGroup_1_json = json.dumps(TaskGroup_1_dict)

    # 'TEST_2'
    Task_5_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 5, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "python"}'
    Task_6_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 6, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "shell"}'
    Task_7_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 7, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "c++"}'
    Task_8_json = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 8, "TaskType": 0, "StrategyID": "TEST_2", "AdditionParams": "{\\"a\\": 2}", "TaskContent": "play+station"}'
    TaskGroup_2_dict = {5 : Task_5_json, 6 : Task_6_json, 7 : Task_7_json, 8 : Task_8_json}
    TaskGroup_2_json = json.dumps(TaskGroup_2_dict)  
    

    if data['strategy_id'].__class__ == u''.__class__:
        if data['strategy_id'] == 'TEST_1':
            TasksGroupJson += TaskGroup_1_json
        elif data['strategy_id'] == 'TEST_2':
            TasksGroupJson += TaskGroup_2_json

    elif data['strategy_id'].__class__ == [].__class__:
        for Strategy in data['strategy_id']:
            if Strategy == 'TEST_1': # in the real server_service it should use taskIns = taskpool[Strategy] to get new tasks
                TasksGroupJson += TaskGroup_1_json
            elif Strategy == 'TEST_2':
                TasksGroupJson += TaskGroup_2_json

        
    return TasksGroupJson # get strategy should be able to deal with empty strategy ""



@app.route('/upload', methods=['POST'])
def upload_server(): # get json directly
    UploadPackJson = request.get_data() # data = '{"TaskID": ["TaskStatus", "ResultPack_zip_b64"], ...}'
    UploadPack = json.loads(UploadPackJson)
    logger.debug(repr(UploadPack))
    
    # store local
    if not os.path.isdir('./results'):
        os.mkdir('./results')
        
    for TaskID in UploadPack:
        _, ResultPack_zip_b64 = UploadPack[TaskID]
        ResultPack_zip = base64.b64decode(ResultPack_zip_b64)
        zipfilename = './results/' + str(TaskID) + '_' + str(int(time.time())) + '.zip'
        with open(zipfilename, 'wb') as zf:
            zf.write(ResultPack_zip)
        
    ComfirmInfo = 'upload_server received TaskID: %s'%str(UploadPack.keys())
    return ComfirmInfo



@app.route('/monitor', methods=['POST'])
def monitor_server():
    UserCollectorMapJson = request.get_data()
    UserCollectorMap = json.loads(UserCollectorMapJson) # (user, {'TEST_1':strategy_status_collector, ...})
    
    user = UserCollectorMap[0]
    MachineStatus_dict = UserCollectorMap[1]

    logger.debug('Machine: %s, Status: %s'%(user, str(MachineStatus_dict)))
        
    ComfirmInfo = 'monitor_server received status of machine: %s'%str(user)
    return ComfirmInfo


@app.route('/register', methods=['POST'])
def register_server():
    UserInfoJson = request.get_data()
    UserInfo_dict = json.loads(UserInfoJson) # (user, {'TEST_1':strategy_status_collector, ...})
    
    user = UserInfo_dict['user']
    password = UserInfo_dict['password']

    logger.debug('user: %s, password: %s'%(user, str(password)))
        
    ComfirmInfo = 'Success in registering: %s'%str(user)
    return ComfirmInfo






if __name__ == '__main__':
    app.run()
    
    
    
    