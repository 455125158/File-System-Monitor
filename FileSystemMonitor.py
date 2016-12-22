#-*- coding: UTF-8 -*- 
import sys,os
import time,thread
import logging,re,getopt
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler
import time,logging
from SysUtils import ConfigUtil,CmdParamsProcess,PluginManager,LogUtil
sys.path.append(os.getcwd()+"/plugin")
from DefPlugin import DefPlugin
class FileEventHandler(FileSystemEventHandler):
    def __init__(self,mpath,plugin_path,logger,log_file,objClass):
        """
        初始化类的方法
        参数：
            plugin_path    为插件路径。
            log_file    为log文件路径
            log_flag    为日志开关
        """
        self.logger = logger
        FileSystemEventHandler.__init__(self)
        self.plugin_path =  plugin_path
        self.pmanager=PluginManager(plugin_path,logger,log_file)
        #获取插件实例
        self.plugins = self.pmanager.getPlugins(objClass)
        self.log_file=log_file
        self.mpath=mpath
        self.objClass = objClass
        
    def on_moved(self, event):
        """
        文件移动接口：
            监听目录范围内移动文件、重命名文件时的流程为：先删除在添加
        """
        t_str = time.strftime('%Y%m%d%H%M%S')
        try :
            ###这里要处理
            del_rdata= None
            del_rdata_err=None
            add_rdata= None
            add_rdata_err=None
            if event.is_directory:
                #print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
                del_rdata= "{'opertion':'move','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'delete','status':'info','mpath':'"+self.mpath+"'}"
                del_rdata_err="{'opertion':'move','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'delete','status':'error','mpath':'"+self.mpath+"'}"
                add_rdata= "{'opertion':'move','time':'"+t_str+"','dtype':'dir','data':'"+event.dest_path+"','response':'add','mpath':'"+self.mpath+"'}"
                add_rdata_err= "{'opertion':'move','time':'"+t_str+"','dtype':'dir','data':'"+event.dest_path+"','response':'add','status':'error','mpath':'"+self.mpath+"'}"
            else:
                #print("file moved from {0} to {1}".format(event.src_path,event.dest_path))
                del_rdata= "{'opertion':'move','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'delete','status':'info','mpath':'"+self.mpath+"'}"
                del_rdata_err= "{'opertion':'move','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'delete','status':'error','mpath':'"+self.mpath+"'}"
                add_rdata= "{'opertion':'move','time':'"+t_str+"','dtype':'file','data':'"+event.dest_path+"','response':'add','status':'info','mpath':'"+self.mpath+"'}"
                add_rdata_err= "{'opertion':'move','time':'"+t_str+"','dtype':'file','data':'"+event.dest_path+"','response':'add','status':'error','mpath':'"+self.mpath+"'}"
                
            #按照plugin业务处理数据
            for plugin in self.plugins:
                try:
                    thread.start_new_thread(plugin.delete,(del_rdata,self.logger,))
                except Exception,e:
                    self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_moved' ,'errors':'" +str(e)+"'}")
                    self.logger.error(del_rdata_err)
                try:
                    thread.start_new_thread(plugin.create,(add_rdata,self.logger,))
                except:
                    self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_moved' ,'errors':'" +str(e)+"'}")
                    self.logger.error(add_rdata_err) 
            #使用默认的插件打印处理日志
            dplugin = self.objClass(self.logger,self.log_file) 
            thread.start_new_thread(dplugin.delete,(del_rdata,))
            thread.start_new_thread(dplugin.create,(add_rdata,))
        except Exception,e  :
            self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_moved' ,'errors':'" +str(e)+"'}")
    def on_created(self, event):
        """
        文件添加：
            监听目录范围内写入文件事件
        """
        t_str = time.strftime('%Y%m%d%H%M%S')
        try :
            ###这里要处理
            add_rdata= None
            add_rdata_err= None
            if event.is_directory:
                #print("directory created:{0}".format(event.src_path))
                add_rdata=      "{'opertion':'create','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'add','status':'info','mpath':'"+self.mpath+"'}"
                add_rdata_err=  "{'opertion':'create','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'add','status':'error','mpath':'"+self.mpath+"'}"
            else:
    #             print("file created:{0}".format(event.src_path))
                add_rdata=      "{'opertion':'create','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'add','status':'info','mpath':'"+self.mpath+"'}"
                add_rdata_err=  "{'opertion':'create','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'add','status':'error','mpath':'"+self.mpath+"'}"
                
            for plugin in self.plugins:
                try:
                    thread.start_new_thread(plugin.create,(add_rdata,self.logger,))
                except Exception ,e :
                    self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_created' ,'errors':'" +str(e)+"'}")
                    self.logger.error(add_rdata_err) 
            #使用默认的插件打印处理日志
            dplugin = self.objClass(self.logger,self.log_file) 
            thread.start_new_thread(dplugin.create,(add_rdata,))
        except Exception,e  :
            self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_created' ,'errors':'" +str(e)+"'}")
            
    def on_deleted(self, event):
        """
        文件删除：
            监听目录范围内删除文件事件
        """
        t_str = time.strftime('%Y%m%d%H%M%S')
        try:
            ###这里要处理
            del_rdata= None
            del_rdata_err=None
            if event.is_directory:
                #print("directory deleted:{0}".format(event.src_path))
                del_rdata=      "{'opertion':'delete','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'delete','status':'info','mpath':'"+self.mpath+"'}"
                del_rdata_err=  "{'opertion':'delete','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'delete','status':'error','mpath':'"+self.mpath+"'}"
            else:
                #print("file deleted:{0}".format(event.src_path))
                del_rdata=      "{'opertion':'delete','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'delete','status':'info','mpath':'"+self.mpath+"'}"
                del_rdata_err=  "{'opertion':'delete','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'delete','status':'error','mpath':'"+self.mpath+"'}"
            
            for plugin in self.plugins:
                try:
                    thread.start_new_thread(plugin.delete,(del_rdata,self.logger,))
                except Exception,e:
                    self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_deleted' ,'errors':'" +str(e)+"'}")
                    self.logger.error(del_rdata_err)
            #使用默认的插件打印处理日志
            dplugin = self.objClass(self.logger,self.log_file) 
            thread.start_new_thread(dplugin.delete,(del_rdata,))
        except Exception,e  :
            self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_deleted' ,'errors':'" +str(e)+"'}")     
    def on_modified(self, event):
        """
        文件内容变更：
            监听目录范围内删除文件事件
        """
        t_str = time.strftime('%Y%m%d%H%M%S')
        try :
            mod_rdata = None
            mod_rdata_err=None
            if event.is_directory:
                #print("directory modified:{0}".format(event.src_path))
                mod_rdata =     "{'opertion':'modify','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'modify','status':'info','mpath':'"+self.mpath+"'}"
                mod_rdata_err = "{'opertion':'modify','time':'"+t_str+"','dtype':'dir','data':'"+event.src_path+"','response':'modify','status':'error','mpath':'"+self.mpath+"'}"
            else:
                #print("file modified:{0}".format(event.src_path))
                mod_rdata =     "{'opertion':'modify','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'modify','status':'info','mpath':'"+self.mpath+"'}"
                mod_rdata_err = "{'opertion':'modify','time':'"+t_str+"','dtype':'file','data':'"+event.src_path+"','response':'modify','status':'error','mpath':'"+self.mpath+"'}"
            
            for plugin in self.plugins:
                try:
                    thread.start_new_thread(plugin.modify,(mod_rdata,self.logger,))
                except Exception,e :
                    self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_modified' ,'errors':'" +str(e)+"'}")
                    self.logger.error(mod_rdata_err) 
            #使用默认的插件打印处理日志
            dplugin = self.objClass(self.logger,self.log_file) 
            thread.start_new_thread(dplugin.modify,(mod_rdata,))
        except Exception,e  :
            self.logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'FileEventHandler','method':'on_modified' ,'errors':'" +str(e)+"'}")     
            
