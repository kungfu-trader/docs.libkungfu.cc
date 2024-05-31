c++策略API文档
===============

快速上手
-----------

策略逻辑简介
~~~~~~~~~~~~~~

功夫系统上的策略在策略连接行情交易柜台，发送订阅请求以后，通过以下回调函数给用户发送消息，
用户在不同的回调函数中调用功能函数实现获取行情，下单，时间回调等逻辑。详细数据定义和接口函数定义可查看后文，以下为一个策略示例

**注意 ： c++策略需要先进行加密打包才可以一添加策略的方式运行**
**注意 ： 策略应和功夫安装目录在一个盘符下面，策略文件路径最好不要有空格**
**注意 : 在运行策略之前一定要看下启动的账户柜台进程(td)和行情源柜台进程(md)是否与策略中填写的柜台ID一致**

.. code-block:: cpp
    :linenos:

    #include <kungfu/wingchun/extension.h>
    #include <kungfu/wingchun/strategy/context.h>
    #include <kungfu/wingchun/strategy/strategy.h>
    #include <kungfu/yijinjing/journal/assemble.h>
    #include <kungfu/wingchun/strategy/live.h>
    #include <kungfu/yijinjing/time.h>

    using namespace kungfu::longfist::enums;
    using namespace kungfu::longfist::types;
    using namespace kungfu::wingchun::strategy;
    using namespace kungfu::wingchun::book;
    using namespace kungfu::yijinjing::data;
    using namespace kungfu::yijinjing;

    KUNGFU_MAIN_STRATEGY(KungfuStrategy101) {
    public:
      KungfuStrategy101() = default;
      ~KungfuStrategy101() = default;

      void pre_start(Context_ptr & context) override {
        SPDLOG_INFO("preparing strategy");

        context->add_account("sim", "123456");
        context->subscribe("sim", {"600000"}, {"SSE"});
      }

      void post_start(Context_ptr & context) override { SPDLOG_INFO("strategy started"); }

      void on_quote(Context_ptr & context, const Quote &quote, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("on quote: {}  location->uid {}", quote.last_price, location->location_uid);
        auto oid = context->insert_order(quote.instrument_id, quote.exchange_id, "sim", "123456", quote.last_price, 1000,
                                PriceType::Limit, Side::Buy, Offset::Open, HedgeFlag::Speculation);

        SPDLOG_INFO("oid: {} ", oid);

        int action_id = context->cancel_order(oid);
        SPDLOG_INFO("action_id: {} ", action_id);
      }

      void on_transaction(Context_ptr &context, const Transaction &transaction, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("on transaction: {}", transaction.to_string());
      }

      void on_entrust(Context_ptr &context, const Entrust &entrust, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("on entrust: {}", entrust.to_string());
      }

      void on_order(Context_ptr &context, const Order &order,const location_ptr &location, uint32_t dest) override{
          SPDLOG_INFO("on order: {}", order.to_string());
      }

      void on_trade(Context_ptr &context, const Trade &trade,const location_ptr &location, uint32_t dest) override{
        SPDLOG_INFO("on trade: {}", trade.to_string());
      }

      void on_broker_state_change(Context_ptr & context, const BrokerStateUpdate &brokerStateUpdate, const location_ptr &location) override {
        SPDLOG_INFO("on_broker_state_change: {}", brokerStateUpdate.to_string());
      }

      void pre_stop(Context_ptr &context) override{
        SPDLOG_INFO("pre_stop");
      }

      void post_stop(Context_ptr &context) override{
        SPDLOG_INFO("post_stop");
      }


    };


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性

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


    void pre_start(Context_ptr &context) override{
      SPDLOG_INFO("pre_start");
    }


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性

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

    void post_start(Context_ptr &context) override{
      SPDLOG_INFO("post_start");
    }


pre_stop
^^^^^^^^^^^^

**策略退出前方法** (当关闭策略的时候,策略退出之前调用这个方法)

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性

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

    void pre_stop(Context_ptr &context) override{
      SPDLOG_INFO("pre_stop");
    }

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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性

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

    void post_stop(Context_ptr &context) override{
      SPDLOG_INFO("post_stop");
    }

on_quote
^^^^^^^^^^^

**行情数据的推送会自动触发该方法的调用。**


参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - quote
     - :ref:`Quote对象 <QuoteC对象>`
     - 行情数据
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_quote(Context_ptr & context, const Quote &quote, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on quote: {}", quote.to_string());
    }


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - transaction
     - :ref:`Transaction对象 <TransactionC对象>`
     - 逐笔成交行情数据
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_transaction(Context_ptr &context, const Transaction &transaction, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on transaction: {}", transaction.to_string());
    }

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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - entrust
     - :ref:`Entrust对象 <EntrustC对象>`
     - 逐笔委托行情数据
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_entrust(Context_ptr &context, const Entrust &entrust, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on entrust: {}", entrust.to_string());
    }


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - order
     - :ref:`Order对象 <OrderC对象>`
     - 订单信息更新数据
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_order(Context_ptr &context, const Order &order,const location_ptr &location, uint32_t dest) override{
        SPDLOG_INFO("on order: {}", order.to_string());
    }


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - trade
     - :ref:`Trade对象 <TradeC对象>`
     - 订单成交更新数据
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_trade(Context_ptr &context, const Trade &trade,const location_ptr &location, uint32_t dest) override{
     SPDLOG_INFO("on trade: {}", trade.to_string());
    }


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - history_order
     - :ref:`HistoryOrder对象 <HistoryOrderC对象>`
     - 当日历史委托信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_history_order(Context_ptr &context, const HistoryOrder &history_order, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on_history_order: {}", history_order.to_string());
    }

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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - history_trade
     - :ref:`HistoryTrade对象 <HistoryTradeC对象>`
     - 当日历史订单成交信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_history_trade(Context_ptr &context, const HistoryTrade &history_trade, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on_history_trade: {}", history_trade.to_string());
    }

