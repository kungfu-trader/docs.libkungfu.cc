Broker启动流程
=====================

柜台和行情源模块都继承 class BrokerService, 在启动进程时, 
会先执行pre_start()做一些启动前的配置处理, 例如, 设置是否从恢复今日委托到内存, 创建Band信道等.

根据pre_start()的设置完成配置处理后, 执行on_start(), 这里一般都是设置柜台链接ip地址和端口, 以及账户密码进行连接.

当进程执行结束退出前, 会执行on_exit(), 这里一般是用于退出登录和内存释放.

.. code-block:: cpp
    :linenos:    

    
    class BrokerService {
        public:
        typedef longfist::enums::BrokerState BrokerState;

        explicit BrokerService(BrokerVendor &vendor);

        virtual ~BrokerService() = default;

        virtual void pre_start();

        virtual void on_start();

        virtual void on_exit();

        // 其他属性
    };


-------------


范例

.. code-block:: cpp
    :linenos:   

    // xtp柜台在pre_start配置是否需要恢复今日委托
    void TraderXTP::pre_start() {
        config_ = nlohmann::json::parse(get_config());
        SPDLOG_INFO("config: {}", get_config());
        if (not config_.recover_order_trade) {
            disable_recover();
        }
    }


    // xtp柜台在on_start进行登录
    void TraderXTP::on_start() {
        if (config_.client_id < 1 or config_.client_id > 99) {
            SPDLOG_ERROR("client_id must between 1 and 99");
        }
        std::string runtime_folder = get_runtime_folder();
        SPDLOG_INFO("Connecting XTP account {} with tcp://{}:{}", config_.account_id, config_.td_ip, config_.td_port);
        api_ = XTP::API::TraderApi::CreateTraderApi(config_.client_id, runtime_folder.c_str());
        api_->RegisterSpi(this);
        api_->SubscribePublicTopic(XTP_TERT_QUICK);
        api_->SetSoftwareVersion("1.1.0");
        api_->SetSoftwareKey(config_.software_key.c_str());
        session_id_ = api_->Login(config_.td_ip.c_str(), config_.td_port, config_.account_id.c_str(),
                                    config_.password.c_str(), XTP_PROTOCOL_TCP);
        if (session_id_ > 0) {
            SPDLOG_INFO("Login successfully");
            req_order_trade();
        } else {
            update_broker_state(BrokerState::LoginFailed);
            SPDLOG_ERROR("Login failed [{}]: {}", api_->GetApiLastError()->error_id, api_->GetApiLastError()->error_msg);
        }
    }

    // xtp行情源在pre_start里申请创建两个页大小为256MB的band信道
    void MarketDataXTP::pre_start() {
        entrust_band_uid_ = request_band("market-data-band-entrust", 256);
        transaction_band_uid_ = request_band("market-data-band-transaction", 256);
    }

    // xtp行情源在on_start里进行登录
    void MarketDataXTP::on_start() {
        MDConfiguration config = nlohmann::json::parse(get_config());
        if (config.client_id < 1 or config.client_id > 99) {
            SPDLOG_ERROR("client_id must between 1 and 99");
        }
        auto md_ip = config.md_ip.c_str();
        auto account_id = config.account_id.c_str();
        auto password = config.password.c_str();
        auto protocol_type = get_xtp_protocol_type(config.protocol);
        std::string runtime_folder = get_runtime_folder();
        SPDLOG_INFO("Connecting XTP MD for {} at {}://{}:{}", account_id, config.protocol, md_ip, config.md_port);
        api_ =
            XTP::API::QuoteApi::CreateQuoteApi(config.client_id, runtime_folder.c_str(), XTP_LOG_LEVEL::XTP_LOG_LEVEL_INFO);
        if (config.protocol == "udp") {
            api_->SetUDPBufferSize(config.buffer_size);
        }
        api_->RegisterSpi(this);
        if (api_->Login(md_ip, config.md_port, account_id, password, protocol_type) == 0) {
            update_broker_state(BrokerState::LoggedIn);
            update_broker_state(BrokerState::Ready);
            SPDLOG_INFO("login success! (account_id) {}", config.account_id);
            if (config.query_instruments and not check_if_stored_instruments(time::strfnow("%Y%m%d"))) {
            api_->QueryAllTickers(XTP_EXCHANGE_SH);
            api_->QueryAllTickers(XTP_EXCHANGE_SZ);
            api_->QueryAllTickersFullInfo(XTP_EXCHANGE_SH);
            api_->QueryAllTickersFullInfo(XTP_EXCHANGE_SZ);
            }
        } else {
            update_broker_state(BrokerState::LoginFailed);
            SPDLOG_ERROR("failed to login, [{}] {}", api_->GetApiLastError()->error_id, api_->GetApiLastError()->error_msg);
        }
    }


    // xtp柜台在on_exit里退出登录
    void TraderXTP::on_exit() {
        if (api_ != nullptr and session_id_ > 0) {
            auto result = api_->Logout(session_id_);
            SPDLOG_INFO("Logout with return code {}", result);
        }
    }



