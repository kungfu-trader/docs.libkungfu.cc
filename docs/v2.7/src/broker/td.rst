交易柜台对接
=============

交易接口基类

.. code-block:: cpp
    :linenos:   

    class Trader : public BrokerService {
    public:
        explicit Trader(BrokerVendor &vendor) : BrokerService(vendor){};

        virtual longfist::enums::AccountType get_account_type() const = 0;

        // 普通委托报单
        virtual bool insert_order(const event_ptr &event) = 0;

        // 预埋单报单
        virtual bool insert_order_trigger(const event_ptr &event);

        // 大宗交易报单
        virtual bool insert_block_order(const event_ptr &event, const longfist::types::BlockMessage &block_message);

        // 批量委托报单
        virtual bool insert_batch_orders(const event_ptr &event, const OrderInputs &order_inputs);

        // 算法单添加
        virtual bool insert_algo_order(const event_ptr &event);

        // 委托撤单(预埋撤单和普通撤单)
        virtual bool cancel_order(const event_ptr &event) = 0;

        // 预埋单撤单
        virtual bool cancel_order_trigger(const event_ptr &event);

        // 算法单删除
        virtual bool cancel_algo_order(const event_ptr &event);

        // 算法单启动/停止
        virtual bool toggle_algo_order(const event_ptr &event);

        // 查询持仓
        virtual bool req_position() = 0;

        // 查询资金
        virtual bool req_account() = 0;

        // 查询预埋单状态
        virtual bool req_order_trigger();

        // 两融合约查询
        virtual bool req_contract();

        // 查询算法单（系统未调用, 最后再确认）
        virtual bool req_algo_order(const event_ptr &event);

        // 查询历史委托
        virtual bool req_history_order(const event_ptr &event);

        // 查询历史成交
        virtual bool req_history_trade(const event_ptr &event);

        // 收到master广播的Band数据会触发该回调, 用于订阅band信道
        virtual void on_band(const event_ptr &event) {}

        // 收到一个TimeKeyValue数据时触发回调
        virtual void on_time_key_value(const event_ptr &event) {}

        // 收到一个策略的Deregister数据时触发回调, 表明Master检测到该进程已经退出
        virtual bool on_strategy_exit(const event_ptr &event);

        // TD启动时处理风控信息
        void on_risk_setting(const longfist::types::RiskSetting &risk_setting);

        // 获取该TD的location uname
        [[nodiscard]] const std::string &get_account_id() const;

        // 获取写入资金Asset的writer
        [[nodiscard]] yijinjing::journal::writer_ptr get_asset_writer() const;

        // 获取写入持仓Position的writer
        [[nodiscard]] yijinjing::journal::writer_ptr get_position_writer() const;

        
        // 启动时第一次获取到的资金Asset写到PUBLIC, 每分钟同步时需要写到SYNC, 调用该函数进行切换
        void enable_asset_sync();

        // 启动时第一次获取到的持仓Position写到PUBLIC, 每分钟同步时需要写到SYNC, 调用该函数进行切换
        void enable_positions_sync();

        [[nodiscard]] const OrderMap &get_orders() const;

        [[nodiscard]] bool has_order(uint64_t order_id) const;

        [[nodiscard]] kungfu::state<longfist::types::Order> &get_order(uint64_t order_id);

        [[nodiscard]] const OrderActionMap &get_order_actions() const;

        [[nodiscard]] bool has_order_action(uint64_t action_id) const;

        [[nodiscard]] kungfu::state<longfist::types::OrderAction> &get_order_action(uint64_t action_id);

        [[nodiscard]] const TradeMap &get_trades() const;

        [[nodiscard]] const OrderTriggerMap &get_order_triggers() const;

        [[nodiscard]] bool has_order_trigger(uint64_t trigger_id) const;

        [[nodiscard]] kungfu::state<longfist::types::OrderTrigger> &get_order_trigger(uint64_t trigger_id);

        [[nodiscard]] const OrderTriggerActionMap &get_order_trigger_actions() const;

        [[nodiscard]] bool has_order_trigger_action(uint64_t action_id) const;

        [[nodiscard]] kungfu::state<longfist::types::OrderTriggerAction> &get_order_trigger_action(uint64_t action_id);

        [[nodiscard]] const AlgoOrderMap &get_algo_orders() const;

        [[nodiscard]] bool has_algo_order(uint64_t algo_order_id) const;

        [[nodiscard]] kungfu::state<longfist::types::AlgoOrder> &get_algo_order(uint64_t algo_order_id);

        [[nodiscard]] const AlgoOrderActionMap &get_algo_order_actions() const;

        [[nodiscard]] uint32_t get_risk_uid() const;

        void disable_recover();

        virtual void on_recover(){};

        [[nodiscard]] bool is_sync_account() const { return sync_account_; }

        void enable_sync_account() { sync_account_ = true; }

        void disable_sync_account() { sync_account_ = false; }

        void try_req_account();

    protected:
        bool disable_recover_ = false;

    private:
        bool sync_asset_ = false;
        bool sync_position_ = false;
        bool sync_account_ = false;
        uint32_t risk_uid_ = 0;

        void on_asset_sync();

        void on_position_sync();

        void recover();

        void recover_from_journal();

        void deal_write_frame();

        void deal_read_frame();

        [[nodiscard]] OrderService &get_order_service();

        [[nodiscard]] const OrderService &get_order_service() const;

        [[nodiscard]] OrderTriggerService &get_order_trigger_service();

        [[nodiscard]] const OrderTriggerService &get_order_trigger_service() const;

        [[nodiscard]] AlgoOrderService &get_algo_order_service();

        [[nodiscard]] const AlgoOrderService &get_algo_order_service() const;
    };


-------------


主要接口
-----------

insert_order
^^^^^^^^^^^^^

普通委托报单

**virtual bool insert_order(const event_ptr &event) = 0;**


收到委托报单输入OrderInput时会调用该函数, 调用 `event->data<OrderInput>()` 获取委托内容, 
将OrderInput中的待报单信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成报单发送.

报单完成后TD需要生成一个Order写回给报单的进程, 通知该笔委托的状态.

API的委托报单接口分为同步和异步两种, 

1. 同步报单: 调用完API下单接口后会立刻获取该委托在柜台服务器的委托编号
    需要立刻建立 <API委托号, order_id> 映射关系, 在收到成交推送后根据此映射生成Trade和修改Order状态
#. 异步报单: 调用完API下单接口后只能获取是否发送报单信息成功
    在API的报单响应回调中才能获取该委托在柜台服务器的委托号, 在报单过程中一般会携带一个本地定义的request_id, 在报单响应中会有request_id和API委托号, 需要在下单时构建好 <request_id, order_id>的映射关系, 在报单响应中根绝request_id找到order_id, 再建立 <API委托号, order_id> 映射关系.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含待报单信息以及来源和触发时间等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 报单成功返回true, 报单失败返回false


范例

.. code-block:: cpp
    :linenos: 

    // 异步报单, ctp的insert_order实现
    bool TraderCTP::insert_order(const event_ptr &event) {
        const OrderInput &input = event->data<OrderInput>();
        SPDLOG_DEBUG("OrderInput: {}", input.to_string());

        int request_id = get_request_id();
        int error_id = 0;
        uint64_t orderRef_key = 0;

        CThostFtdcInputOrderField ctp_input{};
        to_ctp(ctp_input, input);
        strcpy(ctp_input.BrokerID, config_.broker_id.c_str());
        strcpy(ctp_input.InvestorID, config_.account_id.c_str());
        strcpy(ctp_input.OrderRef, std::to_string(++order_ref_).c_str());
        SPDLOG_DEBUG("CThostFtdcInputOrderField: {}", to_string(ctp_input));
        error_id = api_->ReqOrderInsert(&ctp_input, request_id);
        orderRef_key = get_orderRef_key(front_id_, session_id_, ctp_input.OrderRef);

        auto nano = time::now_in_nano();
        auto writer = get_writer(event->source());
        Order &order = writer->open_data<Order>(event->gen_time());
        order_from_input(input, order);
        order.insert_time = nano;
        order.update_time = nano;
        order.time_condition = from_ctp_time_condition(ctp_input.TimeCondition);

        if (error_id != 0) {
            order.error_id = error_id;
            order.status = OrderStatus::Error;
        }

        SPDLOG_DEBUG("Order: {}", order.to_string());
        writer->close_data();
        map_request_id_to_kf_order_id_.insert_or_assign(request_id, uint64_t(input.order_id));
        map_OrderRefKey_to_kf_order_id_.insert_or_assign(orderRef_key, uint64_t(input.order_id));
        map_kf_order_id_to_OrderRef_.insert_or_assign(input.order_id, ctp_input.OrderRef);
        return error_id == 0;
    }

    bool TraderCTP::custom_OnRtnOrder(const CThostFtdcOrderField &ctp_order) {
        SPDLOG_DEBUG("CThostFtdcOrderField: {}", to_string(ctp_order));

        const std::string str_ExchangeID_OrderLocalID =
            make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderLocalID);
        const std::string str_ExchangeID_OrderSysID = make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderSysID);
        // orderRef_key 作为 request_id 中间桥梁的角色, 辅助链接 API委托和order_id
        uint64_t orderRef_key = get_orderRef_key(ctp_order.FrontID, ctp_order.SessionID, ctp_order.OrderRef);
        auto OrderRefKey_iter = map_OrderRefKey_to_kf_order_id_.find(orderRef_key);
        auto ExchangeID_OrderSysID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderSysID);
        auto ExchangeID_OrderLocalID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderLocalID);

        // 系统外订单信息
        if (OrderRefKey_iter == map_OrderRefKey_to_kf_order_id_.end() and
            ExchangeID_OrderSysID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end() and
            ExchangeID_OrderLocalID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            SPDLOG_WARN("external Order with ExchangeID: {}, OrderSysID: {}, OrderLocalID: {}", ctp_order.ExchangeID,
                        ctp_order.OrderSysID, ctp_order.OrderLocalID);
            return generate_external_order(ctp_order);
        }

        uint64_t kf_order_id = 0;
        if (strlen(ctp_order.OrderSysID) != 0 and
            ExchangeID_OrderSysID_iter != map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            // 已经存在 <ExchangeID_OrderSysID, order_id>, 表示撤单或者是重新查询委托状态信息
            kf_order_id = ExchangeID_OrderSysID_iter->second;
        } else if (OrderRefKey_iter != map_OrderRefKey_to_kf_order_id_.end()) {
            // 已经存在 <OrderRefKey, order_id>, 表示本次连接下的单
            kf_order_id = OrderRefKey_iter->second;
        } else if (ExchangeID_OrderLocalID_iter != map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            // 表示系统外委托的第二次推送, 第一次推送时只有 OrderLocalID 没有 OrderLocalID
            kf_order_id = ExchangeID_OrderLocalID_iter->second;
        } else {
            SPDLOG_ERROR("invalidate CThostFtdcOrderField: {}", to_string(ctp_order));
            return false;
        }

        // 该笔报单请求首次到达CTP, 风控通过后返回的第1个OnRtnOrder回报, 此时因为还没有报入到交易所,
        // 所以回报中OrderSysID为空
        if (strlen(ctp_order.OrderSysID) != 0) {
            // 建立 <API委托号, order_id> 映射关系
            map_kf_order_id_to_OrderSysID_.insert_or_assign(kf_order_id, ctp_order.OrderSysID);
            map_ExchangeID_OrderSysID_to_kf_order_id_.insert_or_assign(str_ExchangeID_OrderSysID, kf_order_id);
        }

        if (not has_order(kf_order_id)) {
            SPDLOG_WARN("no order_id {} in orders_", kf_order_id);
            return generate_external_order(ctp_order);
        }

        auto &order_state = get_order(kf_order_id);

        // 订单状态已经处于最终状态了就不再改动, 重连查询的时候会触发该情况
        if (is_final_status(order_state.data.status) and order_state.data.status != longfist::enums::OrderStatus::Lost and
            order_state.data.status != longfist::enums::OrderStatus::Cancelling) {
            return true;
        }

        from_ctp(ctp_order, order_state.data);
        order_state.data.update_time = time::now_in_nano();
        if (has_writer(order_state.dest)) {
            write_to(order_state.data, order_state.dest);
        } else {
            ++try_write_to_order_count;
            try_write_to(order_state.data, order_state.dest, [&]() {
            --try_write_to_order_count;
            try_ready();
            });
        }
        try_deal_trade(str_ExchangeID_OrderSysID);
        return true;
    }


    // 同步报单, xtp的insert_order实现
    bool TraderXTP::insert_order(const event_ptr &event) {
        const OrderInput &input = event->data<OrderInput>();
        SPDLOG_DEBUG("OrderInput: {}", input.to_string());
        XTPOrderInsertInfo xtp_input = {};
        to_xtp(xtp_input, input);

        SPDLOG_DEBUG("XTPOrderInsertInfo: {}", to_string(xtp_input));
        uint64_t order_xtp_id = api_->InsertOrder(&xtp_input, session_id_);
        auto success = order_xtp_id != 0;

        auto nano = yijinjing::time::now_in_nano();
        auto writer = get_writer(event->source());
        Order &order = writer->open_data<Order>(event->gen_time());
        order_from_input(input, order);
        order.external_order_id = std::to_string(order_xtp_id).c_str();
        order.insert_time = nano;
        order.update_time = nano;

        if (success) {
            // 报单成功后直接返回 API委托号, 可以立刻建立 <API委托号, order_id> 映射关系
            map_kf_to_xtp_order_id_.emplace(uint64_t(input.order_id), order_xtp_id);
            map_xtp_to_kf_order_id_.emplace(order_xtp_id, uint64_t(input.order_id));
        } else {
            auto error_info = api_->GetApiLastError();
            order.error_id = error_info->error_id;
            order.error_msg = error_info->error_msg;
            order.status = OrderStatus::Error;
        }

        SPDLOG_DEBUG("Order: {}", order.to_string());
        writer->close_data();
        if (not success) {
            SPDLOG_ERROR("fail to insert order {}, error id {}, {}", to_string(xtp_input), (int)order.error_id,
                        order.error_msg);
        }
        return success;
    }


