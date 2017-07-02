# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
'''parent class of spider spider_plugins'''
from time import sleep
from http.http_methods import http_get, http_post
from data_structure.status import TaskStatus
import global_vars.global_dicts as GlobalDicts
import global_vars.global_config as GlobalConfig
import traceback

class Spider(object):
    def __init__(self):
        self.StrategyStatus_dict = {} # {StrategyID : StrategyStatusCollector}
        self.TasktypeCrawlMethodMap_dict = {} # {0 : 'plain_crawl', 1 : 'deep_crawl'}
        self.LocalEncoding = 'utf-8' # LocalEncoding, of encoding page
        
        self.StrategyID = 'TEST'
        self.Encoding = 'utf-8' # website encoding, for decoding page
        self.Timeout = 10
        self.RetryTime = 3
        self.WaitTime = 1,
        self.AdditionParams = {}
        self.FragmentalUpload = False
        self.FragmentalAmount = 5
        self.ContentException = []
        self.StrategyStatusIns = None # gotten from the GlobalDicts.StrategyStatus_dict
        self.TaskStatusIns = None # instantiate along with each invoke of spider.crawl
        self.CookieUse = False
        
        
        
    def plain_crawl(self, TaskIns, Fast = False):
        pass
    
    def deep_crawl(self, TaskIns, Fast = False):
        pass
    
    
    
    
    def _content_exception_catch(self, response):
    # catch the content exception in non-exception http response
        ExceptionExistingSign = False
        for Excp in self.ContentException:
            if Excp in response:
                ExceptionExistingSign = True
                break
        return ExceptionExistingSign # True or False
    
    
    def http_get(self, url = '', headers = {}, timeout = None, retrytime = None, waittime = None, encoding = None, cookieuse = None):
        self.logger.info('http_get Crawling Page START: %s'%url)
        self.StrategyStatusIns.req_cnt_inc() # req +1
        self.TaskStatusIns.req_cnt_inc()
        
        for i in xrange(retrytime or self.RetryTime):
            self.logger.info('http_get request url %s for the %s time'%(url, str(i+1)))
            try:
                rawresp, respheaders = http_get(url, headers, cookieuse or self.CookieUse, timeout or self.Timeout) # catch http exceptions
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
                response = 'http_get Crawling Page Failed'
            else:
                
                if respheaders.has_key('Content-Type') and 'charset=' in respheaders['Content-Type']: # type to get encoding type automatically from response headers
                    if '=utf-8' in respheaders['Content-Type'] or '=UTF-8' in respheaders['Content-Type']:
                        response = rawresp.decode('utf-8').encode(self.LocalEncoding)
                    elif '=gbk' in respheaders['Content-Type'] or '=GBK' in respheaders['Content-Type']:
                        response = rawresp.decode('gbk').encode(self.LocalEncoding)
                    else:
                        response = rawresp.decode(encoding or self.Encoding).encode(self.LocalEncoding)
                else:
                    response = rawresp.decode(encoding or self.Encoding).encode(self.LocalEncoding)
                    
                ExceptionExistingSign = self._content_exception_catch(response) # catch custom exceptions
                if ExceptionExistingSign == True:
                    self.logger.info('http_get content exceptions occur: %s'%url)
                    response = 'http_get Crawling Page Failed'
                else:
                    break
            finally:
                sleep(waittime or self.WaitTime)
    
        if response == 'Crawling Page Failed':
            self.logger.info('http_get Crawling Page FAILED: %s'%url)
            self.StrategyStatusIns.req_failed_inc() # req failed +1
            self.TaskStatusIns.req_failed_inc()
            response = ''
        else:
            self.logger.info('http_get Crawling Page END: %s'%url)
            self.StrategyStatusIns.req_success_inc() # req success +1
            self.TaskStatusIns.req_success_inc()
        return response
    
    
    def http_post(self, url = '', params = {}, headers = {}, serialization = 'Json', timeout = None, retrytime = None, waittime = None, encoding = None, cookieuse = None):
    # in spider.crawl_method prepare the params with the web accepting encoding method firstly
        self.logger.info('http_post Crawling Page START: %s'%url)
        self.StrategyStatusIns.req_cnt_inc() # req +1
        self.TaskStatusIns.req_cnt_inc()
        
        for i in xrange(retrytime or self.RetryTime):
            self.logger.info('http_post request url %s for the %s time'%(url, str(i+1)))
            try:
                rawresp, respheaders = http_post(url, params, headers, serialization, cookieuse or self.CookieUse, timeout or self.Timeout) # catch http exceptions
                sleep(waittime or self.WaitTime)
            except Exception as e:
                self.logger.warn(traceback.format_exc(e))
                response = 'http_post Crawling Page Failed'
            else:

                if respheaders.has_key('Content-Type') and 'charset=' in respheaders['Content-Type']: # type to get encoding type automatically from response headers
                    if '=utf-8' in respheaders['Content-Type'] or '=UTF-8' in respheaders['Content-Type']:
                        response = rawresp.decode('utf-8').encode(self.LocalEncoding)
                    elif '=gbk' in respheaders['Content-Type'] or '=GBK' in respheaders['Content-Type']:
                        response = rawresp.decode('gbk').encode(self.LocalEncoding)
                    else:
                        response = rawresp.decode(encoding or self.Encoding).encode(self.LocalEncoding)
                else:
                    response = rawresp.decode(encoding or self.Encoding).encode(self.LocalEncoding)
                    
                ExceptionExistingSign = self._content_exception_catch(response) # catch custom exceptions
                if ExceptionExistingSign == True:
                    self.logger.info('http_post content exceptions occur %s'%url)
                    response = 'http_post Crawling Page Failed'
                else:
                    break
                
            finally:
                sleep(waittime or self.WaitTime)
    
        if response == 'http_post Crawling Page Failed':
            self.logger.info('http_post Crawling Page FAILED: %s'%url)
            self.StrategyStatusIns.req_failed_inc() # req failed +1
            self.TaskStatusIns.req_failed_inc()
            response = ''
        else:
            self.logger.info('http_post Crawling Page END: %s'%url)
            self.StrategyStatusIns.req_success_inc() # req success +1
            self.TaskStatusIns.req_success_inc()
        return response
    
    
    
    
    def _deduce_task_status(self, TaskIns):
    # deduce the task status based on TaskStatusCollector
        TaskStatusCollector = self.TaskStatusIns.task_status_collector()
        if TaskStatusCollector['req_success'] == TaskStatusCollector['req_cnt']: # including 0 == 0 not conducting the requests
            TaskIns.TaskStatus = 1 # success
        elif TaskStatusCollector['req_success'] == 0:
            TaskIns.TaskStatus = 0 # fail
        else:
            TaskIns.TaskStatus = 2 # partial success

        self.logger.info('Task Status: %s, %s'%(str(TaskIns.TaskStatus), str(TaskStatusCollector)))

    
    
    def _update_local_strategy(self, StrategyIns, TaskIns): # resolve the parameters from StrategyIns
        self.logger.info('---using strategy: %s'%str(StrategyIns.__dict__))
        
        self.StrategyStatus_dict = GlobalDicts.StrategyStatus_dict
        self.TasktypeCrawlMethodMap_dict = GlobalConfig.TasktypeCrawlMethodMap_dict
        self.LocalEncoding = GlobalConfig.BasicParameters_dict['local_encoding']
        
        self.StrategyID = StrategyIns.StrategyID
        self.Encoding = TaskIns.Encoding or StrategyIns.Encoding or self.LocalEncoding # TaskIns.Encoding has the biggest priority
        self.Timeout = StrategyIns.Timeout
        self.WaitTime = StrategyIns.WaitTime # http requests time interval
        self.RetryTime = StrategyIns.RetryTime
        self.AdditionParams = StrategyIns.AdditionParams
        self.FragmentalUpload = StrategyIns.FragmentalUpload
        self.FragmentalAmount = StrategyIns.FragmentalAmount
        self.ContentException = StrategyIns.ContentException
        self.CookieUse = StrategyIns.CookieUse
        
        self.StrategyStatusIns = self.StrategyStatus_dict[self.StrategyID]
        self.TaskStatusIns = TaskStatus(self.StrategyID)
        
        
    def crawl(self, StrategyIns, TaskIns):
    # entrence
        self._update_local_strategy(StrategyIns, TaskIns)

        try:
            TaskType = TaskIns.TaskType
            TaskID = TaskIns.TaskID
            StrategyID = StrategyIns.StrategyID
            CrawlMethodName = self.TasktypeCrawlMethodMap_dict[TaskType]
            CrawlMethod = getattr(self, CrawlMethodName)
            
        except Exception as e:
            if 'KeyError' in str(e.__class__):
                self.logger.warn('invalid tasktype %s, TaskID %s, StrategyID %s'%(str(TaskType), str(TaskID) ,str(StrategyID)))
            elif 'AttributeError' in str(e.__class__):
                self.logger.warn('invalid crawl method name %s, not implemented'%(str(CrawlMethodName)))
            
            ResultPack = (TaskIns, {}) # if task not being processed, regard it as failed
            TaskIns.TaskStatus = 0
        else:
            ResultPack = CrawlMethod(TaskIns)
            self._deduce_task_status(TaskIns)
        

        return ResultPack
        
        
if __name__ == '__main__':
    print Spider().__dict__


