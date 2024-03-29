策略进程面板
-------------

策略进程面板相当于策略池，允许用户导入策略文件、编辑代码。代码修改将 **实时储存** 。

.. tip:: 结合功夫灵活的多面板调度，点击选中策略能够让系统按策略统计该策略的持仓、委托记录、成交记录（请在对应面板查看）


.. image:: _images/2.6策略面板-new.png


.. image:: _images/策略面板-27.png


-----

添加策略
~~~~~~~~~~~~~

点击“添加”按钮，填写策略相关信息。

.. image:: _images/添加策略-25.png


.. image:: _images/添加策略详细-2-5.png


.. list-table::
   :header-rows: 1

   * - 字段
     - 字段说明
   * - 策略ID
     - 策略名称，策略ID不允许重复
   * - 策略路径
     - 从本地选择 .py 策略文件

完成填写后，点击“确定”完成策略添加。

.. attention::
  - 策略文件所在位置需要与功夫系统安装目录在同一个盘。
  - 启动策略前，需确认策略使用的交易进程(TD)/行情进程(MD)连接是否处于就绪状态，TD、MD未就绪将导致策略下单失败。


------

启动策略
~~~~~~~~~~~~~~~~~~

点击策略进程按钮开启策略进程，再次点击策略进程按钮则停止运行中的策略。

.. image:: _images/启动策略-26.png

.. image:: _images/启动策略-25.png


-----

策略日志查看
~~~~~~~~~~~~~~~~~~~~~~

点击日志按钮，可以在新窗口中查看策略运行日志。

.. image:: _images/查看策略日志-26.png

.. image:: _images/策略日志-25.png


-----

实时编辑策略代码
~~~~~~~~~~~~~~~~~~~~~~

功夫客户端中内嵌了IDE，用户可在客户端中编辑本地策略。点击编辑按钮，将弹出策略编辑弹窗，修改将实时保存。

.. image:: _images/编辑策略-26.png

.. image:: _images/编辑策略.png


.. image:: _images/策略编辑-25.png


.. image:: _images/策略编辑-27.png



.. attention::若编辑代码时策略进程仍处于运行状态，修改的代码将不会实时生效，重启策略进程后生效。


-----

删除策略
~~~~~~~~~~~~~

点击策略后方的删除按钮即可删除策略，删除前系统将将关闭策略进程，停止该策略的下单。

.. image:: _images/删除策略-26.png

.. image:: _images/策略删除-25.png


-----

回放工具
~~~~~~~~~~~~~~~~~~
回放工具通过模拟盘中交易情况，可以帮助用户在盘后进行代码调试、策略复盘。

回放工具可增加log、使用实盘数据进行模拟撮合、使用实盘下单数据查看不同。

-----

回放-增加更加详细级别的log
++++++++++++++++++++++++++++++++++

不使用撮合器的情况下，回放工具仅支持增加log（修改日志级别/在部分代码处增加日志打印代码）。

.. note::
  **例1** 全局设置中，日志级别为info，想看到debug级别的日志以排查存在的问题。

(1) 点击策略进程面板 - 回放按钮

.. image:: _images/打开回放.png

(2) 选择想查看debug日志级别的session，点击确定。

.. tip:: 允许用户自行设定停止回放的结束时间；若策略进程运行时间较长，想回放的部分仅在前半程，可自定义结束时间

.. image:: _images/回放-不使用撮合器.png

(3) 回放产生的debug级别日志将在新窗口中打开。
 
**注：若选择回放的session持续时间较长，回放进程将持续数秒，回放完成后将显示日志**

.. image:: _images/回放-增加log.png

-----

.. note:: 
   **例2** 原策略代码仅打印下单标的代码、order_id，需要增加下单价log以便导出数据进行分析。


.. image:: _images/回放-增加代码前.png


(1) 打开代码编辑器，找到打印日志的代码"context.log.info"，增加打印下单价格的日志。


.. image:: _images/回放-增加代码后代码.png

  
(2) 点击回放按钮。

.. image:: _images/打开回放.png


(3) 选择回放的session，点击确定。


.. image:: _images/回放-不使用撮合器.png

(4) 回放成功运行，成功在日志中增加打印下单价格的内容。

.. image:: _images/回放-增加代码后日志.png


-----


回放-改变策略下单逻辑，使用实盘数据模拟回测
++++++++++++++++++++++++++++++++++++++++++++++++++

- 撮合器能够帮助用户使用实盘行情数据进行模拟交易撮合。用户 **修改下单策略逻辑** 后需要使用回放功能时， **必须使用撮合器** 。

.. note::
  **例3** 用户改变下单策略逻辑，且想使用实盘数据模拟新策略的下单情况。

   - 背景：用户已经在实盘中进行过下单，实盘下单逻辑为: *行情价 + 1 < 200* 时下单。
  
   - 诉求：想模拟下单逻辑修改为 *行情价 + 2 < 200* 时下单的成交情况。