on_req_history_order_error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**历史订单查询报错回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - error
     - :ref:`RequestHistoryOrderError对象 <RequestHistoryOrderErrorC对象>`
     - 报错信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_req_history_order_error(Context_ptr &context, const RequestHistoryOrderError &error, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on_req_history_order_error: {}", error.to_string());
    }

on_req_history_trade_error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**历史成交查询报错回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - error
     - :ref:`RequestHistoryTradeError对象 <RequestHistoryTradeErrorC对象>`
     - 错误信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_req_history_trade_error(Context_ptr &context, const RequestHistoryTradeError &error, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on_req_history_trade_error: {}", error.to_string());
    }

on_position_sync_reset
^^^^^^^^^^^^^^^^^^^^^^^^^^

**本地交易柜台(TD)的持仓与柜台持仓数据不一致时被调用 (60s同步一次)**

注 : 系统会每60s从柜台同步一次账户持仓,并覆盖本地维护的账户持仓数据.当本地维护的账户持仓列表中任意标的数量或者昨仓信息与柜台的不一致就触发此函数

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - old_book
     - :ref:`book对象 <bookC对象>`
     - 本地维护持仓数据
   * - new_book
     - :ref:`book对象 <bookC对象>`
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

    void on_position_sync_reset(Context_ptr &context, const Book &old_book, const Book &new_book) override {
      SPDLOG_INFO("on_position_sync_reset");
      auto position_old_book = old_book.long_positions;
      auto position_new_book = new_book.long_positions;
      for (auto &longPos : position_old_book) {
        SPDLOG_INFO("old_book {}",longPos.second.volume);
      }
      for (auto &longPos : position_new_book) {
        SPDLOG_INFO("new_book {}",longPos.second.volume);
      }
    }

on_asset_sync_reset
^^^^^^^^^^^^^^^^^^^^

**本地维护账户资金与柜台不一致时被调用 (60s同步一次)**

注 : 系统会每60s从柜台同步一次账户资金信息,并覆盖本地维护的账户资金信息.当本地维护的账户中可用资金或者保证金(期货)与柜台同步的不一致时此函数被调用

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - old_asset
     - :ref:`asset <assetC对象>`
     - 本地维护资金信息
   * - new_asset
     - :ref:`asset <assetC对象>`
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

    void on_asset_sync_reset (Context_ptr &context, const Asset &old_asset, const Asset &new_asset) override {
      SPDLOG_INFO("old_asset: {}", old_asset.to_string());
      SPDLOG_INFO("new_asset: {}", new_asset.to_string());
    }


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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - error
     - :ref:`OrderActionError对象 <OrderActionErrorC对象>`
     - 撤单报错信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_order_action_error(Context_ptr &context, const OrderActionError &error, const location_ptr &location, uint32_t dest) override {
      SPDLOG_INFO("on_order_action_error: {}", error.to_string());
    }

on_deregister
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**交易账户(TD)进程 / 行情(MD)进程断开回调此函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - deregister
     - :ref:`Deregister对象 <DeregisterC对象>`
     - 断开回调信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
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

    void on_deregister(Context_ptr &context, const Deregister &deregister,const location_ptr &location) override {
      SPDLOG_INFO("on_deregister: {}", deregister.to_string());
    }

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
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - broker_state_update
     - :ref:`BrokerStateUpdate对象 <BrokerStateUpdateC对象>`
     - 客户端状态变化回调信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
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

    void on_broker_state_change(Context_ptr &context, const BrokerStateUpdate &brokerStateUpdate,const location_ptr &location) override {
     SPDLOG_INFO("on_broker_state_change: {}", brokerStateUpdate.to_string());
    }

on_synthetic_data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**订阅的算子器发布的数据返回**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - synthetic_data
     - :ref:`SyntheticData对象 <SyntheticDataC对象>`
     - 订阅的算子器发布的数据
   * - location
     - :ref:`Location对象 <LocationC对象>`
     - 数据的来源是来自哪个进程
   * - dest
     - uint32_t
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

    void on_synthetic_data(Context_ptr &context, const SyntheticData &synthetic_data, const location_ptr &location,uint32_t dest) override {
      SPDLOG_INFO("on_synthetic_data: {}", synthetic_data.to_string());
    }

on_operator_state_change
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**订阅的算子器状态变化回调**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - context
     - 对象
     - 策略的全局变量，通过点标记（"->"）来获取其属性
   * - operator_state_update
     - :ref:`OperatorStateUpdate对象 <OperatorStateUpdateC对象>`
     - 订阅的其他算子器的状态信息
   * - location
     - :ref:`Location对象 <LocationC对象>`
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

    void on_operator_state_change(Context_ptr &context, const OperatorStateUpdate &operator_state_update, const location_ptr &location) override {
      SPDLOG_INFO("on_operator_state_change: {}", operator_state_update.to_string());
    }


行情交易函数
~~~~~~~~~~~~~~

context->add_account
^^^^^^^^^^^^^^^^^^^^^^^^^

**添加交易柜台，策略需要先添加账户，才能使用该账户报单**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source
     - str
     - 行情柜台ID
   * - account
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
    context->add_account(source, account)
    # 例如 : 添加账户为123456的xtp柜台
    # context->add_account("xtp", "123456")