----------------------------------


insert_order_trigger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

预埋单下单报单

**virtual bool insert_order_trigger(const event_ptr &event);**


收到预埋单输入OrderTriggerInput时会调用该函数, 调用 `event->data<OrderTriggerInput>()` 获取预埋单内容.

将OrderTriggerInput中的待报预埋单信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成报预埋单发送.

报单完成后TD需要生成一个OrderTrigger写回给报单的进程, 通知预埋单的状态.

.. 通常api的报预埋单是同步接口, 会直接返回报预埋单结果, 需要对该值做处理, 最终将api报预埋单的执行结果以bool形式返回.
.. 将OrderTrigger写回给调用报单的进程实例.
.. 同时, 为了后续交易所报撤单以及成交回报返回时能够与本地记录做好映射, 因此通常会在此维护一些map存储相关标识信息.




参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含待报预埋单信息以及来源和触发时间等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 预埋报单成功返回true, 预埋报单失败返回false


范例

.. code-block:: cpp
    :linenos: 

    // ctp的预埋下单为异步接口, 在响应接口才能获取到预埋单委托号 ParkedOrderID
    bool TraderCTP::insert_order_trigger(const event_ptr &event) {
        const OrderTriggerInput &trigger_input = event->data<OrderTriggerInput>();
        SPDLOG_DEBUG("OrderTriggerInput: {}", trigger_input.to_string());

        int request_id = get_request_id();
        int error_id = 0;
        uint64_t orderRef_key = 0;

        //  预埋单
        CThostFtdcParkedOrderField ctp_parked_input{};
        to_ctp_parked(ctp_parked_input, trigger_input);
        strncpy(ctp_parked_input.GTDDate,
                yijinjing::time::strftime(trigger_input.insert_time, KUNGFU_TRADING_DAY_FORMAT).c_str(), 9);
        SPDLOG_DEBUG("insert_order ctp_parked_input. trigger.insert_time={}, GTDDate: {}", trigger_input.insert_time,
                    ctp_parked_input.GTDDate);
        strcpy(ctp_parked_input.BrokerID, config_.broker_id.c_str());
        strcpy(ctp_parked_input.InvestorID, config_.account_id.c_str());
        strcpy(ctp_parked_input.OrderRef, std::to_string(++order_ref_).c_str());
        ctp_parked_input.RequestID = request_id;
        SPDLOG_DEBUG("CThostFtdcParkedOrderField: {}", to_string(ctp_parked_input));
        error_id = api_->ReqParkedOrderInsert(&ctp_parked_input, request_id);
        orderRef_key = get_orderRef_key(front_id_, session_id_, ctp_parked_input.OrderRef);

        auto nano = time::now_in_nano();
        auto writer = get_writer(event->source());
        OrderTrigger &trigger = writer->open_data<OrderTrigger>(event->gen_time());
        order_trigger_from_input(trigger_input, trigger);
        trigger.insert_time = nano;
        trigger.update_time = nano;
        trigger.time_condition = from_ctp_time_condition(ctp_parked_input.TimeCondition);

        if (error_id != 0) {
            trigger.error_id = error_id;
            trigger.status = OrderStatus::Error;
        }

        SPDLOG_DEBUG("OrderTrigger: {}", trigger.to_string());
        writer->close_data();
        map_request_id_to_kf_order_id_.insert_or_assign(request_id, uint64_t(trigger.trigger_id));
        map_OrderRefKey_to_kf_order_id_.insert_or_assign(orderRef_key, uint64_t(trigger.trigger_id));
        return error_id == 0;
    }

    // ctp预埋下单响应
    bool TraderCTP::custom_OnRspParkedOrderInsert(const CThostFtdcParkedOrderField &ParkedOrder,
                                              const CThostFtdcRspInfoField &RspInfo, int nRequestID, bool bIsLast) {
        SPDLOG_DEBUG("CThostFtdcParkedOrderField: {}", to_string(ParkedOrder));
        SPDLOG_DEBUG("CThostFtdcRspInfoField: {}", to_string(RspInfo));
        SPDLOG_DEBUG("nRequestID: {}, bIsLast: {}", nRequestID, bIsLast);

        auto trigger_id_iter = map_request_id_to_kf_order_id_.find(nRequestID);
        if (trigger_id_iter == map_request_id_to_kf_order_id_.end()) {
            SPDLOG_ERROR("CANNOT FIND trigger_id of {} in map_request_id_to_kf_order_id_", nRequestID);
            return false;
        }

        auto trigger_id = trigger_id_iter->second;
        if (not has_order_trigger(trigger_id)) {
            SPDLOG_ERROR("CANNOT FIND tigger_id {} in triggers_", trigger_id);
            return false;
        }

        auto &trigger_state = get_order_trigger(trigger_id);
        map_trigger_id_to_ParkedOrderID_.insert_or_assign(trigger_id,
                                                            std::pair<std::string, bool>{ParkedOrder.ParkedOrderID, false});
        map_ParkedOrderId_to_trigger_id_.insert_or_assign(ParkedOrder.ParkedOrderID, trigger_id);
        trigger_state.data.status = parked_status_to_trigger_status(ParkedOrder.Status);
        strncpy(trigger_state.data.external_trigger_id, ParkedOrder.ParkedOrderID, strlen(ParkedOrder.ParkedOrderID));
        trigger_state.data.error_id = RspInfo.ErrorID;
        const std::string msg = gbk2utf8(RspInfo.ErrorMsg);
        strncpy(trigger_state.data.error_msg, msg.c_str(), msg.length());
        trigger_state.data.update_time = time::now_in_nano();

        if (RspInfo.ErrorID != 0) {
            trigger_state.data.status = OrderStatus::Error;
            SPDLOG_ERROR("failed to insert order, ErrorId: {} ErrorMsg: {}, parked_order: {}", RspInfo.ErrorID,
                        gbk2utf8(RspInfo.ErrorMsg), to_string(ParkedOrder));
        }

        try_write_to(trigger_state.data, trigger_state.dest);
        SPDLOG_DEBUG("OrderTrigger: {}", trigger_state.data.to_string());

        return true;
    }


.. note::

   预埋下单一般是在休盘时间报单, 委托信息挂在ctp服务器上, 当开盘时自动将委托信息提交到交易所.

   在预埋单开盘触发前可以撤销, 但是开盘触发后, 不论下单是否成功, ctp都不会推送预埋单的状态信息, 需要手动查询才能获取预埋单的最新状态信息.


-----------------------------------------------


insert_block_order
^^^^^^^^^^^^^^^^^^^^^^^^^^^

大宗交易报单

**virtual bool insert_block_order(const event_ptr &event, const longfist::types::BlockMessage &block_message);**


大宗交易报单和普通委托报单类似, 委托信息存在event->data<OrderInput>()里, 区别是多了和大宗交易相关的额外信息BlockMessage, 
按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成报大宗单发送.

报单完成后TD需要生成一个Order写回给报单的进程, 通知该笔委托的状态.

.. 通常api的报大宗单是同步接口, 会直接返回报大宗单结果, 需要对该值做处理, 最终将api报大宗单的执行结果以bool形式返回.
.. 接下来将Order写回给调用报单的进程实例.
.. 同时, 为了后续交易所报撤单以及成交回报返回时能够与本地记录做好映射, 因此通常会在此维护一些map存储相关标识信息.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含待报大宗单信息以及来源和触发时间等信息
    * - block_message
      - const longfist::types::BlockMessage &
      - 包含待报对手方席位号以及成交约定号等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 大宗报单成功返回true, 大宗报单失败返回false


范例

