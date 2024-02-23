算子API文档
==============

快速上手
-----------

策略逻辑简介
~~~~~~~~~~~~~~


 **示例：通过算子得出数据最终指导策略下单** 
 
 步骤：
 ①通过订阅行情获得合成数据的原材料
 ②策略代码中增加订阅算子的代码

  1.  :ref:`demo_operator.py <算子文件>` : 先编写算子文件的代码，通过行情源获取数据
  2.  :ref:`demo_strategy.py <策略文件>` : 策略文件中订阅算子，让策略接收到合成数据指导下单


.. attention:: 运行算子前需要确认所订阅的行情源进程已经启动

  例：SOURCE = "sim"，则需要确认先启动了sim柜台，且柜台状态为“就绪”，再打开算子进程，最后打开策略进程


.. _算子文件:

编写算子文件 ： demo_operator.py

::

    # -*- coding: UTF-8 -*-
    from kungfu.wingchun.constants import *

    source = "sim"
    exchange = Exchange.SSE


    def pre_start(context):
        context.log.info("pre start")
        context.subscribe(source, ['600420', '600000'], exchange)


    def post_start(context):
        context.log.info("post start")

    # 获取行情
    def on_quote(context, quote, location,dest):
        context.log.info("on quote: {}".format(quote.instrument_id))
        # 给订阅这个算子器的策略广播发布key标识为'demo-op'的行情数据
        context.publish_synthetic_data('demo-op', "{}".format(quote))


.. _策略文件:

策略文件中调用算子 ： demo_strategy.py

::

    # -*- coding: UTF-8 -*-
    import kungfu.yijinjing.time as kft
    from kungfu.wingchun.constants import *

    SOURCE = "sim"
    ACCOUNT = "123456"

    # 启动前回调，添加交易账户，订阅行情，策略初始化计算等
    def pre_start(context):
        # 添加交易柜台以及账户
        context.add_account(SOURCE, ACCOUNT)
        # 订阅算子ID为"my-bar"的bar数据
        # context.subscribe_operator("bar","my-bar")
        # 订阅算子id为 op 的算子器数据
        context.subscribe_operator("default", "op")


    # 订阅的算子器发布数据回调
    def on_synthetic_data(context, synthetic_data, location, dest):
        context.log.info('[synthetic_data] {}'.format(synthetic_data))

        quote_data = eval(synthetic_data.value)
        # 下单
        order_id = context.insert_order(quote_data['instrument_id'], quota_data["exchange_id"], SOURCE, ACCOUNT, quote_data['last_price'],
                                        VOLUME,
                                        PriceType.Limit, Side.Buy, Offset.Open)
        
        context.log.info("ticker---{},order_id---{}".format(quote_data['instrument_id'], order_id))

    # 收到订单状态回报时回调
    def on_order(context, order, location, dest):
        context.log.info("[on_order] 订单id--{} , 订单状态--{}".format(order.order_id, order.status))


    # 收到成交信息回报时回调
    def on_trade(context, trade, location, dest):
        context.log.info("[on_trade] 订单ID--{},成交量--{}".format(trade.order_id, trade.volume))



函数定义
-----------

基本方法
~~~~~~~~~~~

pre_start
^^^^^^^^^^^^^

**启动前调用函数，在策略启动前调用，用于完成添加交易账户，订阅行情，策略初始化计算等**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性。

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::


    def pre_start(context):
        # 添加柜台id,账户
        context.add_account(source, account)
        # 订阅行情
        context.subscribe(source, tickers, exchange)

post_start
^^^^^^^^^^^^^^

**启动后调用函数，策略连接上行情交易柜台后调用，本函数回调后，策略可以执行添加时间回调、获取策略持仓、报单等操作**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性。

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def post_start(context):
        context.log.info("[post_start] {}".format("post_start"))

pre_stop
^^^^^^^^^^^

**策略退出前方法** (当关闭策略的时候,策略退出之前调用这个方法)

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性。

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    # 退出前函数
    def pre_stop(context):
        context.log.info("strategy will stop")

post_stop
^^^^^^^^^^^^

**进程退出前方法**  (当关闭策略的时候,策略进程退出之前调用这个方法)

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性。

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    # 退出前函数
    def post_stop(context):
        context.log.info("process will stop")

on_quote
^^^^^^^^^^

**行情数据的推送会自动触发该方法的调用。**


