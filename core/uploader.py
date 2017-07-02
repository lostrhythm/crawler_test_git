# -*- coding:utf-8 -*-
'''
Created on 2017年6月21日

@author: Thinkpad
'''
'''upload task results and status?'''
import global_vars.global_config as GlobalConfig
import global_vars.global_queues as GlobalQueues

from utils.data_operations import do_compress
from http.server_interact import upload_results

from log.log import get_logger
from threading import Thread

import traceback

class Uploader():
    def __init__(self, logger = None):
        self.logger = logger or get_logger('Uploader', True) # try to get logger from engine
        
        self.UploadResults_queue = GlobalQueues.UploadResults_queue


    def upload_results(self):
        UploadBatchSize = GlobalConfig.BasicParameters_dict['upload_batchsize']
        UploadQueueTimeout = GlobalConfig.BasicParameters_dict['uploadqueue_timeout']
        self.logger.info('---upload results START: UploadBatchSize %s, UploadQueueTimeout %s'%(str(UploadBatchSize), str(UploadQueueTimeout)))
        
        while True:
            UploadPack = {} 
            for _ in xrange(UploadBatchSize):
                try:
                    ResultPack = self.UploadResults_queue.get(timeout = UploadQueueTimeout) # this timeout is also the wait when queue idle
                except:
                    break
                else:    
                    # (TaskIns, {filename : content, ...}), TaskIns.TaskStatus
                    try:
                        ResultPack_zip_b64 = do_compress(ResultPack)
                    except Exception as e:
                        self.logger.warn(traceback.format_exc(e))
                        ResultPack_zip_b64 = ''
                        
                    TaskIns = ResultPack[0]
                    UploadPack[TaskIns.TaskID] = (TaskIns.TaskStatus, ResultPack_zip_b64)
                
            if UploadPack:
                self.logger.info('upload results START: %s'%str(UploadPack.keys()))
                upload_results(UploadPack, self.logger) # retry inside the upload_result function
                self.logger.info('upload results END')

    def start_upload_thread(self):
        self.logger.info('--start upload results thread--')
        Upload_thread = Thread(target = self.upload_results)
        Upload_thread.start()
        
    def start_threads(self):
        self.start_upload_thread()
        
        
        
if __name__ == '__main__':
# start server_service firstly

    from Queue import Queue
    GlobalQueues.UploadResults_queue = Queue()
    UploadResults_queue = GlobalQueues.UploadResults_queue

    from data_structure.task import Task
    TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 0, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
    TaskIns = Task.load_task(TaskJson)
    ResultPack_1 = (TaskIns, {'filename.jpg' : 'content', 'newtask.html' : 'new taskIns json s'})
    UploadResults_queue.put(ResultPack_1)

    TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 1, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
    TaskIns = Task.load_task(TaskJson)
    ResultPack_2 = (TaskIns, {'filename.jpg' : 'content', 'newtask.html' : 'new taskIns json s'})
    UploadResults_queue.put(ResultPack_2)

    TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 2, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
    TaskIns = Task.load_task(TaskJson)
    ResultPack_3 = (TaskIns, {'filename.jpg' : 'content', 'newtask.html' : 'new taskIns json s'})
    UploadResults_queue.put(ResultPack_3)


    UploaderIns = Uploader()
    UploaderIns.start_threads()
    
    
    
    
    
    
    
    
    
    
    
    