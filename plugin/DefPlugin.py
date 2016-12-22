#-*- coding: UTF-8 -*- 
import os,time
class DefPlugin:
    
    def __init__(self,logger,log_file):
        """
        插件的父类
        """
        self.logger = logger
        self.log_file = log_file
        pass
    
    def create(self,jdata):
        #log data
        """
        监听文件/文件夹添加接口：
            添加文件/文件夹时记录日志
        """
        self.logger.info(jdata) 
            
    def delete(self,jdata):
        #log data
        """
        监听文件/文件夹删除接口：
            删除文件/文件夹时记录日志
        """
        self.logger.info(jdata) 
        
    def modify(self,jdata):
        #log data
        """
        监听文件/文件夹修改接口：
            修改文件/文件夹时记录日志
        """
        self.logger.info(jdata) 
        