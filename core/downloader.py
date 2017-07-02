# -*- coding:utf-8 -*-
'''
Created on 2017年6月21日

@author: Thinkpad
'''
import global_vars.global_config as GlobalConfig
import global_vars.global_queues as GlobalQueues
import global_vars.global_dicts as GlobalDicts
import importlib
from log.log import get_logger
from threading import Thread



class Downloader():
    def __init__(self, logger = None):
        self.logger = logger or get_logger('Downloader', True)
        
        self.StrategySpiderMap_dict = GlobalConfig.StrategySpiderMap_dict # GlobalConfig
        self.StrategyTaskQueue_dict = GlobalQueues.StrategyTaskQueue_dict # GlobalQueues
        self.UploadResults_queue = GlobalQueues.UploadResults_queue
        self.StrategyGroup_dict = GlobalDicts.StrategyGroup_dict # GlobalDicts
        
        self.globalize_spiderthreads() # GlobalDicts
        
        
        
        
    def globalize_spiderthreads(self):
        self.logger.info('globalize spiderthreads START')
        self.SpiderThreads_dict = {} # {StrategyID_1 : thread_1}, StrategyID_1 is corresponding to spiders
        GlobalDicts.SpiderThreads_dict = self.SpiderThreads_dict
        self.logger.info('globalize spiderthreads END')
        
        
        
        
    def process_task(self, StrategyID):
    # corresponding to StrategyID/ spider_ins
    # working in each thread, keep alive to get tasks from task_queue
        self.logger.info('---process task START, strategy: %s'%str(StrategyID))
        SpiderClsName = self.StrategySpiderMap_dict[StrategyID]
        SpiderMoudleName = SpiderClsName.lower() # class name -> moudle name
        SpiderCls = getattr(importlib.import_module('spider_plugins.' + SpiderMoudleName), SpiderClsName)
        SpiderIns = SpiderCls(StrategyID)
        SpiderCrawl_method = SpiderIns.crawl
        
        TaskQueue = self.StrategyTaskQueue_dict[StrategyID]

        
        while TaskQueue:
            TaskIns = TaskQueue.get() 
            self.logger.info('get TaskIns from TaskQueue TaskID: %s'%str(TaskIns.TaskID))
            StrategyIns = self.StrategyGroup_dict.get(StrategyID)

            result_pack = SpiderCrawl_method(StrategyIns, TaskIns) # compress conduct in uploader
            
            self.UploadResults_queue.put(result_pack)
            self.logger.info('put TaskIns into UploadResults_queue: %s'%str(TaskIns.TaskID))
      

    def start_spider_threads(self):
        self.logger.info('--start spider threads')
        for StrategyID in self.StrategySpiderMap_dict: # create threads based on local configs instead of all strategies
            self.SpiderThreads_dict[StrategyID] = Thread(target = self.process_task, args = (StrategyID,))

        [thread.start() for thread in self.SpiderThreads_dict.values()]
    
    def start_threads(self):
    # entrance
        self.start_spider_threads() # corresponding to strategyIDs, processing tasks
        
        
        
        
if __name__ == '__main__':
    # start the mock server and scheduler firstly
    DownloaderIns = Downloader()
    DownloaderIns.start_threads()
