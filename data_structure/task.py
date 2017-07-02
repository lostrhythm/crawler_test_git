# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''
import json
import copy
import global_vars.global_dicts as GlobalDicts
import global_vars.global_config as GlobalConfig

from log.log import get_logger
logger = get_logger('Task')

class Task():
    def __init__(self, TaskID = 0, StrategyID = 'TEST', TaskType = 0, TaskContent = '', TaskStatus = 0, AdditionParams = {}, Encoding = None):
        # TaskType = [0, 1, 2] 
            # 0: plain    return {TaskIns_received : {FileName : FileContent, ...}, TaskIns_generated_1 : {}, ...} 
            # 1: deep     ..
            # 2: reservation
            
        # TaskStatus = [0, 1, 2]
            # 0: fail
            # 1: success
            # 2: partial success
            
        # TaskEncoding has the higher priority than StrategyEncoding
        
        self.TaskID = TaskID # -1 means spider_generate tasks
        self.StrategyID = StrategyID
        self.TaskType = TaskType
        self.TaskContent = TaskContent
        self.TaskStatus = TaskStatus
        self.AdditionParams = AdditionParams
        self.Encoding = Encoding
        

    @classmethod
    def load_task(cls, TaskJson):
        LocalEncoding = GlobalConfig.BasicParameters_dict['local_encoding']
        TaskDict = json.loads(TaskJson, encoding = LocalEncoding) 
        
        TaskID = TaskDict['TaskID']
        StrategyID = TaskDict['StrategyID']
        TaskType = TaskDict['TaskType']
        TaskStatus = TaskDict['TaskStatus']
        
        TaskContent = TaskDict.get('TaskContent') or ''
        AdditionParams = json.loads(TaskDict.get('AdditionParams') or {}, encoding = LocalEncoding)
        Encoding = TaskDict.get('Encoding') # when None, spider using encoding of strategy
        
        TaskIns = cls(TaskID, StrategyID, TaskType, TaskContent, TaskStatus, AdditionParams, Encoding)
        return TaskIns
    

    def get_json(self):
        LocalEncoding = GlobalConfig.BasicParameters_dict['local_encoding']
        
        TaskDict = copy.deepcopy(self.__dict__)
        [TaskDict.pop(key) for key in self.__dict__ if key[0] == '_']
        TaskDict['AdditionParams'] = json.dumps(self.__dict__['AdditionParams'], encoding = LocalEncoding)
        
        TaskJson = json.dumps(TaskDict, encoding = LocalEncoding)
        return TaskJson
    

if __name__ == '__main__':
    t_0 = Task()
    t_1 = Task(TaskType = 3)
    t_2 = Task(TaskStatus = 3)
     
    print repr(t_0.get_json())
    print repr(t_1.get_json())
    print t_1.TaskType
    print t_2.TaskStatus
     
    TaskJson_3 = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 0, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
    t_3 = Task.load_task(TaskJson_3)
    t_3_json = t_3.get_json()
    print t_3.__dict__
    print repr(t_3_json)
     
      
#     task = {'key':'大地'}  
#     print repr(json.dumps(task, encoding='utf-8'))
#     print repr(json.dumps(task, encoding='gbk'))