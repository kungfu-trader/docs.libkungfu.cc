API文档
==========

快速上手
-----------

策略逻辑简介
~~~~~~~~~~~~~~

功夫系统上的策略在策略连接行情交易柜台，发送订阅请求以后，通过以下回调函数给用户发送消息，
用户在不同的回调函数中调用功能函数实现获取行情，下单，时间回调等逻辑。详细数据定义和接口函数定义可查看后文，以下为一个策略示例


**注意 ： 策略应和功夫安装目录在一个盘符下面，策略文件路径最好不要有空格**
**注意 : 在运行策略之前一定要看下启动的账户柜台进程(td)和行情源柜台进程(md)是否与策略中填写的柜台ID一致**

::

    # -*- coding: UTF-8 -*-
    import kungfu.yijinjing.time as kft
    from kungfu.wingchun.constants import *

    # 期货
    # SOURCE = "ctp"
    # ACCOUNT = "089270"
    # tickers = ["rb2001","rb2003"]
    # VOLUME = 2
    # EXCHANGE = Exchange.SHFE

    # 股票柜台
    SOURCE = "xtp"
    # 要链接的账户
    ACCOUNT = "15040910"
    # 准备订阅的标的
    tickers = ["600000", "600001"]
    # 下单数量
    VOLUME = 200
    # 标的对应的交易所
    EXCHANGE = Exchange.SSE


    # 启动前回调，添加交易账户，订阅行情，策略初始化计算等
    def pre_start(context):
        context.add_account(SOURCE, ACCOUNT)
        context.subscribe(SOURCE, tickers, EXCHANGE)


    # 启动准备工作完成后回调，策略只能在本函数回调以后才能进行获取持仓和报单
    def post_start(context):
        context.log.warning("post_start")
        log_book(context, None)


    # 收到快照行情时回调，行情信息通过quote对象获取
    def on_quote(context, quote, location):
        context.log.info("[on_quote] {}".format(quote))
        if quote.instrument_id in tickers:
            # 下单函数
            order_id = context.insert_order(quote.instrument_id, EXCHANGE, SOURCE, ACCOUNT, quote.last_price, VOLUME,
                                            PriceType.Limit, Side.Buy, Offset.Open)
            context.log.info("[order] (rid){} (ticker){}".format(order_id, quote.instrument_id))
            if order_id > 0:
                # 通过添加时间回调，在三秒以后撤单
                context.add_timer(context.now() + 3 * 1000000000, lambda ctx, event: cancel_order(ctx, order_id))


    # 收到订单状态回报时回调
    def on_order(context, order, location):
        context.log.info("[on_order] {}".format(order))


    # 收到成交信息回报时回调
    def on_trade(context, trade, location):
        context.log.info("[on_trade] {}".format(trade))


    def on_position_sync_reset(context, old_book, new_book):
        context.log.warning("on_position_sync_reset ---- {},{}".format(old_book, new_book))


    def on_asset_sync_reset(context, old_asset, new_asset):
        context.log.warning("on_asset_sync_reset ---- {},{}".format(old_asset.avail, new_asset.avail))


    def on_asset_margin_sync_reset(context, old_asset_margin, new_asset_margin):
        context.log.warning("on_asset_margin_sync_reset ---- {},{}".format(old_asset_margin.avail_margin, new_asset_margin.avail_margin))


    # 策略释放资源前回调，仍然可以获取持仓和报单
    def pre_stop(context):
        context.log.info("[before strategy stop]")


    # 策略释放资源后回调
    def post_stop(context):
        context.log.info("[before process stop]")


    # 自定义函数
    # 账户中资金/持仓情况
    def log_book(context, event):
        context.account_book = context.get_account_book(SOURCE, ACCOUNT)

        context.log.warning("账户资金组合信息 {}".format(context.account_book.asset))

        # 账户中多头持仓数据
        long_position = context.account_book.long_positions
        for key in long_position:
            pos = long_position[key]
            context.log.info("多头持仓数据 (instrument_id){} (volume){} (yesterday_volume){} ".format(pos.instrument_id,pos.volume,pos.yesterday_volume))


    # 自定义撤单回调函数
    def cancel_order(context, order_id):
        action_id = context.cancel_order(order_id)
        if action_id > 0:
            context.log.info("[cancel order] (action_id){} (rid){} ".format(action_id, order_id))


策略接口调整对照表
------------------

函数参数变更
~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 功能描述
     - 2.3
     - 2.4
   * - 添加账户,柜台
     - add_account(source_id, account_id, cash_limit)
     - add_account(source_id, account_id)
   * - 下单函数
     - insert_order(instrument_id, Exchange.SSE, account, price, volume, PriceType.Limit, Side.Buy, Offset.Open,HedgeFlag.Speculation)
     - insert_order(instrument_id, Exchange.SSE, source,account, price, volume, PriceType.Limit, Side.Buy, Offset.Open,HedgeFlag.Speculation,is_swap = false)
   * - 行情接收函数
     - on_quote(context, quote)
     - on_quote(context, quote, location)
   * - 逐笔成交行情
     - on_transaction(context, transaction)
     - on_transaction(context, transaction, location)
   * - 逐笔委托行情
     - on_entrust(context, entrust)
     - on_entrust(context, entrust, location)
   * - 订单更新
     - on_order(context, order)
     - on_order(context, order, location)
   * - 订单成交
     - on_trade(context, trade)
     - on_trade(context, trade, location)

