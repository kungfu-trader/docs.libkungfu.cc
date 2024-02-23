策略加密打包
-----------------

**注意 : 如果在相同环境下的两台机器上面,一台加密打包,一台运行.那么需要将加密打包后的策略文件整体复制粘贴到运行的机器上面去,然后添加可执行文件,运行策略.**

比如 : 两台linux环境机器A和B. 在A机器上面加密打包策略文件 : strategy-cpp , 打包出来的可执行的.so文件是在/dist/文件夹下面,但是如果想要在机器B中运行 机器A打包出来的可执行的.so文件,需要将 打包加密后的策略文件 strategy-cpp 整体复制到机器B中,然后执行添加策略


Windows下加密打包
~~~~~~~~~~~~~~~~~~~~~

1. 环境配置
^^^^^^^^^^^^^^^^^^

(1) . 打包需要安装 :
>>>>>>>>>>>>>>>>>>>>>>>>>>>

    visual studio community 2022 及以上版本 (安装 visual studio 会带有 cmake )
    
    Node.js 18.1及以上版本

(2) . visual studio community 2022 / node.js 下载地址
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 **visual studio community 2022** 

 ::

    https://visualstudio.microsoft.com/zh-hans/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&passive=false

 
 **node.js** 
 :: 

    https://nodejs.org/en/download
    
(3) . 编译必须使用visual studio自带的64位shell
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 - 点击电脑左下角的开始菜单

        .. image:: _images/开始菜单.png
           :width: 400px
           :height: 250px

 - 向下查找 visual studio 2022

        .. image:: _images/vs2022.png
           :width: 700px
           :height: 1500px

 - 选择 x64 Native Tools Command Prompt VS 2022

        .. image:: _images/x64native.png
           :width: 800px
           :height: 1500px


.. 注意::

 - 对于2.4版本 (Kungfu-1.0.x-win-x64-latest.exe)、2.5版本(Kungfu-1.1.x-win-x64-latest.exe)，安装visual studio community 2022后可以直接进行策略的加密打包操作。


 - 对于2.6版本(Kungfu-2.6.x-alpha.0-win-x64-alpha.exe)、2.7版本(Kungfu-2.7.x-alpha.0-win-x64-alpha.exe)，需要先更新 visual studio 版本，在进行策略的加密打包操作 (更新操作如下)。

  - 搜索visual studio installer

         .. image:: _images/搜索vs.png
            :width: 600px
            :height: 400px

  - 打开visual studio installer , 点击更新按钮

         .. image:: _images/更新vs.png
            :width: 600px
            :height: 400px

  - 更新完毕 

         .. image:: _images/更新完成vs.png
            :width: 600px
            :height: 400px




2 . Python策略
^^^^^^^^^^^^^^^^^^

(1) . 创建 package.json 文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 ::

    {
      "author": "kungfu-trader",          # 必须
      "kungfuConfig": {                   # 必须,与策略文件所在文件夹相关
        "key": "KungfuStrategyPython"
      },
      "kungfuBuild": {                    # 与打包模块相关
        "python": {
          "dependencies": {
            "redis": "~=4.3.4"
          }
        }
      }
    }

**说明 :**

 - kungfuConfig 中的key对应的是 策略文件中策略文件(.py文件)所在文件夹的名字 , 这个名字不能有 _ , - . 比如命名不可以是 : kungfu-demo , kungfu_demo

 - kungfuBuild 是使用的Python第三方模块. 功夫自带的Python模块之外的模块 写入dependencies中,格式如上图

 - 如果没有打包模块,可以不写 kungfuBuild

    ::

        {
          "author": "kungfu-trader",          # 必须
          "kungfuConfig": {                   # 必须,与策略文件所在文件夹相关
            "key": "KungfuStrategyPython"
          }
        }


(2) . 创建策略文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-python                     # 名字随意
        |-- package.json
        |-- src
        |   |-- python
        |   |   |--  KungfuStrategyPython    # 必须与package.json中kungfuConfig的key相同
        |   |   |    |-- __init__.py        # 主策略文件
        |   |   |    |-- kf.py              # 副策略