.. code-block:: cpp
    :linenos: 

    // 金证股票柜台的大宗交易报单
    bool TraderMaCli::insert_block_order(const event_ptr &event, const longfist::types::BlockMessage &block_message) {
        const OrderInput &order_input = event->data<OrderInput>();
        SPDLOG_DEBUG("OrderInput Message : {}", order_input.to_string());

        const int64_t request_id = get_request_id();
        auto nano = kungfu::yijinjing::time::now_in_nano();
        auto writer = get_writer(event->source());
        Order &order = writer->open_data<Order>(event->gen_time());
        order_from_input(order_input, order);
        set_offset(order);
        order.status = OrderStatus::Pending;
        order.insert_time = nano;
        order.update_time = nano;

        map_request_to_order_.emplace(request_id, order.order_id);

        CReqStkOrderField stField{};
        auto iter_maStkUserLoginFiled = map_maszStkbd_to_maStkUserLoginFiled_.find(
            kf_to_macli_exchange_id(order_input.exchange_id, stField.szStkbd));  
        if (iter_maStkUserLoginFiled == map_maszStkbd_to_maStkUserLoginFiled_.end()) {
            const std::string msg = "找不到和交易板块" + std::string(stField.szStkbd) + "对应的用户下单信息, 无法下单";
            SPDLOG_ERROR("找不到和交易板块{}对应的用户下单信息, 无法下单", stField.szStkbd);
            order.status = OrderStatus::Error;
            order.error_id = -1;
            strncpy(order.error_msg, msg.c_str(), msg.length());
            SPDLOG_DEBUG("Order: {}", order.to_string());
            writer->close_data();
            return false;
        }
        const CRspStkUserLoginField &login_filed = iter_maStkUserLoginFiled->second;
        stField.llCuacctCode = login_filed.llCuacctCode;                                     
        stField.llCustCode = login_filed.llCustCode;                                         
        strncpy(stField.szTrdacct, login_filed.szStkTrdacct, 20);                            
        strncpy(stField.szStkCode, order_input.instrument_id, 8);                            
        strncpy(stField.szOrderPrice, std::to_string(order_input.limit_price).c_str(), 21);  
        stField.llOrderQty = order_input.volume / get_vol_multi(order_input.exchange_id,
                                                                get_instrument_type(order_input.exchange_id,
                                                                                    order_input.instrument_id));  
        if (order_input.instrument_type == InstrumentType::Repo) {
            if (order_input.side != Side::Sell) {
            order.status = OrderStatus::Error;
            order.error_id = -1;
            strncpy(order.error_msg, "逆回购只能以Sell方式下单", ERROR_MSG_LEN);
            SPDLOG_DEBUG("Order: {}", order.to_string());
            writer->close_data();
            return false;
            }
            stField.iStkBiz = 165;  
        } else {
            stField.iStkBiz = kf_to_macli_iStkBiz(order_input.side); 
        }
        stField.iStkBizAction = kf_to_macli_iStkBizAction(order_input); 
        strncpy(stField.szClientInfo, cust_trace_info_.c_str(), 256);   
        stField.chSecurityLevel = '1';                                          
        int iOrderBsn = int(order_input.order_id & 0x0000FFFF);  
        stField.iOrderBsn = iOrderBsn;                           
        stField.iCuacctSn = iCuacctSn_;                          

        /// 大宗交易需要额外填写的信息
        if (order_input.block_id != 0) {
            stField.llMatchNo = block_message.match_number;  // 成交约定号
            std::string str_REDUCT = block_message.is_specific ? "REDUCT=1" : "REDUCT=0";
            stField.iStkBiz = kf_to_macli_block_iStkBiz(order_input);
            strncpy(stField.szOpptStkpbu, block_message.opponent_seat, 8);
            strncpy(stField.szOrderText, str_REDUCT.c_str(), 256);
        }

        SPDLOG_DEBUG("CReqStkOrderField: {}", to_string(stField));
        int ret = api_->ReqOrder(&stField, request_id);
        SPDLOG_DEBUG("ReqOrder ret: {}", ret);
        if (0 != ret) {
            const std::string msg = gbk2utf8(api_->GetLastErrorText());
            SPDLOG_ERROR("下单失败, return code: {}, error msg: {}", ret, msg);
            order.status = OrderStatus::Error;
            order.error_id = ret;
            strncpy(order.error_msg, msg.c_str(), msg.length());
        }

        SPDLOG_DEBUG("Order: {}", order.to_string());
        writer->close_data();
        return 0 == ret;
    }


.. note::

   大部分柜台的大宗交易报单和普通委托报单是同一个委托函数, 委托响应函数也相同, 区别只是是否填写了大宗交易相关的信息: 对手方席号, 成交约定号, 是否受限(特定)股份



-----------------------------------------


insert_batch_orders
^^^^^^^^^^^^^^^^^^^^^^^^^^^

批量委托报单

**virtual bool insert_batch_orders(const event_ptr &event, const OrderInputs &order_inputs);**

有的柜台可能会有流控限制, 发送消息的数量有限制, 如果需要一次性报很多笔委托, 需要用到批量委托接口, 
待报批量单信息将会存在order_inputs中, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成报批量单发送.


.. 通常api的报批量单是同步接口, 会直接返回报批量单结果, 需要对该值做处理, 最终将api报批量单的执行结果以bool形式返回.
.. 将批量单中每一笔对应的Order写回给调用报单的进程实例.
.. 同时, 为了后续交易所报撤单以及成交回报返回时能够与本地记录做好映射, 因此通常会在此维护一些map存储相关标识信息.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含待报批量单来源和触发时间等信息
    * - order_inputs
      - const OrderInputs &
      - 包含待报批量单的信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 批量报单成功返回true, 批量报单失败返回false


范例

.. code-block:: cpp
    :linenos: 

    // 华锐股票柜台批量委托报单
    bool TraderAtp::insert_batch_orders(const event_ptr &event, const broker::OrderInputs &order_inputs) {
        SPDLOG_DEBUG("insert_batch_orders");
        auto writer = get_writer(event->source());
        std::vector<uint64_t> orderids{};
        ATPReqBatchCashAuctionOrderMsg msg{};
        int64_t nano = time::now_in_nano();
        OrderInput first_order = order_inputs.front();
        for (const OrderInput &order_input : order_inputs) {
            APIBatchCashAuctionOrderUnit unit{};
            strcpy(unit.security_id, order_input.instrument_id);              
            kf_exchange_2_hr_market(order_input.exchange_id, unit.market_id); 
            kf_side_2_hr_side(order_input.side, unit.side);                   
            unit.order_qty = ATPTradeAPI::DoubleExpandToInt(
                double(order_input.volume) /
                    get_vol_multi(order_input.instrument_id, order_input.exchange_id, order_input.instrument_type),
                2); 
            unit.price = ATPTradeAPI::DoubleExpandToInt(order_input.limit_price, 4);
            kf_price_type_2_hr_order_type(order_input.price_type, unit.order_type); 
            kf_exchange_2_hr_market(order_input.exchange_id, msg.market_id);        
            msg.order_array.push_back(unit);
            SPDLOG_DEBUG("APIBatchCashAuctionOrderUnit: {}", to_string(unit));

            auto &order = writer->open_data<Order>(event->gen_time());
            order_from_input(order_input, order);
            order.insert_time = nano;
            order.update_time = nano;
            order.status = OrderStatus::Pending;
            SPDLOG_DEBUG("Order: {}", order.to_string());
            writer->close_data();
            orderids.push_back(order.order_id);
        }

        strcpy(msg.security_id, first_order.instrument_id); 
        kf_exchange_2_hr_market(first_order.exchange_id,
                                msg.market_id);                 
        msg.side = ATPSideConst::kBuy;                          
        msg.order_qty = ATPTradeAPI::DoubleExpandToInt(100, 2);         
        msg.price = ATPTradeAPI::DoubleExpandToInt(10, 4);
        msg.order_type = ATPOrdTypeConst::kOptimalFiveLevelFullDealTransferCancel; 

        strcpy(msg.cust_id, cust_id_.c_str());                           
        strcpy(msg.fund_account_id, td_config_.fund_account_id.c_str()); 
        strcpy(msg.branch_id, td_config_.branch_id.c_str());             
        msg.client_seq_id = get_client_seq_id();                        
        msg.order_way = order_way_;                
        strcpy(msg.password, str_cipher_.c_str()); 
        msg.client_feature_code = str_trace_info_; 

        switch (msg.market_id) {
        case ATPMarketIDConst::kShangHai:
            strcpy(msg.account_id, sh_account_id_.c_str());
            break;
        case ATPMarketIDConst::kShenZhen:
            strcpy(msg.account_id, sz_account_id_.c_str());
            break;
        default:
            SPDLOG_ERROR("Invalidated market_id : {}", msg.market_id);
        }
        msg.batch_type = ATPBatchTypeConst::kBatch; 
        // 将华锐批量成交的id与kongfu的批量orderid相对应, 先添加map信息, 防止回调回来过快找不到对应的order_ids
        map_client_to_orderids_.emplace(msg.client_seq_id, orderids);  
        SPDLOG_DEBUG("ATPReqBatchCashAuctionOrderMsg: {}", to_string(msg));
        int ret = atp_trader_api_ptr_->ReqBatchCashAuctionOrder(&msg); 
        SPDLOG_DEBUG("ReqBatchCashAuctionOrder return code : {} , return message : {}", ret,
                    map_error_code.try_emplace(ret).first->second);
        if (ret != ErrorCode::kSuccess) {
            SPDLOG_ERROR("FAILED TO INSERT ORDER ！");
            return false;
        }
        return true;
    }

    // 华锐股票柜台批量委托回调
    bool TraderAtp::custom_OnRspOrderStatusInternalAck(const BufferATPRspOrderStatusAckMsg &internal_ack) {
        // 优先检测是否属于批量单
        auto order_ids_iter = map_client_to_orderids_.find(internal_ack.client_seq_id);
        if (order_ids_iter != map_client_to_orderids_.end()) {
            std::vector<uint64_t> &orderids = order_ids_iter->second;
            if (orderids.empty()) {
            SPDLOG_ERROR("orderids of client_seq_id: {} is empty", internal_ack.client_seq_id);
            return false;
            }
            uint64_t order_id = orderids.front();
            map_kf_orderid_to_hr_cl_ord_no_.emplace(order_id, internal_ack.cl_ord_no);
            map_hr_cl_ord_no_to_kf_orderid_.emplace(internal_ack.cl_ord_no, order_id);
            orderids.erase(orderids.begin());

            if (not has_order(order_id)) {
            SPDLOG_WARN("order_id: {} not in orders_", order_id);
            generate_real_time_external_order(internal_ack);
            return false;
            }

            auto &order_state = get_order(order_id);

            if (not is_final_status(order_state.data.status) or order_state.data.status == OrderStatus::Lost) {
            hr_order_status_ack_2_kf_order(internal_ack, order_state.data);
            // const std::string str_cl_ord_no = std::to_string(internal_ack.cl_ord_no);
            // strncpy(order_state.data.external_order_id, str_cl_ord_no.c_str(), str_cl_ord_no.length());
            if (order_state.data.status == OrderStatus::Error) {
                order_state.data.error_id = internal_ack.reject_reason_code;
                strncpy(order_state.data.error_msg,
                        map_error_code.try_emplace(internal_ack.reject_reason_code).first->second.c_str(), ERROR_MSG_LEN);
            }
            order_state.data.update_time = time::now_in_nano();
            if (OrderStatus ::Pending != order_state.data.status and has_writer(order_state.dest)) {
                get_writer(order_state.dest)->write(order_state.data.update_time, order_state.data);
            } else {
                SPDLOG_WARN("no writer of {}:{}", order_state.dest, get_vendor().get_location_uname(order_state.dest));
                SPDLOG_WARN("batch Order: {}", order_state.data.to_string());
            }
            SPDLOG_DEBUG("batch Order:{}", order_state.data.to_string());
            }
            try_deal_TradeERMsgs_(internal_ack.cl_ord_no);
            return false;
        }
        // 余下为普通委托处理代码
    }