新增函数
~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 功能描述
     - 2.3
     - 2.4
   * - 本地交易柜台(TD)的持仓与柜台持仓数据不一致时被调用
     -
     - on_position_sync_reset(context, old_book, new_book)
   * - 本地维护的账户资金与柜台不一致时被调用
     -
     - on_asset_sync_reset(context, old_asset, new_asset)
   * - 本地维护的两融账户资金与柜台不一致时被调用
     -
     - on_asset_margin_sync_reset(context, old_asset_margin, new_asset_margin)
   * - 断开回调
     -
     - on_deregister(context, deregister, location)
   * - 客户端状态变化回调
     -
     - on_broker_state_change(context, broker_state_update, location)
   * - 调用当天历史委托数据
     -
     - context.req_history_order(source_id,account_id,100)
   * - 调用当天历史成交数据
     -
     - context.req_history_trade(source_id,account_id,100)
   * - 当天历史订单委托信息回报
     -
     - on_history_order(context, history_order, location)
   * - 当天历史订单成交信息回报
     -
     - on_history_trade(context, history_trade, location)
   * - 历史订单查询报错回调
     -
     - on_req_history_order_error(context, error, location)
   * - 历史成交查询报错回调
     -
     - on_req_history_trade_error(context, error, location)
   * - 撤单报错信息触发调用
     -
     - on_order_action_error(context, error, location)
   * - 获取可交易标的信息
     -
     - context.get_account_book(SOURCE, ACCOUNT).instruments
   * - 获取佣金信息
     -
     - context.get_account_book(SOURCE, ACCOUNT).commissions

数据结构变更
~~~~~~~~~~~~~~

    **说明 : 下表表示2.3中数据的某些返回信息在2.4删除了,2.4中某些数据结构有新增**

.. list-table::
   :width: 600px

   * - 功能描述
     - 2.3
     - 2.4
   * - Quote 行情信息
     - source_id
     -
   * - Entrust 逐笔委托
     - source_id
     -
   * - Transaction 逐笔成交
     - source_id
     -
   * - Order 订单回报
     - account_id, client_id, volume_traded
     - is_swap, external_order_id, hedge_flag
   * - Trade 订单成交
     - parent_order_id, account_id, client_id, close_today_volume
     - external_order_id, external_trade_id
   * - Position 持仓信息
     - source_id, account_id, client_id
     -
   * - Asset 投资组合资金信息
     - source_id, account_id, client_id, broker_id
     -
   * - AssetMargin 两融相关信息
     - source_id, account_id, client_id, broker_id, margin_instruments, exchanges
     -
   * - HistoryOrder 历史订单委托信息
     -
     - 新增
   * - HistoryTrade 历史订单成交信息
     -
     - 新增
   * - OrderActionError 撤单报错信息
     -
     - 新增
   * - Instrument 可交易标的信息
     -
     - 新增
   * - Commission 佣金信息
     -
     - 新增


函数定义
-----------

基本方法
~~~~~~~~~~~~~~

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
^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^

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
     - :ref:`Quote对象 <Quote对象>`
     - 行情数据
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_quote(context, quote, location):
        context.log.info('[on_quote] {}, {}, {}'.format( quote.instrument_id, quote.last_price, quote.volume))


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
     - :ref:`Transaction对象 <Transaction对象>`
     - 逐笔成交行情数据
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_transaction(context, transaction, location):
        context.log.info('[on_transaction] {}'.format(transaction))


on_entrust
^^^^^^^^^^^^^^^^^

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
     - :ref:`Entrust对象 <Entrust对象>`
     - 逐笔委托行情数据
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_entrust(context, entrust, location):
        context.log.info('[on_entrust] {}'.format( entrust))


on_order
^^^^^^^^^^^^^^^^^

**订单信息的更新会自动触发该方法的调用**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - order
     - :ref:`Order对象 <Order对象>`
     - 订单信息更新数据
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_order(context, order, location):
        context.log.info('[on_order] {}, {}, {}'.format( order.order_id, order.status, order.volume))

on_trade
^^^^^^^^^^^^^^^^^

**策略订单成交信息的更新会自动触发该方法的调用**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - trade
     - :ref:`Trade对象 <Trade对象>`
     - 订单成交更新数据
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_trade(context, trade, location):
        context.log.info('[on_trade] {}, {}, {}'.format(trade.order_id, trade.volume, trade.price))

on_history_order
^^^^^^^^^^^^^^^^^^^^^

**当天历史订单委托信息回报**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - history_order
     - :ref:`HistoryOrder对象 <HistoryOrder对象>`
     - 当日历史订单委托信息
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def post_start(context):
        context.req_history_order(SOURCE,ACCOUNT,100)

    def on_history_order(context, history_order, location):
        context.log.info('[on_history_order] {}'.format(history_order))

on_history_trade
^^^^^^^^^^^^^^^^^^^^

**当天历史订单成交信息回报**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - history_trade
     - :ref:`HistoryTrade对象 <HistoryTrade对象>`
     - 当日历史订单成交信息
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def post_start(context):
        context.req_history_trade(SOURCE,ACCOUNT,100)

    def on_history_trade(context, history_trade, location):
        context.log.info('[on_history_trade] {}'.format(history_trade))

on_req_history_order_error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**历史订单查询报错回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - error
     - :ref:`RequestHistoryOrderError对象 <RequestHistoryOrderError对象>`
     - 当日历史订单委托信息
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_req_history_order_error(context, error, location):
        context.log.info('[on_req_history_order_error] {}'.format(error))

on_req_history_trade_error
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**历史成交查询报错回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - error
     - :ref:`RequestHistoryTradeError对象 <RequestHistoryTradeError对象>`
     - 当日历史订单成交信息
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_req_history_trade_error(context, error, location):
        context.log.info('[on_req_history_trade_error] {}'.format(error))

on_position_sync_reset
^^^^^^^^^^^^^^^^^^^^^^^^^^

**本地交易柜台(TD)的持仓与柜台持仓数据不一致时被调用 (60s同步一次)**

注 : 本地持仓列表中任何标的的数量和昨仓数量与柜台的不一致就触发此函数

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - old_book
     - :ref:`book对象 <book对象>`
     - 本地维护持仓数据
   * - new_book
     - :ref:`book对象 <book对象>`
     - 柜台持仓数据

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

    def on_position_sync_reset(context, old_book, new_book):
        positions_old_book = old_book.long_positions
        for key in positions_old_book:
            pos = positions_old_book[key]
            context.log.info("positions_old_book   (instrument_id){} (direction){} (volume){} (yesterday_volume){} ".format(
                pos.instrument_id,
                pos.direction,
                pos.volume,
                pos.yesterday_volume))

        positions_new_book = new_book.long_positions
        for key in positions_new_book:
            pos = positions_new_book[key]
            context.log.info("positions_new_book   (instrument_id){} (direction){} (volume){} (yesterday_volume){} ".format(
                pos.instrument_id,
                pos.direction,
                pos.volume,
                pos.yesterday_volume))

