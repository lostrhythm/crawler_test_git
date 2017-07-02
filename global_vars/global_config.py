# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''

from utils.data_operations import tuplelist_to_dict, changecase_keys, integerize_values, integerize_keys
from ConfigParser import ConfigParser



# initial dicts
TCMMap_default = {}
SSMap_default = {}
BParams_default = {} # 'taskqueue_timeout' should not be used, if necessary thread shut down should be managed by update strategy
Deploy_default = {}


# load basic configurations
cfp_basic = ConfigParser()
cfp_basic.read('../global_vars/basic_config.conf')

_TasktypeCrawlMethodMap = cfp_basic.items('Tasktype_CrawlMethod_Map') # [(key, value), ...]
_BasicParameters = cfp_basic.items('Basic_Parameters')
_Deploy = cfp_basic.items('Deploy')


TCMMap_default.update(
                     integerize_keys(
                                     tuplelist_to_dict(_TasktypeCrawlMethodMap))) # {KEY:value, ...}
BParams_default.update(
                       integerize_values(
                                         tuplelist_to_dict(_BasicParameters)))
Deploy_default.update( 
                      tuplelist_to_dict(_Deploy)) 




# load custom configurations
cfp = ConfigParser()
cfp.read('../config.conf')

_StrategySpiderMap = cfp.items('Strategy_Spider_Map') # [(key, value), ...]
_BasicParameters = cfp.items('Basic_Parameters')
_Deploy = cfp.items('Deploy')

# update default dicts
SSMap_default.update(
                     changecase_keys(
                                     tuplelist_to_dict(_StrategySpiderMap))) # {KEY:value, ...}
BParams_default.update(
                       integerize_values(
                                         tuplelist_to_dict(_BasicParameters)))
Deploy_default.update( 
                      tuplelist_to_dict(_Deploy)) 





# get the new parameter dicts
TasktypeCrawlMethodMap_dict = TCMMap_default
StrategySpiderMap_dict = SSMap_default
BasicParameters_dict = BParams_default
Deploy_dict = Deploy_default



if __name__ == '__main__':
    print StrategySpiderMap_dict
    print BasicParameters_dict # {'taskqueue_threshold': 5, 'upload_batchsize': 10, 'tasks_batchsize': 10}
    print Deploy_dict
    
    print TasktypeCrawlMethodMap_dict
    
    