.. image:: _images/回放-修改下单逻辑模拟（原下单代码）.png
  

(1) 打开代码编辑器，找到下单逻辑代码，将逻辑修改为 *行情价 + 2 < 200* 时下单。

.. image:: _images/回放-修改下单逻辑模拟（改后代码）.png

(2) 点击回放按钮。

.. image:: _images/打开回放.png

(3) 选择回放的session，点击确定。

.. attention:: 必须打开“使用撮合器”配置

.. image:: _images/回放-修改下单逻辑模拟（选择回放session）.png

(4) 回放成功运行，系统将按照修改后下单逻辑进行模拟。

 *在回放日志中可以看到逻辑修改后使用实盘数据模拟的下单情况，可导出并与实盘日志的下单结果比对* 。

.. image:: _images/回放-修改下单逻辑模拟（结果对比）.png


-----


回放-测试不同手续费交易成本差别
++++++++++++++++++++++++++++++++++++++++++++++++++
 
.. note::
   **例4** 用户想测试不同期货手续费费率实盘数据下的表现。

若用户的实盘策略中没有“打印手续费”的代码，需要先增加日志打印代码context.log.info，再使用回放工具。

例：

::
  
    #打印手续费
    def on_trade(context, trade, location,dest):
      context.log.info("[on_trade] 订单ID--{},成交量--{},手续费--{}".format(trade.order_id, trade.volume,trade.commission))

(1) 打开全局设置，点击期货手续费，修改对应期货品种手续费。

.. image:: _images/全局设置-进入.png

.. image:: _images/全局-手续费.png

.. note:: 功夫将自动请求账户中持仓标的的手续费，没有持仓时，需要到“全局设置-持仓”进行设置

(2) 点击回放按钮。

.. image:: _images/打开回放.png

(3) 选择回放的session，点击确定 **注：必须打开撮合器** 。

.. image:: _images/回放-修改下单逻辑模拟（选择回放session）.png

(4) 回放成功运行，在回放日志中可以看到每笔成交对应的手续费日志与实盘不同。


-----

诊断工具
------------------------------

  journal文件是功夫交易系统中记录进程行为的数据文件。journal文件具有极其丰富的数据信息，如Quote行情信息中记录了档位报价详细信息，可用于盘后复盘。
  
  浏览、定位journal数据可通过诊断工具进行。诊断工具支持多种 **数据定位方式** ：通过时间戳定位、消息类型过滤、关键字搜索。

.. hint:: 用户可通过诊断工具定位信息，复盘策略运行状况、排查策略运行问题。


-----


查看单一进程的journal文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
目前交易账户、行情源、策略进程、交易任务、算子面板均支持使用诊断工具查看journal数据。

.. image:: _images/journal查看-25.png

-----


查看所有进程的journal文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

点击文件（左上角） -- 打开诊断工具，新窗口将显示所有进程的journal数据。

.. tip::  **journal支持调整上下模块高度**：鼠标悬停在进度轴下方，鼠标变为指针样式即可调整。


.. image:: _images/journal工具.png


.. image:: _images/查看所有journal-27.png


-----

定位journal信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
支持的筛选方式：过滤信道、过滤消息类型、按时间戳跳转。

.. image:: _images/journal工具定位.png


-----


诊断工具-关键字搜索功能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用ctrl+f可调出搜索框，可使用快捷键enter跳转到下一个搜索结果。

.. image:: _images/journal关键字搜索.png

-----


Journal数据可视化工具
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(1) 点击进程后方的小眼睛图标，打开诊断工具。

.. image:: _images/journal查看-25.png

(2) 点击“进入可视化”按钮。

.. image:: _images/进入可视化.png

(3) 进入journal数据可视化界面。

.. image:: _images/journal可视化界面-27.png

- **左侧session栏**：可切换session，查看同一策略不同运行时间的journal记录。
- **左侧标的栏**：展示session中，该策略中不同标的行情获取及下单情况。
- **右侧图表**：展示可视化下单、撤单、行情信号。信号可点击，点击后下方列表将跳转到对应的journal记录。
- **下方journal记录**：以列表方式展示journal详情。记录可点击，若点击的记录为图例中的信号，则图表将高亮对应信号。


.. attention:: 由于journal数据量较大，一次仅加载2000条数据，若策略运行时间较长，需要用户手动下滑加载更多数据


**journal数据可视化可以帮助用户快速跟踪策略的下单情况，包括：**

- 快速查看策略中每个标的总体下单情况、分布状况。
- 查看下单时相对于行情的延时情况。
- 查看同一订单号（order_id）下单、撤单情况。

.. tip:: 
  **鼠标滚轮滑动**：增加/减少展示内容的时间跨度。

  **单击信号图例**：筛选出order_id相同的信号（包括委托、委托回报、撤单），且下方journal记录将跳转到对应位置；点击空白处即可回到正常状态。
  
  **单击下方记录详情**：图上将跳转到该时间段，若该信号为委托、委托回报、撤单信号，则信号将高亮。


-----