on_asset_sync_reset
^^^^^^^^^^^^^^^^^^^^

**本地维护账户资金与柜台不一致时被调用 (60s同步一次)**

注 : 本地维护的账户中可用资金/保证金(期货)与柜台不一致时此函数被调用

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - old_asset
     - :ref:`asset <asset对象>`
     - 本地维护资金信息
   * - new_asset
     - :ref:`asset <asset对象>`
     - 柜台资金信息

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

    def on_asset_sync_reset(context, old_asset, new_asset):
        context.log.warning("on_asset_sync_reset ---- {},{}".format(old_asset.avail, new_asset.avail))

on_asset_margin_sync_reset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**本地维护的两融资金与柜台不一致时被调用 (60s同步一次)**

注 : 本地维护的两融账户中 总资产/可用保证金/融资占用保证金/融券占用保证金/总占用保证金/融资负债/融券卖出金额 与柜台不一致时此函数被调用

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - old_asset_margin
     - :ref:`asset_margin <asset_margin对象>`
     - 本地维护资金信息
   * - new_asset_margin
     - :ref:`asset_margin <asset_margin对象>`
     - 柜台资金信息

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

    def on_asset_margin_sync_reset(context, old_asset_margin, new_asset_margin):
        context.log.warning("on_asset_sync_reset ---- {},{}".format(old_asset_margin.avail_margin, new_asset_margin.avail_margin))

on_order_action_error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**撤单报错信息触发调用**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - python对象
     - 策略的全局变量，通过点标记（”.”）来获取其属性
   * - error
     - :ref:`OrderActionError对象 <OrderActionError对象>`
     - 撤单错误信息
   * - location
     - :ref:`Location对象 <Location对象>`
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

    def on_order_action_error(context, error, location):
        context.log.warning("on_order_action_error {}".format(error))

on_deregister
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
     - :ref:`Deregister对象 <Deregister对象>`
     - 断开回调信息
   * - location
     - :ref:`Location对象 <Location对象>`
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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
     - :ref:`BrokerStateUpdate对象 <BrokerStateUpdate对象>`
     - 客户端状态变化回调信息
   * - location
     - :ref:`Location对象 <Location对象>`
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

行情交易函数
~~~~~~~~~~~~~~

context.add_account
^^^^^^^^^^^^^^^^^^^^^^^^^

**添加交易柜台，策略需要先添加账户，才能使用该账户报单**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source_id
     - str
     - 行情柜台ID
   * - account_id
     - str
     - 账户ID

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

    # 添加柜台、账户
    context.add_account(source_id, account_id)
    # 例如 : 添加账户为123456的xtp柜台
    # context.add_account("xtp", "123456")


context.subscribe
^^^^^^^^^^^^^^^^^^^^^^^^^

**订阅行情(支持动态订阅)**

    注意 :

        在pre_start中订阅,策略持仓中此标的的持仓信息会与账户持仓中此标的的持仓信息同步

        在非pre_start中订阅,策略中的此标的持仓信息只维护本策略中的.

        比如 : 账户中有 “600000” , “600008” 标的持仓 , 持仓分别为500 , 600. 在策略的pre_start订阅 “600000” , post_start中订阅”600008”.运行策略 , 分别下单买入100 , 那么 策略持仓中的标的 “600000” , “600008” 持仓信息分别为 : 600 , 100

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source_id
     - str
     - 行情柜台ID
   * - instrument
     - list
     - 代码列表
   * - exchange_id
     - :ref:`Exchange对象 <Exchange对象>`
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
     - str
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

context.req_history_order
^^^^^^^^^^^^^^^^^^^^^^^^^

**查询当天历史委托数据**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source_id
     - str
     - 行情柜台ID
   * - account_id
     - str
     - 交易账户
   * - num
     - int
     - 本次查询数量(不填,返回本次查询最大值)

注意 : num 这个参数只对某些有限制的柜台起效, 对无限制的柜台, 直接查全部的

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
        context.req_history_order(source_id,account_id,100)


context.req_history_trade
^^^^^^^^^^^^^^^^^^^^^^^^^

**查询当天历史成交数据**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source_id
     - str
     - 行情柜台ID
   * - account_id
     - str
     - 交易账户
   * - num
     - int
     - 本次查询数量(不填,返回本次查询最大值)

注意 : num 这个参数只对某些有限制的柜台起效, 对无限制的柜台, 直接查全部的

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
        context.req_history_trade(source_id,account_id,100)


context.insert_order
^^^^^^^^^^^^^^^^^^^^^^^^^

**报单函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - source_id
     - str
     - 柜台ID
   * - account_id
     - str
     - 交易账号
   * - limit_price
     - float
     - 价格
   * - volume
     - int
     - 数量
   * - priceType
     - :ref:`PriceType <PriceType对象>`
     - 报单类型
   * - side
     - :ref:`Side <Side对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <Offset对象>`
     - 开平方向
   * - hedgeFlag
     - :ref:`HedgeFlag <HedgeFlag对象>`
     - 投机套保标识 (选填)
   * - is_swap
     - :ref:`is_swap <IsSwap对象>`
     - 互换单 (选填,默认为False)

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - order_id
     - long
     - 订单ID

范例

    - 通过"xtp"柜台的交易账户acc_1以12.0元的价格买200股浦发银行:

    ::

     context.insert_order("600000", Exchange.SSE, "xtp","acc_1", 12.0, 200, PriceType.Limit, Side.Buy, Offset.Open)


    - 通过"ctp"柜台的交易账户acc_2以3500元的价格开仓买入2手上期所rb1906合约：

    ::

     context.insert_order("rb1906", Exchange.SHFE, "ctp","acc_2", 3500.0, 2, PriceType.Limit, Side.Buy, Offset.Open)


