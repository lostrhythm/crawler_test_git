# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
'''engine + crawler'''
import global_vars.global_config as GlobalConfig
from utils.decorators import Singleton
from core.scheduler import Scheduler 
from core.downloader import Downloader
from core.uploader import Uploader
from core.monitor import Monitor
from http.server_interact import do_register
from log.log import get_logger

@Singleton
class Engine():
    def __init__(self):
        self.logger = get_logger('Core', True) # core moudles share the same logger
        
        self.Scheduler = Scheduler(self.logger)
        self.Downloader = Downloader(self.logger)
        self.Uploader = Uploader(self.logger)
        self.Monitor = Monitor(self.logger)
        
    def _do_register(self):
        user = GlobalConfig.Deploy_dict['user']
        password = GlobalConfig.Deploy_dict['password']
        self.logger.info('registering START: %s'%user)
        RegisterSuccess = do_register(user, password, self.logger)
        self.logger.info('registering END: %s'%str(RegisterSuccess))
        return RegisterSuccess
    
    def start(self):
        if self._do_register():
            self.logger.info('---engine START---')
            
            self.Scheduler.start_threads()
            self.Monitor.start_threads()
            self.Downloader.start_threads() # Downloader uses spiders which uses Status, so Monitor should run in front
            self.Uploader.start_threads()

            
        else:
            self.logger.info('---engine START failed---')
        
    
    def stop(self):
        pass
    
if __name__ == '__main__':
    engie = Engine()
    engie.start()