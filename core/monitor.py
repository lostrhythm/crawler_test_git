# -*- coding:utf-8 -*-
'''
Created on 2017年6月21日

@author: Thinkpad
'''
import global_vars.global_config as GlobalConfig
import global_vars.global_dicts as GlobalDicts
from data_structure.status import MachineStatus, StrategyStatus
from http.server_interact import upload_status
from log.log import get_logger
from threading import Thread
from time import sleep

'''upload status'''
class Monitor():
    def __init__(self, logger = None):
        self.logger = logger or get_logger('Monitor', True) # try to get logger from engine
        
        self.StrategySpiderMap_dict = GlobalConfig.StrategySpiderMap_dict # will be used in spider plugin s
        
        self.globalize_strategystatus()
        
        
    def start_status(self):
        self.logger.info('start status START')
        user = GlobalConfig.Deploy_dict['user']
        self.MachineStatusIns = MachineStatus(user)
        self.StrategyStatus_dict = {} # {StrategyID : StrategyStatusIns}
        
        for StrategyID in self.StrategySpiderMap_dict:
            self.StrategyStatus_dict[StrategyID] = StrategyStatus(self.MachineStatusIns, StrategyID)
            
        self.logger.info('start status END: %s'%str(self.StrategyStatus_dict.keys()))
        
        
    def globalize_strategystatus(self):
        self.logger.info('globalize status START')
        self.start_status()
        GlobalDicts.StrategyStatus_dict = self.StrategyStatus_dict
        
        self.logger.info('globalize status END: %s'%str(GlobalDicts.StrategyStatus_dict))
        
        
    def upload_status(self):
        while True:
            UploadstatusTimeinterval = GlobalConfig.BasicParameters_dict['uploadstatus_timeinterval']
            sleep(UploadstatusTimeinterval)
            
            user = self.MachineStatusIns.get_user()
            MachineStatusCollector_dict = self.MachineStatusIns.machine_status_collector()
            self.logger.info('---upload status START, time interval: %s'%str(UploadstatusTimeinterval))

            self.logger.info('upload status START: %s'%str(self.MachineStatusIns.get_json()))
            upload_status(user, MachineStatusCollector_dict, self.logger)
            self.logger.info('upload status END')
            
            self.logger.info('restart StrategyStatusCollectors')
            for StrategyID in self.StrategyStatus_dict:
                StrategyStatusIns = self.StrategyStatus_dict[StrategyID]
                StrategyStatusIns.start_collector()
                
            
        
        
    def start_upload_thread(self):
        self.logger.info('--start upload status thread--')
        Upload_thread = Thread(target = self.upload_status)
        Upload_thread.start()
    
    def start_threads(self):
        self.start_upload_thread()
    
    
    
if __name__ == '__main__':
# start server_service firstly
    MonitorIns = Monitor()
    MonitorIns.start_threads()
    
    