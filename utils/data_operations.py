# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
from copy import deepcopy
import os
import zipfile
import shutil
import base64

def tuplelist_to_dict(tuplelist):
    new_dict = {}
    for tup in tuplelist:
        key = tup[0]
        value = tup[1]
        new_dict[key] = value
    return new_dict

def changecase_keys(OrigDict, AimCase = 'upper'):
    NewDict = {}
    if AimCase == 'upper': # {'a': 1, 'b': 2} -> {'A': 1, 'B': 2}
        for key in OrigDict:
            UpperKey = key.upper()
            NewDict[UpperKey] = OrigDict[key]
            
    if AimCase == 'lower': # {'a': 1, 'b': 2} -> {'A': 1, 'B': 2}
        for key in OrigDict:
            UpperKey = key.lower()
            NewDict[UpperKey] = OrigDict[key]
            
    return NewDict


def integerize_values(OrigDict):
    NewDict = deepcopy(OrigDict)
    
    for key in NewDict:
        try:
            NewDict[key] = int(NewDict[key])
        except:
            pass
    
    return NewDict
        
        
def integerize_keys(OrigDict):
    NewDict = {}
    
    for key in OrigDict:
        try:
            NewDict[int(key)] = OrigDict[key]
        except:
            pass
    
    return NewDict
        
        
def do_compress(ResultPack): # ResultPack : (TaskIns, {'filename.jpg' : 'content', 'newtask.html' : 'new taskIns json s'})
    TaskIns = ResultPack[0]
    ResultFiles_dict = ResultPack[1]
    
    # write files in ResultPack to local directory
    ResultPack_dirpath = './%s'%str(TaskIns.TaskID)
    if not os.path.isdir(ResultPack_dirpath):
        os.mkdir(ResultPack_dirpath)
    
    for filename in ResultFiles_dict:
        filepath = ResultPack_dirpath + '/' + filename
        filecontent = ResultFiles_dict[filename]
        
        if '.html' in filename or '.json' in filename: # the string files
            with open(filepath, 'w') as f:
                f.write(filecontent)
        else:
            with open(filepath, 'wb') as f:
                f.write(filecontent)
            
    # compress the directory and delete local uncompressed files
    # SOURCE: http://blog.csdn.net/b_h_l/article/details/9406675
    zipfilepath = ResultPack_dirpath + '.zip'
    zf = zipfile.ZipFile(zipfilepath, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, _, filenames in os.walk(ResultPack_dirpath):
        for filename in filenames:
            zf.write(os.path.join(dirpath, filename)) # file -write-> zipfile
    zf.close()
    shutil.rmtree(ResultPack_dirpath)
    
    
    # load the zipfile into memeory and delete the local one
    with open(zipfilepath, 'rb') as zf:
        ResultPack_zip = zf.read()
    os.remove(zipfilepath)
    
    # do base64
    ResultPack_zip_b64 = base64.b64encode(ResultPack_zip)
    return ResultPack_zip_b64 # only the file content, file name has to been repaired in uploader
                          # finally, it is a string




if __name__ == '__main__':
#     tuplelist = [(1,2),(3,4)]
#     print tuplelist_to_dict(tuplelist)
#      
#     origd = {'a':1,'b':2}
#     newd = changecase_keys(origd)
#     print origd
#     print newd
#      
#     origd = {'A':1,'B':2}
#     newd = changecase_keys(origd, 'lower')
#     print origd
#     print newd
#      
#     origd = {'A':'1','B':'b','C':2}
#     newd = integerize_values(origd)
#     print origd
#     print newd

    origd = {'1':'A','2':'b','3':'c'}
    newd = integerize_keys(origd)
    print origd
    print repr(newd)
    print newd[1]
    
    
    from data_structure.task import Task
    TaskJson = '{"Encoding": "utf-8", "TaskStatus": 0, "TaskID": 0, "TaskType": 0, "StrategyID": "TEST", "AdditionParams": "{\\"a\\":2}", "TaskContent": ""}'
    TaskIns = Task.load_task(TaskJson)
    ResultPack = (TaskIns, {'filename.jpg' : 'content', 'newtask.html' : 'new taskIns json s'})
    ResultPack_zip_b64 = do_compress(ResultPack)
    print ResultPack_zip_b64
