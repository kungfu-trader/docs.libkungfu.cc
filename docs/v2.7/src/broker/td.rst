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

        // Kungfu本地算法单添加
        virtual bool insert_algo_order(const event_ptr &event);

        // 委托撤单(预埋撤单和普通撤单)
        virtual bool cancel_order(const event_ptr &event) = 0;

        // 预埋单撤单
        virtual bool cancel_order_trigger(const event_ptr &event);

        // Kungfu本地算法单删除
        virtual bool cancel_algo_order(const event_ptr &event);

        // Kungfu本地算法单启动/停止
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

   大部分柜台的大宗交易报单和普通委托报单是同一个委托函数, 委托响应函数也想通, 区别只是是否填写了大宗交易相关的信息: 对手方席号, 成交约定号, 是否受限(特定)股份



-----------------------------------------


insert_batch_orders
^^^^^^^^^^^^^^^^^^^^^^^^^^^

批量委托报单

**virtual bool insert_batch_orders(const event_ptr &event, const OrderInputs &order_inputs);**

有的柜台可能会有流控限制, 发送消息的数量有限制, 如果需要一次性报很多笔委托, 需要用到批量委托接口, 依据order_inputs中的输入信息完成向券商柜台报批量单.

策略或者前端下批量单后, 待报批量单信息将会存在order_inputs中.
将order_inputs中的待报批量单信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成报批量单发送.
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

**virtual bool req_position() = 0;**

向券商柜台查询账户当前持仓.

前端和策略可以主动查询当前账户持仓情况, 同时系统也会每分钟自动触发一次查询以同步最新的持仓状态.
将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成持仓查询发送.
通常api的持仓查询是异步接口, 会返回查询执行结果, 需要对该值做处理, 最终将api查询的执行结果以bool形式返回.
有的时候会遇到流速控制等情况, 可以使用定时器等方式, 若干秒后再次尝试查询账户持仓.


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

    bool TraderCTP::req_position() {
        CThostFtdcQryInvestorPositionField req = {};
        strcpy(req.BrokerID, config_.broker_id.c_str());
        strcpy(req.InvestorID, config_.account_id.c_str());
        long_position_map_.clear();
        short_position_map_.clear();
        std::this_thread::sleep_for(std::chrono::seconds(1));
        SPDLOG_TRACE("CThostFtdcQryInvestorPositionField: {}", to_string(req));
        int rtn = api_->ReqQryInvestorPosition(&req, get_request_id());
        SPDLOG_TRACE("ReqQryInvestorPosition rtn {}", rtn);
        if (rtn != 0) {
            add_timer_req_position(now() + 2 * time_unit::NANOSECONDS_PER_SECOND);
        }
        return rtn == 0;
    }



req_account
^^^^^^^^^^^^^^^^^^^^

**virtual bool req_account() = 0;**

向券商柜台查询账户资金.

策略可以主动查询当前账户资金情况, 同时系统也会每分钟默认触发一次查询以同步最新的资金状态.
将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成资金查询发送.
通常api的资金查询是异步接口, 会返回查询行为结果, 需要对该值做处理, 最终将api查询的执行结果以bool形式返回.
有的时候会遇到流速控制等情况, 可以使用定时器等方式, 若干秒后再次尝试查询账户资金.


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

    bool TraderCTP::req_account() {
        CThostFtdcQryTradingAccountField req = {};
        strcpy(req.BrokerID, config_.broker_id.c_str());
        strcpy(req.InvestorID, config_.account_id.c_str());
        SPDLOG_TRACE("CThostFtdcQryTradingAccountField: {}", to_string(req));
        std::this_thread::sleep_for(std::chrono::seconds(1));
        int rtn = api_->ReqQryTradingAccount(&req, get_request_id());
        SPDLOG_TRACE("ReqQryTradingAccount rtn {}", rtn);

        if (rtn != 0) {
            add_timer_req_account(now() + 2 * time_unit::NANOSECONDS_PER_SECOND);
        }

        return rtn == 0;
    }



req_history_order
^^^^^^^^^^^^^^^^^^^^^^^^^

**virtual bool req_history_order(const event_ptr &event);**

向券商柜台查询账户历史委托.

策略可以主动查询账户当日历史委托情况, 同时前端如果开启了“恢复今日订单”会在启动时查询今日所有委托.
将全局存储的账户等信息, 按照柜台api的要求直接填写或者构建所需的消息体后填写, 调用api完成历史委托查询发送.
通常api的历史委托查询是异步接口, 会返回查询行为结果, 需要对该值做处理, 最终将api查询的执行结果以bool形式返回.
有的时候会遇到流速控制等情况, 可以使用定时器等方式, 若干秒后再次尝试查询账户历史委托.
存储操作来源, 方便获取对应writer, 将柜台后续返回的历史委托信息写回给该进程.
通常只能查询到当前交易日内的历史委托情况.


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

    bool TraderCTP::req_history_order(const event_ptr &event) {
        CThostFtdcQryOrderField req = {};
        strcpy(req.BrokerID, config_.broker_id.c_str());
        strcpy(req.InvestorID, config_.account_id.c_str());
        std::this_thread::sleep_for(std::chrono::seconds(1));
        SPDLOG_DEBUG("CThostFtdcQryOrderField: {}", to_string(req));
        int request_id = get_request_id();
        int rtn = api_->ReqQryOrder(&req, request_id);
        SPDLOG_DEBUG("ReqQryOrder rtn {}", rtn);
        map_request_location_.insert_or_assign(request_id, event->source());
        return rtn == 0;
    }



req_history_trade
^^^^^^^^^^^^^^^^^^^^^^^^^

**virtual bool req_history_trade(const event_ptr &event);**

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

    bool TraderCTP::req_history_trade(const event_ptr &event) {
        CThostFtdcQryTradeField req = {};
        strcpy(req.BrokerID, config_.broker_id.c_str());
        strcpy(req.InvestorID, config_.account_id.c_str());
        std::this_thread::sleep_for(std::chrono::seconds(1));
        SPDLOG_DEBUG("CThostFtdcQryTradeField: {}", to_string(req));
        int request_id = get_request_id();
        int rtn = api_->ReqQryTrade(&req, request_id);
        SPDLOG_DEBUG("ReqQryTrade rtn {}", rtn);
        map_request_location_.insert_or_assign(request_id, event->source());
        return rtn == 0;
    }



on_band
^^^^^^^^^^^^^^^

**virtual void on_band(const event_ptr &event) {}**