-------------------------------------------



.. insert_algo_order
.. ^^^^^^^^^^^^^^^^^^^^^^^


.. **virtual bool insert_algo_order(const event_ptr &event);**

.. 依据order_inputs中的输入信息完成向券商柜台报批量单.

.. 策略或者前端下批量单后, 待报批量单信息将会存在order_inputs中.
.. 将order_inputs中的待报批量单信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成报批量单发送.
.. 通常api的报批量单是同步接口, 会直接返回报批量单结果, 需要对该值做处理, 最终将api报批量单的执行结果以bool形式返回.
.. 将批量单中每一笔对应的Order写回给调用报单的进程实例.
.. 同时, 为了后续交易所报撤单以及成交回报返回时能够与本地记录做好映射, 因此通常会在此维护一些map存储相关标识信息.


.. 参数

.. .. list-table::
..     :width: 600px

..     * - 参数
..       - 类型
..       - 说明
..     * - event
..       - const event_ptr &
..       - 包含待报批量单来源和触发时间等信息
..     * - order_inputs
..       - const OrderInputs &
..       - 包含待报批量单的信息


.. 返回值

.. .. list-table::
..    :width: 600px

..    * - 类型
..      - 说明
..    * - bool
..      - 批量报单成功返回true, 批量报单失败返回false


.. 范例

.. .. code-block:: cpp
..     :linenos: 



cancel_order
^^^^^^^^^^^^^^^^^^^^

普通撤单和预埋撤单

**virtual bool cancel_order(const event_ptr &event) = 0;**

event->data<OrderAction>()中有一个OrderActionFlag枚举值, 表明是普通撤单还是预埋撤单.

按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成撤单发送.

若撤单失败, 需要写一个OrderActionError给调用撤单的进程, 说明失败原因.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含待撤单信息以及来源和触发时间等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 撤单成功返回true, 撤单失败返回false


范例

.. code-block:: cpp
    :linenos: 

    // CTP撤单实现
    bool TraderCTP::cancel_order(const event_ptr &event) {
        const OrderAction &action = event->data<OrderAction>();
        SPDLOG_DEBUG("order_action: {}", action.to_string());
        int request_id = get_request_id();
        int error_id = 0;

        auto fn_generate_error = [&](const std::string &msg) -> bool {
            auto writer = get_writer(event->source());
            OrderActionError &error = writer->open_data<OrderActionError>(event->gen_time());
            error.error_id = -1;
            error.order_id = action.order_id;
            error.order_action_id = action.order_action_id;
            strncpy(error.error_msg, msg.c_str(), msg.length());
            SPDLOG_ERROR("OrderActionError: {}", error.to_string());
            writer->close_data();
            return false;
        };

        auto OrderSysID_iter = map_kf_order_id_to_OrderSysID_.find(action.order_id);
        auto OrderRef_iter = map_kf_order_id_to_OrderRef_.find(action.order_id);
        if (OrderSysID_iter == map_kf_order_id_to_OrderSysID_.end() and OrderRef_iter == map_kf_order_id_to_OrderRef_.end()) {
            const std::string msg = fmt::format("FAILED TO CANCEL order {}, can't find related ctp order id", action.order_id);
            return fn_generate_error(msg);
        }

        if (not has_order(action.order_id)) {
            SPDLOG_ERROR("no kf_order_id {} in orders_", action.order_id);
            const std::string msg = fmt::format("{} not in orders_, try again later!", action.order_id);
            return fn_generate_error(msg);
        }

        auto &order_state = get_order(action.order_id);
        map_request_id_to_kf_order_id_.insert_or_assign(request_id, action.order_id);
        map_request_id_to_kf_action_id_.insert_or_assign(request_id, action.order_action_id);

        // 普通撤单
        if (action.action_flag == OrderActionFlag::Cancel) {
            CThostFtdcInputOrderActionField ctp_action{};
            strcpy(ctp_action.BrokerID, config_.broker_id.c_str());
            strcpy(ctp_action.InvestorID, config_.account_id.c_str());
            ctp_action.FrontID = front_id_;
            ctp_action.SessionID = session_id_;
            ctp_action.ActionFlag = THOST_FTDC_AF_Delete;
            strcpy(ctp_action.InstrumentID, order_state.data.instrument_id);
            strcpy(ctp_action.ExchangeID, order_state.data.exchange_id);
            strcpy(ctp_action.OrderSysID, order_state.data.external_order_id);
            if (OrderRef_iter != map_kf_order_id_to_OrderRef_.end()) {
            strncpy(ctp_action.OrderRef, OrderRef_iter->second.c_str(), OrderRef_iter->second.length());
            }
            SPDLOG_DEBUG("CThostFtdcInputOrderActionField: {}", to_string(ctp_action));
            error_id = api_->ReqOrderAction(&ctp_action, request_id);

            if (not is_final_status(order_state.data.status)) {
            order_state.data.status = OrderStatus::Cancelling;
            try_write_to(order_state.data, order_state.dest);
            }
            SPDLOG_DEBUG("Order: {}", order_state.data.to_string());
            return error_id == 0;
        }

        // 预埋撤单
        if (action.action_flag == OrderActionFlag::TriggerCancel) {
            CThostFtdcParkedOrderActionField ctp_parked_input_action{};
            strcpy(ctp_parked_input_action.InstrumentID, order_state.data.instrument_id);
            strcpy(ctp_parked_input_action.ExchangeID, order_state.data.exchange_id);
            ctp_parked_input_action.ActionFlag = THOST_FTDC_AF_Delete;
            strcpy(ctp_parked_input_action.BrokerID, config_.broker_id.c_str());
            strcpy(ctp_parked_input_action.InvestorID, config_.account_id.c_str());
            strcpy(ctp_parked_input_action.UserID, config_.account_id.c_str());
            strcpy(ctp_parked_input_action.OrderSysID, order_state.data.external_order_id);
            if (OrderRef_iter != map_kf_order_id_to_OrderRef_.end()) {
            strncpy(ctp_parked_input_action.OrderRef, OrderRef_iter->second.c_str(), OrderRef_iter->second.length());
            }
            SPDLOG_DEBUG("CThostFtdcParkedOrderActionField: {}", to_string(ctp_parked_input_action));
            error_id = api_->ReqParkedOrderAction(&ctp_parked_input_action, request_id);

            auto nano = time::now_in_nano();
            auto writer = get_writer(event->source());
            OrderTrigger &trigger = writer->open_data<OrderTrigger>(event->gen_time());
            trigger.trigger_id = action.order_action_id;
            order_trigger_from_order(order_state.data, trigger);
            trigger.insert_time = nano;
            trigger.update_time = nano;

            if (error_id != 0) {
            trigger.error_id = error_id;
            trigger.status = OrderStatus::Error;
            }

            SPDLOG_DEBUG("OrderTrigger: {}", trigger.to_string());
            writer->close_data();

            return error_id == 0;
        }

        SPDLOG_ERROR("Unrecognized action_flag: {}", action.action_flag);

        return false;
    }


.. note::
    普通撤单会触发委托推送, 和普通下单类似.

    预埋撤单是在休盘时间提交, 开盘后立刻撤单, 同预埋下单一样, 触发前可以撤销, 触发后需要手动查询. 



----------------------------------


cancel_order_trigger
^^^^^^^^^^^^^^^^^^^^^^^^^


预埋单撤销

**virtual bool cancel_order_trigger(const event_ptr &event);**

根据event->data<OrderTriggerAction>()的trigger_id找到对应的预埋单委托号, 
按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成撤单发送.


如果撤单失败, 需要写一个OrderTriggerActionError给调用报单的进程, 说明失败原因.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含待撤预埋单信息以及来源和触发时间等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 撤预埋单成功返回true, 撤预埋单失败返回false


范例

.. code-block:: cpp
    :linenos: 

    bool TraderCTP::cancel_order_trigger(const event_ptr &event) {
        const OrderTriggerAction &action = event->data<OrderTriggerAction>();
        SPDLOG_DEBUG("OrderTriggerAction: {}", action.to_string());

        auto parked_id_iter = map_trigger_id_to_ParkedOrderID_.find(action.trigger_id);
        if (parked_id_iter == map_trigger_id_to_ParkedOrderID_.end()) {
            SPDLOG_ERROR("CANNOT FIND trigger_id {} in map_trigger_id_to_ParkedOrderID_", action.trigger_id);
            return false;
        }

        const std::pair<std::string, bool> &str_parked_pair = parked_id_iter->second;
        int request_id = get_request_id();
        int error_id = 0;

        auto fn_generate_error = [&](int32_t error_id, const std::string &msg) -> bool {
            auto writer = get_writer(event->source());
            OrderTriggerActionError &error = writer->open_data<OrderTriggerActionError>(event->gen_time());
            error.error_id = error_id;
            error.trigger_id = action.trigger_id;
            error.order_trigger_action_id = action.order_trigger_action_id;
            strncpy(error.external_trigger_id, str_parked_pair.first.c_str(), str_parked_pair.first.length());
            strncpy(error.error_msg, msg.c_str(), msg.length());
            error.insert_time = time::now_in_nano();
            SPDLOG_ERROR("OrderTriggerActionError: {}", error.to_string());
            writer->close_data();
            return false;
        };

        // ParkedOrderId 是空的说明下预埋单的时候是失败的, 响应函数返回的ParkedOrderId是空
        if (str_parked_pair.first.empty()) {
            return fn_generate_error(-1, "待删除的OrderTrigger没有对应的ParkedId");
        }

        if (str_parked_pair.second) {
            // 删除预埋撤单
            CThostFtdcRemoveParkedOrderActionField ctp_remove_parked_order_action{};
            strcpy(ctp_remove_parked_order_action.BrokerID, config_.broker_id.c_str());
            strcpy(ctp_remove_parked_order_action.InvestorID, config_.account_id.c_str());
            strcpy(ctp_remove_parked_order_action.InvestUnitID, config_.account_id.c_str());
            strcpy(ctp_remove_parked_order_action.ParkedOrderActionID, str_parked_pair.first.c_str()); /// 预埋撤单编号
            SPDLOG_DEBUG("CThostFtdcRemoveParkedOrderActionField: {}", to_string(ctp_remove_parked_order_action));
            error_id = api_->ReqRemoveParkedOrderAction(&ctp_remove_parked_order_action, request_id);
        } else {
            // 删除预埋下单
            CThostFtdcRemoveParkedOrderField ctp_remove_parked_order{};
            strcpy(ctp_remove_parked_order.BrokerID, config_.broker_id.c_str());
            strcpy(ctp_remove_parked_order.InvestorID, config_.account_id.c_str());
            strcpy(ctp_remove_parked_order.InvestUnitID, config_.account_id.c_str());
            strcpy(ctp_remove_parked_order.ParkedOrderID, str_parked_pair.first.c_str());
            SPDLOG_DEBUG("CThostFtdcRemoveParkedOrderField: {}", to_string(ctp_remove_parked_order));
            error_id = api_->ReqRemoveParkedOrder(&ctp_remove_parked_order, request_id);
        }

        if (error_id != 0) {
            return fn_generate_error(error_id, "删除预埋单出错");
        }

        auto &trigger_state = get_order_trigger(action.trigger_id);
        trigger_state.data.update_time = time::now_in_nano();
        trigger_state.data.status = OrderStatus::Cancelling;
        try_write_to(trigger_state.data, trigger_state.dest);

        return true;
    }


