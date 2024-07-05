Broker配置和启动流程
=====================

Broker配置
---------------------------------


TD和MD的账户信息配置通过package.json来设置, 详情参考 **package.json配置信息**  一节.

通过前端界面配置的账户信息, 可以通过get_config()获取到一个json格式的字符串, 
可以直接使用Kungfu引入的nlohmann json库进行解析, 使用方式有两种, 

1. 直接使用json对象通过key和value键值对获取前端输入的信息.
#. 定义一个struct并且配置from_json函数, nlohmann json库可以直接将json格式的字符串转换成对应的struct对象.

建议使用第二种, 以下是xtp的范例



.. code-block:: cpp
    :linenos:   

    // 自定义一个struct
    struct MDConfiguration {
        int client_id;
        std::string account_id;
        std::string password;
        std::string md_ip;
        int md_port;
        std::string protocol;
        int buffer_size;
        bool query_instruments;
    };

    // 定义如何从json转换成struct对象
    void from_json(const nlohmann::json &j, MDConfiguration &c) {
        j.at("client_id").get_to(c.client_id);
        j.at("account_id").get_to(c.account_id);
        j.at("password").get_to(c.password);
        j.at("md_ip").get_to(c.md_ip);
        j.at("md_port").get_to(c.md_port);
        c.protocol = j.value("protocol", "tcp");
        if (c.protocol != "udp") {
            c.protocol = "tcp";
        }
        c.buffer_size = j.value("buffer_size", 64);
        c.query_instruments = j.value<bool>("query_instruments", false);
    }

    // 获取前端配置的参数信息
    void MarketDataXTP::on_start() {
        MDConfiguration config = nlohmann::json::parse(get_config()); 
        // 其他处理代码
    }




