行情源对接
============

行情接口基类

.. code-block:: cpp
    :linenos:    

    class MarketData : public BrokerService {      
    public:
      explicit MarketData(BrokerVendor &vendor) : BrokerService(vendor) {}

      // 策略或前端调用subscribe订阅指定标的行情时会触发该回调, 用于根据交易所和标的号订阅行情
      virtual bool subscribe(const std::vector<longfist::types::InstrumentKey> &instrument_keys);

      // subscribe_custom默认实现会调用该回调, 用于订阅行情源全市场行情
      virtual bool subscribe_all();

      // 策略调用subscribe_all会触发该回调, 用于根据自定义的行情类型, 标的类型, 逐笔类型进行全市场订阅; 默认实现为调用MarketData::subscribe_all
      virtual bool subscribe_custom(const longfist::types::CustomSubscribe &custom_sub);

      // 保留接口
      virtual bool unsubscribe(const std::vector<longfist::types::InstrumentKey> &instrument_keys);

      // 收到master广播的Band数据会触发该回调, 用于订阅band信道
      virtual void on_band(const event_ptr &event);

    protected:
      [[nodiscard]] bool has_instrument(const std::string &instrument_id) const;

      [[nodiscard]] const longfist::types::Instrument &get_instrument(const std::string &instrument_id) const;

      void update_instrument(longfist::types::Instrument instrument);

      void try_subscribe();

      void add_instrument_key(const longfist::types::InstrumentKey &key);

      std::unordered_map<std::string, longfist::types::Instrument> instruments_ = {};
      std::vector<longfist::types::InstrumentKey> instruments_to_subscribe_ = {};
    };


-------------






主要接口
-----------


subscribe
^^^^^^^^^^^^^


**virtual bool subscribe(const std::vector<InstrumentKey> &instrument_keys);**

用于根据交易所和标的号订阅行情

策略或前端订阅指定标的时, 订阅的标的会暂存在 ``std::vector<InstrumentKey> instruments_to_subscribe_``, 
每隔一秒会检查 ``instruments_to_subscribe_.empty()``, 
如果非空则调用 ``subscribe(instruments_to_subscribe_)``,
结束后执行 ``instruments_to_subscribe_.clear()`` 清空列表.


参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - instrument_keys
      - const std::vector<InstrumentKey> &
      - 订阅的标的列表

返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 订阅成功返回true, 订阅失败返回false
     

范例

.. code-block:: cpp
    :linenos: 

    // ctp的subscribe实现
    bool MarketDataCTP::subscribe(const std::vector<InstrumentKey> &instruments) {
      auto length = instruments.size();
      auto targets = new char *[length];
      for (int i = 0; i < length; i++) {
        targets[i] = const_cast<char *>(instruments[i].instrument_id.value);
      }
      auto rtn = api_->SubscribeMarketData(targets, length);
      delete[] targets;
      return rtn == 0;
    }


-------------


subscribe_all
^^^^^^^^^^^^^^^


**virtual bool subscribe_all();**

用于订阅全市场行情

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
     - 订阅成功返回true, 订阅失败返回false
     

范例

.. code-block:: cpp
    :linenos: 

    // xtp的subscribe_all实现
    bool subscribe_all() override {
      auto result = api_->SubscribeAllMarketData() && api_->SubscribeAllTickByTick();
      SPDLOG_INFO("subscribe all, rtn code {}", result);
      return result;
    }


-------------


subscribe_custom
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**virtual bool subscribe_custom(const longfist::types::CustomSubscribe &custom_sub);**
  
用于根据自定义的行情类型, 标的类型, 逐笔类型进行全市场订阅; 
默认实现为调用 MarketData::subscribe_all



参数

.. list-table::
    :width: 600px

    * - 参数
      - 类型
      - 说明
    * - custom_sub
      - CustomSubscribe
      - 自定义交易市场, 

返回值

.. list-table::
   :width: 600px

   * - 类型
     - 说明
   * - bool
     - 订阅成功返回true, 订阅失败返回false
     

.. 范例

.. .. code-block:: cpp
..     :linenos: 

