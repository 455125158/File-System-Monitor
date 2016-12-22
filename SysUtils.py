#-*- coding: UTF-8 -*- 

import os,sys,re,logging,getopt
import ConfigParser,time
from logging.handlers import TimedRotatingFileHandler
class FileUtil:
    
    def __init__(self,logger):
        self.logger=logger
        pass
    
    def getFilesByEndWith(self,path,str):
        """
        根据路径获取指定后缀的文件名列表。
            path，为文件目录
            str，为文件后缀
        """
        t_str = time.strftime('%Y%m%d%H%M%S')
        try :
            filenames = os.listdir(path)
            fnames = []
            for fname in filenames :
                if fname.endswith(str):
                    fnames.append(fname)
            return fnames
        except Exception,e :
            self.logger.error("{'time':'"+t_str+"','module':'SysUtil','class':'FileUtil','method':'getFilesByEndWith' ,'errors':'" +str(e)+"'}")
        
class CmdParamsProcess :
    
    def __init__(self,args):
        self.args = args
        
    def getParams(self) :
        """
        获取命令行参数
        返回值： 
        config_path , 为配置文件路径
        log_flag， 屏幕打印日志开关
        """
        config_path = None
        log_flag = "debug"
        t_str = time.strftime('%Y%m%d%H%M%S')
        try :
            opts,args =getopt.getopt(sys.argv[1:], "hc:p:", ["help","conf","printlog"])
            
            for option ,value in opts :
                if option in ['-h',"--help"]:
                    print """
                    
                    参数1 ： -h, 帮助提示
                    参数2 ： -c,--conf=, 配置文件绝对路径，不配置该参数，程序默认在程序根目录找"monitor.conf"文件，没有将报错。用法： -c /home/lee/monitor/monitor.conf
                    参数3 ： -p,--printlog=,打印log开关， 取值范围：debug/info/warn/error，目前只实现debug与非debug模式。
                    """
                    sys.exit(0)
                elif option in ["-c","--conf"] :
                    config_path = value
                elif option in ["-p","--printlog"] :
                    log_flag = value
                        
            if config_path != None :
                i0 = config_path[0]
                if i0 != "/" :
                    config_path = os.getcwd() + "/" + config_path
                else :
                    pass
                
            else :
                config_path= os.getcwd() + "/" + "monitor.conf"
            ## 根据配置文件路径判断其是否村在
            if os.path.exists(config_path) != True or os.path.isdir(config_path):
                config_path = None
                
            if log_flag.lower() in ["debug","info","warn","error"] :
                log_flag = "debug"
        except Exception,e:
            print "{'time':'"+t_str+"','module':'SysUtil','class':'CmdParamsProcess','method':'getParams' ,'errors':'" +str(e)+"'}"
        return config_path,log_flag
class ConfigUtil:
    
    def __init__(self,path):
#         self.logger = logger
#         try :
        config = ConfigParser.ConfigParser()
        config.read(path)
        self.log_file_name=config.get("info","log_file_name")
        self.log_file_path=config.get("info","log_file_path")
        #self.monitor_paths=config.get("info","monitor_paths")
        self.monitor_path=config.get("info","monitor_path")
#         except Exception ,e :
#             self.logger.error("module : SysUtil ,class : ConfigUtil,method : __init__-->" + str(e)) 
    def get_log_file_name(self): 
        return self.log_file_name
    def get_log_file_path(self):
        return self.log_file_path
    def get_monitor_path(self):
        #self.monitor_paths=[]
#         mpaths=[]
#         try :
#         if self.monitor_paths != None and self.monitor_paths != "" :
#             mpaths = re.split(",|;", self.monitor_paths)
#         except Exception ,e :
#             self.logger.error("module : SysUtil ,class : ConfigUtil,method : get_monitor_paths-->" + str(e))     
        mpath = None
        if  os.path.exists(self.monitor_path) :
            mpath = self.monitor_path 
        return mpath
    def get_plugin_path(self):
        return self.plugin_path

class  PluginManager:
    def __init__ (self,path,logger,log_file):
        self.plugin_path=path
        self.logger = logger
        self.log_file=log_file
    def getPlugins(self,objClass):
        t_str = time.strftime('%Y%m%d%H%M%S')
        plugins=[]
        try :
            fu =FileUtil(self.logger)
            filenames = fu.getFilesByEndWith(self.plugin_path, ".py")
            
            for fname in filenames:
                
                if fname == "DefPlugin.py" :
                    continue
                fullName = self.plugin_path+"/"+fname
                if os.path.isfile(fullName):
                    #plugins.append(fname)
                    sys.path.append(os.getcwd()+"/plugin")
                    fname=fname.replace(".py","")
                    plugins = self.getPluginObj(objClass,fname,plugins,self.logger,self.log_file)
        except Exception ,e :
            self.logger.debug("{'time':'"+t_str+"','module':'SysUtil','class':'PluginManager','method':'getPlugins' ,'errors':'" +str(e)+"'}")
        return plugins
    
    def getPluginObj(self,objClass,fname,plugins,logger,log_file):
        t_str = time.strftime('%Y%m%d%H%M%S')
        _module = __import__(fname)
        #_module = imp.load_source("_module",fname)
        subObj=object
        for attr in dir(_module) :
            try :
                subClass = getattr(_module, attr)
                subObj  = subClass()
                #if isinstance(subObj ,objClass) and not isinstance(objClass(),subClass) :
                if isinstance(subObj ,objClass) :
                    plugins.append(subObj)
            except Exception ,e :
                self.logger.debug("{'time':'"+t_str+"','module':'SysUtil','class':'PluginManager','method':'getPluginObj' ,'errors':'" +str(e)+"'}")
                
        return plugins   

class LogUtil:
    
    def __init__(self,log_file,flag):
        self.log_file = log_file
#         logging.basicConfig(level=logging.DEBUG,
#         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#         datefmt='%Y-%m-%D %H:%M:%S',
#         filename=self.log_file,
#         filemode='w')
#         trfhdr = logging.handlers.TimedRotatingFileHandler(log_file,when='M',interval=1,backupCount=40)
    
    
        logger = logging.getLogger()
        ###按照日期分割
        hdr = logging.handlers.TimedRotatingFileHandler(log_file,when='H',interval=1,backupCount=168)
        ###按照文件大小分割
        #hdr = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes=1024*1024,backupCount=40)

        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        hdr.setFormatter(formatter)
        logger.addHandler(hdr)
        logger.setLevel(logging.DEBUG)
        #################################################################################################
        #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        if flag.lower() == "debug" :
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            #formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
             
            logger.addHandler(console)
        #################################################################################################
        #定义日志文件轮转机制
        #logging.getLogger("").addHandler(trfhdr)
        self.logger = logger
        
    def getLoger(self):
        return  self.logger
# p = PluginManager("/home/lee/monitor/test2/")
# print p.getPlugins()

    
    
    
    
    
    
    
    
    