.. code-block:: json
    :linenos:   

    {
        "name": "@kungfu-trader/kfx-broker-xtp-demo",
        "author": {
            "name": "Kungfu Trader",
            "email": "info@kungfu.link"
        },
        "version": "2.7.5-alpha.14",
        "description": "Kungfu Extension - XTP Demo",
        "license": "Apache-2.0",
        "main": "package.json",
        "repository": {
            "url": "https://github.com/kungfu-trader/kungfu.git"
        },
        "publishConfig": {
            "registry": "https://npm.pkg.github.com"
        },
        "binary": {
            "module_name": "kfx-broker-xtp-demo",
            "module_path": "dist/xtp",
            "remote_path": "{module_name}/v{major}/v{version}",
            "package_name": "{module_name}-v{version}-{platform}-{arch}-{configuration}.tar.gz",
            "host": "https://prebuilt.libkungfu.cc"
        },
        "scripts": {
            "build": "kfs extension build",
            "clean": "kfs extension clean",
            "format": "node ../../framework/core/.gyp/run-format-cpp.js src",
            "install": "node -e \"require('@kungfu-trader/kungfu-core').prebuilt('install')\"",
            "package": "kfs extension package"
        },
        "dependencies": {
            "@kungfu-trader/kungfu-core": "^2.7.5-alpha.14"
        },
        "devDependencies": {
            "@kungfu-trader/kungfu-sdk": "^2.7.5-alpha.14"
        },
        "kungfuDependencies": {
            "xtp": "v2.2.37.4"
        },
        "kungfuBuild": {
            "build_type": "Release",
            "cpp": {
                "target": "bind/python",
                "links": {
                    "windows": [
                        "xtptraderapi",
                        "xtpquoteapi"
                    ],
                    "linux": [
                        "xtptraderapi",
                        "xtpquoteapi"
                    ],
                    "macos": [
                        "xtptraderapi",
                        "xtpquoteapi"
                    ]
                }
            }
        },
        "kungfuConfig": {
            "key": "xtp",
            "name": "XTP",
            "language": {
                "zh-CN": {
                    "account_name": "账户别名",
                    "account_name_tip": "请填写账户别名",
                    "account_id": "账户",
                    "account_id_tip": "请填写账户, 例如:1504091",
                    "password": "密码",
                    "password_tip": "请填写密码, 例如:123456",
                    "software_key": "软件密钥",
                    "software_key_tip": "请填写软件密钥, 例如:b8aa7173bba3470e390d787219b2112",
                    "td_ip": "交易IP",
                    "td_ip_tip": "请填写交易IP, 例如:61.152.102.111",
                    "td_port": "交易端口",
                    "td_port_tip": "请填写交易端口, 例如:8601",
                    "client_id": "客户ID",
                    "client_id_tip": "请填写自定义多点登录ID 1-99整数,不同节点之间不要重复",
                    "md_ip": "行情IP",
                    "md_ip_tip": "请填写行情IP, 例如:61.152.102.110",
                    "md_port": "行情端口",
                    "md_port_tip": "请填写行情端口, 例如:8602",
                    "protocol": "协议",
                    "protocol_tip": "请选择协议, tcp 或者 udp",
                    "buffer_size": "缓冲区大小",
                    "buffer_size_tip": "请填写 缓冲区大小(mb)",
                    "sync_external_order": "同步外部订单",
                    "sync_external_order_msg": "是否同步外部订单",
                    "sync_external_order_tip": "若开启则同步用户在其他交易软件的订单",
                    "recover_order_trade": "恢复订单",
                    "recover_order_trade_msg": "启动时是否查询恢复订单",
                    "recover_order_trade_tip": "若开启则启动时查询今日委托和成交",
                    "query_instruments": "查询可交易标的",
                    "query_instruments_tip": "是否查询可交易标的, 开启后会查询所有可交易标的, 流量太大频繁查询可能导致账号或ip被XTP拉黑"
                },
                "en-US": {
                    "account_name": "account name",
                    "account_name_tip": "Please enter account name",
                    "account_id": "account id",
                    "account_id_tip": "Please enter account id",
                    "password": "password",
                    "password_tip": "Please enter password, for example:123456",
                    "software_key": "software key",
                    "software_key_tip": "Please enter software key, for example :b8aa7173bba3470e390d787219b2112",
                    "td_ip": "td IP",
                    "td_ip_tip": "Please enter td IP, for example:61.152.102.111",
                    "td_port": "td port",
                    "td_port_tip": "Please enter td port, for example:8601",
                    "client_id": "client id",
                    "client_id_tip": "Please enter t user-defined multipoint client ID, which is an integer ranging from 1 to 99. The value must be unique on different nodes",
                    "md_ip": "md IP",
                    "md_ip_tip": "Please enter md IP, for example :61.152.102.110",
                    "md_port": "md port",
                    "md_port_tip": "Please enter md port, for example:8602",
                    "protocol": "protocol",
                    "protocol_tip": "Please select protocol, tcp or udp",
                    "buffer_size": "buffer size",
                    "buffer_size_tip": "Please enter buffer size(mb)",
                    "sync_external_order": "sync external order",
                    "sync_external_order_msg": "Whether open sync_external_order",
                    "sync_external_order_tip": "If enabled, it synchronizes users' orders in other trading software",
                    "recover_order_trade": "recover order trade",
                    "recover_order_trade_msg": "Whether recover order trade",
                    "recover_order_trade_tip": "If enabled, query order and trade when TD ready",
                    "query_instruments": "query instruments",
                    "query_instruments_tip": "If enabled, query instruments. too much infomation may result in account or ip blacklisted by XTP"
                }
            },
            "config": {
                "td": {
                    "type": [
                        "stock"
                    ],
                    "settings": [
                        {
                            "key": "account_name",
                            "name": "xtp.account_name",
                            "type": "str",
                            "tip": "xtp.account_name_tip"
                        },
                        {
                            "key": "account_id",
                            "name": "xtp.account_id",
                            "type": "str",
                            "required": true,
                            "primary": true,
                            "tip": "xtp.account_id_tip"
                        },
                        {
                            "key": "password",
                            "name": "xtp.password",
                            "type": "password",
                            "required": true,
                            "tip": "xtp.password_tip"
                        },
                        {
                            "key": "software_key",
                            "name": "xtp.software_key",
                            "type": "str",
                            "required": true,
                            "tip": "xtp.software_key_tip"
                        },
                        {
                            "key": "td_ip",
                            "name": "xtp.td_ip",
                            "type": "str",
                            "required": true,
                            "tip": "xtp.td_ip_tip"
                        },
                        {
                            "key": "td_port",
                            "name": "xtp.td_port",
                            "type": "int",
                            "required": true,
                            "tip": "xtp.td_port_tip"
                        },
                        {
                            "key": "client_id",
                            "name": "xtp.client_id",
                            "type": "int",
                            "required": true,
                            "tip": "xtp.client_id_tip"
                        },
                        {
                            "key": "sync_external_order",
                            "name": "xtp.sync_external_order",
                            "type": "bool",
                            "errMsg": "xtp.sync_external_order_msg",
                            "required": false,
                            "default": false,
                            "tip": "xtp.sync_external_order_tip"
                        },
                        {
                            "key": "recover_order_trade",
                            "name": "xtp.recover_order_trade",
                            "type": "bool",
                            "errMsg": "xtp.recover_order_trade_msg",
                            "required": false,
                            "default": false,
                            "tip": "xtp.recover_order_trade_tip"
                        }
                    ]
                },
                "md": {
                    "type": [
                        "stock"
                    ],
                    "settings": [
                        {
                            "key": "account_id",
                            "name": "xtp.account_id",
                            "type": "str",
                            "required": true,
                            "tip": "xtp.account_id_tip",
                            "default": "15011218"
                        },
                        {
                            "key": "password",
                            "name": "xtp.password",
                            "type": "password",
                            "required": true,
                            "tip": "xtp.password_tip",
                            "default": "PsVqy99v"
                        },
                        {
                            "key": "md_ip",
                            "name": "xtp.md_ip",
                            "type": "str",
                            "required": true,
                            "tip": "xtp.md_ip_tip",
                            "default": "119.3.103.38"
                        },
                        {
                            "key": "md_port",
                            "name": "xtp.md_port",
                            "type": "int",
                            "required": true,
                            "tip": "xtp.md_port_tip",
                            "default": 6002
                        },
                        {
                            "key": "protocol",
                            "name": "xtp.protocol",
                            "type": "select",
                            "options": [
                                {
                                    "value": "tcp",
                                    "label": "tcp"
                                },
                                {
                                    "value": "udp",
                                    "label": "udp"
                                }
                            ],
                            "required": false,
                            "tip": "xtp.protocol_tip",
                            "default": "tcp"
                        },
                        {
                            "key": "buffer_size",
                            "name": "xtp.buffer_size",
                            "type": "int",
                            "tip": "xtp.buffer_size_tip",
                            "required": false
                        },
                        {
                            "key": "client_id",
                            "name": "xtp.client_id",
                            "type": "int",
                            "required": true,
                            "tip": "xtp.client_id_tip",
                            "default": 23
                        },
                        {
                            "key": "query_instruments",
                            "name": "xtp.query_instruments",
                            "type": "bool",
                            "required": false,
                            "tip": "xtp.query_instruments_tip",
                            "default": false
                        }
                    ]
                }
            }
        }
    }
  