.. note::
    撤销预埋单成功之后, 需要手动查询预埋单才能获取预埋单的最新状态. 



----------------------------------


req_position
^^^^^^^^^^^^^^^^^^^^

查询持仓

**virtual bool req_position() = 0;**

向券商柜台查询账户当前持仓, TD进程进入就绪状态是会触发该函数, 同时系统也会每分钟自动触发一次查询以同步最新的持仓状态.

将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成持仓查询发送.

有的柜台支持同步查询和异步查询, 有的柜台只支持同步查询.



参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - 无
      - 无
      - 无


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 查询持仓成功返回true, 查询持仓失败返回false


范例

.. code-block:: cpp
    :linenos:


    // xtp 异步查询持仓
    bool TraderXTP::req_position() {
        SPDLOG_INFO("req_position");
        return api_->QueryPosition(nullptr, session_id_, get_request_id()) == 0;
    }

    bool TraderXTP::custom_OnQueryPosition(const XTPQueryStkPositionRsp &position, const XTPRI &error_info, int request_id,
                                       bool is_last, uint64_t session_id) {
        if (error_info.error_id != 0) {
            SPDLOG_ERROR("error_id:{}, error_msg: {}, request_id: {}, last: {}", error_info.error_id, error_info.error_msg,
                        request_id, is_last);
            return false;
        }

        SPDLOG_TRACE("XTPQueryStkPositionRsp: {}", to_string(position));
        auto writer = get_position_writer(); // 第一次获取writer是写入到PUBLIC
        Position &stock_pos = writer->open_data<Position>(0);
        from_xtp(position, stock_pos);
        stock_pos.holder_uid = get_home_uid();
        stock_pos.source_id = get_home_uid();
        stock_pos.instrument_type = get_instrument_type(stock_pos.exchange_id, stock_pos.instrument_id);
        stock_pos.direction = Direction::Long;
        stock_pos.update_time = yijinjing::time::now_in_nano();
        SPDLOG_TRACE("Position: {}", stock_pos.to_string());
        writer->close_data();
        if (is_last) {
            PositionEnd &end = writer->open_data<PositionEnd>(0);
            end.holder_uid = get_home_uid();
            writer->close_data();
            enable_positions_sync(); // 调用该函数后, 之后每分钟同步一次的查询获取到的writer是写入到SYNC
        }
        return true;
    }


    // 顶点股票柜台只支持同步查询
    bool TraderItp::req_position() {
        long nRet = 1;
        bool update = false;
        int64 idx = 0;
        auto writer = get_position_writer();
        while (nRet > 0) {
            vector<ITPDK_ZQGL> arZqgl;
            arZqgl.reserve(200); // 需要预分配足够空间，查询结果最大返回200条
            nRet =
                (long)SECITPDK_QueryPositions(get_account_id().c_str(), SORT_TYPE_AES,
                                            200, idx, "", "", "", 1, arZqgl);
            SPDLOG_TRACE("req_position success. Num of results {}", nRet);
            for (auto &itr : arZqgl) {
            idx = itr.BrowIndex;
            if (get_account_id() == itr.AccountId) {
                update = true;
                auto &pos = writer->open_data<Position>(0);
                //        SPDLOG_DEBUG("exchange {} instrumentid {}", itr.Market,
                //        itr.StockCode);
                from_itp(itr, pos);
                pos.holder_uid = get_home_uid();
                pos.source_op_id = get_home_uid();
                pos.source_id = get_home_uid();
                pos.ledger_category = LedgerCategory::Account;
                writer->close_data();
                SPDLOG_TRACE("req_position: {}", pos.to_string());
                SPDLOG_TRACE("req_position StockName:{} -- "
                            "AccountId:{}; StockCode:{}; CurrentQty:{}; BrowIndex:{}; "
                            "DiluteCostPrice:{}; AvgBuyPrice: {}; "
                            "CostBalance: {}",
                            gbk2utf8(itr.StockName), itr.AccountId, itr.StockCode,
                            (long)itr.CurrentQty, (long)itr.BrowIndex,
                            itr.DiluteCostPrice, itr.AvgBuyPrice, itr.CostBalance);
            }
            }
            idx++;
        }
        if (update) {
            auto &end = writer->open_data<PositionEnd>(now());
            end.holder_uid = get_home_uid();
            writer->close_data();
            enable_positions_sync();
        }
        return true;
    }


-----------------------------


req_account
^^^^^^^^^^^^^^^^^^^^

查询资金

**virtual bool req_account() = 0;**

向券商柜台查询账户当前资金, TD进程进入就绪状态是会触发该函数, 同时系统也会每分钟自动触发一次查询, 每7秒内如果有成交也会触发一次查询, 以同步最新的资金.

将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成持仓查询发送.

有的柜台支持同步查询和异步查询, 有的柜台只支持同步查询.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - 无
      - 无
      - 无


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 查询资金成功返回true, 查询资金失败返回false


范例

.. code-block:: cpp
    :linenos:

    
    // xtp 异步查询资金
    bool TraderXTP::req_account() {
        SPDLOG_INFO("req_account");
        return api_->QueryAsset(session_id_, get_request_id()) == 0;
    }

    bool TraderXTP::custom_OnQueryAsset(const XTPQueryAssetRsp &asset, const XTPRI &error_info, int request_id,
                                    bool is_last, uint64_t session_id) {
        if (error_info.error_id != 0) {
            SPDLOG_ERROR("error_id: {}, error_msg: {}, request_id: {}, last: {}", error_info.error_id, error_info.error_msg,
                        request_id, is_last);
        }

        if (error_info.error_id == 0 || error_info.error_id == 11000350) {
            SPDLOG_TRACE("OnQueryAsset: {}", to_string(asset));
            auto writer = get_asset_writer();
            Asset &account = writer->open_data<Asset>(0);
            if (error_info.error_id == 0) {
            from_xtp(asset, account);
            }
            account.holder_uid = get_live_home_uid();
            account.update_time = yijinjing::time::now_in_nano();
            SPDLOG_TRACE("Asset: {}", account.to_string());
            writer->close_data();
            enable_asset_sync();
        }
        return true;
    }

    // 顶点股票柜台只支持同步查询
    bool TraderItp::req_account() {
        vector<ITPDK_ZJZH> arZjzh;
        arZjzh.reserve(5);
        long nRet = (long)SECITPDK_QueryFundInfo(get_account_id().c_str(), arZjzh);
        if (nRet < 0) // 查询失败
        {
            // itp_update_broker_state(BrokerState::DisConnected);
            string msg = SECITPDK_GetLastError();
            SPDLOG_ERROR("req_account failed. Msg: {}", gbk2utf8(msg));
            return false;
        } else {
            SPDLOG_TRACE("req_account success. Num of results {}", nRet);
            for (auto &itr : arZjzh) {
            SPDLOG_TRACE("FundAccount:{};AccountId:{} -- "
                        "MoneyType:{};FundAvl:{};FrozenBalance:{};TotalAsset:{};"
                        "MarketValue:{}",
                        itr.FundAccount, itr.AccountId, itr.MoneyType, itr.FundAvl,
                        itr.FrozenBalance, itr.TotalAsset, itr.MarketValue);
            if (strcmp(itr.AccountId, get_account_id().c_str()) ==
                0 /* && strcmp(itr.FundAccount, fund_id_.c_str()) == 0*/) {
                auto writer = get_asset_writer();
                auto &asset = writer->open_data<Asset>(0);
                memset(&asset, 0, sizeof(Asset));
                asset.update_time = yijinjing::time::now_in_nano();
                asset.avail = itr.FundAvl;
                asset.frozen_cash = itr.FrozenBalance;
                asset.holder_uid = get_home_uid();
                asset.ledger_category = LedgerCategory::Account;
                writer->close_data();
                enable_asset_sync();
                return true;
            }
            }
        }
        return false;
    }


-----------------------------------


req_history_order
^^^^^^^^^^^^^^^^^^^^^^^^^

查询历史委托

**virtual bool req_history_order(const event_ptr &event);**

向券商柜台查询账户历史委托, 以下两个场景需要调用柜台API的查询历史接口

1. TD重启后恢复今日委托的最新状态, 更新在关闭期间的委托状态变化到本地
#. 策略想要获取今日的所有委托信息, 以HistoryOrder的数据格式进行推送

该接口为策略主动查询账户当日历史委托情况, 
将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成历史委托查询发送.

交易柜台通常只能查询到当前交易日内的历史委托情况, 有的柜台支持同步查询和异步查询, 有的柜台只支持同步查询.

.. 通常api的历史委托查询是异步接口, 会返回查询行为结果, 需要对该值做处理, 最终将api查询的执行结果以bool形式返回.
.. 有的时候会遇到流速控制等情况, 可以使用定时器等方式, 若干秒后再次尝试查询账户历史委托.
.. 存储操作来源, 方便获取对应writer, 将柜台后续返回的历史委托信息写回给该进程.



参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含该查询操作来源等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 查询历史委托成功返回true, 查询历史委托失败返回false


范例

