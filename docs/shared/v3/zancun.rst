【命令行】运行回测
++++++++++++++++++++++++++++++++++++

   在命令行使用kfc模块即可运行回测


kfc文件路径
^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    Windows: {kungfu安装目录}/resources/kfc/kfc.exe

    Linux: {kungfu安装目录}/resources/kfc/kfc

    MacOS: {kungfu安装目录}/Contents/Resources/kfc/kfc


.. tip:: 
  
  Windows与MacOS版本可通过图形化界面的菜单栏， **文件->打开功夫安装目录**， 可以直接打开 **{kungfu安装目录}/resources** 目录


使用说明
^^^^^^^^^^^^^^^^

登录
^^^^^^^^^^^^^^^^

    必须先完成登录才能进行后续操作

::

    kfc -s {stage} login -A {phone}

    # stage: 回测环境， 默认为 "prod"
    # phone: 登录手机号

例如 : 

    以安装在Windows电脑为例，安装目录为下载(Downloads)目录下

::

    C:\Users\kf\Downloads\kungfu\resources\kfc\kfc.exe login -A 18686868886

    # 然后填写验证码，回车完成登录

.. image:: _images/kfc-login.png


提交回测
^^^^^^^^^^^^^^^^^^^^^^^^

::

    kfc -s {stage} backtest submit -f {strategy} -b {begin_time} -e {end_time} -l {level}

    # stage: 回测环境， "prod"
    # strategy: 策略所在路径，建议绝对路径
    # begin_time: 开始时间， 如: 2023-01-03
    # end_time: 结束时间， 如: 2023-01-31 
    # level: 数据， "level1" 或 "level2"

例如 : 

    以安装在Windows电脑为例，安装目录为下载(Downloads)目录下; 策略路径为桌面的Strategy/strategy_demo/文件夹下


::

    C:\Users\kf\Downloads\kungfu\resources\kfc\kfc.exe -s "prod" backtest submit -f C:\Users\zmc\Desktop\Strategy\strategy_demo\MAStrategy.py -b 2023-01-03 -e 2023-01-31 -l "level2"


.. image:: _images/back-1.png

.. image:: _images/back-2.png


查看回测可用数据
^^^^^^^^^^^^^^^^

    跟提交回测submit里的开始时间-b，结束时间-e强相关

::

    kfc -s {stage} backtest datarange   

    # stage: 回测环境，"prod"

例如 : 

    以安装在Windows电脑为例，安装目录为下载(Downloads)目录下

::

    C:\Users\kf\Downloads\kungfu\resources\kfc\kfc.exe -s "prod" backtest datarange   


.. image:: _images/datarange.png

------