参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - quote
     - :ref:`Quote对象 <QuoteOperator对象>`
     - 行情数据
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - int
     - 以16进制打印出来与location配合可以知道数据保存的journal文件名

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_quote(context, quote, location, dest):
        context.log.info('[on_quote] {}, {}, {}'.format( quote.instrument_id, quote.last_price, quote.volume))

dest举例说明::

    def on_quote(context, quote, location, dest):
        context.log.info("[on_quote] ----{}, {}, {}".format(location.category, location.group, location.name, hex(dest)))
    # [on_quote] ---- md, xtp, xtp, 0x0
    # location.category为: "md" , location.group为 : "xtp" ,location.name为: "xtp" , hex(dest)为 : 0x0
    # 数据存储在kf_home(kungfu\home\runtime\ md \ xtp \ xtp \journal\live) 中以16进制打印dest的同名文件中: 00000000.1.journal

on_transaction
^^^^^^^^^^^^^^^^^

**逐笔成交行情数据的推送会自动触发该方法的调用**

注意 : sim模拟柜台不支持逐笔行情

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - transaction
     - :ref:`Transaction对象 <TransactionOperator对象>`
     - 逐笔成交行情数据
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - int
     - 以16进制打印出来与location配合可以知道数据保存的journal文件名

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_transaction(context, transaction, location, dest):
        context.log.info('[on_transaction] {}'.format(transaction))

dest举例说明::

    def on_transaction(context, transaction, location, dest):
        context.log.info("[on_transaction] ----{}, {}, {}".format(location.category, location.group, location.name,hex(dest)))
    # [on_transaction] ---- md, xtp, xtp, 0x0
    # location.category为: "md" , location.group为 : "xtp" ,location.name为: "xtp" , hex(dest)为 : 0x0
    # 数据存储在kf_home(kungfu\home\runtime\ md \ xtp \ xtp \journal\live) 中以16进制打印dest的同名文件中: 00000000.1.journal

on_entrust
^^^^^^^^^^^^^

**逐笔委托行情数据的推送会自动触发该方法的调用**

注意 : sim模拟柜台不支持逐笔行情

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - entrust
     - :ref:`Entrust对象 <EntrustOperator对象>`
     - 逐笔委托行情数据
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - int
     - 以16进制打印出来与location配合可以知道数据保存的journal文件名

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_entrust(context, entrust, location, dest):
        context.log.info('[on_entrust] {}'.format(entrust))

dest举例说明::

    def on_entrust(context, entrust, location, dest):
        context.log.info("[on_entrust] ----{}, {}, {}".format(location.category, location.group, location.name,hex(dest)))
    # [on_entrust] ---- md, xtp, xtp, 0x0
    # location.category为: "md" , location.group为 : "xtp" ,location.name为: "xtp" , hex(dest)为 : 0x0
    # 数据存储在kf_home(kungfu\home\runtime\ md \ xtp \ xtp \journal\live) 中以16进制打印dest的同名文件中: 00000000.1.journal

on_deregister
^^^^^^^^^^^^^^^^^

**断开回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - deregister
     - :ref:`Deregister对象 <DeregisterOperator对象>`
     - 断开回调信息
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_deregister(context, deregister, location):
        context.log.info('[on_deregister] {}'.format(deregister))

on_broker_state_change
^^^^^^^^^^^^^^^^^^^^^^^^^^

**客户端状态变化回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - broker_state_update
     - :ref:`BrokerStateUpdate对象 <BrokerStateUpdateOperator对象>`
     - 客户端状态变化回调信息
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_broker_state_change(context, broker_state_update, location):
        context.log.info('[on_broker_state_change] {}'.format(broker_state_update))

on_synthetic_data
^^^^^^^^^^^^^^^^^^^^^

**订阅的算子器发布的数据返回**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - synthetic_data
     - :ref:`SyntheticData对象 <SyntheticDataOperator对象>`
     - 订阅的算子器发布的数据
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - int
     - 以16进制打印出来与location配合可以知道数据保存的journal文件名

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_synthetic_data(context, synthetic_data, location, dest):
        context.log.info("on_synthetic_data: {}".format(synthetic_data))