.. code-block:: cpp
    :linenos:

    // xtp 异步查询历史委托
    bool TraderXTP::req_history_order(const event_ptr &event) {
        XTPQueryOrderReq query_param{};
        int request_id = get_request_id();
        int ret = api_->QueryOrders(&query_param, session_id_, request_id);
        if (0 != ret) {
            SPDLOG_ERROR("QueryOrders False: {}", ret);
        }
        map_request_location_.emplace(request_id, event->source()); // 标记为策略查询历史委托
        return 0 == ret;
    }

    bool TraderXTP::custom_OnQueryOrder(const XTPOrderInfo &order_info, const XTPRI &error_info, int request_id,
                                    bool is_last, uint64_t session_id) {
        SPDLOG_DEBUG("XTPOrderInfo: {}", to_string(order_info));
        SPDLOG_DEBUG("XTPRI: {}", to_string(error_info));
        SPDLOG_DEBUG("request_id: {}, is_last: {}", request_id, is_last);

        if (order_info.order_xtp_id == 0 and is_last and
            map_request_location_.find(request_id) != map_request_location_.end()) {
            SPDLOG_WARN("XTPQueryOrderRsp* order_info == nullptr, no data returned!");
            auto writer = get_history_writer(request_id);
            HistoryOrder &history_order = writer->open_data<HistoryOrder>();
            history_order.is_last = true;
            history_order.data_type = HistoryDataType::TotalEnd;
            const std::string msg = "No order today";
            history_order.error_msg = msg.c_str();
            writer->close_data();
            SPDLOG_DEBUG("HistoryOrder: {}", history_order.to_string());
            return false;
        }

        // 此处判断是属于启动TD时恢复查询还是策略查询
        if (map_request_location_.find(request_id) == map_request_location_.end()) {
            // TD重连收到推送当做普通下单委托响应处理
            if (is_last) {
                req_order_over_ = true;
                try_ready();
            }
            return order_info.order_xtp_id != 0 and custom_OnOrderEvent(order_info, error_info, request_id);
        }

        auto writer = get_history_writer(request_id);
        HistoryOrder &history_order = writer->open_data<HistoryOrder>();

        if (error_info.error_id != 0) {
            SPDLOG_ERROR("OnQueryOrder False , error_code : {}, error_msg : {}", error_info.error_id, error_info.error_msg);
            history_order.error_id = error_info.error_id;
            history_order.error_msg = error_info.error_msg;
        }

        from_xtp(order_info, history_order);
        history_order.order_id = writer->current_frame_uid();
        history_order.is_last = is_last;
        history_order.insert_time = yijinjing::time::now_in_nano();
        history_order.update_time = history_order.insert_time;
        SPDLOG_DEBUG("HistoryOrder: {}", history_order.to_string());
        writer->close_data();
        return true;
    }


    // xtp在启动时查询今日委托和成交信息, 没有标记 map_request_location_, custom_OnQueryOrder会走到custom_OnOrderEvent作为普通委托处理
    void TraderXTP::req_order_trade() {
        if (disable_recover_) {
            return try_ready();
        }

        XTPQueryOrderReq query_order_param{};
        int ret = api_->QueryOrders(&query_order_param, session_id_, get_request_id());
        if (0 != ret) {
            SPDLOG_ERROR("QueryOrders False: {}", ret);
        }

        XTPQueryTraderReq query_trade_param{};
        ret = api_->QueryTrades(&query_trade_param, session_id_, get_request_id());
        if (0 != ret) {
            SPDLOG_ERROR("QueryTrades False ： {}", ret);
        }
    }


    // 顶点股票柜台同步查询历史委托
    bool TraderItp::req_history_order(const event_ptr &event) {
        SPDLOG_INFO("req_history_order");
        const RequestHistoryOrder &request = event->data<RequestHistoryOrder>();
        SPDLOG_INFO("RequestHistoryOrder: {}", request.to_string());
        uint32_t source = event->source();
        uint32_t limit = request.query_num;

        auto writer = get_writer(event->source());
        if (req_history_order_query_.find(source) == req_history_order_query_.end()) {
            long nRet = 1;
            std::vector<ITPDK_DRWT> his_orders;
            req_history_order_query_.insert(std::make_pair(source, his_orders));
            int64 idx = 0;
            while (nRet > 0) {
            vector<ITPDK_DRWT> arDrwt;
            arDrwt.reserve(200); // 需要预分配足够空间，查询结果最大返回200条
            nRet =
                (long)SECITPDK_QueryOrders(get_account_id().c_str(), 0, SORT_TYPE_AES,
                                            200, idx, "", "", 0, arDrwt);
            req_history_order_query_[source].insert(
                req_history_order_query_[source].end(), arDrwt.begin(), arDrwt.end());
            idx = arDrwt.back().BrowIndex + 1;

            if (nRet < 0) {
                std::string error_msg = gbk2utf8(SECITPDK_GetLastError());
                SPDLOG_ERROR("req_history_order ERROR! SECITPDK_QueryOrders return: {} "
                            ", error message : {}",
                            nRet, error_msg);

                RequestHistoryOrderError &error =
                    writer->open_data<RequestHistoryOrderError>(event->gen_time());
                error.error_id = nRet;
                strncpy(error.error_msg, error_msg.c_str(), ERROR_MSG_LEN);
                error.trigger_time = event->gen_time();
                writer->close_data();
                return false;
            }
            }
            size_t ret_size = req_history_order_query_[source].size();
            SPDLOG_INFO("req_history_order success. Num of results {}", ret_size);
        }
        auto it = req_history_order_query_[source].begin();
        while (it != req_history_order_query_[source].end() && limit > 0) {
            HistoryOrder &history_order = writer->open_data<HistoryOrder>(now());
            from_itp(*it, history_order, trading_day_);
            history_order.order_id = writer->current_frame_uid();
            limit--;
            it++;
            if (it == req_history_order_query_[source].end()) {
            history_order.data_type = HistoryDataType::TotalEnd;
            } else if (limit == 0) {
            history_order.data_type = HistoryDataType::PageEnd;
            } else {
            history_order.data_type = HistoryDataType::Normal;
            }
            writer->close_data();
        }
        if (it == req_history_order_query_[source].end()) {
            req_history_order_query_.erase(source);
        } else {
            req_history_order_query_[source].erase(
                req_history_order_query_[source].begin(),
                req_history_order_query_[source].begin() + request.query_num);
        }
        return true;
    }


-----------------------------------


req_history_trade
^^^^^^^^^^^^^^^^^^^^^^^^^

查询历史成交

**virtual bool req_history_trade(const event_ptr &event);**

向券商柜台查询账户历史成交, 以下两个场景需要调用柜台API的查询历史接口

1. TD重启后恢复今日成交, 更新在关闭期间的成交到本地
#. 策略想要获取今日的所有成交信息, 以HistoryTrade的数据格式进行推送

该接口为策略主动查询账户当日历史成交情况, 
将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成历史成交查询发送.

交易柜台通常只能查询到当前交易日内的历史成交情况, 有的柜台支持同步查询和异步查询, 有的柜台只支持同步查询.




参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含该查询操作来源等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 查询历史成交成功返回true, 查询历史成交失败返回false


范例

.. code-block:: cpp
    :linenos:


    // 
    bool TraderXTP::req_history_trade(const event_ptr &event) {
        XTPQueryTraderReq query_param{};
        int request_id = get_request_id();
        int ret = api_->QueryTrades(&query_param, session_id_, request_id);
        if (0 != ret) {
            SPDLOG_ERROR("QueryTrades False ： {}", ret);
        }
        map_request_location_.emplace(request_id, event->source());
        return 0 == ret;
    }

    bool TraderXTP::custom_OnQueryTrade(const XTPTradeReport &trade_info, const XTPRI &error_info, int request_id,
                                    bool is_last, uint64_t session_id) {
        SPDLOG_DEBUG("XTPTradeReport: {}", to_string(trade_info));
        SPDLOG_DEBUG("XTPRI: {}", to_string(error_info));
        SPDLOG_DEBUG("request_id: {}, is_last: {}", request_id, is_last);

        // 查询历史流水收到nullptr, 经过journal走一圈后表现形式为 order_xtp_id == 0
        if (trade_info.order_xtp_id == 0 and is_last and
            map_request_location_.find(request_id) != map_request_location_.end()) {
            SPDLOG_WARN("XTPQueryTradeRsp* trade_info == nullptr, no data returned!");
            auto writer = get_history_writer(request_id);
            HistoryTrade &history_trade = writer->open_data<HistoryTrade>(now());
            history_trade.is_last = true;
            history_trade.data_type = HistoryDataType::TotalEnd;
            const std::string msg = "No trade today";
            history_trade.error_msg = msg.c_str();
            writer->close_data();
            return false;
        }

        if (map_request_location_.find(request_id) == map_request_location_.end()) {
            // TD重连收到推送当做普通交易成交回报推送处理
            if (is_last) {
            req_trade_over_ = true;
            try_ready();
            }
            return trade_info.order_xtp_id != 0 and custom_OnTradeEvent(trade_info, session_id);
        }

        auto writer = get_history_writer(request_id);
        HistoryTrade &history_trade = writer->open_data<HistoryTrade>(now());

        if (error_info.error_id != 0) {
            SPDLOG_ERROR("OnQueryTrade False , error_code : {}, error_msg : {}", error_info.error_id, error_info.error_msg);
            history_trade.error_id = error_info.error_id;
            history_trade.error_msg = error_info.error_msg;
        }

        from_xtp(trade_info, history_trade);
        history_trade.trade_id = writer->current_frame_uid();
        history_trade.is_last = is_last;
        history_trade.trade_time = yijinjing::time::now_in_nano();
        history_trade.instrument_type = get_instrument_type(history_trade.exchange_id, history_trade.instrument_id);
        SPDLOG_DEBUG("HistoryTrade: {}", history_trade.to_string());
        writer->close_data();
        return false;
    }


    // 顶点股票柜台同步查询历史委托
    bool TraderItp::req_history_trade(const event_ptr &event) {
        SPDLOG_INFO("req_history_trade");
        const RequestHistoryTrade &request = event->data<RequestHistoryTrade>();
        SPDLOG_INFO("RequestHistoryTrade: {}", request.to_string());
        uint32_t source = event->source();
        uint32_t limit = request.query_num;

        auto writer = get_writer(event->source());
        if (req_history_trade_query_.find(source) == req_history_trade_query_.end()) {
            long nRet = 1;
            std::vector<ITPDK_SSCJ> his_trades;
            req_history_trade_query_.insert(std::make_pair(source, his_trades));
            int64 idx = 0;
            while (nRet > 0) {
            vector<ITPDK_SSCJ> arSscj;
            arSscj.reserve(200); // 需要预分配足够空间，查询结果最大返回200条
            nRet =
                (long)SECITPDK_QueryMatchs(get_account_id().c_str(), 0, SORT_TYPE_AES,
                                            200, idx, "", "", 0, arSscj);
            req_history_trade_query_[source].insert(
                req_history_trade_query_[source].end(), arSscj.begin(), arSscj.end());
            idx = arSscj.back().BrowIndex + 1;

            if (nRet < 0) {
                std::string error_msg = gbk2utf8(SECITPDK_GetLastError());
                SPDLOG_ERROR("req_history_trade ERROR! SECITPDK_QueryMatchs return: {} "
                            ", error message : {}",
                            nRet, error_msg);
                RequestHistoryTradeError &error =
                    writer->open_data<RequestHistoryTradeError>(event->gen_time());
                error.error_id = nRet;
                strncpy(error.error_msg, error_msg.c_str(), ERROR_MSG_LEN);
                error.trigger_time = event->gen_time();
                writer->close_data();
                return false;
            }
            }
            size_t ret_size = req_history_trade_query_[source].size();
            SPDLOG_DEBUG("req_history_trade success. Num of results {}", ret_size);
        }
        auto it = req_history_trade_query_[source].begin();
        while (it != req_history_trade_query_[source].end() && limit > 0) {
            HistoryTrade &history_trade = writer->open_data<HistoryTrade>(now());
            from_itp(*it, history_trade, trading_day_);
            history_trade.trade_id = writer->current_frame_uid();
            limit--;
            it++;
            if (it == req_history_trade_query_[source].end()) {
            history_trade.data_type = HistoryDataType::TotalEnd;
            } else if (limit == 0) {
            history_trade.data_type = HistoryDataType::PageEnd;
            } else {
            history_trade.data_type = HistoryDataType::Normal;
            }
            writer->close_data();
        }
        if (it == req_history_trade_query_[source].end()) {
            req_history_trade_query_.erase(source);
        } else {
            req_history_trade_query_[source].erase(
                req_history_trade_query_[source].begin(),
                req_history_trade_query_[source].begin() + request.query_num);
        }
        return true;
    }