**注（期权）：当买卖方向为：Lock（锁仓）、Unlock（解锁）、Exec（行权）、Drop（放弃行权）时，设定的price（委托价）以及offset（开平方向）都不生效**


context.cancel_order
^^^^^^^^^^^^^^^^^^^^^^^^^

**撤单函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - order_id
     - long
     - 订单ID

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - action_id
     - long
     - 订单操作

范例::

    # 通过context.insert_order函数进行下单，同时用order_id记录下单的订单ID号，然后撤单
    order_id = context.insert_order(quote.instrument_id, exchange, source,account, quote.last_price - 10, volume, PriceType.Limit, Side.Buy, Offset.Open)
    action_id =  context.cancel_order(order_id)

投资组合相关功能
~~~~~~~~~~~~~~~~~~~~~

盈亏及持仓
~~~~~~~~~~~~~~~~~~~~~

功夫系统支持实时维护策略收益及持仓及对应的历史记录，针对不同的应用场景，提供共计四种不同的维护收益及持仓的模式。对于任一策略，具体采用的模式由两个 API 决定：context.hold_book() 及 context.hold_positions()，使用者需要在策略的 pre_start() 方法里决定是否调用这两个方法，系统在 pre_start() 处理完成时会根据是否调用这两个方法对应出的共计四种状态来设置维护收益及持仓的结果。

context.hold_book()
^^^^^^^^^^^^^^^^^^^^^^^^^

**保持策略运行历史上的交易过的标的。缺省设置即没有调用此方法时，系统只会维护当前策略代码中通过 subscribe 方法订阅过的标的；当调用此方法后，系统会在策略启动后，根据该同名策略在历史上的交易情况，构造一份包含所有该同名策略所交易过标的，及当前策略代码中通过 subscribe 订阅的标的的账目。注意此方法仅影响标的列表，对于每个标的的具体持仓数值，是由 hold_positions() 方法来决定。**


范例::

    # 历史曾执行过订阅某些标的
    # context.subscribe(source, ['600000', '600001'], EXCHANGE)

    # 当前代码中重置了 subscribe，且没有调用 context.hold_book()，则该策略只会收到新订阅的标的行情，且账目收益及持仓中只包含新订阅的标的
    context.subscribe(source, ['600002', '600003'], EXCHANGE)

    # 如果调用 hold_book，则该策略订阅行情列表中会自动包含历史记录中有的标的
    #，且账目收益及持仓中也会包含对应标的的数据
    context.hold_book()


context.hold_positions()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**保持账目中每一标的的历史持仓。缺省设置即没有调用此方法时，系统会通过同步柜台查询到的持仓数据来构建策略账目，每次策略启动后，账目中所有标的的持仓都会同步为最新的柜台账户对应的持仓；当调用此方法后，系统会使用功夫内部记录的历史数据来恢复策略的账目持仓。缺省设置保证了策略账目中的持仓数据是绝对准确的，但无法反映功夫运行期间内的策略历史交易情况；如果需要获取之前运行策略时产生的历史持仓记录，则需要通过调用该方法来使系统使用本地存储的历史记录，在这种情况下，当因为各种因素（例如在功夫系统外使用别的软件对同一账户手动交易）都会使得功夫内部维护的持仓记录产生偏差，（例如同一账户下对应的不同策略持仓汇总之和不等于账户总持仓），当发生此类偏差时，建议使用缺省模式来从账户持仓恢复策略持仓。**


范例::

    # 策略账目所包含的持仓标的列表取决于是否调用context.hold_book()，但每个标的的具体持仓数值则由context.hold_positions()来决定，
    # 当缺省即没有调用该方法时，策略启动后的账目中的标的持仓等于所对应账户下的标的持仓：
    context.subscribe(source, ['600000', '600001'], EXCHANGE)

    # 当调用 hold_positions() 方法后，策略启动后的账目中标的持仓等于上次运行策略结束时所对应的标的持仓：
    context.hold_positions()

context.book
^^^^^^^^^^^^^^^^^^^^^^^^^

**策略的投资组合** (当前策略的投资组合信息)

.. list-table::
   :width: 600px

   * - 类型
   * - :ref:`book对象 <book对象>`

范例::

    #获取策略的投资组合，并打印相关参数
    book = context.book
    context.log.warning("[strategy capital] (avail){} (margin){}".format(book.asset.avail, book.asset.margin))

context.get_account_book(SOURCE, ACCOUNT)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**账户的投资组合** (选择的这个柜台的账户的持仓,账户资金等信息)

.. list-table::
   :width: 600px

   * - 类型
   * - :ref:`book对象 <book对象>`


范例::

    #获取账户的投资组合，并打印相关参数
    book = context.get_account_book(SOURCE, ACCOUNT)
    context.log.warning("[account capital] (avail){} (margin){} ".format(book.asset.avail, book.asset.margin))

辅助函数
~~~~~~~~~~~~~~~~~~~~~

context.log.info
^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
-------------

Source柜台
~~~~~~~~~~~~~~~~~

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
    SOURCE = Source.XTP
    # SOURCE = "xtp"
    ACCOUNT = "1111111"
    def pre_start(context):
        # 添加账户柜台信息
        context.add_account(SOURCE, ACCOUNT)


.. _Exchange对象:

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

.. _InstrumentType对象:

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
   * - Warrant
     - 认权证
   * - Iopt
     - 牛熊证
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


.. _PriceType对象:

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

报单类型使用方法::

    # 案例示范
    from kungfu.wingchun.constants import PriceType, Side, Offset

    context.insert_order("600000", Exchange.SSE, "xtp","acc_1", 12.0, 200, PriceType.Limit, Side.Buy, Offset.Open)
    # 通过xtp柜台的交易账户acc_1以12.0元的限价价格买开200股浦发银行


.. _Side对象:

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