dest举例说明::

    def pre_start(context):
        context.subscribe_operator("bar", "test")

    def on_synthetic_data(context, synthetic_data, location, dest):
        context.log.info("[on_synthetic_data] -----{}, {}, {}".format(location.category, location.group, location.name, hex(dest)))

    # [on_synthetic_data] ----operator, bar, test, 0x0
    # location.category为: "operator" , location.group为 : "bar" ,location.name为: "test" , hex(dest)为 : 0x0
    # 数据存储在kf_home(kungfu\home\runtime\ operator \ bar \ test \journal\live) 中以16进制打印dest的同名文件中 : 00000000.1.journal

on_operator_state_change
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**订阅的算子器状态变化回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - operator_state_update
     - :ref:`OperatorStateUpdate对象 <OperatorStateUpdateOperator对象>`
     - 订阅的其他算子器的状态信息
   * - location
     - :ref:`Location对象 <LocationOperator对象>`
     - 数据的来源是来自哪个进程

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    def on_operator_state_change(context, operator_state_update, location):
        context.log.info("on_operator_state_change {}".format(operator_state_update))


行情交易函数
~~~~~~~~~~~~~

context.subscribe
^^^^^^^^^^^^^^^^^^^^^^

**订阅行情(支持动态订阅)**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source
     - :ref:`Source对象 <SourceOperator对象>`
     - 行情柜台ID
   * - instrument
     - list
     - 代码列表
   * - exchange_id
     - :ref:`Exchange对象 <ExchangeOperator对象>`
     - 交易所ID


返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    # 向source柜台的exchange_id交易所订阅了instruments列表中的合约的行情
    context.subscribe(source, instruments, exchange_id)
    # 例如 : 在行情源柜台为xtp柜台订阅上交所的 600001,600002这两支股票
    # context.subscribe("xtp", ['600001','600002'], "SSE")


context.subscribe_all
^^^^^^^^^^^^^^^^^^^^^^^^^

**订阅全市场行情**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source
     - :ref:`Source对象 <SourceOperator对象>`
     - 行情柜台ID


返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    # 订阅source柜台全市场标的
    context.subscribe_all(source)
    # 例如 xtp的全市场股票
    # context.subscribe_all("xtp")

context.subscribe_operator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**订阅算子器/bar数据**

    注意 : 注意 :算子器的 group 默认为 'default' ； bar数据的 group 为 'bar'

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - group
     - str
     - 组名
   * - name
     - str
     - 名字ID


返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    context.subscribe_operator(group, name)
    # 例如 : 订阅算子id为test的算子器
    # context.subscribe_operator("default", "test")

    # 例如 : 订阅Bar_id为 bar1 的bar数据
    # context.subscribe_operator("bar", "bar1")

context.publish_synthetic_data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**发布算子数据 (给订阅这个算子器的算子/策略发布标识为key，内容为value的数据)**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - key
     - str
     - 标识
   * - value
     - str
     - 内容


返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无

范例::

    context.publish_synthetic_data(key, value)
    # 例如 : 给订阅这个算子器的算子/策略发布标识为'test',内容为"208.43"的数据
    # context.publish_synthetic_data("test", "208.43")

辅助函数
~~~~~~~~~

context.log.info
^^^^^^^^^^^^^^^^^^^^

**输出INFO级别 Log 信息**

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - msg
     - str
     - Log信息

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    context.log.info(msg)


context.log.warning
^^^^^^^^^^^^^^^^^^^^^^^

**输出WARN级别Log信息**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - msg
     - str
     - Log信息

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    context.log.warning(msg)

context.log.error
^^^^^^^^^^^^^^^^^^^^^

**输出ERROR级别Log信息**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - msg
     - str
     - Log信息

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    context.log.error(msg)

context.strftime()
^^^^^^^^^^^^^^^^^^^^^

**时间格式转换 ： 将纳秒级时间戳时间转换成文本时间**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - msg
     - int
     - 时间戳时间

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    context.log.info(" 当前时间是 {} 纳秒".format(context.now()))
    # 当前时间是 1669344957395751800 纳秒
    context.log.info(" 当前时间转换为 文本类型时间 ： {} ".format(context.strftime(context.now())))
    # 当前时间转换为 文本类型时间 ： 2022-11-25 10:55:57.395751800

context.strptime()
^^^^^^^^^^^^^^^^^^^^^

