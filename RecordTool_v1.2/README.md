#录制工具使用说明(Mac、Windows版）

---

## **一、 环境准备** ##

>1. 安装mysql
>2. 配置mysql环境变量
>3. 安装MySQLdb (mac中直接安装mysql-python)
>4. 安装并配置adb

> **Mac用户:**

>* 配置mysql环境变量：

    export PATH=${PATH}:/usr/local/mysql/bin
    export DYLD_LIBRARY_PATH=/usr/local/mysql/lib
    export VERSIONER_PYTHON_PREFER_64_BIT=yes
    export VERSIONER_PYTHON_PREFER_32_BIT=no

---

## **二、使用说明** ##

>1. 工具运行中生成的视频文件都存储在与data目录下
>2. source文件夹存放着工具的源代码，修改源代码后需要使用“pack“打包脚本，重新打包源代码。重新打包会导致旧的可执行文件被新的覆盖，旧可执行文件备份在“bin-backup”目录下。

> **Mac用户:**

>* bin目录下有一个“Recorder_Mac”可执行文件，直接双击运行即可。如果界面没有出来，请检查是否连接内网。

> **Windows用户:**

>* bin目录下有一个“Recorder_Win.exe”可执行文件，直接双击运行即可。如果界面没有出来，请检查是否连接内网。 

---

## **三、参数修改说明** ##

>1. 如需更改数据库服务器地址等参数，更改/configurations/sql.json文件参数即可 
>2. 如需更改录制的命令参数，进入/source/record_tool_setting.py，按需配置record_args或default_record_args变量的值
>3. 如需更改上传视频ftp的相关配置，更改/configurations/ftp.json文件参数即可

---

## **四、注意事项** ##

>1. “configurations”目录下的version.json文件存放着工具的版本信息，打包脚本依赖该文件，不能移动、删除或更改名字。

---

## **五、更新日志** ##

>- **1.0版本**

    - 增加自动上传功能
    
    - 增加机型识别
    
    - 增加错误提示
    

>- **1.1版本**

    - UI整体缩小
    
    - 按机型过滤app
    
    - 按机型自动匹配录制命令参数
    
    - 增加补录模式
    
>- **1.2版本**

    - 兼容windows系统

---

#打包脚本使用说明

---

## **一. 环境准备** ##

>**Mac用户:**

1. 安装pyinstaller：

      > pip install pyinstaller 
      
2. 配置pyinstaller环境变量：

    > which pyinstaller,获取pyinstaller的位置
    
    > vim ~/.bash_profile
    
    > 按i进入插入模式，添加“export PATH=${PATH}:pyinstaller的位置“
  
    > 按esc退出插入模式，输入:wq，保存退出即可

>**Windows用户:**

1. 安装pyinstaller：
    > cmd窗口输入:pip install pyinstaller,等待安装完成即可

---

## **二、使用说明** ##

>1. 该脚本用于将录制工具的源码转换成一个可执行文件
>2. 该脚本依赖configurations目录下的version.json配置文件，不能移动、删除或重命名该文件
>3. 应确保录制工具的源码放在“source”目录下

>**Mac用户:**

>* 生成的可执行文件存放在打包脚本的同级目录下，命名为“Recorder_Mac”，同时会备份一份存放在“bin-backup“目录中

>**Windows用户:** 

>* 生成的可执行文件存放在打包脚本的同级目录下，命名为“Recorder_Win.exe”，同时会备份一份存放在“bin-backup“目录中

---


>作者 罗盛亨     
>2018 年 02月 06日    