买卖方向使用方法::

    # 案例示范
    from kungfu.wingchun.constants import PriceType, Side, Offset

    context.insert_order("600000", Exchange.SSE, "xtp","acc_1", 12.0, 200, PriceType.Limit, Side.Buy, Offset.Open)
    # 通过xtp柜台的交易账户acc_1以12.0元的限价价格买开200股浦发银行


.. _Offset对象:

Offset 开平
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Open
     - 开
   * - Close
     - 平
   * - CloseToday
     - 平今
   * - CloseYesterday
     - 平昨

买卖方向使用方法::

    # 案例示范
    from kungfu.wingchun.constants import PriceType, Side, Offset

    context.insert_order("600000", Exchange.SSE, "xtp", "acc_1", 12.0, 200, PriceType.Limit, Side.Buy, Offset.Open)
    # 通过xtp柜台的交易账户acc_1以12.0元的限价价格买开200股浦发银行

.. _HedgeFlag对象:

HedgeFlag 投机套保标识
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Speculation
     - 投机

**注意 : Python策略中insert_order可以不写这个参数,因为已经默认是投机.c++策略中需要填写**

.. _IsSwap对象:

IsSwap 是否为互换单
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - true
     - 互换单
   * - false
     - 不是互换单

.. _Direction对象:

Direction 多空
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Long
     - 多
   * - Short
     - 空

持仓方向使用方法::

    # 案例示范
    from kungfu.wingchun.constants import Direction

    positions = context.get_account_book(SOURCE, ACCOUNT)

    for key in positions.long_positions:
        pos = positions.long_positions[key]
        if pos.direction == Direction .Long:
            context.log.info("这个ticker的持仓方向 : 多")
        elif pos.direction == Direction .Short:
            context.log.info("这个ticker的持仓方向 : 空")

.. _OrderStatus对象:

OrderStatus 委托状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Unknown
     - 未知
   * - Submitted
     - 已提交
   * - Pending
     - 等待
   * - Cancelled
     - 已撤单
   * - Error
     - 错误
   * - Filled
     - 已成交
   * - PartialFilledNotActive
     - 部分成交不在队列中（部成部撤）
   * - PartialFilledActive
     - 部分成交还在队列中
   * - Lost
     - 丢失

订单状态获取::

    # 案例示范
    from kungfu.wingchun.constants import OrderStatus

    def on_order(context, order):
      if order.status == OrderStatus.Submitted:
          context.log.warning("此时的订单状态为 : 已提交")
      elif order.status == OrderStatus.Pending:
          context.log.warning("此时的订单状态为 : 等待中")
      elif order.status == OrderStatus.Filled:
          context.log.warning("此时的订单状态为 : 已成交")

.. _ExecType对象:

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

.. _BsFlag对象:

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


.. _LedgerCategory对象:

LedgerCategory 标识
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Account
     - 账户投资组合数据
   * - Strategy
     - 策略投资组合数据


.. _VolumeCondition对象:

VolumeCondition 标识
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Any
     - 任何
   * - Min
     - 最小
   * - All
     - 所有


.. _TimeCondition对象:

TimeCondition 标识
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - IOC
     - 立刻成交，否则撤销
   * - GFD
     - 当日有效
   * - GTC
     - 撤单前有效


.. _Location对象:

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
     - 对于交易进程(如:on_order,on_trade)是账户名(比如: 123456, 123321 ) , 对于行情进程(如:on_quote)是柜台id (比如: xtp , sim)
   * - uid
     - mode/category/group/name 组成的字符串的哈希值
   * - uname
     - location的整体信息 (比如 : td/sim/123/live (数据来源是td , 柜台是sim柜台 , 账号是 123 , 交易规则是实时交易) )

例子::

    def on_order(context, order, location):
        context.log.info(
            "[location]  mode{}, category {}, group {}, name {}, uid{}, uname {}".format(
                location.mode, location.category, location.group, location.name, location.uid, location.uname))


.. _CommissionRateMode对象:

CommissionRateMode 手续费模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - ByAmount
     - 交易额
   * - ByVolume
     - 交易量

.. _BrokerState对象:

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


.. _HistoryDataType对象:

HistoryDataType 标识
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Normal
     - 进行
   * - PageEnd
     - 本页结束
   * - TotalEnd
     - 全部结束


.. _CurrencyType对象:

CurrencyType 币种
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Unknown
     - 未知
   * - CNY
     - 人民币
   * - HKD
     - 港币
   * - USD
     - 美元
   * - JPY
     - 日元
   * - GBP
     - 英镑
   * - EUR
     - 欧元
   * - CNH
     - 离岸人民币
   * - SGD
     - 新加坡币
   * - MYR
     - 马来西亚币
   * - CEN
     - 美分


数据结构
-----------

.. _Quote对象:

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
     - 交易所
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
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


.. _Entrust对象:

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
     - 交易所
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - price
     - float
     - 委托价格
   * - volume
     - int
     - 委托量
   * - side
     - Side
     - 委托方向
   * - price_type
     - :ref:`PriceType <PriceType对象>`
     - 订单价格类型（市价、限价、本方最优）
   * - main_seq
     - long
     - 主序号
   * - seq
     - long
     - 子序号
   * - biz_index
     - int
     - 业务序号


.. _Transaction对象:

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
     - 交易所
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
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
     - :ref:`ExecType <ExecType对象>`
     - SZ: 成交标识
   * - bs_flag
     - :ref:`BsFlag <BsFlag对象>`
     - SH: 内外盘标识
   * - main_seq
     - long
     - 主序号
   * - seq
     - long
     - 子序号
   * - biz_index
     - int
     - 业务序号

.. _Order对象:

Order 订单回报
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - long
     - 订单ID
   * - insert_time
     - long
     - 订单写入时间(功夫时间)
   * - update_time
     - long
     - 订单更新时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - external_order_id
     - str
     - 柜台订单id
   * - parent_id
     - int
     - 母单号
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - limit_price
     - float
     - 价格
   * - frozen_price
     - float
     - 冻结价格（市价单冻结价格为0.0）
   * - volume
     - int
     - 数量
   * - volume_left
     - int
     - 剩余数量
   * - tax
     - float
     - 税
   * - commission
     - float
     - 手续费
   * - status
     - :ref:`OrderStatus <OrderStatus对象>`
     - 订单状态
   * - error_id
     - int
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - is_swap
     - bool
     - 互换单
   * - side
     - :ref:`Side <Side对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <Offset对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlag对象>`
     - 投机套保标识
   * - price_type
     - :ref:`PriceType <PriceType对象>`
     - 价格类型
   * - volume_condition
     - :ref:`VolumeCondition <VolumeCondition对象>`
     - 成交量类型
   * - time_condition
     - :ref:`TimeCondition <TimeCondition对象>`
     - 成交时间类型


.. _Trade对象:

Trade 订单成交
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trade_id
     - long
     - 成交ID
   * - order_id
     - long
     - 订单ID
   * - trade_time
     - long
     - 成交时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - external_order_id
     - str
     - 柜台订单id
   * - external_trade_id
     - str
     - 柜台成交编号id
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - side
     - :ref:`Side <Side对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <Offset对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlag对象>`
     - 投机套保标识
   * - price
     - float
     - 成交价格
   * - volume
     - int
     - 成交量
   * - tax
     - float
     - 税
   * - commission
     - float
     - 手续费


.. _HistoryOrder对象:

HistoryOrder 历史订单
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - long
     - 订单ID
   * - insert_time
     - long
     - 订单写入时间(功夫时间)
   * - update_time
     - long
     - 订单更新时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - external_order_id
     - str
     - 柜台订单id
   * - is_last
     - bool
     - 是否为本次查询的最后一条记录
   * - data_type
     - :ref:`HistoryDataType <HistoryDataType对象>`
     - 标记本数据是正常数据, 还是本页最后一条数据, 或者全部数据的最后一条
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - limit_price
     - float
     - 价格
   * - frozen_price
     - float
     - 冻结价格（市价单冻结价格为0.0）
   * - volume
     - int
     - 数量
   * - volume_left
     - int
     - 剩余数量
   * - tax
     - float
     - 税
   * - commission
     - float
     - 手续费
   * - status
     - :ref:`OrderStatus <OrderStatus对象>`
     - 订单状态
   * - error_id
     - int
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - is_swap
     - bool
     - 互换单
   * - side
     - :ref:`Side <Side对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <Offset对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlag对象>`
     - 投机套保标识
   * - price_type
     - :ref:`PriceType <PriceType对象>`
     - 价格类型
   * - volume_condition
     - :ref:`VolumeCondition <VolumeCondition对象>`
     - 成交量类型
   * - time_condition
     - :ref:`TimeCondition <TimeCondition对象>`
     - 成交时间类型


.. _HistoryTrade对象:

HistoryTrade 历史成交
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trade_id
     - long
     - 成交ID
   * - order_id
     - long
     - 订单ID
   * - trade_time
     - long
     - 成交时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - external_order_id
     - str
     - 柜台订单id
   * - external_trade_id
     - str
     - 柜台成交编号id
   * - is_last
     - bool
     - 是否为本次查询的最后一条记录
   * - data_type
     - :ref:`HistoryDataType <HistoryDataType对象>`
     - 标记本数据是正常数据, 还是本页最后一条数据, 或者全部数据的最后一条
   * - is_withdraw
     - bool
     - 是否是撤单流水
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - side
     - :ref:`Side <Side对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <Offset对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlag对象>`
     - 投机套保标识
   * - price
     - float
     - 成交价格
   * - volume
     - int
     - 成交量
   * - close_today_volume
     - int
     - 平今日仓量（期货）
   * - tax
     - float
     - 税
   * - commission
     - float
     - 手续费
   * - error_id
     - int
     - 错误ID
   * - error_msg
     - str
     - 错误信息

.. _RequestHistoryOrderError对象:

RequestHistoryOrderError 历史订单查询报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - error_id
     - int
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - trigger_time
     - int
     - 写入时间

.. _RequestHistoryTradeError对象:

RequestHistoryTradeError 历史成交查询报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - error_id
     - int
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - trigger_time
     - int
     - 写入时间

.. _OrderActionError对象:

OrderActionError 撤单报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - int
     - 订单ID
   * - external_order_id
     - str
     - 撤单原委托柜台订单id, 新生成撤单委托编号不记录
   * - order_action_id
     - int
     - 订单操作ID
   * - error_id
     - int
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - insert_time
     - int
     - 写入时间


.. _Deregister对象:

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
     - 柜台id  (比如 : xtp , ctp)
   * - name
     - str
     - 对于交易进程(如:on_order,on_trade)是账户名(比如: 123456, 123321 ) , 对于行情进程(如:on_quote)是柜台id (比如: xtp , sim)
   * - location_uid
     - int
     - mode/category/group/name 组成的字符串的哈希值

例子::

    def on_deregister(context, deregister, location):
        context.log.info(
            '[on_deregister] {}---{}---{}---{}--{}--{}'.format(deregister, deregister.mode, deregister.category,
                                                       deregister.group, deregister.name,deregister.location_uid))

.. _BrokerStateUpdate对象:

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
     - :ref:`BrokerState <BrokerState对象>`
     - 进程连接状态

例子::

    def on_broker_state_change(context, broker_state_update, location):
        context.log.info('[on_broker_state_change] {}--{}'.format(broker_state_update, broker_state_update.state))


**注意:功夫时间在最开始会以真实时间对时，然后根据cpu震动++，是个单调递增的时间，和真实时间是有差别的。交易所时间和本机时间也会有差别**

Utils
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - hash_instrument
     - long
     - 获取账户中某个标的信息对应的key值
   * - is_valid_price
     - bool
     - 判断当前价格是否为有效价格
   * - is_final_status
     - bool
     - 判断当前状态是否为最终状态
   * - get_instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 获取类型