..     // xtp的subscribe_all实现
..     bool subscribe_all() override {
..       auto result = api_->SubscribeAllMarketData() && api_->SubscribeAllTickByTick();
..       SPDLOG_INFO("subscribe all, rtn code {}", result);
..       return result;
..     }


-------------


unsubscribe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**virtual bool unsubscribe(const std::vector<longfist::types::InstrumentKey> &instrument_keys);**

最初设计时是为了方面取消订阅指定的标的行情, 但是在多策略场景下, 一个策略调用取消订阅了指定标的后, 会导致订阅了同样标的的其他策略无法收到行情, 故而不建议使用.


-------------


on_band
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**virtual void on_band(const event_ptr &event);**

当有一个进程调用request_band创建一个写入信道时, master会广播这条信道的信息, 所有的进程都会收到一个Band信息, 可以在on_band中选择是否要订阅这条信道.

一般场景下不会用到该接口.


-----------------------


快照行情写入
^^^^^^^^^^^^^^^^^^^^^^

当行情源API的快照回调虚函数触发时, 需要将行情源的快照数据转换成kungfu::longfist::types::Quote数据结构, 快照数据可以直接写入到PUBLIC信道里, 具体操作方式参考以下XTP范例.


范例

.. code-block:: cpp
    :linenos: 

    // 交易所转换
    inline void from_xtp(const XTP_MARKET_TYPE &xtp_market_type, char *exchange_id) {
        if (xtp_market_type == XTP_MKT_SH_A) {
            strcpy(exchange_id, "SSE");
        } else if (xtp_market_type == XTP_MKT_SZ_A) {
            strcpy(exchange_id, "SZE");
        }
    }

    // xtp的Quote数据结构转换实现
    inline void from_xtp(const XTPMarketDataStruct &ori, Quote &des) {
        des.data_time = nsec_from_xtp_timestamp(ori.data_time);
        des.instrument_id = ori.ticker;
        from_xtp(ori.exchange_id, des.exchange_id);

        des.instrument_type = ori.data_type != XTP_MARKETDATA_OPTION ? get_instrument_type(des.exchange_id, des.instrument_id)
                                                                    : InstrumentType::StockOption;

        des.last_price = ori.last_price;
        des.pre_settlement_price = ori.pre_settl_price;
        des.pre_close_price = ori.pre_close_price;
        des.open_price = ori.open_price;
        des.high_price = ori.high_price;
        des.low_price = ori.low_price;
        des.volume = ori.qty;
        des.turnover = ori.turnover;
        des.close_price = ori.close_price;
        des.settlement_price = ori.settl_price;
        des.upper_limit_price = ori.upper_limit_price;
        des.lower_limit_price = ori.lower_limit_price;
        des.total_trade_num = ori.trades_count;

        memcpy(des.ask_price, ori.ask, sizeof(des.ask_price));
        memcpy(des.bid_price, ori.bid, sizeof(des.ask_price));
        for (std::size_t i = 0; i < 10; i++) {
            des.ask_volume[i] = ori.ask_qty[i];
            des.bid_volume[i] = ori.bid_qty[i];
        }
    }

    void MarketDataXTP::OnDepthMarketData(XTPMD *market_data, int64_t *bid1_qty, int32_t bid1_count, int32_t max_bid1_count,
                                      int64_t *ask1_qty, int32_t ask1_count, int32_t max_ask1_count) {
        if (nullptr == market_data) {
            SPDLOG_ERROR("XTPMD is nullptr");
        }

        Quote &quote = get_public_writer()->open_data<Quote>(0);
        from_xtp(*market_data, quote);
        get_public_writer()->close_data();
    }


逐笔行情写入  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

当行情源API的快照回调虚函数触发时, 
需要将行情源的逐笔委托行情数据转换成 `kungfu::longfist::types::Entrust` 数据结构, 
需要将行情源的逐笔成交行情数据转换成 `kungfu::longfist::types::Transaction` 数据结构.


建议分别为Entrust和Transaction分别创建各自的band的信道, 具体操作参考以下XTP范例.