req_order_trigger
^^^^^^^^^^^^^^^^^^^^^^^^^

查询预埋单

**virtual bool req_order_trigger();**

向券商柜台查询预埋单最新状态, 预埋单触发或者撤销后, 不会实时推送预埋单的最新状态, 需要手动查询




参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - event
      - const event_ptr &
      - 包含该查询操作来源等信息


返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 查询历史成交成功返回true, 查询历史成交失败返回false


范例

.. code-block:: cpp
    :linenos:

    // ctp的查询预埋单的实现
    bool TraderCTP::req_order_trigger() { return req_trigger(); }

    bool TraderCTP::req_trigger() {
        if (disable_recover_) {
            return false;
        }

        add_timer_req_insert_trigger(now() + 1 * time_unit::NANOSECONDS_PER_SECOND);
        add_timer_req_cancel_trigger(now() + 3 * time_unit::NANOSECONDS_PER_SECOND);
        return true;
    }

    // 查询预埋下单
    void TraderCTP::add_timer_req_insert_trigger(int64_t nano) {
        add_timer(nano, [&](const auto &event) {
            CThostFtdcQryParkedOrderField req_parked{};
            strcpy(req_parked.BrokerID, config_.broker_id.c_str());
            strcpy(req_parked.InvestorID, config_.account_id.c_str());
            SPDLOG_INFO("CThostFtdcQryParkedOrderField: {}", to_string(req_parked));
            int request_id = get_request_id();
            int rtn = api_->ReqQryParkedOrder(&req_parked, request_id);
            SPDLOG_INFO("ReqQryTrade rtn {}", rtn);
            if (rtn != 0) {
            add_timer_req_insert_trigger(time::now_in_nano() + 3 * time_unit::NANOSECONDS_PER_SECOND);
            }
        });
    }

    // 查询预埋撤单
    void TraderCTP::add_timer_req_cancel_trigger(int64_t nano) {
        add_timer(nano, [&](const auto &event) {
            CThostFtdcQryParkedOrderActionField req_parked_action{};
            strcpy(req_parked_action.BrokerID, config_.broker_id.c_str());
            strcpy(req_parked_action.InvestorID, config_.account_id.c_str());
            SPDLOG_INFO("CThostFtdcQryParkedOrderActionField: {}", to_string(req_parked_action));
            int request_id = get_request_id();
            int rtn = api_->ReqQryParkedOrderAction(&req_parked_action, request_id);
            SPDLOG_INFO("ReqQryTrade rtn {}", rtn);
            if (rtn != 0) {
            add_timer_req_cancel_trigger(time::now_in_nano() + 3 * time_unit::NANOSECONDS_PER_SECOND);
            }
        });
    }



.. note::
    ctp有流控限制, 连续查询可能会失败, 失败后可以添加一个定时器3秒后再查一次.



-------------------------------------


req_contract
^^^^^^^^^^^^^^^^^^^^^^^^^

两融合约查询

**virtual bool req_contract();**

向券商柜台查询两融合约状态, 融资买入和融券卖出成交后, 两融合约不会实时推送, 想要获取当前最新的两融合约状态需要手动查询.


范例

.. code-block:: cpp
    :linenos:

    // 华锐两融查询合约
    bool TraderATP::req_contract() { return req_contractSpecifications(false); }

    // 融资融券合约明细查询函数
    bool TraderATP::req_contractSpecifications(bool is_query_position) {
        if (!req_contract_status_) {
            // 如果上次点击前端按钮查合约 还没有结束 就不能重复查询
            // 因为查持仓那里已经有防止重复查的开关了 所以持仓查合约是不会重复查的 可以不做处理
            SPDLOG_ERROR("上次更新尚未结束 请稍后再点击更新合约按钮");
            return false;
        }
        if (!is_query_position) {
            req_contract_status_ = false;
        }
        SPDLOG_INFO("融资融券合约明细查询 req_contractSpecifications");
        ATPReqExtQueryContractSpecificationsMsg req_contract_specifications_msg{};

        strcpy(req_contract_specifications_msg.cust_id, cust_id_.c_str()); /// 客户号ID（必填）
        strcpy(req_contract_specifications_msg.fund_account_id, td_config_.fund_account_id.c_str()); /// 资金账户ID（必填）
        int64_t seq_id = get_client_seq_id();
        if (is_query_position) {
            set_contract_id_.insert(seq_id);
        }
        req_contract_specifications_msg.client_seq_id = seq_id; /// 用户系统消息序号（必填）
        strcpy(req_contract_specifications_msg.branch_id, td_config_.branch_id.c_str()); /// 营业部ID（必填）
        ATPRetCodeType ret = atp_trader_api_ptr_->ReqExtQueryContractSpecifications(&req_contract_specifications_msg);
        SPDLOG_INFO("req_contract return code : {} , "
                    "return message : {}",
                    ret, map_error_code.try_emplace(ret).first->second);
        if (ret != ErrorCode::kSuccess) {
            SPDLOG_ERROR("req_contract error return code : {} , "
                        "return message : {}",
                        ret, map_error_code.try_emplace(ret).first->second);
        }
        return true;
    }


-------------------------------------



.. insert_algo_order
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. **virtual bool insert_algo_order(const event_ptr &event);**

.. 算法单添加

.. ------------------------------------

.. cancel_algo_order
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. **virtual bool cancel_algo_order(const event_ptr &event);**

.. 算法单删除


.. ------------------------------------

.. toggle_algo_order
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. **virtual bool toggle_algo_order(const event_ptr &event);**

.. 算法单启动/停止

.. ------------------------------------

.. on_band
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. **virtual bool req_algo_order(const event_ptr &event);**
    
.. 查询算法单（系统未调用, 最后再确认）

.. ------------------------------------



on_band
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**virtual void on_band(const event_ptr &event);**

当有一个进程调用request_band创建一个写入信道时, master会广播这条信道的信息, 所有的进程都会收到一个Band信息, 可以在on_band中选择是否要订阅这条信道.

一般场景下不会用到该接口.



推送处理
-------------------

成交推处理
^^^^^^^^^^^^^^^^^^^^^^

委托成交时, 会触发柜台API的成交推送函数, 需要根据推送的成交数据中的 *柜台API委托号* 找到Kungfu对应的Order, 然后生成Trade, 并且修改Order的状态.

针对于异步柜台, 可能会发生成交推送函数早于委托响应函数触发的情况, 此时还没有获得*柜台API委托号*, 无法找到Kungfu对应的Order,
此时需要先将委托暂存, 当收到委托响应后, 再将成交数据取出来处理.

重启TD时, 查询并恢复今日的成交数据, 可能会导致同一笔成交处理两次, 所以针对于已处理的成交数据做标记, 再次收到已经处理过的成交数据时, 不再处理.


范例

