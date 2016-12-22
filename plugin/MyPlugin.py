#-*- coding: UTF-8 -*- 
from DefPlugin import DefPlugin

class myplugin(DefPlugin):
    """
    """
    def __init__(self):
        #DefPlugin.__init__(self)
        pass
    
    def create(self,jdata,plogger):
        #log data
        
        print "my plugin:"+jdata
        pass
        return jdata
    def delete(self,jdata,plogger):
        #log data
        print "my plugin:"+jdata
        pass
    
    def modify(self,jdata,plogger):
        #log data
        print "my plugin:"+jdata
        pass





  