# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
'''
thesse methods are out of box methods, but can also use loggers, as these are not the really fundermental methods?
'''
import global_vars.global_config as GlobalConfig
from http.http_methods import http_get, http_post # really basic methods
from log.log import get_logger
import traceback


def get_strategy(logger = None): # invoked in scheduler
    strategy_server_url = 'http://%s'%GlobalConfig.Deploy_dict['strategy_server']
    InnerCommunicationRetry = GlobalConfig.BasicParameters_dict['innercommunication_retry']
    
    method_logger = logger
    method_logger.info('strategy_server: %s'%strategy_server_url)
    
    for i in xrange(InnerCommunicationRetry):
        try:
            method_logger.info('request for StrategyGroupJson for the %s time'%str(i+1))
            StrategyGroupJson, _ = http_get(strategy_server_url)
            
        except Exception as e:
            method_logger.warn(e)
            method_logger.info('request for StrategyGroupJson failed')
            StrategyGroupJson = '' # when exception happens in http_get, returns ''
        else:
            method_logger.info('get StrategyGroupJson: %s'%StrategyGroupJson)
            break
        
    return StrategyGroupJson # may be ""


def get_task(StrategyID, TasksBatchSize, logger = None): # invoked in scheduler

    task_server_url = 'http://%s'%GlobalConfig.Deploy_dict['task_server']
    InnerCommunicationRetry = GlobalConfig.BasicParameters_dict['innercommunication_retry']
    User = GlobalConfig.Deploy_dict['user'] # already register, do not need pw here
    params = {'strategy_id' : StrategyID, 'tasks_batchsize' : TasksBatchSize, 'user' : User}
    
    method_logger = logger
    method_logger.info('task_server: %s'%task_server_url)
    
    for i in xrange(InnerCommunicationRetry):
        try:
            method_logger.info('request for TaskGroupJson for the %s time'%str(i+1))
            TaskGroupJson, _ = http_post(task_server_url, params)
        except Exception as e:
            method_logger.warn(traceback.format_exc(e))
            method_logger.info('request for TaskGroupJson failed')
            TaskGroupJson = ''
        else:
            method_logger.info('get TaskGroupJson: %s'%TaskGroupJson)
            break
    
    return TaskGroupJson


def upload_results(UploadPack, logger = None):
# UploadPack : {TaskID : (TaskStatus, zipfile_md5), ...}
    upload_server_url = 'http://%s'%GlobalConfig.Deploy_dict['upload_server']
    InnerCommunicationRetry = GlobalConfig.BasicParameters_dict['innercommunication_retry']
    
    method_logger = logger
    method_logger.info('upload_server: %s'%upload_server_url)
    
    for i in xrange(InnerCommunicationRetry):
        try:
            method_logger.info('upload UploadPack for the %s time'%str(i+1))
            ComfirmInfo, _ = http_post(upload_server_url, UploadPack)
        except Exception as e:
            method_logger.warn(traceback.format_exc(e))
            method_logger.info('upload UploadPack failed')
            ComfirmInfo = ''
        else:
            method_logger.info('upload UploadPacK, get Confirmation: %s'%ComfirmInfo)
            break
    
    
    
def upload_results_fragment(logger, *args, **kws): # TODO: add a sign in additional params of tasks?
    method_logger = logger or get_logger('server_interact')
    pass
    
    
    
def upload_status(user, MachineStatusCollector_dict, logger = None):
    upload_status_url = 'http://%s'%GlobalConfig.Deploy_dict['monitor_server']
    InnerCommunicationRetry = GlobalConfig.BasicParameters_dict['innercommunication_retry']

    method_logger = logger
    method_logger.info('monitor_server: %s'%upload_status_url)
    
    UserCollectorMap = (user, MachineStatusCollector_dict)
    
    for i in xrange(InnerCommunicationRetry):
        try:
            method_logger.info('upload Status for the %s time'%str(i+1))
            ComfirmInfo, _ = http_post(upload_status_url, UserCollectorMap)
        except Exception as e:
            method_logger.warn(traceback.format_exc(e))
            method_logger.info('upload Status failed')
            ComfirmInfo = ''
        else:
            method_logger.info('upload Status, get Confirmation: %s'%ComfirmInfo)
            break



def do_register(user, password, logger = None):
    register_server_url = 'http://%s'%GlobalConfig.Deploy_dict['register_server']
    InnerCommunicationRetry = GlobalConfig.BasicParameters_dict['innercommunication_retry']
    
    method_logger = logger
    method_logger.info('register_server: %s'%register_server_url)
    
    UserInfo_dict = {'user' : user, 'password' : password}
    
    for i in xrange(InnerCommunicationRetry):
        try:
            method_logger.info('do registering for the %s time'%str(i+1))
            ComfirmInfo, _ = http_post(register_server_url, UserInfo_dict)
        except Exception as e:
            method_logger.warn(traceback.format_exc(e))
            method_logger.info('do registering failed')
            ComfirmInfo = ''
        else:
            method_logger.info('do registering, get Confirmation: %s'%ComfirmInfo)
            break
        
    if 'Success' in ComfirmInfo:
        RegisterSuccess = True
    else:
        RegisterSuccess = False
    
    return RegisterSuccess



def get_captcha(logger, *args, **kws):
    method_logger = logger or get_logger('server_interact')
    pass

def get_proxy(logger, *args, **kw):
    method_logger = logger or get_logger('server_interact')
    pass






if __name__ == '__main__':
    methods_shared_logger = get_logger('server_interact',True)
  
    get_strategy(methods_shared_logger)
    get_task('TEST_1', 10,methods_shared_logger)
    
    # UploadPack = {0 : ("TaskStatus", "zipfile_md5_task0"), 1 : ("TaskStatus", "zipfile_md5_task1")}
    UploadPack = {0 : ("TaskStatus", "emlwZmlsZV9tZDVfdGFzazA=")}
    ComfirmInfo = upload_results(UploadPack, methods_shared_logger)


 
    from data_structure.status import MachineStatus, StrategyStatus
    MachineStatusIns = MachineStatus()
    StrategyStatusIns = StrategyStatus(MachineStatusIns, 'TEST_1')
    StrategyStatusIns = StrategyStatus(MachineStatusIns, 'TEST_2')
      
    user = MachineStatusIns.get_user()
    MachineStatusCollector_dict = MachineStatusIns.machine_status_collector()
      
    upload_status(user, MachineStatusCollector_dict, methods_shared_logger)
 
 
 
    do_register('user', 123, methods_shared_logger)