**说明**

 - python的策略要写入 主策略文件中,如果策略需要引用其他python的脚本文件,其他python脚本文件放在主策略的同级目录下,例如 : kf.py ::

    __init__.py策略中引用kf.py文件的方法 :
    from . import kf

(3) . 执行加密打包
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 ::

	xxx\Kungfu\resources\kfc\kfs.exe strategy clean  	# 清理之前的打包文件
	xxx\Kungfu\resources\kfc\kfs.exe strategy build  	# 编译策略

**说明**

 - xxx 是软件安装目录 比如安装在 C盘根目录,那么命令就是 ::

    C:\Kungfu\resources\kfc\kfs.exe strategy build

 - 在策略文件的跟目录下打包,例如 : (策略放在了电脑桌面上,策略文件夹为 strategy-python ) ::

    C:\Users\Administrator\Desktop\strategy-python>C:\Kungfu\resources\kfc\kfs.exe strategy clean
    C:\Users\Administrator\Desktop\strategy-python>C:\Kungfu\resources\kfc\kfs.exe strategy build

 - **安装目录不能有空格**

 - 打包之前要执行 C:\Kungfu\resources\kfc\kfs.exe strategy clean

(4) . 打包文件所在
>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-python                     # 名字随意
        |-- package.json
        |-- src
        |   |-- python
        |   |   |--  KungfuStrategyPython    # 必须与package.json中kungfuConfig的key相同
        |   |   |    |-- __init__.py        # 主策略文件
        |   |   |    |-- kf.py              # 副策略
        |-- dist                            # build之后生产的文件夹
        |   |-- KungfuStrategyPython        # package.json中kungfuConfig的key对应的名字
        |   |   |--  xxx.pyd     # 加密之后的策略文件


(5) . 运行加密策略文件
>>>>>>>>>>>>>>>>>>>>>>>

    将 xxx.pyd文件当做正常的策略文件,在策略面板中添加即可


3 . c++策略
^^^^^^^^^^^^^^^^^^

(1) . 创建package.json文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 ::

    {
      "kungfuConfig": {        # 必须,key对应与策略相关
        "key": "demoKungfu"
      },
      "kungfuBuild": {         # 与打包模块相关
        "cpp": {
          "target": "bind/python",
          "links": [
          ]
        }
      }
    }


**说明**

 - kungfuConfig中key对应的是打包之后加密的策略所在的文件夹.这个名字不能有 _ , - . 比如命名不可以是 : kungfu-demo , kungfu_demo

(2) . 创建策略文件
>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-cpp                     # 名字随意
        |-- package.json
        |-- src
        |   |-- cpp
        |   |   |--  strategy.cpp        # c++的策略必须写入这里


**说明**

 - strategy.cpp 是c++策略所在的文件 (c++的策略要写入 strategy.cpp 中)

(3) . 使用第三方库说明
>>>>>>>>>>>>>>>>>>>>>>>>>

 以mysql为例

 - 下载源码,编译.导出头文件和动态库
 - 在策略文件夹根目录下创建文件夹