-------------------------------


Broker启动流程
--------------------


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

TD启动流程
^^^^^^^^^^^^^^^^^^^

对于同步登陆接口, 在on_start中调用登陆接口后能立刻判断是否登录成功, 登陆成功后, 立即调用恢复Order和Trade的函数, 如果设置跳过了恢复今日委托, 则立即进入Ready状态; 
否则在恢复完Order和Trade之后再进入Ready状态, 进入Ready状态后会立即执行req_position和req_account, 查询持仓和资金, 之后就可以进行委托报单操作.

对于异步登陆接口, 需要在登陆响应回调函数中才能知道是否登陆成功, 后续执行与同步登录接口同样的操作.


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
            req_order_trade(); // 登陆成功后恢复Order和Trade, 恢复完后将TD状态设置成Ready
        } else {
            update_broker_state(BrokerState::LoginFailed);
            SPDLOG_ERROR("Login failed [{}]: {}", api_->GetApiLastError()->error_id, api_->GetApiLastError()->error_msg);
        }
    }

    // 查询恢复Order和Trade
    void TraderXTP::req_order_trade() {
        if (disable_recover_) {
            return try_ready(); // 设置跳过恢复则立即设置成Ready
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

    // 将TD状态设置成Ready
    void TraderXTP::try_ready() {
        if (BrokerState::Ready == get_state()) {
            return;
        }

        SPDLOG_DEBUG("req_order_over_: {}, req_trade_over_: {}", req_order_over_, req_trade_over_);
        if (disable_recover_ or (req_order_over_ and req_trade_over_)) {
            update_broker_state(BrokerState::Ready);
        }
    }

    // xtp柜台在on_exit里退出登录
    void TraderXTP::on_exit() {
        if (api_ != nullptr and session_id_ > 0) {
            auto result = api_->Logout(session_id_);
            SPDLOG_INFO("Logout with return code {}", result);
        }
    }


---------------------------------


MD启动流程
^^^^^^^^^^^^^^^^^^^

MD的登录流程相对简单, 对于同步登陆接口, 直接在on_start里面将MD状态设置成Ready; 
对于异步登陆接口, 在登陆响应接口直接将MD状态设置成Ready.


范例

.. code-block:: cpp
    :linenos:   

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