Utils范例::

    # 案例示范
    from pykungfu import wingchun as wc

    def post_start(context):
        key = wc.utils.hash_instrument("SSE", "600000")
        positions = context.get_account_book("tora", "123456").long_positions
        context.log.warning(
            " 600000 标得的总仓{} , 昨仓{}".format(positions[key].volume, positions[key].yesterday_volume))


    def on_quote(context, quote, location):
        is_valid_price = wc.utils.is_valid_price(quote.last_price)
        context.log.warning("当前价格是否为有效价格 {}".format(is_valid_price))


    def on_order(context, order, location):
        is_valid_status = wc.utils.is_final_status(order.status)
        context.log.warning("当前状态是否为最终状态 {}".format(is_valid_status))


    def post_start(context):
        ticker_instrument_type = wc.utils.get_instrument_type("SSE", "600000")
        context.log.warning("标的的合约类型是 {}".format(ticker_instrument_type))


.. _book对象:

Book 投资组合
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - asset
     - :ref:`asset <asset对象>`
     - 投资组合资金信息
   * - asset_margin
     - :ref:`asset_margin <asset_margin对象>`
     - 两融相关信息
   * - long_positions
     - List of Position
     - 投资组合的持仓列表，对应多头仓位
   * - short_positions
     - List of Position
     - 投资组合的持仓列表，对应空头仓位
   * - commissions
     - :ref:`Commission <Commission对象>`
     - 获取佣金信息
   * - instruments
     - :ref:`Instruments <Instruments对象>`
     - 获取当日可交易标的信息
   * - has_long_position
     - bool
     - 判断是否为多头仓位
   * - has_short_position
     - bool
     - 判断是否为空头仓位
   * - has_position
     - bool
     - 判断是否有仓位
   * - has_position_for
     - bool
     - 判断是否有持仓
   * - get_position_for
     - bool
     - 判断是否有持仓
   * - get_long_position
     - dict
     - 多头持仓信息
   * - get_short_position
     - dict
     - 空头持仓信息
   * - get_position
     - dict
     - 获取多(空)头标的的持仓信息

获取投资组合持仓列表范例::

    def post_start(context):
        context.log.warning("post_start")

        context.account_book = context.get_account_book(SOURCE, ACCOUNT)

        context.log.warning("资金组合信息 {}".format(context.account_book.asset))

        context.log.warning("两融资金组合信息 {}".format(context.account_book.asset_margin))

        # 账户中多头持仓数据
        long_position = context.account_book.long_positions
        for key in long_position:
            pos = long_position[key]
            context.log.info("多头持仓数据 (instrument_id){} (volume){} (yesterday_volume){} ".format(pos.instrument_id,pos.volume,pos.yesterday_volume))

        # 账户中空头持仓数据
        short_position = context.account_book.short_positions
        for key in short_position:
            pos = short_position[key]
            context.log.info("空头持仓数据 (instrument_id){} (volume){} (yesterday_volume){} ".format(pos.instrument_id,pos.volume,pos.yesterday_volume))

        # 获取佣金信息
        commission = context.account_book.commissions
        for key in commission:
            pos = commission[key]
            context.log.info(
                "佣金信息 product_id {}，exchange_id {} ,open_ratio {}  ".format(pos.product_id, pos.exchange_id,
                                                                                pos.open_ratio))

        # 获取当日可交易标得信息
        instrument = context.account_book.instruments
        for key in instrument:
            pos = instrument[key]
            context.log.info(
                "当日可交易标的信息 instrument_id {} , exchange_id {}".format(pos.instrument_id, pos.exchange_id))

        # 判断是否为多头仓位
        context.log.warning("判断是否为多头仓位 {}".format(context.account_book.has_long_position("SSE", "600000")))

        # 判断是否为空头仓位
        context.log.warning("判断是否为空头仓位 {}".format(context.account_book.has_short_position("SHFE", "ag2212")))

        # 判断是否有仓位
        context.log.warning("判断是否有仓位 {}".format(context.account_book.has_position("SSE", "600000")))

        # 获取多(空)头标的的持仓信息
        position = context.account_book.get_position(Direction.Long, Exchange.SSE, "600000")
        context.log.info("多头标的持仓明细  {}".format(position))

        # 获取多(空)头标的的持仓信息
        position = context.account_book.get_position(Direction.Short, Exchange.SHFE, "ag2212")
        context.log.info("空头标的持仓明细  {}".format(position))

        # 多头标的持仓信息
        context.log.warning("多头标的持仓信息 {}".format(context.account_book.get_long_position("SSE", "600000")))

        # 空头标的持仓信息
        context.log.warning("空头标的持仓信息 {}".format(context.account_book.get_short_position("SHFE", "ag2212")))


    def on_quote(context, quote, location):
        context.log.info("[on_quote] {}".format(quote.instrument_id))

        # 判断是否有持仓
        context.log.info("[on_quote] 判断是否有持仓 {}".format(context.account_book.has_position_for(quote)))

        # 多(空)头标的持仓信息
        context.log.info(
            "[on_quote] 多头标的持仓信息 {}".format(context.account_book.get_position_for(Direction.Long, quote)))

        context.log.info(
            "[on_quote] 空头标的持仓信息 {}".format(context.account_book.get_position_for(Direction.Short, quote)))


    def on_order(context, order, location):
        context.log.warning("on_order")

        # 判断是否有持仓
        context.log.info("[on_order] 判断是否有持仓 {}".format(context.account_book.has_position_for(order)))


    def on_trade(context, trade, location):
        context.log.warning("on_trade")

        # 判断是否有持仓
        context.log.info("[on_trade] 判断是否有持仓 {}".format(context.account_book.has_position_for(trade)))

.. _asset对象:

Book.asset 投资组合资金信息
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int
     - 更新时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - holder_uid
     - int
     - 持有人id
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategory对象>`
     - 账户类别
   * - initial_equity
     - float
     - 期初权益
   * - static_equity
     - float
     - 静态权益
   * - dynamic_equity
     - float
     - 动态权益
   * - realized_pnl
     - float
     - 累计收益
   * - unrealized_pnl
     - float
     - 未实现盈亏
   * - avail
     - float
     - 可用资金
   * - market_value
     - float
     - 市值(股票)
   * - margin
     - float
     - 保证金(期货)
   * - accumulated_fee
     - float
     - 累计手续费
   * - intraday_fee
     - float
     - 当日手续费
   * - frozen_cash
     - float
     - 冻结资金(股票: 买入挂单资金), 期货: 冻结保证金+冻结手续费)
   * - frozen_margin
     - float
     - 冻结保证金(期货)
   * - frozen_fee
     - float
     - 冻结手续费(期货)
   * - position_pnl
     - float
     - 持仓盈亏(期货)
   * - close_pnl
     - float
     - 平仓盈亏(期货)

.. _asset_margin对象:

Book.asset_margin 两融相关信息
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int
     - 更新时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - holder_uid
     - int
     - 持有人id
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategory对象>`
     - 账户类别
   * - total_asset
     - float
     - 总资产
   * - avail_margin
     - float
     - 可用保证金
   * - cash_margin
     - float
     - 融资占用保证金
   * - short_margin
     - float
     - 融券占用保证金
   * - margin
     - float
     - 总占用保证金
   * - cash_debt
     - float
     - 融资负债
   * - short_cash
     - float
     - 融券卖出金额
   * - short_market_value
     - float
     - 融券卖出证券市值
   * - margin_market_value
     - float
     - 融资买入证券市值
   * - margin_interest
     - float
     - 融资融券利息
   * - settlement
     - float
     - 融资融券清算资金
   * - commission_ratio
     - float
     - 手续费费率
   * - credit
     - float
     - 信贷额度
   * - collateral_ratio
     - float
     - 担保比例

.. _Commission对象:

Commission 佣金信息
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - product_id
     - str
     - 产品ID (品种)
   * - exchange_id
     - str
     - 交易所
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - mode
     - :ref:`CommissionRateMode <CommissionRateMode对象>`
     - 手续费模式(按照交易额或者交易量)
   * - open_ratio
     - float
     - 开仓费率
   * - close_ratio
     - float
     - 平仓费率
   * - close_today_ratio
     - float
     - 平仓费率
   * - min_commission
     - float
     - 平仓费率

.. _Instruments对象:

Instruments 当日可交易标得信息
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - product_id
     - list of float
     - 产品ID commit by JC
   * - contract_multiplier
     - int
     - 合约乘数
   * - price_tick
     - float
     - 最小变动价位
   * - open_date
     - str
     - 上市日
   * - create_date
     - str
     - 创建日
   * - expire_date
     - str
     - 到期日
   * - delivery_year
     - int
     - 交割年份
   * - delivery_month
     - int
     - 交割月
   * - is_trading
     - bool
     - 当前是否交易
   * - delivery_year
     - bool
     - 两融柜台折算率及保证金率
   * - long_margin_ratio
     - float
     - 多头保证金率
   * - short_margin_ratio
     - float
     - 空头保证金率
   * - conversion_rate
     - float
     - 担保品折扣率


Position 持仓信息
~~~~~~~~~~~~~~~~~~~~~

期货持仓

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int
     - 更新时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - instrument_id
     - str
     - 合约ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - exchange_id
     - str
     - 交易所ID
   * - holder_uid
     - int
     - 持有人id
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategory对象>`
     - 账户类别
   * - direction
     - :ref:`Direction <Direction对象>`
     - 持仓方向
   * - volume
     - int
     - 数量
   * - yesterday_volume
     - int
     - 昨仓数量
   * - frozen_total
     - int
     - 冻结数量
   * - frozen_yesterday
     - int
     - 冻结昨仓
   * - last_price
     - float
     - 最新价
   * - avg_open_price
     - float
     - 开仓均价
   * - position_cost_price
     - float
     - 持仓成本价
   * - settlement_price
     - float
     - 结算价
   * - pre_settlement_price
     - float
     - 昨结价
   * - margin
     - float
     - 保证金
   * - position_pnl
     - float
     - 持仓盈亏
   * - close_pnl
     - float
     - 平仓盈亏
   * - realized_pnl
     - float
     - 已实现盈亏
   * - unrealized_pnl
     - float
     - 未实现盈亏


股票持仓

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int
     - 更新时间(功夫时间)
   * - trading_day
     - str
     - 交易日
   * - instrument_id
     - str
     - 合约ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentType对象>`
     - 合约类型
   * - exchange_id
     - str
     - 交易所
   * - holder_uid
     - int
     - 持有人id
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategory对象>`
     - 账户类别
   * - direction
     - :ref:`Direction <Direction对象>`
     - 持仓方向
   * - volume
     - int
     - 数量
   * - yesterday_volume
     - int
     - 昨仓数量
   * - frozen_total
     - int
     - 冻结数量
   * - frozen_yesterday
     - int
     - 冻结昨仓
   * - last_price
     - float
     - 最新价
   * - avg_open_price
     - float
     - 开仓均价
   * - position_cost_price
     - float
     - 持仓成本
   * - close_price
     - float
     - 收盘价
   * - pre_close_price
     - float
     - 昨收价
   * - realized_pnl
     - float
     - 已实现盈亏
   * - unrealized_pnl
     - float
     - 未实现盈亏

**注意 : 对于T+0标的，当前可交易数量为volume总持仓量；对于T+1标的，当前可交易数量为yesterday_volume昨仓数量**


功夫自带 Python 库
--------------------------------------

::

    name = "aliyun"
    url = "https://mirrors.aliyun.com/pypi/simple"
    default = false
    secondary = true

  [packages]
  black = "~22.3.0"
  nuitka = "~0.9.0"
  pdm = "~1.15.0"
  poetry-core = "^1.0.0"
  scons = "^4.3.0"
  click = "^8.0.0"
  psutil = "^5.9.0"
  tabulate = "^0.8.10"
  numpy = "^1.22.0"
  pandas = "^1.4.0"
  scipy = ">=1.7 <1.8"
  statsmodels = "^0.13.2"
  ordered-set = "^4.0.0"
  pytest = "^7.1.0"
  conan = "^1.49.0"
  pyinstaller = "^5.1"