def startMonitor(mpath,plugin_path,logger,log_file,objClass):
    """
    开启监听：
        mpath，监听目录
        plugin_path,插件目录
        log_file,日志文件路径
        objClass，插件父类
    
    """
    t_str = time.strftime('%Y%m%d%H%M%S')
    logger.info("service  is started !!!!")
    try :
        observer = Observer()
        event_handler = FileEventHandler(mpath,plugin_path,logger,log_file,objClass)
        observer.schedule(event_handler,mpath,True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt,e:
            observer.stop()
            logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'None','method':'startMonitor' ,'errors':'" +str(e)+"'}")     
        observer.join()
    except Exception,e :
        logger.error("{'time':'"+t_str+"','module':'FileSystemMonitor','class':'None','method':'startMonitor' ,'errors':'" +str(e)+"'}")
        
if __name__ == "__main__":
    
    cmd = CmdParamsProcess(sys.argv)
    config_path , log_flag = cmd.getParams()
    if config_path == None :
        print "无效的配置文件。"
    else :
        config = ConfigUtil(config_path)
        
        #日志文件名
        logName=config.get_log_file_name()
        
        plogName = logName +".plugin"
        
        logPath = config.get_log_file_path()
        if os.path.exists(logPath) == False :
            os.makedirs(logPath)
        log_file = logPath + "/" + logName;
        log = LogUtil(log_file,log_flag)
        logger = log.getLoger()
        #插件路径
        plugin_path = os.getcwd()+"/plugin/"
        #监听路径
        monitor_path=config.get_monitor_path()
        
        
        if monitor_path != None :
            startMonitor(monitor_path,plugin_path,logger,log_file,DefPlugin)
        else :
            logger.error("monitor_path is null  | not dir  and so on！！！！")
        