**时间格式转换 ： 将文本时间转换成纳秒级时间戳时间**
注意 ： 文本字符串必须是 "%Y-%m-%d %H:%M:%S." 的格式，注意最后有一个英文句点（.）不要漏掉了 。

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - msg
     - str
     - 文本格式时间

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    context.log.info(" 文本时间转换为时间戳 : {} ".format(context.strptime("2022-11-25 11:04:01.")))
    # 文本时间转换为时间戳 : 1669345441000000000

context.add_timer
^^^^^^^^^^^^^^^^^^^^

**注册时间回调函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - nano
     - long
     - 触发回调的纳秒时间戳
   * - callback
     - object
     - 回调函数

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    # 通过时间回调函数，在1s后撤去订单号为order_id的报单
    context.add_timer(context.now() + 1*1000000000, lambda ctx, event: cancel_order(ctx, order_id))

context.add_time_interval
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**时间间隔回调函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - nano
     - long
     - 触发回调的纳秒时间戳
   * - callback
     - object
     - 回调函数

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - 无
     - 无
     - 无


范例::

    # 通过时间间隔回调函数，每过60s,调用一次func函数
    context.add_time_interval(60 * 1000000000, lambda ctx, event: func(ctx))


常量定义
----------

.. _SourceOperator对象:

Source柜台
~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 值
     - 说明
   * - CTP
     - “ctp“
     - CTP柜台
   * - XTP
     - “xtp“
     - XTP柜台
   * - SIM
     - “sim“
     - SIM柜台

柜台使用方法::

    # 案例示范
    from kungfu.wingchun.constants import Source
    SOURCE = "xtp"
    def pre_start(context):
        context.subscribe_all(SOURCE)

.. _ExchangeOperator对象:

Exchange交易所
~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 值
     - 说明
   * - BSE
     - “BSE”
     - 北交所 (北京证券交易所)
   * - SSE
     - “SSE”
     - 上交所 (上海证券交易所)
   * - SZE
     - “SZE”
     - 深交所 (深圳证券交易所)
   * - SHFE
     - “SHFE”
     - 上期所 (上海期货交易所)
   * - DCE
     - “DCE”
     - 大商所 (大连商品交易所)
   * - CZCE
     - “CZCE”
     - 郑商所 (郑州商品交易所)
   * - CFFEX
     - “CFFEX”
     - 中金所 (中国金融期货交易所)
   * - INE
     - “INE”
     - 能源中心 (上海国际能源交易中心)
   * - GFEX
     - “GFEX”
     - 广期所（广州期货交易所）

交易所使用方法::

    # 案例示范
    from kungfu.wingchun.constants import Exchange
    tickers_sze = ['128145', '000700']
    EXCHANGE_SZE = Exchange.SZE
    tickers_sse = ['688689', '688321']
    EXCHANGE_SSE = Exchange.SSE

    def pre_start(context):
        # 订阅某些深交所股票的行情
        context.subscribe(SOURCE, tickers_sze, EXCHANGE_SZE)
        # 订阅某些上交所股票的行情
        context.subscribe(SOURCE, tickers_sse, EXCHANGE_SSE)

.. _InstrumentTypeOperator对象:

InstrumentType 代码类型
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Unknown
     - 未知
   * - Stock
     - 股票
   * - Future
     - 期货
   * - Bond
     - 债券
   * - StockOption
     - 股票期权
   * - TechStock
     - 科技股
   * - Fund
     - 基金
   * - Index
     - 指数
   * - Repo
     - 回购
   * - CryptoFuture
     - 数字货币期货
   * - CryptoUFuture
     - 数字货币期货U本位
   * - Crypto
     - 数字货币

合约类型判断方法::

      # 案例示范
      from kungfu.wingchun.constants import InstrumentType

      positions = context.get_account_book(SOURCE, ACCOUNT)

      for key in positions.long_positions:
        pos = positions.long_positions[key]
        if pos.instrument_type == InstrumentType.Stock:
            context.log.info("这个ticker的合约类型是股票类型")
        elif pos.instrument_type == InstrumentType.Future:
            context.log.info("这个ticker的合约类型是期货类型")
        elif pos.instrument_type == InstrumentType.Bond:
            context.log.info("这个ticker的合约类型是债券类型")


.. _PriceTypeOperator对象:

PriceType 报单类型
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Limit
     - 限价,通用
   * - Any
     - 市价，通用，对于股票上海为最优五档剩余撤销，深圳为即时成交剩余撤销
   * - FakBest5
     - 上海深圳最优五档即时成交剩余撤销，不需要报价
   * - ForwardBest
     - 仅深圳本方方最优价格申报, 不需要报价
   * - ReverseBest
     - 上海最优五档即时成交剩余转限价，深圳对手方最优价格申报，不需要报价
   * - Fak
     - 股票（仅深圳）即时成交剩余撤销，不需要报价；期货即时成交剩余撤销，需要报价
   * - Fok
     - 股票（仅深圳）市价全额成交或者撤销，不需要报价；期货全部或撤销，需要报价
   * - EnhancedLimit
     - 增强限价盘-港股
   * - AtAuctionLimit
     - 增强限价盘-港股
   * - AtAuction
     - 竞价盘-港股 , 期货(竞价盘的价格就是开市价格)

.. _SideOperator对象:

Side 买卖
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Buy
     - 买
   * - Sell
     - 卖
   * - Lock
     - 锁仓
   * - Unlock
     - 解锁
   * - Exec
     - 行权
   * - Drop
     - 放弃行权
   * - Purchase
     - 申购
   * - Redemption
     - 赎回
   * - Split
     - 拆分
   * - Merge
     - 合并
   * - MarginTrade
     - 融资买入
   * - ShortSell
     - 融券卖出
   * - RepayMargin
     - 卖券还款
   * - RepayStock
     - 买券还券
   * - CashRepayMargin
     - 现金还款
   * - StockRepayStock
     - 现券还券
   * - SurplusStockTransfer
     - 余券划转
   * - GuaranteeStockTransferIn
     - 担保品转入
   * - GuaranteeStockTransferOut
     - 担保品转出

.. _ExecTypeOperator对象:

ExecType 标识
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Unknown
     - 未知
   * - Cancel
     - 撤单
   * - Trade
     - 成交

.. _BsFlagOperator对象:

BsFlag 标识
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Unknown
     - 未知
   * - Buy
     - 买
   * - Sell
     - 卖

.. _LocationOperator对象:

Location 标识
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - mode
     - 交易规则(目前只支持 LIVE,实时交易)
   * - category
     - 类别(TD/MD) (这条数据的来源是 td还是md)
   * - group
     - 柜台id  (比如 : xtp , ctp , sim)
   * - name
     - 对于交易进程(如:on_order,on_trade)是账户名(比如: 123456, 123321 ) , 对于行情进程(如:on_quote)是柜台ID (比如: xtp , sim)
   * - uid
     - mode/category/group/name 组成的字符串的哈希值
   * - uname
     - location的整体信息 (比如 : td/sim/123/live (数据来源是td , 柜台是sim柜台 , 账号是 123 , 交易规则是实时交易) )

例子::

    def on_order(context, order, location):
        context.log.info(
            "[location]  mode{}, category {}, group {}, name {}, uid{}, uname {}".format(
                location.mode, location.category, location.group, location.name, location.uid, location.uname))


.. _BrokerStateOperator对象:

BrokerState 进程连接状态
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Pending
     - 等待中
   * - Idle
     - 无数据
   * - DisConnected
     - 已断开
   * - Connected
     - 已连接
   * - LoggedIn
     - 已登录
   * - LoginFailed
     - 登录失败
   * - Ready
     - 就绪

注意 : Idle只有行情模块有, 连续15秒没有数据就会把前端行情状态设置为Idle, 只在前端显示不通知到策略

.. _OperatorStateOperator对象:

OperatorState 连接状态
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Pending
     - 等待中
   * - DisConnected
     - 已断开
   * - ErrConnectedor
     - 错误连接
   * - Ready
     - 就绪

数据结构
-----------

.. _QuoteOperator对象:

Quote 行情信息
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trading_day
     - str
     - 交易日
   * - data_time
     - long
     - 数据生成时间(交易所时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType对象 <InstrumentTypeOperator对象>`
     - 合约类型
   * - pre_close_price
     - float
     - 昨收价
   * - pre_settlement_price
     - float
     - 昨结价
   * - last_price
     - float
     - 最新价
   * - volume
     - int
     - 数量
   * - turnover
     - float
     - 成交金额
   * - pre_open_interest
     - float
     - 昨持仓量
   * - open_interest
     - float
     - 持仓量
   * - open_price
     - float
     - 今开盘
   * - high_price
     - float
     - 最高价
   * - low_price
     - float
     - 最低价
   * - upper_limit_price
     - float
     - 涨停板价
   * - lower_limit_price
     - float
     - 跌停板价
   * - close_price
     - float
     - 收盘价
   * - settlement_price
     - float
     - 结算价
   * - iopv
     - float
     - 基金实时参考净值
   * - bid_price
     - list of float
     - 申买价
   * - ask_price
     - list of float
     - 申卖价
   * - bid_volume
     - list of float
     - 申买量
   * - ask_volume
     - list of float
     - 申卖量


.. _EntrustOperator对象:

Entrust 逐笔委托
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trading_day
     - str
     - 交易日
   * - data_time
     - long
     - 数据生成时间(交易所时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType对象 <InstrumentTypeOperator对象>`
     - 合约类型
   * - price
     - float
     - 委托价格
   * - volume
     - int
     - 委托量
   * - side
     - :ref:`Side对象 <SideOperator对象>`
     - 委托方向
   * - price_type
     - :ref:`PriceType对象 <PriceTypeOperator对象>`
     - 订单价格类型（市价、限价、本方最优）
   * - main_seq
     - long
     - 主序号
   * - seq
     - long
     - 子序号
   * - orig_order_no
     - int
     - 原始订单号 上海为原始订单号, 深圳为索引号
   * - biz_index
     - int
     - 业务序号


.. _TransactionOperator对象:

Transaction 逐笔成交
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trading_day
     - str
     - 交易日
   * - data_time
     - long
     - 数据生成时间(交易所时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType对象 <InstrumentTypeOperator对象>`
     - 合约类型
   * - price
     - float
     - 成交价
   * - volume
     - int
     - 成交量
   * - bid_no
     - long
     - 买方订单号
   * - ask_no
     - long
     - 卖方订单号
   * - exec_type
     - :ref:`ExecType对象 <ExecTypeOperator对象>`
     - SZ: 成交标识
   * - bs_flag
     - :ref:`BsFlag对象 <BsFlagOperator对象>`
     - 买卖方向
   * - main_seq
     - long
     - 主序号
   * - seq
     - long
     - 子序号
   * - biz_index
     - int
     - 业务序号

.. _SyntheticDataOperator对象:

SyntheticData 订阅的算子器返回数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int
     - 更新时间
   * - key
     - str
     - 订阅的算子器发布的标识
   * - value
     - str
     - 订阅的算子器发布的内容
   * - tag_a
     - str
     - 占位(目前没有用到)
   * - tag_b
     - str
     - 占位(目前没有用到)
   * - tag_c
     - str
     - 占位(目前没有用到)


.. _OperatorStateUpdateOperator对象:

OperatorStateUpdate 订阅的其他算子器状态变化信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - state
     - :ref:`OperatorState对象 <OperatorStateOperator对象>`
     - 连接状态
   * - update_time
     - int
     - 更新时间
   * - location_uid
     - int
     - mode/category/group/name 组成的字符串的哈希值
   * - value
     - str
     - 内容
   * - info_a
     - str
     - 占位(目前没有用到)
   * - info_b
     - str
     - 占位(目前没有用到)

.. _DeregisterOperator对象:

Deregister 断开回调信息
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - mode
     - enums
     - 交易规则(目前只支持 LIVE,实时交易)
   * - category
     - enums
     - 类别(TD/MD) (这条数据的来源是 td还是md)
   * - group
     - str
     - 柜台ID  (比如 : xtp , ctp)
   * - name
     - str
     - 对于交易进程(如:on_order,on_trade)是账户名(比如: 123456, 123321 ) , 对于行情进程(如:on_quote)是柜台ID (比如: xtp , sim)
   * - location_uid
     - int
     - mode/category/group/name 组成的字符串的哈希值

例子::

    def on_deregister(context, deregister, location):
        context.log.info(
            '[on_deregister] {}---{}---{}---{}--{}--{}'.format(deregister, deregister.mode, deregister.category,
                                                       deregister.group, deregister.name,deregister.location_uid))

.. _BrokerStateUpdateOperator对象:

BrokerStateUpdate 客户端状态变化回调信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - location_uid
     - int
     - mode/category/group/name 组成的字符串的哈希值
   * - state
     - :ref:`BrokerState对象 <BrokerStateOperator对象>`
     - 进程连接状态

例子::

    def on_broker_state_change(context, broker_state_update, location):
        context.log.info('[on_broker_state_change] {}--{}'.format(broker_state_update, broker_state_update.state))


