# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
'''manage queues'''
import global_vars.global_config as GlobalConfig
import global_vars.global_queues as GlobalQueues
import global_vars.global_dicts as GlobalDicts
from threading import Thread
from utils.decorators import Singleton
from Queue import Queue
from log.log import get_logger
from http.server_interact import get_task, get_strategy
from data_structure.task import Task
from data_structure.strategy import Strategy
from time import sleep
import json


@Singleton
class Scheduler():
    def __init__(self, logger = None):
        self.logger = logger or get_logger('Scheduler', True) # try to get logger from engine
        
        self.StrategySpiderMap_dict = GlobalConfig.StrategySpiderMap_dict
        self.SpiderThreads_dict = GlobalDicts.SpiderThreads_dict
        
        self.globalize_queues()
        self.globalize_strategygroup()
        self.load_strategies()
                

                
        
    def globalize_strategygroup(self):
        self.logger.info('globalize strategygroup START: StrategyGroup_dict')
        self.StrategyGroup_dict = {}
        
        GlobalDicts.StrategyGroup_dict = self.StrategyGroup_dict # strategies will be reloaded simultaneously
        self.logger.info('globalize strategygroup END: global %s'%str(GlobalDicts.StrategyGroup_dict))
        
    def start_queues(self):
        self.logger.info('start queues START: UploadResults_queue & StrategyTask_queue s for %s'%str(self.StrategySpiderMap_dict.keys()))
        self.StrategyTaskQueue_dict ={}
        for StrategyID in self.StrategySpiderMap_dict:
            self.StrategyTaskQueue_dict[StrategyID] = Queue() # {StrategyID_1 : strategy_task_queue_1, ... }

        self.UploadResults_queue = Queue()
        # self.UploadStatus_queue = Queue() # status sent simultaneously do not use queue?
        self.logger.info('start queues END: UploadResults_queue & StrategyTaskQueue_dict')
        
    def globalize_queues(self):
    # add queues into global_queues
        self.logger.info('globalize queues START: UploadResults_queue & StrategyTaskQueue_dict')
        self.start_queues()
        
        GlobalQueues.StrategyTaskQueue_dict = self.StrategyTaskQueue_dict
        GlobalQueues.UploadResults_queue = self.UploadResults_queue
        self.logger.info('globalize queues END: global %s & %s'%(str(GlobalQueues.UploadResults_queue),str(GlobalQueues.StrategyTaskQueue_dict)))
        

        
        
    def load_strategies(self):
    # {StrategyID : StrategyIns, ...}
        self.logger.info('load strategies START')

        StrategyGroupJson = get_strategy(self.logger) # TEST, there to set the TEST_1 strategy
        if StrategyGroupJson: # when no Strategies got, get_strategy returns '', do not update the StrategyGroup_dict
            StrategyJsonGroup_dict = json.loads(StrategyGroupJson)
            
            for StrategyID in StrategyJsonGroup_dict:
                StrategyJson = StrategyJsonGroup_dict[StrategyID]
                self.StrategyGroup_dict[StrategyID] = Strategy.load_Strategy(StrategyJson)

                
        self.logger.info('load strategies END, includes %s'%str(self.StrategyGroup_dict.keys()))
        
    def update_strategies(self):
        
        while True:
            UpdatestrategiesTimeinterval = GlobalConfig.BasicParameters_dict['updatestrategies_timeinterval']
            sleep(UpdatestrategiesTimeinterval)
            self.logger.info('---update strategies START, time interval: %s'%str(UpdatestrategiesTimeinterval))
            
            self.load_strategies()

            
            self.logger.info('---update strategies END')
        


    '''get new tasks'''
    def enqueue_tasks(self, TaskGroup_dict): # TasksGroupJson received in engine and loaded into dictionary
        self.logger.info('enqueue tasks START: %s'%str(TaskGroup_dict.keys()))
        for TaskIns in TaskGroup_dict.values():
            self.StrategyTaskQueue_dict[TaskIns.StrategyID].put(TaskIns) # use the TaskIns.StrategyID to get TaskID, to avoid the vartype of TaskGroup_dict.keys
        self.logger.info('enqueue tasks END: %s'%str(TaskGroup_dict.keys()))

    def next_tasks(self):

        TaskQueueThreshold = GlobalConfig.BasicParameters_dict['taskqueue_threshold'] # default value is set in basic_config
        TasksBatchSize = GlobalConfig.BasicParameters_dict['tasks_batchsize'] # this param will be sent to the server
        NexttaskTimeinterval = GlobalConfig.BasicParameters_dict['nexttask_timeinterval']
        
        while True:
            self.logger.info('next tasks START: check queues for %s, minimum queue length: %s, tasks amount: %s'%(\
                            str(self.StrategyTaskQueue_dict.keys()), str(TaskQueueThreshold), str(TasksBatchSize) ))
            
            for StrategyID in self.StrategyTaskQueue_dict:
                TaskGroup_dict = {}  # {TaskID : TaskIns, ...}
                            
                if self.StrategyTaskQueue_dict[StrategyID].qsize() <= TaskQueueThreshold: # threshold
                    self.logger.info('strategy %s need new tasks'%str(StrategyID))
                    TaskGroupJson = get_task(StrategyID, TasksBatchSize, self.logger)
                    if TaskGroupJson: # when no new tasks get None
                        TaskJsonGroup_dict = json.loads(TaskGroupJson) # {TaskID : TaskJson, ...}
                        
                        for TaskID in TaskJsonGroup_dict:
                            TaskJson = TaskJsonGroup_dict[TaskID]
                            TaskGroup_dict[TaskID] = Task.load_task(TaskJson) # {TaskID : TaskIns, ...}
                        
                        self.enqueue_tasks(TaskGroup_dict) 
                        
            self.logger.info('next tasks END: check queues for %s, wait for %s'%( str(self.StrategyTaskQueue_dict.keys()), str(5) ))
            sleep(NexttaskTimeinterval) 

            
    def start_next_tasks_thread(self):
    # checking task_queues, asking for next batches of tasks
        self.logger.info('--start next tasks thread--')
        NextTasks_thread = Thread(target = self.next_tasks)
        NextTasks_thread.start()
        
    def start_update_strategies_thread(self):
    # update strategies each 5 minutes
        self.logger.info('--start update strategies thread--')
        UpdateStrategies_thread = Thread(target = self.update_strategies)
        UpdateStrategies_thread.start()
        
    def start_threads(self):
    # entrence
        self.start_next_tasks_thread()
        self.start_update_strategies_thread() # the initial strategies is loaded when instantiate the Scheduler





if __name__ == '__main__':
# start server_service firstly
    
    SchedulerIns = Scheduler()
    SchedulerIns.start_threads()
    
    from core.monitor import Monitor
    MonitorIns = Monitor()
    MonitorIns.start_threads()
     
    from core.downloader import Downloader
    DownloaderIns = Downloader()
    DownloaderIns.start_threads() 
    
    from core.uploader import Uploader
    UploaderIns = Uploader()
    UploaderIns.start_threads()
    
    while True:
        sleep(10)
        print GlobalQueues.UploadResults_queue.qsize()
        
        