.. code-block:: cpp
    :linenos:

    // ctp的处理实现

    std::unordered_map<std::string, std::unordered_set<std::string>> map_ExchangeID_OrderSysID_to_TradeIDs_{}; // <交易所:订单号, set<已经处理过的成交编号>>
    std::unordered_map<std::string, std::vector<CThostFtdcTradeField>> map_ExchangeID_OrderSysID_to_CThostFtdcTradeFields_{}; // <交易所:订单号, vector<先于委托响应回来的成交回报>>
    std::unordered_map<std::string, uint64_t> map_ExchangeID_OrderSysID_to_kf_order_id_{}; // <交易所:订单号, kf_order_id>
    std::unordered_map<uint64_t, std::string> map_kf_order_id_to_OrderSysID_{}; // <kf_order_id, 订单号> 撤单用    
    std::unordered_map<uint64_t, std::string> map_kf_order_id_to_OrderRef_{}; // <kf_order_id, OrderRef> 撤未提交到交易所的单用

    // 判断成交是否已经处理
    bool TraderCTP::has_dealt_trade(const CThostFtdcTradeField &ctp_trade) {
        auto &dealt_TradeIDs = map_ExchangeID_OrderSysID_to_TradeIDs_
                                    .try_emplace(make_ExchangeID_OrderSysID(ctp_trade.ExchangeID, ctp_trade.OrderSysID))
                                    .first->second;
        return dealt_TradeIDs.find(ctp_trade.TradeID) != dealt_TradeIDs.end();
    }

    // 记录已经处理过的成交
    void TraderCTP::add_TradeID(const CThostFtdcTradeField &ctp_trade) {
        map_ExchangeID_OrderSysID_to_TradeIDs_
            .try_emplace(make_ExchangeID_OrderSysID(ctp_trade.ExchangeID, ctp_trade.OrderSysID))
            .first->second.insert(ctp_trade.TradeID);
    }

    // 成交推送处理
    bool TraderCTP::custom_OnRtnTrade(const CThostFtdcTradeField &ctp_trade) {
        SPDLOG_DEBUG("CThostFtdcTradeField: {}", to_string(ctp_trade));
        if (ctp_trade.Price < 1 || ctp_trade.Price == 2.2250738585072014e-308 || ctp_trade.Price == 1.7976931348623158e+308 ||
            ctp_trade.Volume == -2147483648 || ctp_trade.Volume == 2147483647) {
            SPDLOG_ERROR("Order Price too low, Not True ctp_trade.Price {}, *ctp_trade {}", ctp_trade.Price,
                        to_string(ctp_trade));
            return false;
        }

        const std::string &str_ExchangeID_OrderSysID = make_ExchangeID_OrderSysID(ctp_trade.ExchangeID, ctp_trade.OrderSysID);
        auto ExchangeID_OrderSysID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderSysID);
        if (ExchangeID_OrderSysID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            SPDLOG_WARN("CANNOT FIND {} in map_ExchangeID_OrderSysID_to_kf_order_id_, STORE CThostFtdcTradeField IN "
                        "map_ExchangeID_OrderSysID_to_CThostFtdcTradeFields_",
                        str_ExchangeID_OrderSysID);
            map_ExchangeID_OrderSysID_to_CThostFtdcTradeFields_.try_emplace(str_ExchangeID_OrderSysID)
                .first->second.push_back(ctp_trade); // 暂存先于委托响应收到的成交推送
            return false;
        }
        deal_trade(ctp_trade);
        return true;
    }

    // 委托响应和推送处理
    bool TraderCTP::custom_OnRtnOrder(const CThostFtdcOrderField &ctp_order) {
        SPDLOG_DEBUG("CThostFtdcOrderField: {}", to_string(ctp_order));

        const std::string str_ExchangeID_OrderLocalID =
            make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderLocalID);
        const std::string str_ExchangeID_OrderSysID = make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderSysID);
        uint64_t orderRef_key = get_orderRef_key(ctp_order.FrontID, ctp_order.SessionID, ctp_order.OrderRef);
        auto OrderRefKey_iter = map_OrderRefKey_to_kf_order_id_.find(orderRef_key);
        auto ExchangeID_OrderSysID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderSysID);
        auto ExchangeID_OrderLocalID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderLocalID);

        // 系统外订单信息
        if (OrderRefKey_iter == map_OrderRefKey_to_kf_order_id_.end() and
            ExchangeID_OrderSysID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end() and
            ExchangeID_OrderLocalID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            SPDLOG_WARN("external Order with ExchangeID: {}, OrderSysID: {}, OrderLocalID: {}", ctp_order.ExchangeID,
                        ctp_order.OrderSysID, ctp_order.OrderLocalID);
            return generate_external_order(ctp_order);
        }

        uint64_t kf_order_id = 0;
        if (strlen(ctp_order.OrderSysID) != 0 and
            ExchangeID_OrderSysID_iter != map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            kf_order_id = ExchangeID_OrderSysID_iter->second;
        } else if (OrderRefKey_iter != map_OrderRefKey_to_kf_order_id_.end()) {
            kf_order_id = OrderRefKey_iter->second;
        } else if (ExchangeID_OrderLocalID_iter != map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            kf_order_id = ExchangeID_OrderLocalID_iter->second;
        } else {
            SPDLOG_ERROR("invalidate CThostFtdcOrderField: {}", to_string(ctp_order));
            return false;
        }

        if (strlen(ctp_order.OrderSysID) != 0) {
            map_kf_order_id_to_OrderSysID_.insert_or_assign(kf_order_id, ctp_order.OrderSysID);
            map_ExchangeID_OrderSysID_to_kf_order_id_.insert_or_assign(str_ExchangeID_OrderSysID, kf_order_id);
        }

        if (not has_order(kf_order_id)) {
            SPDLOG_WARN("no order_id {} in orders_", kf_order_id);
            return generate_external_order(ctp_order);
        }

        auto &order_state = get_order(kf_order_id);

        if (is_final_status(order_state.data.status) and order_state.data.status != longfist::enums::OrderStatus::Lost and
            order_state.data.status != longfist::enums::OrderStatus::Cancelling) {
            return true;
        }

        from_ctp(ctp_order, order_state.data);
        order_state.data.update_time = time::now_in_nano();
        if (has_writer(order_state.dest)) {
            write_to(order_state.data, order_state.dest);
        } else {
            ++try_write_to_order_count;
            try_write_to(order_state.data, order_state.dest, [&]() {
                --try_write_to_order_count;
                try_ready();
            });
        }
        try_deal_trade(str_ExchangeID_OrderSysID); // 处理暂存的委托
        return true;
    }

    // 处理暂存的委托
    void TraderCTP::try_deal_trade(const std::string &str_ExchangeID_OrderSysID) {
        SPDLOG_DEBUG("ExchangeID_OrderSysID: {}", str_ExchangeID_OrderSysID);
        auto &ctp_trades =
            map_ExchangeID_OrderSysID_to_CThostFtdcTradeFields_.try_emplace(str_ExchangeID_OrderSysID).first->second;
        for (const CThostFtdcTradeField &ctp_trade : ctp_trades) {
            deal_trade(ctp_trade);
        }
        ctp_trades.clear();
    }

    // 生成Trade
    void TraderCTP::deal_trade(const CThostFtdcTradeField &ctp_trade) {
        SPDLOG_DEBUG("CThostFtdcTradeField: {}", to_string(ctp_trade));
        const std::string &str_ExchangeID_OrderSysID = make_ExchangeID_OrderSysID(ctp_trade.ExchangeID, ctp_trade.OrderSysID);
        auto ExchangeID_OrderSysID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderSysID);
        if (ExchangeID_OrderSysID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            SPDLOG_ERROR("CANNOT FIND {} in map_ExchangeID_OrderSysID_to_kf_order_id_", str_ExchangeID_OrderSysID);
            return;
        }
        uint64_t kf_order_id = ExchangeID_OrderSysID_iter->second;
        if (not has_order(kf_order_id)) {
            SPDLOG_ERROR("no order_id {} in orders_", kf_order_id);
            return;
        }

        // 判断委托是否已经处理过
        if (has_dealt_trade(ctp_trade)) {
            SPDLOG_WARN("trade: [{}:{}] HAS DEALT, DO NOT DEAL SECOND TIME", str_ExchangeID_OrderSysID, ctp_trade.TradeID);
            return;
        }
        add_TradeID(ctp_trade); // 记录已处理委托

        auto &order_state = get_order(kf_order_id);
        // 生成Trade
        if (has_writer(order_state.dest)) {
            auto writer = get_writer(order_state.dest);
            Trade &trade = writer->open_data<Trade>(0);
            from_ctp(ctp_trade, trade);
            uint64_t trade_id = writer->current_frame_uid();
            trade.trade_id = trade_id;
            trade.order_id = order_state.data.order_id;
            SPDLOG_DEBUG("Trade: {}", trade.to_string());
            writer->close_data();
        } else {
            Trade trade{};
            from_ctp(ctp_trade, trade);
            uint64_t trade_id = get_public_writer()->current_frame_uid() xor (time::now_in_nano() & 0x0000FFFF);
            trade.trade_id = trade_id;
            trade.order_id = order_state.data.order_id;
            SPDLOG_DEBUG("Trade: {}", trade.to_string());
            ++try_write_to_trade_count;
            try_write_to(trade, order_state.dest, [&]() {
                --try_write_to_trade_count;
                try_ready();
            });
        }
    }

---------------------------------------------


系统外委托和成交推送处理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

当同一个交易账户在多个客户端同时登陆时, Kungfu客户端会收到其他客户端提交的委托的推送信息, 可以根据个人需求选择是否要处理系统外的委托和成交.


范例

.. code-block:: cpp
    :linenos:

    // ctp处理实现

    // 委托响应和推送处理
    bool TraderCTP::custom_OnRtnOrder(const CThostFtdcOrderField &ctp_order) {
        SPDLOG_DEBUG("CThostFtdcOrderField: {}", to_string(ctp_order));

        const std::string str_ExchangeID_OrderLocalID =
            make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderLocalID);
        const std::string str_ExchangeID_OrderSysID = make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderSysID);
        uint64_t orderRef_key = get_orderRef_key(ctp_order.FrontID, ctp_order.SessionID, ctp_order.OrderRef);
        auto OrderRefKey_iter = map_OrderRefKey_to_kf_order_id_.find(orderRef_key);
        auto ExchangeID_OrderSysID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderSysID);
        auto ExchangeID_OrderLocalID_iter = map_ExchangeID_OrderSysID_to_kf_order_id_.find(str_ExchangeID_OrderLocalID);

        // 系统外订单信息
        if (OrderRefKey_iter == map_OrderRefKey_to_kf_order_id_.end() and
            ExchangeID_OrderSysID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end() and
            ExchangeID_OrderLocalID_iter == map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            SPDLOG_WARN("external Order with ExchangeID: {}, OrderSysID: {}, OrderLocalID: {}", ctp_order.ExchangeID,
                        ctp_order.OrderSysID, ctp_order.OrderLocalID);
            return generate_external_order(ctp_order); // 处理系统外委托
        }

        uint64_t kf_order_id = 0;
        if (strlen(ctp_order.OrderSysID) != 0 and
            ExchangeID_OrderSysID_iter != map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            kf_order_id = ExchangeID_OrderSysID_iter->second;
        } else if (OrderRefKey_iter != map_OrderRefKey_to_kf_order_id_.end()) {
            kf_order_id = OrderRefKey_iter->second;
        } else if (ExchangeID_OrderLocalID_iter != map_ExchangeID_OrderSysID_to_kf_order_id_.end()) {
            kf_order_id = ExchangeID_OrderLocalID_iter->second;
        } else {
            SPDLOG_ERROR("invalidate CThostFtdcOrderField: {}", to_string(ctp_order));
            return false;
        }

        if (strlen(ctp_order.OrderSysID) != 0) {
            map_kf_order_id_to_OrderSysID_.insert_or_assign(kf_order_id, ctp_order.OrderSysID);
            map_ExchangeID_OrderSysID_to_kf_order_id_.insert_or_assign(str_ExchangeID_OrderSysID, kf_order_id);
        }

        if (not has_order(kf_order_id)) {
            SPDLOG_WARN("no order_id {} in orders_", kf_order_id);
            return generate_external_order(ctp_order);
        }

        auto &order_state = get_order(kf_order_id);

        if (is_final_status(order_state.data.status) and order_state.data.status != longfist::enums::OrderStatus::Lost and
            order_state.data.status != longfist::enums::OrderStatus::Cancelling) {
            return true;
        }

        from_ctp(ctp_order, order_state.data);
        order_state.data.update_time = time::now_in_nano();
        if (has_writer(order_state.dest)) {
            write_to(order_state.data, order_state.dest);
        } else {
            ++try_write_to_order_count;
            try_write_to(order_state.data, order_state.dest, [&]() {
            --try_write_to_order_count;
            try_ready();
            });
        }
        try_deal_trade(str_ExchangeID_OrderSysID); // 处理暂存的委托
        return true;
    }

    // 根据系统外的委托推送信息生成Kunfu的Order
    bool TraderCTP::generate_external_order(const CThostFtdcOrderField &ctp_order) {
        SPDLOG_DEBUG("CThostFtdcOrderField: {}", to_string(ctp_order));

        if (not config_.sync_external_order) {
            return false;
        }

        auto nano = time::now_in_nano();
        auto writer_order = get_public_writer();
        Order &order = writer_order->open_data<Order>(now());
        order.order_id = writer_order->current_frame_uid();
        from_ctp(ctp_order, order);
        order.insert_time = nsec_from_ctp_time(ctp_order.InsertDate, ctp_order.InsertTime);
        if (order.insert_time > nano) {
            order.insert_time -= time_unit::NANOSECONDS_PER_DAY;
        }
        order.update_time = nano;
        writer_order->close_data();
        SPDLOG_DEBUG("Order: {}", order.to_string());

        uint64_t orderRef_key = get_orderRef_key(ctp_order.FrontID, ctp_order.SessionID, ctp_order.OrderRef);
        map_OrderRefKey_to_kf_order_id_.insert_or_assign(orderRef_key, uint64_t(order.order_id));

        const std::string str_ExchangeID_OrderSysID =
            strlen(ctp_order.OrderSysID) == 0 ? make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderLocalID)
                                                : make_ExchangeID_OrderSysID(ctp_order.ExchangeID, ctp_order.OrderSysID);
        if (strlen(ctp_order.OrderSysID) != 0) {
            map_ExchangeID_OrderSysID_to_kf_order_id_.insert_or_assign(str_ExchangeID_OrderSysID, uint64_t(order.order_id));
            map_kf_order_id_to_OrderSysID_.insert_or_assign(uint64_t(order.order_id), ctp_order.OrderSysID);
        }
        try_deal_trade(str_ExchangeID_OrderSysID); // 处理暂存的成交
        return true;
    }

.. note::
    如果系统外的委托推送先于成交推送到达, 处理完系统外委托后, 成交推送就可以当做系统内正常顺序的成交推送处理.

    如果系统外的成交推送先于委托推送到达, 成交信息会暂存, 处理完系统外委托后, 会和处理系统内暂存的成交信息一样处理.


---------------------------    