# FileSystem_monitor

#本程序编写目的：

随着大数据、hpc、ML等技术普遍应用，应用程序为了满足用户复杂的文件查询，需要使用数据库储存文件相关信息，这样查询速度可以得到保证.

用户的操作习惯：在页面上操作文件;同时在操作系统内部也会操作文件，这样就会出现数据库文件信息与文件系统中文件信息不匹配，怎么解决.

各类语言及操作系统均有一些组件可以使用，都需要研发人员进行组装，于是我自己弄了一个文件系统监听器.

该监听器监听某个目录下子文件及文件夹变化，包括增加移动，添加，修改，删除.

#本程序提供记录日志的功能:

用户不经过应用程序直接在文件系统中进行操作时（这些操作在监听的目录中），本程序会在日志文件中记录下来.
 
日志按照时间进行分割，单位（小时），7天一循环.

#本程序对开发者提供自定义插件功能:

开发者根据默认插件类编写自定义的插件，同时重写默认插件的方法，以实现自定义的功能，完成复杂的业务流程.

编写插件很简单，只需要继承DefPlugin类即可，之后把自定义插件文件（XXX.py）放入plugin/目录中即可.

本程序默认在plugin/中提供了一个自定义插件演示的例子程序：MyPlugin.py

本程序支持多个插件共同运行

友情提示：插件可以使用resetful 方式进行跨平台/系统处理，具体参看MyPlugin.py中的说明.

注意：事件阻塞式操作/同步操作请在插件中自行设置超时时间及异常捕获.

#本程序结构：

plugin|                   #插件目录

   |DefPlugin.py       #插件父类，内部已实现目录的监听日志记录工作.
   
   |MyPlugin.py        #插件演示Demo，里面记录了插件编写方式，及测试例子.

FileSystemMonitor.py      #监听器主类，python  FileSystemMonitor.py   #   -h    后面跟上-h参数可以查看参数说明.

SysUtils.py               #常用工具类

monitor.conf.sample       #配置文件的模板，程序运行目录中复制一份，重命名为：monitor.conf,修改一下内容即可

#本程序运行前提条件:

python环境：     2.6+   小于3.0（3.0+未测试，本人只熟悉2.X的编程）

python插件：     watchdog

OS:             ubuntu16/centos6.7已测，其他操作系统未测试

#本程序运行方法：

在程序目录下复制 monitor.conf.sample并重命名为：monitor.conf,修改其中内容.

按照自己的需要进行配置，如下参数：

下面是正/常日志名称

log_file_name=monitor.log

日志文件路径

log_file_path=/home/lee/monitor/log/

监听的目录

monitor_path=/home/lee/monitor/test1/


查看命令行参数

python  FileSystemMonitor.py   #   -h    后面跟上-h参数可以查看参数说明.

  参数1 ： -h, 帮助提示
  
  参数2 ： -c,--conf=, 配置文件绝对路径，不配置该参数，程序默认在程序根目录找"monitor.conf"文件，文件不存在将报错.
  
  用法：python  FileSystemMonitor.py -c /home/lee/monitor/monitor.conf
          
  参数3 ： -p,--printlog=,屏幕打印log开关， 取值范围：debug/info/warn/error，目前只实现debug与非debug模式.
  
  用法：python  FileSystemMonitor.py  -p debug 
          