策略文件夹目录树结构如下 ::

    |-- strategy-cpp                     # 名字随意
        |-- package.json
        |-- src
        |   |-- cpp
        |   |   |--  strategy.cpp        # c++的策略必须写入这里
        |-- __kungfulibs__                     # 文件夹名字必须是这个 ************
        |   |-- party_name                     # 库名(名字随意,比如: DataToMysql)
        |   |   |--  party_name_version        # 库的版本(比如:v1.0.1 )
        |   |   |  |--  include                # 库的头文件放入这个文件夹中 比如 ：TestDll.h 放此文件夹
        |   |   |  |--  lib                    # 第三方库需要链接的库文件放入这个文件夹中
    ```

注意 : 检查三方库所需的依赖库,需要依次寻找依赖库中所依赖的的非系统库,将其放入 __kungfulibs__ /party_name/party_name_version/lib文件夹中.

比如 : mysql 需要第三方库libmysql.lib,使用依赖检查工具检查,发现 libmysql.lib 依赖 libcrypto-1_1-x64.dll 和 libssl-1_1-x64.dll 以及其他系统自带库.再次使用依赖检查工具检查 libcrypto-1_1-x64.dll和libssl-1_1-x64.dll, 发现并无其他非系统库 (如果有其他依赖的非系统库,还需要继续向下寻找)。 那么将策略所需的 这三个放入 __kungfulib__ /party_name/party_name_version/lib文件夹中.

 - 在package.json中加入三方库

 ::

    {
      "kungfuDependencies": {    		# 三方库相关
        party_name: party_name_version  # 库名：库的版本 比如 ："DataToMysql":"v1.0.1" ,
      },
      "kungfuConfig": {          	    # 必须,key对应与策略相关
        "key": "demoKungfu"
      },
      "kungfuBuild": {                  # 与打包模块相关
        "cpp": {
          "target": "bind/python",
          "links": [                    # .lib动态库在其中声明
                "DataToMysql",
                "libmysql"
          ]
        }
      }
    }

注意 ：

    a. 上图 ： kungfuDependencies 中 party_name: party_name_version 是 策略创建的 库名文件夹的名字 ： 库的版本文件夹的名字

    b. 在package.json中的 links 下面添加所需的 .lib动态库

 - 在策略strategy.cpp 中引用头文件 : \#include <DataToMysql.h>

(4) . 执行加密打包
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 ::

	xxx\Kungfu\resources\kfc\kfs.exe strategy clean  	# 清理之前的打包文件
	xxx\Kungfu\resources\kfc\kfs.exe strategy build  	# 编译策略

**说明**

 - xxx 是软件安装目录 比如安装在 C盘根目录,那么命令就是

 ::

    C:\Kungfu\resources\kfc\kfs.exe strategy build

 - 在策略文件的跟目录下打包,例如 : (策略放在了电脑桌面上,策略文件夹为 strategy-cpp )

 ::

    C:\Users\Administrator\Desktop\strategy-cpp>C:\Kungfu\resources\kfc\kfs.exe strategy clean
    C:\Users\Administrator\Desktop\strategy-cpp>C:\Kungfu\resources\kfc\kfs.exe strategy build

 - **安装目录不能有空格**

 - 打包之前要执行 C:\Kungfu\resources\kfc\kfs.exe strategy clean

(5) . 打包文件所在
>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-cpp                     # 名字随意
        |-- package.json
        |-- src
        |   |-- cpp
        |   |   |--  strategy.cpp    	 # c++的策略必须写入这里
        |-- dist                         # build之后生产的文件夹
        |   |-- demoKungfu        		 # package.json中kungfuConfig的key对应的名字
        |   |   |--  xxx.pyd             # 加密之后的策略文件


(6) . 运行加密策略文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

将 xxx.pyd文件当做正常的策略文件,在策略面板中添加即可



Linux下加密打包
~~~~~~~~~~~~~~~~~~~~~

1 . 环境配置
^^^^^^^^^^^^^^^^^^

 **需保证gcc版本为11**

2 . Python策略
^^^^^^^^^^^^^^^^^^

(1) . 创建 package.json 文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 ::

    {
      "author": "kungfu-trader",          # 必须
      "kungfuConfig": {                   # 必须,与策略文件所在文件夹相关
        "key": "KungfuStrategyPython"
      },
      "kungfuBuild": {                    # 与打包模块相关
        "python": {
          "dependencies": {
            "redis": "~=4.3.4"
          }
        }
      }
    }



**说明**

 - kungfuConfig 中的key对应的是 策略文件中策略文件(.py文件)所在文件夹的名字 , 这个名字不能有 _ , - . 比如命名不可以是 : kungfu-demo , kungfu_demo

 - kungfuBuild 是使用的Python第三方模块. 功夫自带的Python模块之外的模块 写入dependencies中,格式如上图

 - 如果没有打包模块,可以不写 kungfuBuild

    ::

        {
          "author": "kungfu-trader",          # 必须
          "kungfuConfig": {                   # 必须,与策略文件所在文件夹相关
            "key": "KungfuStrategyPython"
          }
        }

(2) . 创建策略文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-python                      # 名字随意
        |-- package.json
        |-- src
        |   |-- python
        |   |   |--  KungfuStrategyPython    # 必须与package.json中kungfuConfig的key相同
        |   |   |    |-- __init__.py         # 主策略文件,必须叫这个名字
        |   |   |    |-- kf.py               # 副策略

**说明**

 - python的策略要写入 主策略文件中,如果策略需要引用其他python的脚本文件,其他python脚本文件放在主策略的同级目录下,例如 : kf.py

    ::

        __init__.py策略中引用kf.py文件的方法 :
        from . import kf

(3) . 执行加密打包
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

在策略文件中执行打包命令 :

 ::

    /opt/Kungfu/resources/kfc/kfs strategy clean  	# 清理之前的打包文件
    /opt/Kungfu/resources/kfc/kfs strategy build  	# 编译策略


比如 : 我的策略文件名是 strategy-python

 ::

    [root@server-102-centos strategy-python]# /opt/Kungfu/resources/kfc/kfs strategy clean
    [root@server-102-centos strategy-python]# /opt/Kungfu/resources/kfc/kfs strategy build

(4) . 打包文件所在
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-python                     # 名字随意
        |-- package.json
        |-- src
        |   |-- python
        |   |   |--  KungfuStrategyPython    # 必须与package.json中kungfuConfig的key相同
        |   |   |    |-- __init__.py        # 主策略文件
        |   |   |    |-- kf.py              # 副策略
        |-- dist                            # build之后生产的文件夹
        |   |-- KungfuStrategyPython        # package.json中kungfuConfig的key对应的名字
        |   |   |--  xxx.so     # 加密之后的策略文件



(5) . 运行加密策略文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 将 xxx.so文件当做正常的策略文件,在策略面板中添加即可

3 . c++策略
^^^^^^^^^^^^^^^^^^

(1) . 创建package.json文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 ::

    {
      "kungfuConfig": {        # 必须,key对应与策略相关
        "key": "demoKungfu"
      },
      "kungfuBuild": {         # 与打包模块相关
        "cpp": {
          "target": "bind/python",
          "links": [
            "TestDll"
          ]
        }
      }
    }

**说明**

 - kungfuConfig中key对应的是打包之后加密的策略所在的文件夹.这个名字不能有 _ , - . 比如命名不可以是 : kungfu-demo , kungfu_demo

**使用三方库说明**

 - 下载源码,编译.导出头文件和动态库 (比如:我导出的是 : TestDll.h , TestDll.dll , TestDll.lib )

 - 将头文件放入/opt/Kungfu/resources/kfc/include/kungfu/ 下面

     比如:/opt/Kungfu/resources/kfc/include/kungfu/TestDll.h

 - 将动态库放入/opt/Kungfu/resources/kfc/ 下面

 - 在package.json中的 links 下面添加 动态库 .lib (如上图)

 - 在策略strategy.cpp 中引用头文件 : \#include <kungfu/TestDll.h>

(2) . 创建策略文件
>>>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-cpp                     # 名字随意
        |-- package.json
        |-- src
        |   |-- cpp
        |   |   |--  strategy.cpp        # c++的策略必须写入这里

**说明**

 - strategy.cpp 是c++策略所在的文件 (c++的策略要写入 strategy.cpp 中)

(3) . 执行加密打包
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

在策略文件中执行打包命令 :

 ::

    /opt/Kungfu/resources/kfc/kfs strategy clean  	# 清理之前的打包文件
    /opt/Kungfu/resources/kfc/kfs strategy build  	# 编译策略

比如 : 我的策略文件名是 strategy-cpp

 ::

    [root@server-102-centos strategy-cpp]# /opt/Kungfu/resources/kfc/kfs strategy clean
    [root@server-102-centos strategy-cpp]# /opt/Kungfu/resources/kfc/kfs strategy build


(4) . 打包文件所在
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

策略文件夹目录树结构如下 ::

    |-- strategy-cpp                     # 名字随意
        |-- package.json
        |-- src
        |   |-- cpp
        |   |   |--  strategy.cpp    	 # c++的策略必须写入这里
        |-- dist                         # build之后生产的文件夹
        |   |-- demoKungfu        		 # package.json中kungfuConfig的key对应的名字
        |   |   |--  xxx.so             # 加密之后的策略文件


(5) . 运行加密策略文件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 将 xxx.so文件当做正常的策略文件,在策略面板中添加即可





