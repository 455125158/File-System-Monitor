#-*- coding: UTF-8 -*- 
from DefPlugin import DefPlugin
import os
class myplugin(DefPlugin):
    
    """
    该插件可以定义多个，每个可以执行不同的业务。
    """
    def __init__(self):
        #DefPlugin.__init__(self)
        pass
    
    def create(self,jdata,plogger):
        """
        当用户在监听文件夹出现添加操作时将调用此方法，
        jdata, 操作描述的json串
            {'opertion':'move','time':'20161222142535','dtype':'file','data':'/home/lee/monitor/test1/a','response':'add','status':'info','mpath':'/home/lee/monitor/test1/'}
            解释：
            opertion:        用户在文件系统上做的操作，取值范围[move，delete,create,modify]
            time:            程序方法执行时的时间，
            dtype:           操作对象类型，取值范围[file,dir] ,file表示文件，dir表示目录
            response:        响应操作类型，取值范围[delete,add,modify],开发者处理数据时判断处理的依据。
            status:          操作状态，取值范围[info,error],info表示操作正常，error表示操作出现异常。
            mpath:           表示监听的目录。
            
        plogger,  日志对象（loggging),提供方法如下：
            plogger.debug(str)
            plogger.info(str)
            plogger.warn(str)
            plogger.error(str)
        
        """
        #log data
        
        print "my plugin:"+jdata
        pass
        return jdata
    def delete(self,jdata,plogger):
        """
        当用户在监听文件夹出现删除操作时将调用此方法，
        jdata, 操作描述的json串
            {'opertion':'move','time':'20161222142535','dtype':'file','data':'/home/lee/monitor/test1/a','response':'add','status':'info','mpath':'/home/lee/monitor/test1/'}
            解释：
            opertion:        用户在文件系统上做的操作，取值范围[move，delete,create,modify]
            time:            程序方法执行时的时间，
            dtype:           操作对象类型，取值范围[file,dir] ,file表示文件，dir表示目录
            response:        响应操作类型，取值范围[delete,add,modify],开发者处理数据时判断处理的依据。
            status:          操作状态，取值范围[info,error],info表示操作正常，error表示操作出现异常。
            mpath:           表示监听的目录。
            
        plogger,  日志对象（loggging),提供方法如下：
            plogger.debug(str)
            plogger.info(str)
            plogger.warn(str)
            plogger.error(str)
        
        """
        #log data
        print "my plugin:"+jdata
        """
        #用法1：
        try :
            os.system("curl  http(s)://xxxx?data="+jdata)
            解释：在linux系统下可以很方便的使用系统命令进行远程URL调用。
            也可以使用 urllib/urllib2模块进行http url  访问，同时还可以指定超时时间。
        
        except :
            plogger.debug("xxx  errro")
        """
        
        """
        #用法2
        try:
            #直接python编程，根据jdata进行直接更新数据库。
        ....
        """
        pass
    
    def modify(self,jdata,plogger):
        """
        当用户在监听文件夹出现修改操作时将调用此方法，
        jdata, 操作描述的json串
            {'opertion':'move','time':'20161222142535','dtype':'file','data':'/home/lee/monitor/test1/a','response':'add','status':'info','mpath':'/home/lee/monitor/test1/'}
            解释：
            opertion:        用户在文件系统上做的操作，取值范围[move，delete,create,modify]
            time:            程序方法执行时的时间，
            dtype:           操作对象类型，取值范围[file,dir] ,file表示文件，dir表示目录
            response:        响应操作类型，取值范围[delete,add,modify],开发者处理数据时判断处理的依据。
            status:          操作状态，取值范围[info,error],info表示操作正常，error表示操作出现异常。
            mpath:           表示监听的目录。
            
        plogger,  日志对象（loggging),提供方法如下：
            plogger.debug(str)
            plogger.info(str)
            plogger.warn(str)
            plogger.error(str)
        
        """
        #log data
        print "my plugin:"+jdata
        pass





  
