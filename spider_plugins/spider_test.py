# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
from log.log import get_logger
from core.spider import Spider
from data_structure.strategy import Strategy
from data_structure.task import Task
from time import sleep

class Spider_Test(Spider):
    def __init__(self, StrategyID): # cause when firstly instantiate the SpiderIns, the StrategyIns is not loaded yet, so pass the StrategyID artificially
        super(Spider_Test, self).__init__() # load default params
        LogFileName = 'Spider_Test_%s'%str(StrategyID)
        self.logger = get_logger(LogFileName, True)
    
    def plain_crawl(self, TaskIns, Fast = False):
        self.logger.info('plain crawling: %s'%str(TaskIns.TaskID))
        
        url = "https://www.zhihu.com/search?type=content&q=" + TaskIns.TaskContent
        headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language":"zh-CN,zh;q=0.8",
                        "Connection":"keep-alive",
                        "Host":"www.zhihu.com",
                        "Referer":"https://www.zhihu.com/search?type=content&q=data%20science",
                        "Upgrade-Insecure-Requests":"1",
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
        
        from time import time
        PageName = 'zhihu_%s.html'%str(time()) 
        Page = self.http_get(url, headers)
        
        ResultPack = (TaskIns, {PageName : Page})
        with open(PageName, 'w') as f:
            f.write(Page)
        
        return ResultPack
    
    
    
    def deep_crawl(self, TaskIns, Fast = False):
        self.logger.info('deep crawling: %s'%str(TaskIns.TaskID))
        sleep(5) # TEST: simulate the processing
        ResultPack = (TaskIns, {'filename.jpg' : 'content', 'newtask.html' : 'new taskIns json s'})
        return ResultPack
    





if __name__ == '__main__':
    from data_structure.status import MachineStatus, StrategyStatus
    import global_vars.global_dicts as GlobalDicts
    
    StrategyJson = '{"RetryTime": 3, "WaitTime": 1, "StrategyID": "TEST", "AdditionParams": "{\\"rules\\":[\\"rule_1\\", \\"rule_2\\"]}", "Timeout": 1, "Encoding": "utf-8", "FragmentalUpload": false, "FragmentalAmount":5, "CookieUse":false}'
    StrategyIns = Strategy.load_Strategy(StrategyJson)
    
    MachineStatusIns = MachineStatus()
    StrategyStatusIns = StrategyStatus(MachineStatusIns, 'TEST')
    GlobalDicts.StrategyStatus_dict.update({'TEST':StrategyStatusIns})
    
#     # tasktype 0
#     TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 0, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
#     TaskIns = Task.load_task(TaskJson)
#     Spider_Test_Ins = Spider_Test(StrategyIns.StrategyID)
#     ResultPack = Spider_Test_Ins.crawl(StrategyIns, TaskIns)
    
#     # tasktype 1
#     TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 1, "TaskType": 1, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
#     TaskIns = Task.load_task(TaskJson)
#     Spider_Test_Ins = Spider_Test(StrategyIns.StrategyID)
#     ResultPack = Spider_Test_Ins.crawl(StrategyIns, TaskIns)
     
#     # tasktype 2
#     # test attribute error
#     TaskJson = '{"Encoding": "utf-8", "TaskStatus": 1, "TaskID": 2, "TaskType": 2, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
#     TaskIns = Task.load_task(TaskJson)
#     Spider_Test_Ins = Spider_Test(StrategyIns.StrategyID)
#     ResultPack = Spider_Test_Ins.crawl(StrategyIns, TaskIns)
 
#     # tasktype 3
#     # test key error
#     TaskJson = '{"Encoding": "utf-8", "TaskStatus": 1, "TaskID": 3, "TaskType": 3, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
#     TaskIns = Task.load_task(TaskJson)
#     Spider_Test_Ins = Spider_Test(StrategyIns.StrategyID)
#     ResultPack = Spider_Test_Ins.crawl(StrategyIns, TaskIns)
#     print TaskIns.get_json()
    
    # tasktype 0
    TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 0, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": "data+science"}'
    TaskIns = Task.load_task(TaskJson)
    Spider_Test_Ins = Spider_Test(StrategyIns.StrategyID)
    ResultPack = Spider_Test_Ins.crawl(StrategyIns, TaskIns)
    print ResultPack[0].get_json()
    
    
    
    
    