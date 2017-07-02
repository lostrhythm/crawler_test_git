# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
import os


class Crawler():
    def __init__(self):
        os.chdir('./global_vars')
        from core.engine import Engine
        os.chdir('..')
        self.engine = Engine()
        
    def _start_engine(self):
        self.engine.start()
        
    def _stop_engine(self):
        self.engine.stop()
        
    def crawl(self): # entrance method
        self._start_engine()
        
    def stop(self):
        self._stop_engine()
        
if __name__ == '__main__':
    Crawler().crawl()
    