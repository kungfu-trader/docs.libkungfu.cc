开发者指南
==============

Intro 简介
~~~~~~~~~~~~~~

功夫量化 是专为量化交易者设计的开源交易执行系统。功夫想要解决以下问题：

    - 低延迟交易 - 量化交易者对系统内响应速度有极高要求，功夫提供微秒级别的系统响应，支持带纳秒级时间戳的交易数据实时存储和盘后分析。
    - 开放的策略编写方式 - 功夫支持 Python 3 及 C++ 形式的策略编写，策略师可以不受限的自由使用第三方计算库，放飞创意。
    - 友好的使用方式 - 告别 Linux shell 小黑屋，功夫提供图形化操作界面，简化策略运维流程。而进阶用户仍然具备通过底层 API 以无界面形式使用系统的能力。
    - 跨平台运行 - 三大主流平台（Windows、MacOSX、Linux）皆可编译运行。


功夫系统架构如下：
~~~~~~~~~~~~~~~~~~~

    - 后台核心（C++）
        - 长拳（longfist） - 金融交易相关的数据格式定义，提供涵盖 c++/python/javascript/sqlite 的序列化支持。
        - 易筋经（yijinjing） - 专为金融交易设计的超低延迟时间序列内存数据库，提供纳秒级时间精度，可落地交易相关的全部数据。
        - 咏春（wingchun） - 策略执行引擎，提供策略开发接口，实时维护策略账目及持仓情况。
    - 策略接口（C++/Python）
        - RxCpp - 响应式事件处理框架，可对丰富数据类型的金融交易数据进行灵活处理。
        - numpy/pandas - 自带的 Python 运行环境原生提供 numpy/pandas 等工具供策略使用。
    - 前端UI（Node.js）
        - Electron - 跨平台的桌面应用开发框架
        - Vue.js - UI开发框架

功夫在系统设计上支持任意柜台的对接（涵盖中国所有股票、期货市场），功夫开源版提供 XTP 柜台对接的参考实现。 如果需要接入更多柜台请至 `功夫量化官网 <https://www.kungfu-trader.com>`_ 下载专业版或 `联系我们 <https://www.kungfu-trader.com/index.php/about-us/>`_ 。

初次使用请参考 功夫文档。

更多介绍请关注知乎专栏 `硅商冲击 <https://www.zhihu.com/column/silicontrader>`_ 。

License
~~~~~~~~~~~~~~

Apache License 2.0


Setup 编译及运行环境
~~~~~~~~~~~~~~~~~~~~

功夫的编译依赖以下工具：

    - 支持 C++20 的编译器
    - cmake (>=3.15)
    - Node.js (^14.x)
    - yarn (^1.x)
    - Python 3 (~3.9)
    - pipenv (^1.x)

开始编译前，请先确保安装以上工具，且正确设置 PATH 环境变量。

Windows下环境配置
^^^^^^^^^^^^^^^^^^

1 . 需要安装 :
>>>>>>>>>>>>>>>>>>>>>>>>>>>

    visual studio community 2022 及以上版本 (安装 visual studio 会带有 cmake )
    
    Node.js 18.1及以上版本

2 . visual studio community 2022 / node.js 下载地址
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

 **visual studio community 2022** 

 ::

    https://visualstudio.microsoft.com/zh-hans/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&passive=false

 
 **node.js** 
 :: 

    https://nodejs.org/en/download


3 . visual studio需要下载的组件
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    需要选择 Python开发、Node.js开发、使用C++的桌面开发、通用Windows平台开发、Visual Studio扩展开发。(具体安装信息见下图)

 - Python开发

        .. image:: _images/vspython开发.png
           :width: 400px
           :height: 250px

 - Node.js开发

        .. image:: _images/vs-node.png
           :width: 600px
           :height: 500px

 - 使用C++的桌面开发

        .. image:: _images/vs-c++桌面.png
           :width: 500px
           :height: 800px

 - 通用Windows平台开发

        .. image:: _images/vs-windows平台.png
           :width: 400px
           :height: 600px

 - Visual Studio扩展开发

        .. image:: _images/vs扩展开发.png
           :width: 700px
           :height: 500px


4 . 使用visual studio自带的64位shell
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

 - 对于2.4版本 (Kungfu-1.0.x-win-x64-latest.exe)、2.5版本(Kungfu-1.1.x-win-x64-latest.exe)，安装visual studio community 2022后可以进行操作。


 - 对于2.6版本(Kungfu-2.6.x-win-x64-latest.exe)、2.7版本(Kungfu-2.7.x-win-x64-latest.exe)，需要先更新 visual studio 版本，在进行操作 (更新操作如下)。

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


Linux下环境配置
^^^^^^^^^^^^^^^^^^

 **需保证gcc版本为11**


.. tip:: 

  可以使用我们的docker来编译
  
  docker run --name kf --ulimit memlock=-1 --privileged --net=host -td -v /path/to/package:/Project:rw docker.io/kungfutrader/kungfu-builder-centos:v1.2.3 /usr/sbin/init 
   - kf : 指定的名字 (根据个⼈修改) 
   - /path/to/package : docker外的地址 (根据个⼈修改) 
   - /Project : docker内地址 (根据个⼈修改)


Compile 编译
~~~~~~~~~~~~~~

常规操作
获取代码并编译::

    $ git clone git@github.com:kungfu-origin/kungfu.git
    $ cd kungfu
    $ yarn install
    $ yarn build
    $ yarn package

编译结果输出在 artifact/build 目录下。

遇到编译问题需要完整的重新编译时，执行以下命令::

    $ yarn rebuild
    $ yarn package

编译过程产生的临时文件
编译过程会在代码所在目录下生成如下临时文件::

    node_modules
    **/node_modules
    **/build
    **/dist

通常情况下可通过执行如下命令对 build 和 dist 进行清理::

    $ yarn clean

需要注意 node_modules 目录为 yarn 产生的包目录，一般情况下无需清除，如有特殊需要可手动删除。

另外，编译过程中会在系统的以下路径产生输出::

    $HOME/.conan                        # [conan](https://conan.io/center/) 的配置信息以及其存储的 C++ 依赖包
    $HOME/.cmake-js                     # [cmake.js](https://www.npmjs.com/package/cmake-js) 存储的 C++ 依赖包
    $HOME/.virtualenvs                  # pipenv(windows) 存储的 Python 依赖
    $HOME/.local/share/virtualenvs      # pipenv(unix) 存储的 Python 依赖

如果需要清理这些文件,都需要手动删除