范例

.. code-block:: cpp
    :linenos: 

    // 声明两个线程私有writer变量
    class MarketDataXTP : public XTP::API::QuoteSpi, public broker::MarketData {
    // ... 其他内容
    private:
        inline static thread_local yijinjing::journal::writer_ptr entrust_band_writer_ = nullptr;
        inline static thread_local yijinjing::journal::writer_ptr transaction_band_writer_ = nullptr;
    };

    // pre_start 申请创建对应的band信道
    void MarketDataXTP::pre_start() {
        entrust_band_uid_ = request_band("market-data-band-entrust", 256);
        transaction_band_uid_ = request_band("market-data-band-transaction", 256);
    }

    // 交易所转换
    inline void from_xtp(const XTP_MARKET_TYPE &xtp_market_type, char *exchange_id) {
        if (xtp_market_type == XTP_MKT_SH_A) {
            strcpy(exchange_id, "SSE");
        } else if (xtp_market_type == XTP_MKT_SZ_A) {
            strcpy(exchange_id, "SZE");
        }
    }

    // 逐笔委托转换
    inline void from_xtp(const XTPTickByTickStruct &ori, Entrust &des) {
        from_xtp(ori.exchange_id, des.exchange_id);
        des.instrument_id = ori.ticker;
        des.data_time = nsec_from_xtp_timestamp(ori.data_time);

        des.price = ori.entrust.price;
        des.volume = ori.entrust.qty;
        des.main_seq = ori.entrust.channel_no;
        des.seq = ori.entrust.seq;

        if (ori.entrust.ord_type == '1') {
            des.price_type = PriceType::Any;
        } else if (ori.entrust.ord_type == '2') {
            des.price_type = PriceType::Limit;
        } else if (ori.entrust.ord_type == 'U') {
            des.price_type = PriceType::ForwardBest;
        }

        // xtp（深交所的order_no在xtp接口注释标注为无意义，偶尔为0 seq对应的是真正的订单号 上交所的order_no是订单号）
        if (strcmp(des.exchange_id, "SSE")) {
            des.orig_order_no = ori.entrust.order_no;
        } else {
            des.orig_order_no = ori.entrust.seq;
        }

        switch (ori.entrust.side) {
        case 'B': {
            des.side = Side::Buy;
            break;
        }
        case 'S': {
            des.side = Side::Sell;
            break;
        }
        case '1': {
            des.side = Side::Buy;
            break;
        }
        case '2': {
            des.side = Side::Sell;
            break;
        }
        default: {
            des.side = Side::Unknown;
            break;
        }
        }
    }




    // XTP行情源的逐笔行情回调
    void MarketDataXTP::OnTickByTick(XTPTBT *tbt_data) {
        if (tbt_data->type == XTP_TBT_ENTRUST) {
            if (tbt_data->entrust.ord_type == 'D') {
            if (not transaction_band_writer_) {
                if (not has_band_writer(transaction_band_uid_)) {
                return;
                }
                transaction_band_writer_ = get_band_writer(transaction_band_uid_);
            }
            Transaction &transaction = transaction_band_writer_->open_data<Transaction>(0);
            from_xtp(*tbt_data, transaction);
            transaction_band_writer_->close_data();
            } else {
            if (not entrust_band_writer_) {
                if (not has_band_writer(entrust_band_uid_)) {
                return;
                }
                entrust_band_writer_ = get_band_writer(entrust_band_uid_);
            }
            Entrust &entrust = entrust_band_writer_->open_data<Entrust>(0);
            from_xtp(*tbt_data, entrust);
            entrust_band_writer_->close_data();
            }
        } else if (tbt_data->type == XTP_TBT_TRADE) {
            if (not transaction_band_writer_) {
            if (not has_band_writer(transaction_band_uid_)) {
                return;
            }
            transaction_band_writer_ = get_band_writer(transaction_band_uid_);
            }
            Transaction &transaction = transaction_band_writer_->open_data<Transaction>(0);
            from_xtp(*tbt_data, transaction);
            transaction_band_writer_->close_data();
        }
    }