context->subscribe
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
   * - source
     - str
     - 行情柜台ID
   * - instrument
     - list
     - 代码列表
   * - exchange_id
     - :ref:`Exchange对象 <ExchangeC对象>`
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

    context->subscribe(source, instruments, exchange_id)
    # 例如 : 
    # context->subscribe("sim", {"600000"}, {"SSE"});


context->subscribe_operator
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

    context->subscribe_operator(group, name)
    # 例如 : 订阅算子id为test的算子器
    # context->subscribe_operator("default", "test")

    # 例如 : 订阅Bar_id为 bar1 的bar数据
    # context->subscribe_operator("bar", "bar1")

context->subscribe_all
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
    context->subscribe_all(source)
    # 例如 xtp的全市场股票
    # context->subscribe_all("xtp")

context->req_history_order
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**查询当天历史委托数据**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source
     - str
     - 行情柜台ID
   * - account
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

    context->req_history_order("xtp","123456",100);


context->req_history_trade
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**查询当天历史成交数据**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - source
     - str
     - 行情柜台ID
   * - account
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

    context->req_history_trade("xtp","123456",100);  


context->insert_order
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
   * - source
     - str
     - 柜台ID
   * - account
     - str
     - 交易账号
   * - limit_price
     - double
     - 价格
   * - volume
     - int
     - 数量
   * - priceType
     - :ref:`PriceType <PriceTypeC对象>`
     - 报单类型
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <OffsetC对象>`
     - 开平方向
   * - hedgeFlag
     - :ref:`HedgeFlag <HedgeFlagC对象>`
     - 投机套保标识
   * - is_swap
     - :ref:`is_swap <IsSwapC对象>`
     - 互换单 (选填,默认为False)
   * - block_id
     - int
     - 大宗交易信息 （不填，默认为0）
   * - parent_id
     - int
     - 母单号 （不填，默认为0）

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - order_id
     - uint64_t
     - 订单ID

范例

    auto oid = context->insert_order(quote.instrument_id, quote.exchange_id, "sim", "123456", quote.last_price, 100,
                              PriceType::Limit, Side::Buy, Offset::Open, HedgeFlag::Speculation);


context->cancel_order
^^^^^^^^^^^^^^^^^^^^^^^^^

**撤单函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - order_id
     - uint64_t
     - 订单ID

返回

.. list-table::
   :width: 600px

   * - 返回
     - 类型
     - 说明
   * - action_id
     - uint64_t
     - 订单操作

范例::

    int action_id = context->cancel_order(order_id);


辅助函数
~~~~~~~~~~~~~~~~~~~~~

info级别日志
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

    SPDLOG_INFO(msg);


warning级别日志
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

    SPDLOG_WARN(msg)

error级别日志
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

    SPDLOG_ERROR(msg)


context->add_timer
^^^^^^^^^^^^^^^^^^^^^^^^^

**注册时间回调函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - nano
     - uint64_t
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

    // 5s后撤单
    context->add_timer(time::now_in_nano() + 5*1e9,[context,order_id](const kungfu::event_ptr &e){
      int action_id = context->cancel_order(order_id);
      SPDLOG_INFO("action_id : {}",action_id);
    });


context->add_time_interval
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**时间间隔回调函数**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - nano
     - uint64_t
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

    // 每10s回调一次
    context->add_time_interval(10 * 1e9,[&](const kungfu::event_ptr &e){
      SPDLOG_INFO("调用add_time_interval 函数");
    });

context->clear_timer()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**取消定时器**

参数

.. list-table::
   :width: 600px

   * - 参数
     - 类型
     - 说明
   * - timer_id
     - int32_t
     - 时间回调函数ID

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

    auto timer_id = context->add_time_interval(10 * 1e9,[&](const kungfu::event_ptr &e){
      SPDLOG_INFO("调用add_time_interval 函数");
    });
    context->clear_timer(timer_id)

context.req_deregister()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**关闭策略进程**

范例::

    context->req_deregister()


投资组合相关功能
~~~~~~~~~~~~~~~~~~~~~

Utils 状态判断
^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - hash_instrument
     - uint64_t
     - 获取账户中某个标的信息对应的key值
   * - is_valid_price
     - bool
     - 判断当前价格是否为有效价格
   * - is_final_status
     - bool
     - 判断当前状态是否为最终状态
   * - get_instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 获取类型

Utils范例::

    SPDLOG_INFO("hash_instrument: {}", kungfu::wingchun::hash_instrument({"SSE"},"600000"));
    
    SPDLOG_INFO("is_valid_price: {}", kungfu::wingchun::is_valid_price(10));
    
    SPDLOG_INFO("is_final_status: {}", kungfu::wingchun::is_final_status(order.status));

    SPDLOG_INFO("get_instrument_type: {}", kungfu::wingchun::get_instrument_type({"SSE"},"600000"));


账户投资组合相关
^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - asset
     - :ref:`asset <assetC对象>`
     - 投资组合资金信息
   * - commissions
     - :ref:`Commission <CommissionC对象>`
     - 获取佣金信息
   * - instruments
     - :ref:`Instrument <InstrumentC对象>`
     - 获取当日可交易标的信息
   * - instrument_factors
     - :ref:`InstrumentFactor <InstrumentFactorC对象>`
     - 获取账户保证金信息
   * - long_positions
     - :ref:`Position <PositionC对象>`
     - 投资组合的持仓列表，对应多头仓位
   * - short_positions
     - :ref:`Position <PositionC对象>`
     - 投资组合的持仓列表，对应空头仓位
   * - orders
     - :ref:`Order <OrderC对象>`
     - 获取订单委托信息
   * - trades
     - :ref:`Trade <TradeC对象>`
     - 获取订单成交信息
   * - order_inputs
     - :ref:`OrderInput <OrderInputC对象>`
     - 获取订单输出信息
   * - has_long_position
     - bool
     - 判断是否为多头仓位
   * - has_short_position
     - bool
     - 判断是否为空头仓位
   * - get_long_position
     - dict
     - 多头持仓信息
   * - get_short_position
     - dict
     - 空头持仓信息


获取投资组合持仓列表范例::

    auto &runtime = dynamic_cast<LiveContext &>(*context);
    auto &bookkeeper = runtime.get_bookkeeper();
    // 获取账户信息
    auto td_location = location::make_shared(mode::LIVE, category::TD, "sim", "123456", std::make_shared<locator>());
    kungfu::wingchun::book::Book_ptr book = bookkeeper.get_book(td_location->uid);
    // 获取账户资金信息
    SPDLOG_INFO("book asset: {}", book->asset.to_string());
    // 获取可用资金
    SPDLOG_INFO("book avail : {}", book->asset.avail);
    // 打印组合投资的多头持仓数量
    for (auto &longPos : book->long_positions)
    {
      SPDLOG_INFO("volumes: {}", longPos.second.volume);
    }

    // 获取当日可交易标的信息
    for (auto &longPos : book->instruments)
    {
      SPDLOG_INFO("instruments: {}", longPos.second.instrument_id);
    };

    // 获取账户保证金信息
    for (auto &longPos : book->instrument_factors)
    {
      SPDLOG_INFO("instrument_factors: {}", longPos.second.instrument_id);
    };

    // 获取佣金信息
    for (auto &longPos : book->commissions)
    {
      SPDLOG_INFO("commissions: {}", longPos.second.to_string());
    };

    // 获取账户订单委托信息
    for (auto &longPos : book->orders)
    {
      SPDLOG_INFO("orders: {}", longPos.second.instrument_id);
    };

    // 获取账户订单成交信息
    for (auto &longPos : book->trades)
    {
      SPDLOG_INFO("trades: {}", longPos.second.instrument_id);
    };

    // 获取账户订单输出信息
    for (auto &longPos : book->order_inputs)
    {
      SPDLOG_INFO("order_inputs: {}", longPos.second.instrument_id);
    };

    SPDLOG_INFO("has_long_position : {}", book->has_long_position("xtp", "123456", {"SSE"}, "600000"));

    SPDLOG_INFO("has_short_position : {}", book->has_short_position("xtp", "123456", {"SSE"}, "600000"));

    SPDLOG_INFO("get_long_position : {}", book->get_long_position("xtp", "123456", {"SSE"}, "600000").to_string());

    SPDLOG_INFO("get_short_position : {}", book->get_short_position("xtp", "123456", {"SSE"}, "600000").to_string());


Orderbook 重建订单簿
^^^^^^^^^^^^^^^^^^^^^^^^^


.. note:: **重建订单簿有何用处？** 

   - **1. 市场深度和流动性分析：** 
   
   重建订单簿可以展示不同价格水平上愿意买卖的订单数量，直观展示市场深度的。有助于评估市场的流动性，特定价格区间内能够吸收多少交易量而不会引起价格显著变动。了解市场深度对于制定交易策略和评估市场冲击成本至关重要。

  
   - **2. 价格发现：** 
  
   订单簿中的买卖订单反映了市场参与者对未来价格的预期和需求。通过分析订单簿，更好地理解价格形成机制以预测价格走势。

   - **3. 交易执行优化：** 
   
   在量化交易中，了解订单簿的状态可以帮助交易算法选择最佳的交易路径和价格，以最小化交易成本。例如，如果订单簿显示买方需求强劲，可考虑以略高于当前市场价格的价格买入，以提高成交概率。

   - **4.  风险管理：** 
   
   通过监控订单簿的变化，可以及时发现潜在的市场异常或流动性枯竭情况，从而采取相应的风险控制措施。


.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - get_bids
     - 获取买单信息
   * - get_asks
     - 获取卖单信息



- **注意**：

   - 只有在行情源提供逐笔行情数据的情况下，才能准确地重建订单簿

   - 将维护从策略开始到策略结束收到的所有逐笔数据


::
  
  订单簿维护规则详解 ( **只适用于Entrust 逐笔委托** ) : 

  当收到一笔新的逐笔数据时,检测当前数据的price和side 是否被记录过，

    1). 若当前数据的价格档位不存在，则将当前数据的volume增加到对应价格档位的volume中

    2). 若当前数据的价格档位已存在。将根据以下规则更新订单簿 : 

      a. 如果当前数据方向（side）为买, 比较当前price和买1价, 如果小于买1价, 直接存储; 进一步与最低要价（卖1价）比较，若大于卖一价则撮合成交。

      b. 如果当前数据方向（side）为卖, 比较当前price和卖1价, 如果大于买1价, 直接存储; 进一步与最高出价（买1价）比较，若小于买一价则撮合成交。

      c. 如果产生撮合且新数据的volume小于买1/卖1单的volume, 此时买1/卖1单的volume会扣除对应数量; 如果大于买/卖单的volume, 原买1单/卖1单的price档位会被消除 ,然后继续和新的买1价(原买2价)和卖1价(原卖2价)进行判断是否会和当前数据发生撮合,如果继续撮合则重复本条逻辑。如果未发生撮合，就把对应的价格和剩余的volume存到买单或者卖单里。
     
      d. 撮合规则 : 新数据为买入方向: 新数据的price >= 卖1价 则触发撮合 ; 新数据为卖出方向: 新数据的price <= 买1价 则触发撮合。

      e. 卖1价 : 当前已存储的卖单信息, 按照价格由低到高排列, 卖1价为当前卖单信息的最低价格

      f. 买1价 : 当前已存储的买单信息, 按照价格由高到低排列, 买1价为当前买单信息的最高价格        

    3). 撤单处理: 

      只有当Transaction的exex_type（成交类型）为Cancel时,买单或卖单才会根据bid_no或者ask_no 减去对应price的volume,  其他类型的Transaction数据不会被处理


示例代码↓::

    #include <kungfu/wingchun/extension.h>
    #include <kungfu/wingchun/orderbook/depthorderbooks.h>
    #include <kungfu/wingchun/orderbook/orderbooks.h>
    #include <kungfu/wingchun/strategy/context.h>
    #include <kungfu/wingchun/strategy/strategy.h>
    #include <kungfu/yijinjing/journal/assemble.h>

    using namespace kungfu::longfist::enums;
    using namespace kungfu::longfist::types;
    using namespace kungfu::wingchun::strategy;
    using namespace kungfu::yijinjing::data;
    using namespace kungfu::wingchun::orderbook;
    int i = 0;
    auto orderbooks = DepthOrderbooks();
    KUNGFU_MAIN_STRATEGY(KungfuStrategy101) {
    public:
      KungfuStrategy101() = default;
      ~KungfuStrategy101() = default;

      void pre_start(Context_ptr & context) override {

        SPDLOG_INFO("preparing strategy");
        context->subscribe("xtp", {"300059"}, {"SZE"});
        context->attach_orderbooks(orderbooks);
      }

      void post_start(Context_ptr & context) override { SPDLOG_INFO("strategy started"); }

      void on_entrust(Context_ptr & context, const Entrust &entrust, const location_ptr &location, uint32_t dest) override {
        
        for (const auto &level : orderbooks.get_bids("300059", "SZE")) {
          SPDLOG_INFO("测试 Buy level: {}", (*it).to_string());
        }

        for (const auto &level : orderbooks.get_asks("300059", "SZE")) {
          SPDLOG_INFO("测试 Sell level: {}", level.to_string());
        }
      }

      void on_transaction(Context_ptr & context, const Transaction &transaction, const location_ptr &location,uint32_t dest) override {
                            
        for (const auto &level : orderbooks.get_bids("300059", "SZE")) {
          SPDLOG_INFO("测试 Buy level: {}", (*it).to_string());
        }

        for (const auto &level : orderbooks.get_asks("300059", "SZE")) {
          SPDLOG_INFO("测试 Sell level: {}", level.to_string());
        }
      };
    };


.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - data_time
     - int64_t
     - 数据生成时间(交易所时间)
   * - price
     - double
     - 价格
   * - volume
     - double
     - 数量


枚举值(enums)
----------------

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


.. _ExchangeC对象:

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


.. _InstrumentTypeC对象:

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


.. _PriceTypeC对象:

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



.. _SideC对象:

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


.. _OffsetC对象:

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


.. _HedgeFlagC对象:

HedgeFlag 投机套保标识
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - Speculation
     - 投机


.. _IsSwapC对象:

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

.. _DirectionC对象:

Direction 多空
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - uint64_t
     - 多
   * - Short
     - 空


.. _OrderStatusC对象:

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
     - 部成部撤
   * - PartialFilledActive
     - 部成交易中
   * - Lost
     - 丢失
   * - Cancelling
     - 待撤
   * - Pause
     - 暂停


.. _ExecTypeC对象:

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

.. _BsFlagC对象:

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


.. _LedgerCategoryC对象:

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


.. _VolumeConditionC对象:

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


.. _TimeConditionC对象:

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
   * - GFS
     - 本节有效
   * - GTD
     - 指定日期前有效
   * - GFA
     - 集合竞价有效
   * - Unknown
     - 未知

.. _LocationC对象:

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


.. _CommissionRateModeC对象:

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

.. _BrokerStateC对象:

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

.. _OperatorStateC对象:

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

.. _HistoryDataTypeC对象:

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


.. _CurrencyC对象:

Currency 币种
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

.. _QuoteC对象:

Quote 行情信息
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - data_time
     - int64_t
     - 数据生成时间(交易所时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - pre_close_price
     - double
     - 昨收价
   * - pre_settlement_price
     - double
     - 昨结价
   * - last_price
     - double
     - 最新价
   * - volume
     - double
     - 数量
   * - turnover
     - double
     - 成交金额
   * - pre_open_interest
     - double
     - 昨持仓量
   * - open_interest
     - double
     - 持仓量
   * - open_price
     - double
     - 今开盘
   * - high_price
     - double
     - 最高价
   * - low_price
     - double
     - 最低价
   * - upper_limit_price
     - double
     - 涨停板价
   * - lower_limit_price
     - double
     - 跌停板价
   * - close_price
     - double
     - 收盘价
   * - settlement_price
     - double
     - 结算价
   * - iopv
     - double
     - 基金实时参考净值
   * - total_bid_volume
     - double
     - 总委托买入量
   * - total_ask_volume
     - double
     - 总委托卖出量
   * - total_trade_num
     - int64_t
     - 总成交笔数   
   * - bid_price
     - array
     - 申买价
   * - ask_price
     - array
     - 申卖价
   * - bid_volume
     - array
     - 申买量
   * - ask_volume
     - array
     - 申卖量


.. _EntrustC对象:

Entrust 逐笔委托
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - data_time
     - int64_t
     - 数据生成时间(交易所时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - price
     - double
     - 委托价格
   * - volume
     - double
     - 委托量
   * - side
     - :ref:`Side <SideC对象>`
     - 委托方向
   * - price_type
     - :ref:`PriceType <PriceTypeC对象>`
     - 订单价格类型（市价、限价、本方最优）
   * - main_seq
     - int64_t
     - 主序号
   * - seq
     - int64_t
     - 子序号
   * - orig_order_no
     - int64_t
     - 原始订单号 上海为原始订单号, 深圳为索引号
   * - biz_index
     - int64_t
     - 业务序号


.. _TransactionC对象:

Transaction 逐笔成交
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - data_time
     - int64_t
     - 数据生成时间(交易所时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - price
     - double
     - 成交价
   * - volume
     - double
     - 成交量
   * - bid_no
     - int64_t
     - 买方订单号
   * - ask_no
     - int64_t
     - 卖方订单号
   * - exec_type
     - :ref:`ExecType <ExecTypeC对象>`
     - SZ: 成交标识
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - main_seq
     - int64_t
     - 主序号
   * - seq
     - int64_t
     - 子序号
   * - biz_index
     - int64_t
     - 业务序号

.. _OrderC对象:

Order 订单回报
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - uint64_t
     - 订单ID
   * - external_order_id
     - str
     - 柜台订单ID
   * - parent_id
     - uint64_t
     - 母单号
   * - insert_time
     - int64_t
     - 订单写入时间(功夫时间)
   * - update_time
     - int64_t
     - 订单更新时间(功夫时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - contract_id
     - str
     - 两融合约唯一标识
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - limit_price
     - double
     - 价格
   * - frozen_price
     - double
     - 冻结价格（市价单冻结价格为0.0）
   * - volume
     - double
     - 数量
   * - volume_left
     - double
     - 剩余数量
   * - tax
     - double
     - 税
   * - commission
     - double
     - 手续费
   * - status
     - :ref:`OrderStatus <OrderStatusC对象>`
     - 订单状态
   * - error_id
     - int32_t
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - is_swap
     - bool
     - 互换单
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <OffsetC对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlagC对象>`
     - 投机套保标识
   * - price_type
     - :ref:`PriceType <PriceTypeC对象>`
     - 价格类型
   * - volume_condition
     - :ref:`VolumeCondition <VolumeConditionC对象>`
     - 成交量类型
   * - time_condition
     - :ref:`TimeCondition <TimeConditionC对象>`
     - 成交时间类型


.. _TradeC对象:

Trade 订单成交
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trade_id
     - uint64_t
     - 成交ID
   * - parent_order_id
     - uint64_t
     - 母单号
   * - external_order_id
     - str
     - 柜台订单ID
   * - external_trade_id
     - str
     - 柜台成交编号ID
   * - order_id
     - uint64_t
     - 订单ID
   * - trade_time
     - int64_t
     - 成交时间(功夫时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - contract_id
     - str
     - 两融合约唯一标识
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <OffsetC对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlagC对象>`
     - 投机套保标识
   * - price
     - double
     - 成交价格
   * - volume
     - double
     - 成交量
   * - tax
     - double
     - 税
   * - commission
     - double
     - 手续费


.. _HistoryOrderC对象:

HistoryOrder 历史订单
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - uint64_t
     - 订单ID
   * - insert_time
     - int64_t
     - 订单写入时间(功夫时间)
   * - update_time
     - int64_t
     - 订单更新时间(功夫时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - external_order_id
     - str
     - 柜台订单ID
   * - contract_id
     - str
     - 两融合约唯一标识
   * - is_last
     - bool
     - 是否为本次查询的最后一条记录
   * - data_type
     - :ref:`HistoryDataType <HistoryDataTypeC对象>`
     - 标记本数据是正常数据, 还是本页最后一条数据, 或者全部数据的最后一条
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - limit_price
     - double
     - 价格
   * - frozen_price
     - double
     - 冻结价格（市价单冻结价格为0.0）
   * - volume
     - double
     - 数量
   * - volume_left
     - double
     - 剩余数量
   * - tax
     - double
     - 税
   * - commission
     - double
     - 手续费
   * - status
     - :ref:`OrderStatus <OrderStatusC对象>`
     - 订单状态
   * - error_id
     - int32_t
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - is_swap
     - bool
     - 互换单
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <OffsetC对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlagC对象>`
     - 投机套保标识
   * - price_type
     - :ref:`PriceType <PriceTypeC对象>`
     - 价格类型
   * - volume_condition
     - :ref:`VolumeCondition <VolumeConditionC对象>`
     - 成交量类型
   * - time_condition
     - :ref:`TimeCondition <TimeConditionC对象>`
     - 成交时间类型


.. _HistoryTradeC对象:

HistoryTrade 历史成交
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - trade_id
     - uint64_t
     - 成交ID
   * - order_id
     - uint64_t
     - 订单ID
   * - trade_time
     - int64_t
     - 成交时间(功夫时间)
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - external_order_id
     - str
     - 柜台订单ID
   * - contract_id
     - str
     - 两融合约唯一标识
   * - external_trade_id
     - str
     - 柜台成交编号ID
   * - is_last
     - bool
     - 是否为本次查询的最后一条记录
   * - data_type
     - :ref:`HistoryDataType <HistoryDataTypeC对象>`
     - 标记本数据是正常数据, 还是本页最后一条数据, 或者全部数据的最后一条
   * - is_withdraw
     - bool
     - 是否是撤单流水
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <OffsetC对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlagC对象>`
     - 投机套保标识
   * - price
     - double
     - 成交价格
   * - volume
     - double
     - 成交量
   * - close_today_volume
     - double
     - 平今日仓量（期货）
   * - tax
     - double
     - 税
   * - commission
     - double
     - 手续费
   * - error_id
     - int32_t
     - 错误ID
   * - error_msg
     - str
     - 错误信息

.. _OrderInputC对象:

OrderInput 订单输出
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - uint64_t
     - 订单ID
   * - parent_id
     - uint64_t
     - 母单号
   * - instrument_id
     - str
     - 合约ID
   * - exchange_id
     - str
     - 交易所ID
   * - contract_id
     - str
     - 两融合约唯一标识
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - limit_price
     - double
     - 价格
   * - frozen_price
     - double
     - 冻结价格
   * - volume
     - double
     - 数量
   * - is_swap
     - bool
     - 互换单
   * - side
     - :ref:`Side <SideC对象>`
     - 买卖方向
   * - offset
     - :ref:`Offset <OffsetC对象>`
     - 开平方向
   * - hedge_flag
     - :ref:`HedgeFlag <HedgeFlagC对象>`
     - 投机套保标识
   * - price_type
     - :ref:`PriceType <PriceTypeC对象>`
     - 价格类型
   * - volume_condition
     - :ref:`VolumeCondition <VolumeConditionC对象>`
     - 成交量类型
   * - time_condition
     - :ref:`TimeCondition <TimeConditionC对象>`
     - 成交时间类型
   * - block_id
     - uint64_t
     - 大宗交易信息id, 非大宗交易则为0
   * - insert_time
     - int64_t
     - 订单写入时间(功夫时间)

.. _RequestHistoryOrderErrorC对象:

RequestHistoryOrderError 历史订单查询报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - error_id
     - int32_t
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - trigger_time
     - int64_t
     - 写入时间

.. _RequestHistoryTradeErrorC对象:

RequestHistoryTradeError 历史成交查询报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - error_id
     - int32_t
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - trigger_time
     - int64_t
     - 写入时间

.. _OrderActionErrorC对象:

OrderActionError 撤单报错信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - order_id
     - uint64_t
     - 订单ID
   * - external_order_id
     - str
     - 撤单原委托柜台订单ID, 新生成撤单委托编号不记录
   * - order_action_id
     - uint64_t
     - 订单操作ID
   * - error_id
     - int32_t
     - 错误ID
   * - error_msg
     - str
     - 错误信息
   * - insert_time
     - int64_t
     - 写入时间

.. _SyntheticDataC对象:

SyntheticData 订阅的算子器返回数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int64_t
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


.. _OperatorStateUpdateC对象:

OperatorStateUpdate 订阅的其他算子器状态变化信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - state
     - :ref:`OperatorState <OperatorStateC对象>`
     - 连接状态
   * - update_time
     - int64_t
     - 更新时间
   * - location_uid
     - int64_t
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

.. _DeregisterC对象:

Deregister 断开回调信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - uint32_t
     - mode/category/group/name 组成的字符串的哈希值


.. _BrokerStateUpdateC对象:

BrokerStateUpdate 客户端状态变化回调信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - location_uid
     - uint32_t
     - mode/category/group/name 组成的字符串的哈希值
   * - state
     - :ref:`BrokerState <BrokerStateC对象>`
     - 进程连接状态


**注意:功夫时间在最开始会以真实时间对时，然后根据cpu震动++，是个单调递增的时间，和真实时间是有差别的。交易所时间和本机时间也会有差别**


.. _assetC对象:

asset 投资组合资金信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int64_t
     - 更新时间(功夫时间)
   * - holder_uid
     - uint64_t
     - 持有人ID
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategoryC对象>`
     - 账户类别
   * - initial_equity
     - double
     - 期初权益
   * - static_equity
     - double
     - 静态权益
   * - dynamic_equity
     - double
     - 动态权益
   * - realized_pnl
     - double
     - 累计收益
   * - unrealized_pnl
     - double
     - 未实现盈亏
   * - market_value
     - double
     - 市值
   * - long_market_value
     - double
     - 融资买入证券市值, 或otc业务市值(多)
   * - short_market_value
     - double
     - 融券卖出证券市值, 或otc业务市值(空)
   * - margin
     - double
     - 保证金占用
   * - long_margin
     - double
     -  融资占用保证金, 或otc业务保证金占用(多)
   * - short_margin
     - double
     - 融券占用保证金, 或otc业务保证金占用(空)
   * - accumulated_fee
     - double
     - 累计手续费
   * - intraday_fee
     - double
     - 当日手续费
   * - frozen_cash
     - double
     - 冻结资金(股票: 买入挂单资金, 期货: 冻结保证金+冻结手续费)
   * - frozen_margin
     - double
     - 冻结保证金(期货)
   * - frozen_fee
     - double
     - 冻结手续费(期货)
   * - position_pnl
     - double
     - 持仓盈亏(期货)
   * - close_pnl
     - double
     - 平仓盈亏(期货)
   * - avail
     - double
     - 可用资金  
   * - long_avail
     - double
     - otc业务可用资金(多)
   * - short_avail
     - double
     - otc业务可用资金(空)
   * - total_asset
     - double
     - 总资产
   * - avail_margin
     - double
     - 可用保证金
   * - long_debt
     - double
     - 融资欠款金额 (融资负债)
   * - short_cash
     - double
     - 融券卖出金额
   * - margin_interest
     - double
     - 融资融券利息
   * - settlement
     - double
     - 融资融券清算资金
   * - credit
     - double
     - 信贷额度
   * - collateral_ratio
     - double
     - 担保比例
   * - total_debt
     - double
     - 总负债
   * - net_assets
     - double
     - 净资产
   * - long_total_debt
     - double
     - 融资总负债（融资欠款+融资利息+融资费用）
   * - short_total_debt
     - double
     - 融券总负债（融券市值+融券利息+融券费用）
   * - gage_buy_fund_available
     - double
     - 担保品买入可用资金
   * - credit_buy_fund_available
     - double
     - 融资融券可用资金
   * - buyredeliver_fund_available
     - double
     - 买券还券可用资金
   * - directrepay_fund_available
     - double
     - 现金还款可用资金

.. _CommissionC对象:

Commission 佣金信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - mode
     - :ref:`CommissionRateMode <CommissionRateModeC对象>`
     - 手续费模式(按照交易额或者交易量)
   * - open_ratio
     - double
     - 开仓费率
   * - close_ratio
     - double
     - 平仓费率
   * - close_today_ratio
     - double
     - 平仓费率
   * - min_commission
     - double
     - 最小手续费

.. _InstrumentC对象:

Instrument 当日可交易标的信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - product_id
     - int8_t
     - 产品ID (品种)
   * - contract_multiplier
     - int32_t
     - 合约乘数
   * - price_tick
     - double
     - 最小变动价位
   * - quantity_unit
     - double
     - 最小数量单位
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
   * - currency
     - - :ref:`Currency <CurrencyC对象>`
     - 币种

.. _InstrumentFactorC对象:

InstrumentFactor 账户保证金信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
     - 交易所ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - product_id
     - int8_t
     - 产品ID (品种)
   * - source_id
     - uint32_t
     - 持仓账户
   * - is_trading
     - bool
     - 当前是否交易
   * - long_margin_ratio
     - double
     - 多头保证金率
   * - short_margin_ratio
     - double
     - 空头保证金率
   * - conversion_rate
     - double
     - 担保品折扣率
   * - exchange_rate
     - double
     - 汇率

.. _PositionCC对象:

Position 持仓信息
~~~~~~~~~~~~~~~~~~~~~

期货持仓

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int64_t
     - 更新时间(功夫时间)
   * - instrument_id
     - str
     - 合约ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - exchange_id
     - str
     - 交易所ID
   * - holder_uid
     - uint32_t
     - 持有人ID
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategoryC对象>`
     - 账户类别
   * - direction
     - :ref:`Direction <DirectionC对象>`
     - 持仓方向
   * - volume
     - double
     - 数量
   * - yesterday_volume
     - double
     - 昨仓数量
   * - frozen_total
     - double
     - 冻结数量
   * - frozen_yesterday
     - double
     - 冻结昨仓
   * - static_yesterday
     - double
     - 固定昨仓数量
   * - open_volume
     - double
     - 今开数量
   * - last_price
     - double
     - 最新价
   * - avg_open_price
     - double
     - 开仓均价
   * - position_cost_price
     - double
     - 持仓成本价
   * - settlement_price
     - double
     - 结算价
   * - pre_settlement_price
     - double
     - 昨结价
   * - margin
     - double
     - 保证金
   * - position_pnl
     - double
     - 持仓盈亏
   * - close_pnl
     - double
     - 平仓盈亏
   * - realized_pnl
     - double
     - 已实现盈亏
   * - unrealized_pnl
     - double
     - 未实现盈亏
   * - source_id
     - int64_t
     - 来源账户
   * - source_op_id
     - int64_t
     - 来源账户 xor holder_uid


股票持仓

.. list-table::
   :width: 600px

   * - 属性
     - 类型
     - 说明
   * - update_time
     - int64_t
     - 更新时间(功夫时间)
   * - instrument_id
     - str
     - 合约ID
   * - instrument_type
     - :ref:`InstrumentType <InstrumentTypeC对象>`
     - 合约类型
   * - exchange_id
     - str
     - 交易所ID
   * - holder_uid
     - uint32_t
     - 持有人ID
   * - ledger_category
     - :ref:`LedgerCategory <LedgerCategoryC对象>`
     - 账户类别
   * - direction
     - :ref:`Direction <DirectionC对象>`
     - 持仓方向
   * - volume
     - double
     - 总持仓量
   * - yesterday_volume
     - double
     - 昨仓数量
   * - frozen_total
     - double
     - 冻结数量
   * - frozen_yesterday
     - double
     - 冻结昨仓
   * - static_yesterday
     - double
     - 固定昨仓数量
   * - open_volume
     - double
     - 今开数量
   * - last_price
     - double
     - 最新价
   * - avg_open_price
     - double
     - 开仓均价
   * - position_cost_price
     - double
     - 持仓成本
   * - close_price
     - double
     - 收盘价
   * - pre_close_price
     - double
     - 昨收价
   * - realized_pnl
     - double
     - 已实现盈亏
   * - unrealized_pnl
     - double
     - 未实现盈亏
   * - source_id
     - int64_t
     - 来源账户
   * - source_op_id
     - int64_t
     - 来源账户 xor holder_uid

**注意 : 对于T+0标的，当前可交易数量为volume总持仓量；对于T+1标的，当前可交易数量为yesterday_volume昨仓数量**

