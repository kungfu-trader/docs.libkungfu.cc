快速开始
============

添加代码
----------------------

创建目录结构
^^^^^^^^^^^^^^^^^^^^^^^^^^

源码目录结构::

    xtp/                                        # xtp柜台名称
    ├── src/
    │   └── cpp
    │       ├── buffer_data.h
    │       ├── exports.cpp
    │       ├── marketdata_xtp.cpp
    │       ├── marketdata_xtp.h
    │       ├── serialize_xtp.h
    │       ├── trader_xtp.cpp
    │       ├── trader_xtp.h
    │       └── type_convert.h
    └── package.json                            # 编译配置信息




配置package.json文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json
    :linenos:    


    {
        "name": "@kungfu-trader/kfx-broker-xtp-demo",
        "author": {
            "name": "Kungfu Trader",
            "email": "info@kungfu.link"
        },
        "version": "2.7.5-alpha.6",
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
            "build": "C:/Users/PC/Documents/kfgit/v27/kf27/artifact/build/stage/artifact-kungfu/v2/v2.7.5-alpha.6/win-unpacked/resources/kfc/kfs.exe extension build",
            "clean": "C:/Users/PC/Documents/kfgit/v27/kf27/artifact/build/stage/artifact-kungfu/v2/v2.7.5-alpha.6/win-unpacked/resources/kfc/kfs.exe extension clean",
            "format": "node ../../framework/core/.gyp/run-format-cpp.js src",
            "install": "node -e \"require('@kungfu-trader/kungfu-core').prebuilt('install')\"",
            "package": "kfs extension package"
        },
        "dependencies": {
            "@kungfu-trader/kungfu-core": "^2.7.5-alpha.6"
        },
        "devDependencies": {
            "@kungfu-trader/kungfu-sdk": "^2.7.5-alpha.6"
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


-------------


serialize_xtp.h文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

XTP数据结构添加to_stirng方便打印日志查看数据

.. code-block:: cpp
    :linenos:  


    #ifndef KUNGFU_SERIALIZE_XTP_H
    #define KUNGFU_SERIALIZE_XTP_H
    #include <nlohmann/json.hpp>
    #include <xtp_api_struct.h>
    namespace nlohmann {
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPQueryOrderRsp, order_xtp_id, order_client_id, order_cancel_client_id,
                                    order_cancel_xtp_id, ticker, market, price, quantity, price_type, side,
                                    position_effect, reserved1, reserved2, business_type, qty_traded, qty_left,
                                    insert_time, update_time, cancel_time, trade_amount, order_local_id, order_status,
                                    order_submit_status, order_type);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPOrderInsertInfo, order_xtp_id, order_client_id, ticker, market, price, stop_price,
                                    quantity, price_type, side, position_effect, reserved1, reserved2, business_type);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPTradeReport, order_xtp_id, order_client_id, ticker, market, local_order_id,
                                    exec_id, price, quantity, trade_time, trade_amount, report_index, order_exch_id,
                                    trade_type, side, position_effect, reserved1, reserved2, business_type, branch_pbu);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPOrderCancelInfo, order_cancel_xtp_id, order_xtp_id);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPQueryStkPositionRsp, ticker, ticker_name, market, total_qty, sellable_qty,
                                    avg_price, unrealized_pnl, yesterday_position, purchase_redeemable_qty,
                                    position_direction, position_security_type, executable_option, lockable_position,
                                    executable_underlying, locked_position, usable_locked_position, profit_price,
                                    buy_cost, profit_cost, unknown);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPQueryAssetRsp, total_asset, buying_power, security_asset, fund_buy_amount,
                                    fund_buy_fee, fund_sell_amount, fund_sell_fee, withholding_amount, account_type,
                                    frozen_margin, frozen_exec_cash, frozen_exec_fee, pay_later, preadva_pay,
                                    orig_banlance, banlance, deposit_withdraw, trade_netting, captial_asset,
                                    force_freeze_amount, preferred_amount, repay_stock_aval_banlance,
                                    exchange_cur_risk_degree, company_cur_risk_degree, unknown);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPMarketDataStruct, exchange_id, ticker, last_price, pre_close_price, open_price,
                                    high_price, low_price, close_price, pre_total_long_positon, total_long_positon,
                                    pre_settl_price, settl_price, upper_limit_price, lower_limit_price, pre_delta,
                                    curr_delta, data_time, qty, turnover, avg_price, bid, ask, bid_qty, ask_qty,
                                    trades_count, ticker_status);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPRspInfoStruct, error_id, error_msg);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPOrderInfoEx, order_xtp_id, order_client_id, order_cancel_client_id,
                                    order_cancel_xtp_id, ticker, market, price, quantity, price_type, business_type,
                                    qty_traded, qty_left, insert_time, update_time, cancel_time, trade_amount,
                                    order_local_id, order_status, order_submit_status, order_type, order_exch_id,
                                    order_err_t, unknown);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XTPSpecificTickerStruct, exchange_id, ticker);
    } // namespace nlohmann
    namespace kungfu::wingchun::xtp {
    template <typename T> std::string to_string(const T &ori) {
        nlohmann::json j;
        to_json(j, ori);
        return j.dump();
    }
    } // namespace kungfu::wingchun::xtp
    #endif




-------------


type_convert.h文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

XTP和Kungfu数据结构的转换

.. code-block:: cpp
    :linenos:  


    #ifndef KUNGFU_XTP_EXT_TYPE_CONVERT_H
    #define KUNGFU_XTP_EXT_TYPE_CONVERT_H

    #include <cstddef>
    #include <cstdio>
    #include <cstring>
    #include <ctime>
    #include <kungfu/longfist/longfist.h>
    #include <kungfu/wingchun/common.h>
    #include <kungfu/yijinjing/time.h>
    #include <nlohmann/json.hpp>
    #include <xtp_api_struct.h>

    using namespace kungfu::longfist;
    using namespace kungfu::longfist::enums;
    using namespace kungfu::longfist::types;

    namespace kungfu::wingchun::xtp {

    template <typename T> inline void set_offset(T &t) {
        switch (t.side) {
        case Side::Buy:
            t.offset = Offset::Open;
            break;
        case Side::Sell:
            t.offset = Offset::Close;
            break;
        default:
            SPDLOG_ERROR("Invalidated kf_side : {} ", t.side);
            break;
        }
    }

    inline XTP_PROTOCOL_TYPE get_xtp_protocol_type(const std::string &p) {
        if (p == "udp") {
            return XTP_PROTOCOL_UDP;
        } else {
            return XTP_PROTOCOL_TCP;
        }
    }

    inline int64_t nsec_from_xtp_timestamp(int64_t xtp_time) {
        std::tm result = {};
        result.tm_year = xtp_time / (int64_t)1e13 - 1900;
        result.tm_mon = xtp_time % (int64_t)1e13 / (int64_t)1e11 - 1;
        result.tm_mday = xtp_time % (int64_t)1e11 / (int64_t)1e9;
        result.tm_hour = xtp_time % (int64_t)1e9 / (int64_t)1e7;
        result.tm_min = xtp_time % (int)1e7 / (int)1e5;
        result.tm_sec = xtp_time % (int)1e5 / (int)1e3;
        int milli_sec = xtp_time % (int)1e3;
        std::time_t parsed_time = std::mktime(&result);
        return parsed_time * kungfu::yijinjing::time_unit::NANOSECONDS_PER_SECOND +
            milli_sec * kungfu::yijinjing::time_unit::NANOSECONDS_PER_MILLISECOND;
    }

    inline void from_xtp(const XTP_MARKET_TYPE &xtp_market_type, char *exchange_id) {
        if (xtp_market_type == XTP_MKT_SH_A) {
            strcpy(exchange_id, "SSE");
        } else if (xtp_market_type == XTP_MKT_SZ_A) {
            strcpy(exchange_id, "SZE");
        }
    }

    inline void to_xtp(XTP_MARKET_TYPE &xtp_market_type, const char *exchange_id) {
        if (!strcmp(exchange_id, "SSE")) {
            xtp_market_type = XTP_MKT_SH_A;
        } else if (!strcmp(exchange_id, "SZE")) {
            xtp_market_type = XTP_MKT_SZ_A;
        } else {
            xtp_market_type = XTP_MKT_UNKNOWN;
        }
    }

    inline std::string exchange_id_from_xtp(const XTP_EXCHANGE_TYPE ex) {
        if (ex == XTP_EXCHANGE_SH) {
            return EXCHANGE_SSE;
        } else if (ex == XTP_EXCHANGE_SZ) {
            return EXCHANGE_SZE;
        } else {
            return "Unknown";
        }
    }

    inline void from_xtp(const XTP_EXCHANGE_TYPE &xtp_exchange_type, char *exchange_id) {
        if (xtp_exchange_type == XTP_EXCHANGE_SH) {
            strcpy(exchange_id, "SSE");
        } else if (xtp_exchange_type == XTP_EXCHANGE_SZ) {
            strcpy(exchange_id, "SZE");
        }
    }

    inline void to_xtp_exchange(XTP_EXCHANGE_TYPE &xtp_exchange_type, const char *exchange_id) {
        if (strcmp(exchange_id, "SSE") == 0) {
            xtp_exchange_type = XTP_EXCHANGE_SH;
        } else if (strcmp(exchange_id, "SZE") == 0) {
            xtp_exchange_type = XTP_EXCHANGE_SZ;
        } else {
            xtp_exchange_type = XTP_EXCHANGE_UNKNOWN;
        }
    }

    inline void from_xtp(const XTP_PRICE_TYPE &xtp_price_type, const XTP_MARKET_TYPE &xtp_exchange_type,
                        PriceType &price_type) {
        if (xtp_price_type == XTP_PRICE_LIMIT)
            price_type = PriceType::Limit;
        else if (xtp_price_type == XTP_PRICE_BEST5_OR_CANCEL)
            price_type = PriceType::FakBest5;
        else if (xtp_exchange_type == XTP_MKT_SH_A) {
            if (xtp_price_type == XTP_PRICE_BEST5_OR_LIMIT)
                price_type = PriceType::ReverseBest;
        } else if (xtp_exchange_type == XTP_MKT_SZ_A) {
            if (xtp_price_type == XTP_PRICE_BEST_OR_CANCEL)
                price_type = PriceType::Fak;
            else if (xtp_price_type == XTP_PRICE_FORWARD_BEST)
                price_type = PriceType::ForwardBest;
            else if (xtp_price_type == XTP_PRICE_REVERSE_BEST_LIMIT)
                price_type = PriceType::ReverseBest;
            else if (xtp_price_type == XTP_PRICE_ALL_OR_CANCEL)
                price_type = PriceType::Fok;
        } else
            price_type = PriceType::Unknown;
    }

    inline void to_xtp(XTP_PRICE_TYPE &xtp_price_type, const PriceType &price_type, const char *exchange) {
        if (price_type == PriceType::Limit)
            xtp_price_type = XTP_PRICE_LIMIT;
        else if ((price_type == PriceType::Any) || (price_type == PriceType::FakBest5))
            xtp_price_type = XTP_PRICE_BEST5_OR_CANCEL;
        else if (strcmp(exchange, EXCHANGE_SSE) == 0) {
            if (price_type == PriceType::ReverseBest)
                xtp_price_type = XTP_PRICE_BEST5_OR_LIMIT;
        } else if (strcmp(exchange, EXCHANGE_SZE) == 0) {
            if (price_type == PriceType::Fak)
                xtp_price_type = XTP_PRICE_BEST_OR_CANCEL;
            else if (price_type == PriceType::ForwardBest)
                xtp_price_type = XTP_PRICE_FORWARD_BEST;
            else if (price_type == PriceType::ReverseBest)
                xtp_price_type = XTP_PRICE_REVERSE_BEST_LIMIT;
            else if (price_type == PriceType::Fok)
                xtp_price_type = XTP_PRICE_ALL_OR_CANCEL;
        } else
            xtp_price_type = XTP_PRICE_TYPE_UNKNOWN;
    }

    inline void from_xtp(const XTP_ORDER_STATUS_TYPE &xtp_order_status, OrderStatus &status) {
        if (xtp_order_status == XTP_ORDER_STATUS_INIT || xtp_order_status == XTP_ORDER_STATUS_NOTRADEQUEUEING) {
            status = OrderStatus::Pending;
        } else if (xtp_order_status == XTP_ORDER_STATUS_ALLTRADED) {
            status = OrderStatus::Filled;
        } else if (xtp_order_status == XTP_ORDER_STATUS_CANCELED) {
            status = OrderStatus::Cancelled;
        } else if (xtp_order_status == XTP_ORDER_STATUS_PARTTRADEDQUEUEING) {
            status = OrderStatus::PartialFilledActive;
        } else if (xtp_order_status == XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING) {
            status = OrderStatus::PartialFilledNotActive;
        } else if (xtp_order_status == XTP_ORDER_STATUS_REJECTED) {
            status = OrderStatus::Error;
        } else {
            status = OrderStatus::Unknown;
        }
    }

    inline void from_xtp(XTPQSI *ticker_info, Instrument &instrument) {
        instrument.instrument_id = ticker_info->ticker;
        if (ticker_info->exchange_id == 1) {
            instrument.exchange_id = EXCHANGE_SSE;
        } else if (ticker_info->exchange_id == 2) {
            instrument.exchange_id = EXCHANGE_SZE;
        } else {
            instrument.exchange_id = "unknown";
        }
        memcpy(instrument.product_id, ticker_info->ticker_name, strlen(ticker_info->ticker_name));
        instrument.instrument_type = get_instrument_type(instrument.exchange_id, instrument.instrument_id);
        instrument.price_tick = ticker_info->price_tick;
    }

    inline void from_xtp(const XTP_SIDE_TYPE &xtp_side, Side &side) {
        if (xtp_side == XTP_SIDE_BUY) {
            side = Side::Buy;
        } else if (xtp_side == XTP_SIDE_SELL) {
            side = Side::Sell;
        }
    }

    inline void to_xtp(XTP_SIDE_TYPE &xtp_side, const Side &side) {
        if (side == Side::Buy) {
            xtp_side = XTP_SIDE_BUY;
        } else if (side == Side::Sell) {
            xtp_side = XTP_SIDE_SELL;
        }
    }

    inline void to_xtp(XTPMarketDataStruct &des, const Quote &ori) {
        // TODO
    }

    inline void from_xtp(const XTPMarketDataStruct &ori, Quote &des) {
        des.data_time = nsec_from_xtp_timestamp(ori.data_time);
        des.instrument_id = ori.ticker;
        from_xtp(ori.exchange_id, des.exchange_id);

        des.instrument_type = ori.data_type != XTP_MARKETDATA_OPTION
                                ? get_instrument_type(des.exchange_id, des.instrument_id)
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

    inline void to_xtp(XTPOrderInsertInfo &des, const OrderInput &ori) {
        strcpy(des.ticker, ori.instrument_id);
        to_xtp(des.market, ori.exchange_id);
        des.price = ori.limit_price;
        des.quantity = ori.volume;
        to_xtp(des.side, ori.side);
        to_xtp(des.price_type, ori.price_type, ori.exchange_id);
        des.business_type = XTP_BUSINESS_TYPE_CASH;
    }

    inline void from_xtp(const XTPOrderInsertInfo &ori, OrderInput &des) {
        // TODO
    }

    inline void from_xtp(const XTPOrderInfo &ori, Order &des) {
        des.instrument_id = ori.ticker;
        from_xtp(ori.market, des.exchange_id);
        from_xtp(ori.price_type, ori.market, des.price_type);
        des.volume = ori.quantity;
        des.volume_left = ori.quantity - ori.qty_traded;
        des.limit_price = ori.price;
        from_xtp(ori.order_status, des.status);
        from_xtp(ori.side, des.side);
        set_offset(des);
        des.instrument_type = get_instrument_type(des.exchange_id, des.instrument_id);
        if (ori.update_time > 0) {
            des.update_time = nsec_from_xtp_timestamp(ori.update_time);
        }
        std::string str_external_order_id = std::to_string(ori.order_xtp_id);
        des.external_order_id = str_external_order_id.c_str();
    }

    inline void from_xtp(const XTPQueryOrderRsp &ori, HistoryOrder &des) {
        des.instrument_id = ori.ticker;
        from_xtp(ori.market, des.exchange_id);
        from_xtp(ori.price_type, ori.market, des.price_type);
        des.volume = ori.quantity;
        des.volume_left = ori.qty_left;
        des.limit_price = ori.price;
        from_xtp(ori.order_status, des.status);
        from_xtp(ori.side, des.side);
        set_offset(des);
        des.instrument_type = get_instrument_type(des.exchange_id, des.instrument_id);
        if (ori.update_time > 0) {
            des.update_time = nsec_from_xtp_timestamp(ori.update_time);
        }
        des.external_order_id, std::to_string(ori.order_xtp_id).c_str();
    }

    inline void from_xtp_no_price_type(const XTPOrderInfo &ori, Order &des) {
        des.instrument_id = ori.ticker;
        from_xtp(ori.market, des.exchange_id);
        des.volume = ori.quantity;
        des.volume_left = ori.quantity - ori.qty_traded;
        des.limit_price = ori.price;
        from_xtp(ori.order_status, des.status);
        from_xtp(ori.side, des.side);
        set_offset(des);
        des.instrument_type = get_instrument_type(des.exchange_id, des.instrument_id);
        if (ori.update_time > 0) {
            des.update_time = nsec_from_xtp_timestamp(ori.update_time);
        }
        std::string str_external_order_id = std::to_string(ori.order_xtp_id);
        des.external_order_id = str_external_order_id.c_str();
    }

    inline void from_xtp(const XTPTradeReport &ori, Trade &des) {
        des.instrument_id = ori.ticker;
        des.volume = ori.quantity;
        des.price = ori.price;
        from_xtp(ori.market, des.exchange_id);
        des.instrument_type = get_instrument_type(des.exchange_id, des.instrument_id);
        from_xtp(ori.side, des.side);
        set_offset(des);
        des.trade_time = yijinjing::time::now_in_nano();
        des.external_order_id = std::to_string(ori.order_xtp_id).c_str();
        des.external_trade_id = ori.exec_id;
    }

    inline void from_xtp(const XTPQueryTradeRsp &ori, HistoryTrade &des) {
        des.instrument_id = ori.ticker;
        des.volume = ori.quantity;
        des.price = ori.price;
        from_xtp(ori.market, des.exchange_id);
        from_xtp(ori.side, des.side);
        //  des.offset = Offset::Open;
        set_offset(des);
        des.instrument_type = get_instrument_type(des.exchange_id, des.instrument_id);
        des.trade_time = nsec_from_xtp_timestamp(ori.trade_time);
        des.external_order_id = std::to_string(ori.order_xtp_id).c_str();
        des.external_trade_id = ori.exec_id;
    }

    inline void from_xtp(const XTPQueryStkPositionRsp &ori, Position &des) {
        des.instrument_id = ori.ticker;
        from_xtp(ori.market, des.exchange_id);
        des.volume = ori.total_qty;
        des.yesterday_volume = ori.sellable_qty;
        des.avg_open_price = ori.avg_price;
        des.position_cost_price = ori.avg_price;
        des.static_yesterday = ori.yesterday_position;
        //  des.open_volume // 数据不足以算出该字段, 保持为0
        //  des.frozen_yesterday // 数据不足以算出该字段, 保持为0
        //  des.frozen_total // 数据不足以算出该字段, 保持为0
    }

    inline void from_xtp(const XTPQueryAssetRsp &ori, Asset &des) { des.avail = ori.buying_power; }

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

    inline void from_xtp(const XTPTickByTickStruct &ori, Transaction &des) {
        from_xtp(ori.exchange_id, des.exchange_id);
        des.instrument_id = ori.ticker;
        des.data_time = nsec_from_xtp_timestamp(ori.data_time);

        if (ori.type == XTP_TBT_ENTRUST) {
            des.instrument_id = ori.ticker;
            des.data_time = nsec_from_xtp_timestamp(ori.data_time);

            des.main_seq = ori.entrust.channel_no;
            des.seq = ori.entrust.seq;

            des.price = ori.entrust.price;
            des.volume = ori.entrust.qty;

            if (ori.entrust.side == 'B') {
                des.side = Side::Buy;
                des.bid_no = ori.entrust.order_no;
            } else {
                des.side = Side::Sell;
                des.ask_no = ori.entrust.order_no;
            }
            des.exec_type = ExecType::Cancel;

        } else {

            des.main_seq = ori.trade.channel_no;
            des.seq = ori.trade.seq;

            des.price = ori.trade.price;
            des.volume = ori.trade.qty;

            des.bid_no = ori.trade.bid_no;
            des.ask_no = ori.trade.ask_no;

            switch (ori.trade.trade_flag) {
            case 'B': {
                des.side = Side::Buy;
                des.exec_type = ExecType::Trade;
                break;
            }
            case 'S': {
                des.side = Side::Sell;
                des.exec_type = ExecType::Trade;
                break;
            }
            case 'N': {
                des.side = Side::Unknown;
                des.exec_type = ExecType::Trade;
                break;
            }
            case '4': {
                des.side = (des.bid_no < des.ask_no) ? Side::Sell : Side::Buy;
                des.exec_type = ExecType::Cancel;
                break;
            }
            case 'F': {
                des.side = (des.bid_no < des.ask_no) ? Side::Sell : Side::Buy;
                des.exec_type = ExecType::Trade;
                break;
            }
            default: {
                break;
            }
            }
        }
    }
    } // namespace kungfu::wingchun::xtp
    #endif // KUNGFU_XTP_EXT_TYPE_CONVERT_H



-------------


buffer_data.h文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

封装xtp回调函数参数, 方便落地原始数据到journal

.. code-block:: cpp
    :linenos:  


    #ifndef XTP_BUFFER_DATA_H
    #define XTP_BUFFER_DATA_H

    #include "serialize_xtp.h"

    static constexpr int32_t kXTPOrderInfoType = 12340001;
    static constexpr int32_t kXTPTradeReportType = 12340002;
    static constexpr int32_t kQueryXTPOrderInfoType = 12340003;
    static constexpr int32_t kQueryXTPTradeReportType = 12340004;
    static constexpr int32_t kCancelOrderErrorType = 12340005;

    static constexpr int32_t kQueryAssetType = 12340011;
    static constexpr int32_t kQueryPositionType = 12340012;

    struct BufferXTPTradeReport {
        XTPQueryTradeRsp trade_info;
        XTPRI error_info;
        int request_id;
        bool is_last;
        uint64_t session_id;
    };

    struct BufferXTPOrderInfo {
        XTPOrderInfo order_info;
        XTPRI error_info;
        int request_id;
        bool is_last;
        uint64_t session_id;
    };

    struct BufferXTPOrderCancelInfo {
        XTPOrderCancelInfo cancel_info;
        XTPRI error_info;
        uint64_t session_id;
    };

    struct BufferXTPQueryAssetRsp {
        XTPQueryAssetRsp asset;
        XTPRI error_info;
        int request_id;
        bool is_last;
        uint64_t session_id;
    };

    struct BufferXTPQueryStkPositionRsp {
        XTPQueryStkPositionRsp position;
        XTPRI error_info;
        int request_id;
        bool is_last;
        uint64_t session_id;
    };

    namespace nlohmann {
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(BufferXTPTradeReport, trade_info, session_id, error_info, request_id, is_last);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(BufferXTPOrderInfo, order_info, session_id, error_info, request_id, is_last);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(BufferXTPOrderCancelInfo, cancel_info, error_info, session_id);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(BufferXTPQueryAssetRsp, asset, error_info, session_id, request_id, is_last);
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(BufferXTPQueryStkPositionRsp, position, error_info, session_id, request_id, is_last);

    } // namespace nlohmann

    #endif // XTP_BUFFER_DATA_H    


----------------------------


trader_xtp.h文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

xtp的交易柜台头文件定义

.. code-block:: cpp
    :linenos:  


    #ifndef KUNGFU_XTP_EXT_TRADER_H
    #define KUNGFU_XTP_EXT_TRADER_H

    #include <kungfu/wingchun/broker/trader.h>
    #include <xtp_trader_api.h>

    namespace kungfu::wingchun::xtp {
    using namespace kungfu::longfist;
    using namespace kungfu::longfist::types;

    struct TDConfiguration {
    int client_id;
    std::string account_id;
    std::string password;
    std::string software_key;
    std::string td_ip;
    int td_port;
    bool sync_external_order;
    bool recover_order_trade;
    };

    inline void from_json(const nlohmann::json &j, TDConfiguration &c) {
    j.at("client_id").get_to(c.client_id);
    j.at("account_id").get_to(c.account_id);
    j.at("password").get_to(c.password);
    j.at("software_key").get_to(c.software_key);
    j.at("td_ip").get_to(c.td_ip);
    j.at("td_port").get_to(c.td_port);
    c.sync_external_order = j.value<bool>("sync_external_order", false);
    c.recover_order_trade = j.value<bool>("recover_order_trade", true);
    }

    class TraderXTP : public XTP::API::TraderSpi, public broker::Trader {
    public:
    explicit TraderXTP(broker::BrokerVendor &vendor);

    ~TraderXTP() override;

    [[nodiscard]] longfist::enums::AccountType get_account_type() const override {
        return longfist::enums::AccountType::Stock;
    }

    void pre_start() override;

    void on_start() override;

    void on_exit() override;

    bool insert_order(const event_ptr &event) override;

    bool cancel_order(const event_ptr &event) override;

    bool req_position() override;

    bool on_custom_event(const event_ptr &event) override;

    bool req_account() override;

    bool req_history_order(const event_ptr &event) override;

    bool req_history_trade(const event_ptr &event) override;

    void on_recover() override;

    /// 当客户端的某个连接与交易后台通信连接断开时，该方法被调用。
    ///@param reason 错误原因，请与错误代码表对应
    ///@param session_id 资金账户对应的session_id，登录时得到
    ///@remark
    /// 用户主动调用logout导致的断线，不会触发此函数。api不会自动重连，当断线发生时，请用户自行选择后续操作，可以在此函数中调用Login重新登录，并更新session_id，此时用户收到的数据跟断线之前是连续的
    void OnDisconnected(uint64_t session_id, int reason) override;

    /// 错误应答
    ///@param error_info
    /// 当服务器响应发生错误时的具体的错误代码和错误信息,当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@remark 此函数只有在服务器发生错误时才会调用，一般无需用户处理
    void OnError(XTPRI *error_info) override{};

    /// 报单通知
    ///@param order_info 订单响应具体信息，用户可以通过order_info.order_xtp_id来管理订单，通过GetClientIDByXTPID() ==
    ///  client_id来过滤自己的订单，order_info.qty_left字段在订单为未成交、部成、全成、废单状态时，表示此订单还没有成交的数量，在部撤、全撤状态时，表示此订单被撤的数量。order_info.order_cancel_xtp_id为其所对应的撤单ID，不为0时表示此单被撤成功
    ///@param error_info
    /// 订单被拒绝或者发生错误时错误代码和错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@remark
    /// 每次订单状态更新时，都会被调用，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线，在订单未成交、全部成交、全部撤单、部分撤单、已拒绝这些状态时会有响应，对于部分成交的情况，请由订单的成交回报来自行确认。所有登录了此用户的客户端都将收到此用户的订单响应
    void OnOrderEvent(XTPOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) override;

    /// 成交通知
    ///@param trade_info 成交回报的具体信息，用户可以通过trade_info.order_xtp_id来管理订单，通过GetClientIDByXTPID() ==
    ///  client_id来过滤自己的订单。对于上交所，exec_id可以唯一标识一笔成交。当发现2笔成交回报拥有相同的exec_id，则可以认为此笔交易自成交了。对于深交所，exec_id是唯一的，暂时无此判断机制。report_index+market字段可以组成唯一标识表示成交回报。
    ///@remark
    /// 订单有成交发生的时候，会被调用，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线。所有登录了此用户的客户端都将收到此用户的成交回报。相关订单为部成状态，需要用户通过成交回报的成交数量来确定，OnOrderEvent()不会推送部成状态。
    void OnTradeEvent(XTPTradeReport *trade_info, uint64_t session_id) override;

    /// 撤单出错响应
    ///@param cancel_info 撤单具体信息，包括撤单的order_cancel_xtp_id和待撤单的order_xtp_id
    ///@param error_info
    /// 撤单被拒绝或者发生错误时错误代码和错误信息，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@remark 此响应只会在撤单发生错误时被回调
    void OnCancelOrderError(XTPOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) override;

    /// 请求查询报单响应
    ///@param order_info 查询到的一个报单
    ///@param error_info
    /// 查询报单时发生错误时，返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark
    /// 由于支持分时段查询，一个查询请求可能对应多个响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryOrder(XTPQueryOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last,
                        uint64_t session_id) override;

    /// 请求查询成交响应
    ///@param trade_info 查询到的一个成交回报
    ///@param error_info
    /// 查询成交回报发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark
    /// 由于支持分时段查询，一个查询请求可能对应多个响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryTrade(XTPQueryTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last,
                        uint64_t session_id) override;

    /// 请求查询投资者持仓响应
    ///@param position 查询到的一只股票的持仓情况
    ///@param error_info
    /// 查询账户持仓发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark
    /// 由于用户可能持有多个股票，一个查询请求可能对应多个响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryPosition(XTPQueryStkPositionRsp *position, XTPRI *error_info, int request_id, bool is_last,
                        uint64_t session_id) override;

    /// 请求查询资金账户响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param asset 查询到的资金账户情况
    ///@param error_info
    /// 查询资金账户发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryAsset(XTPQueryAssetRsp *asset, XTPRI *error_info, int request_id, bool is_last,
                        uint64_t session_id) override;

    /// 请求查询分级基金信息响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param fund_info 查询到的分级基金情况
    ///@param error_info
    /// 查询分级基金发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryStructuredFund(XTPStructuredFundInfo *fund_info, XTPRI *error_info, int request_id, bool is_last,
                                uint64_t session_id) override{};

    /// 请求查询资金划拨订单响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param fund_transfer_info 查询到的资金账户情况
    ///@param error_info
    /// 查询资金账户发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, int request_id, bool is_last,
                            uint64_t session_id) override{};

    /// 资金划拨通知
    ///@param fund_transfer_info
    /// 资金划拨通知的具体信息，用户可以通过fund_transfer_info.serial_id来管理订单，通过GetClientIDByXTPID() ==
    ///  client_id来过滤自己的订单。
    ///@param error_info
    /// 资金划拨订单被拒绝或者发生错误时错误代码和错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@remark
    /// 当资金划拨订单有状态变化的时候，会被调用，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线。所有登录了此用户的客户端都将收到此用户的资金划拨通知。
    void OnFundTransfer(XTPFundTransferNotice *fund_transfer_info, XTPRI *error_info, uint64_t session_id) override{};

    /// 请求查询ETF清单文件的响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param etf_info 查询到的ETF清单文件情况
    ///@param error_info
    /// 查询ETF清单文件发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryETF(XTPQueryETFBaseRsp *etf_info, XTPRI *error_info, int request_id, bool is_last,
                    uint64_t session_id) override{};

    /// 请求查询ETF股票篮的响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param etf_component_info 查询到的ETF合约的相关成分股信息
    ///@param error_info
    /// 查询ETF股票篮发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryETFBasket(XTPQueryETFComponentRsp *etf_component_info, XTPRI *error_info, int request_id, bool is_last,
                            uint64_t session_id) override{};

    /// 请求查询今日新股申购信息列表的响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param ipo_info 查询到的今日新股申购的一只股票信息
    ///@param error_info
    /// 查询今日新股申购信息列表发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryIPOInfoList(XTPQueryIPOTickerRsp *ipo_info, XTPRI *error_info, int request_id, bool is_last,
                            uint64_t session_id) override{};

    /// 请求查询用户新股申购额度信息的响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    ///@param quota_info 查询到的用户某个市场的今日新股申购额度信息
    ///@param error_info
    /// 查查询用户新股申购额度信息发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
    ///@param request_id 此消息响应函数对应的请求ID
    ///@param is_last
    /// 此消息响应函数是否为request_id这条请求所对应的最后一个响应，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
    ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    void OnQueryIPOQuotaInfo(XTPQueryIPOQuotaRsp *quota_info, XTPRI *error_info, int request_id, bool is_last,
                            uint64_t session_id) override{};

    private:
    TDConfiguration config_{};
    XTP::API::TraderApi *api_{};
    uint64_t session_id_{};
    int request_id_{};
    int get_request_id() { return ++request_id_; }
    std::string trading_day_{};

    std::unordered_map<uint64_t, uint64_t> map_kf_to_xtp_order_id_{};
    std::unordered_map<uint64_t, uint64_t> map_xtp_to_kf_order_id_{};
    std::unordered_map<uint64_t, uint64_t> map_request_location_{};
    std::unordered_map<uint64_t, std::unordered_set<std::string>> map_xtp_order_id_to_xtp_trader_ids_{};
    std::unordered_map<uint64_t, std::vector<XTPTradeReport>> map_xtp_order_id_to_XTPTradeReports_{};
    std::unordered_map<uint64_t, int64_t> map_xtp_order_id_to_traded_volume_{};
    std::unordered_map<uint64_t, std::queue<uint64_t>> map_xtp_order_id_to_action_ids_{};

    yijinjing::journal::writer_ptr get_history_writer(uint64_t request_id);

    bool custom_OnCancelOrderError(const event_ptr &event);
    bool custom_OnOrderEvent(const event_ptr &event);
    bool custom_OnTradeEvent(const event_ptr &event);
    bool custom_OnQueryOrder(const event_ptr &event);
    bool custom_OnQueryTrade(const event_ptr &event);
    bool custom_OnQueryAsset(const event_ptr &event);
    bool custom_OnQueryPosition(const event_ptr &event);

    bool custom_OnCancelOrderError(const XTPOrderCancelInfo &cancel_info, const XTPRI &error_info, uint64_t session_id);
    bool custom_OnOrderEvent(const XTPOrderInfo &order_info, const XTPRI &error_info, uint64_t session_id);
    bool custom_OnTradeEvent(const XTPTradeReport &trade_info, uint64_t session_id);
    bool custom_OnQueryOrder(const XTPOrderInfo &order_info, const XTPRI &error_info, int request_id, bool is_last,
                            uint64_t session_id);
    bool custom_OnQueryTrade(const XTPTradeReport &trade_info, const XTPRI &error_info, int request_id, bool is_last,
                            uint64_t session_id);
    bool custom_OnQueryAsset(const XTPQueryAssetRsp &asset, const XTPRI &error_info, int request_id, bool is_last,
                            uint64_t session_id);
    bool custom_OnQueryPosition(const XTPQueryStkPositionRsp &position, const XTPRI &error_info, int request_id,
                                bool is_last, uint64_t session_id);

    void try_deal_XTPTradeReport(uint64_t xtp_order_id);
    bool generate_external_order(const XTPOrderInfo &order_info);

    void add_XTPTradeReport(const XTPTradeReport &trade_info);
    bool has_dealt_trade(uint64_t xtp_order_id, const std::string &exec_id);
    void add_dealt_trade(uint64_t xtp_order_id, const std::string &exec_id);

    void add_traded_volume(uint64_t order_xtp_id, int64_t trade_volume);
    int64_t get_traded_volume(uint64_t order_xtp_id);

    void add_action_id(uint64_t xtp_order_id, int64_t action_id);
    uint64_t get_action_id(uint64_t xtp_order_id);

    void req_order_trade();
    void try_ready();
    bool req_order_over_{false};
    bool req_trade_over_{false};
    };
    } // namespace kungfu::wingchun::xtp
    #endif // KUNGFU_XTP_EXT_TRADER_H


----------------------------


trader_xtp.cpp文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

xtp的交易柜台函数实现

.. code-block:: cpp
    :linenos: 

    #include "trader_xtp.h"
    #include "buffer_data.h"
    #include "serialize_xtp.h"
    #include "type_convert.h"
    #include <algorithm>

    namespace kungfu::wingchun::xtp {
    using namespace kungfu::yijinjing::data;
    using namespace kungfu::yijinjing;

    TraderXTP::TraderXTP(broker::BrokerVendor &vendor) : Trader(vendor) {
        KUNGFU_SETUP_LOG();
        SPDLOG_DEBUG("arguments: {}", get_vendor().get_arguments());
    }

    TraderXTP::~TraderXTP() {
        if (api_ != nullptr) {
            api_->Release();
        }
    }

    void TraderXTP::pre_start() {
        config_ = nlohmann::json::parse(get_config());
        SPDLOG_INFO("config: {}", get_config());
        if (not config_.recover_order_trade) {
            disable_recover();
        }
    }

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

    void TraderXTP::on_exit() {
        if (api_ != nullptr and session_id_ > 0) {
            auto result = api_->Logout(session_id_);
            SPDLOG_INFO("Logout with return code {}", result);
        }
    }

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

    bool TraderXTP::cancel_order(const event_ptr &event) {
        const OrderAction &action = event->data<OrderAction>();
        SPDLOG_DEBUG("OrderAction: {}", action.to_string());
        auto order_id_iter = map_kf_to_xtp_order_id_.find(action.order_id);
        if (order_id_iter == map_kf_to_xtp_order_id_.end()) {
            SPDLOG_ERROR("failed to cancel order {}, can't find related xtp order id", action.order_id);
            return false;
        }

        if (not has_order(action.order_id)) {
            SPDLOG_ERROR("no order_id {} in orders_", action.order_id);
            return false;
        }

        auto &order_state = get_order(action.order_id);
        uint64_t order_xtp_id = order_id_iter->second;
        add_action_id(order_xtp_id, action.order_action_id);
        auto xtp_action_id = api_->CancelOrder(order_xtp_id, session_id_);
        auto success = xtp_action_id != 0;

        if (not success) {
            XTPRI *error_info = api_->GetApiLastError();
            SPDLOG_ERROR("failed to cancel order {}, order_xtp_id: {} session_id: {} error_id: {} error_msg: {}",
                        action.order_id, order_xtp_id, session_id_, error_info->error_id, error_info->error_msg);
            OrderActionError &error = get_writer(event->source())->open_data<OrderActionError>(now());
            error.order_id = action.order_id; // 订单ID
            std::string str_external_order_id = std::to_string(order_xtp_id);
            error.external_order_id = str_external_order_id.c_str();
            error.order_action_id = action.order_action_id; // 订单操作ID,
            error.error_id = xtp_action_id;                 // 错误ID
            error.error_msg = error_info->error_msg;        // 错误信息
            error.insert_time = time::now_in_nano();        // 写入时间
            SPDLOG_DEBUG("OrderActionError: {}", error.to_string());
            get_writer(event->source())->close_data();
            return false;
        }

        if (not is_final_status(order_state.data.status) or order_state.data.status == OrderStatus::Lost) {
            order_state.data.status = OrderStatus::Cancelling;
            try_write_to(order_state.data, order_state.dest);
        }
        SPDLOG_DEBUG("Order: {}", order_state.data.to_string());
        return success;
    }

    bool TraderXTP::req_position() {
        SPDLOG_INFO("req_position");
        return api_->QueryPosition(nullptr, session_id_, get_request_id()) == 0;
    }

    bool TraderXTP::req_account() {
        SPDLOG_INFO("req_account");
        return api_->QueryAsset(session_id_, get_request_id()) == 0;
    }

    void TraderXTP::OnDisconnected(uint64_t session_id, int reason) {
        if (session_id == session_id_) {
            update_broker_state(BrokerState::DisConnected);
            SPDLOG_ERROR("disconnected, reason: {}", reason);
        }
    }

    void TraderXTP::OnOrderEvent(XTPOrderInfo *order_info, XTPRI *error_info, uint64_t session_id) {
        if (nullptr == order_info) {
            SPDLOG_ERROR("XTPOrderInfo is nullptr");
            return;
        }
        SPDLOG_DEBUG("XTPOrderInfo: {}", to_string(*order_info));
        auto &bf_order_info = get_thread_writer()->open_custom_data<BufferXTPOrderInfo>(kXTPOrderInfoType, now());
        memcpy(&bf_order_info.order_info, order_info, sizeof(XTPOrderInfo));
        bf_order_info.session_id = session_id;
        if (error_info != nullptr) {
            memcpy(&bf_order_info.error_info, error_info, sizeof(XTPRI));
        } else {
            memset(&bf_order_info.error_info, 0, sizeof(XTPRI));
        }
        SPDLOG_DEBUG("BufferXTPOrderInfo: {}", to_string(bf_order_info));
        get_thread_writer()->close_data();
    }

    bool TraderXTP::custom_OnOrderEvent(const event_ptr &event) {
        const auto *bf_order_info = reinterpret_cast<const BufferXTPOrderInfo *>(event->data_address());
        return custom_OnOrderEvent(bf_order_info->order_info, bf_order_info->error_info, bf_order_info->session_id);
    }

    bool TraderXTP::custom_OnOrderEvent(const XTPOrderInfo &order_info, const XTPRI &error_info, uint64_t session_id) {
        SPDLOG_DEBUG("XTPOrderInfo: {}", to_string(order_info));
        SPDLOG_DEBUG("session_id: {}, XTPRI: {}", session_id, to_string(error_info));

        auto order_xtp_id_iter = map_xtp_to_kf_order_id_.find(order_info.order_xtp_id);
        if (order_xtp_id_iter == map_xtp_to_kf_order_id_.end()) {
            SPDLOG_WARN("unrecognized order_xtp_id {}@{}", order_info.order_xtp_id, trading_day_);
            return generate_external_order(order_info);
        }

        uint64_t kf_order_id = order_xtp_id_iter->second;
        if (not has_order(kf_order_id)) {
            return generate_external_order(order_info);
        }

        auto &order_state = get_order(kf_order_id);
        if (not is_final_status(order_state.data.status) or order_state.data.status == OrderStatus::Lost) {
            from_xtp_no_price_type(order_info, order_state.data);
            order_state.data.update_time = yijinjing::time::now_in_nano();
            if (error_info.error_id != 0) {
                order_state.data.error_id = error_info.error_id;
                order_state.data.error_msg = error_info.error_msg;
            }
            try_write_to(order_state.data, order_state.dest);
            SPDLOG_DEBUG("Order: {}", order_state.data.to_string());
            try_deal_XTPTradeReport(order_info.order_xtp_id);
        }
        return true;
    }

    bool TraderXTP::generate_external_order(const XTPOrderInfo &order_info) {
        SPDLOG_DEBUG("XTPOrderInfo: {}", to_string(order_info));
        static const std::unordered_set<int> set_cancel_enum = {
            XTP_ORDER_SUBMIT_STATUS_TYPE::XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED, //
            XTP_ORDER_SUBMIT_STATUS_TYPE::XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED,  //
            XTP_ORDER_SUBMIT_STATUS_TYPE::XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED   //
        };

        if (not config_.sync_external_order) {
            return false;
        }

        if (set_cancel_enum.find(order_info.order_submit_status) != set_cancel_enum.end()) {
            SPDLOG_DEBUG("this XTPOrderInfo is xtp cancel order, do not generate kungfu Order");
            return false;
        }

        auto writer = get_public_writer();
        auto nano = yijinjing::time::now_in_nano();
        Order &order = writer->open_data<Order>(now());
        order.order_id = writer->current_frame_uid();
        from_xtp(order_info, order);
        order.insert_time = nsec_from_xtp_timestamp(order_info.insert_time);
        order.update_time = nano;
        map_kf_to_xtp_order_id_.emplace(uint64_t(order.order_id), order_info.order_xtp_id);
        map_xtp_to_kf_order_id_.emplace(order_info.order_xtp_id, uint64_t(order.order_id));
        SPDLOG_DEBUG("Order: {}", order.to_string());
        writer->close_data();
        try_deal_XTPTradeReport(order_info.order_xtp_id);
        return true;
    }

    void TraderXTP::OnTradeEvent(XTPTradeReport *trade_info, uint64_t session_id) {
        if (nullptr == trade_info) {
            SPDLOG_ERROR("XTPTradeReport is nullptr");
            return;
        }
        SPDLOG_DEBUG("XTPTradeReport: {}", to_string(*trade_info));

        auto &bf_trade_info = get_thread_writer()->open_custom_data<BufferXTPTradeReport>(kXTPTradeReportType, now());
        memcpy(&bf_trade_info.trade_info, trade_info, sizeof(XTPTradeReport));
        bf_trade_info.session_id = session_id;
        SPDLOG_DEBUG("BufferXTPOrderInfo: {}", to_string(bf_trade_info));
        get_thread_writer()->close_data();
    }

    bool TraderXTP::custom_OnTradeEvent(const XTPTradeReport &trade_info, uint64_t session_id) {
        SPDLOG_DEBUG("XTPTradeReport: {}", to_string(trade_info));
        SPDLOG_DEBUG("session_id: {}", session_id);

        auto order_xtp_id_iter = map_xtp_to_kf_order_id_.find(trade_info.order_xtp_id);
        if (order_xtp_id_iter == map_xtp_to_kf_order_id_.end()) {
            SPDLOG_WARN("unrecognized order_xtp_id {}, store in map_xtp_order_id_to_XTPTradeReports_",
                        trade_info.order_xtp_id);
            add_XTPTradeReport(trade_info);
            return false;
        }

        if (has_dealt_trade(trade_info.order_xtp_id, trade_info.exec_id)) {
            SPDLOG_DEBUG("order_xtp_id:{}, exec_id: {}, has dealt", trade_info.order_xtp_id, trade_info.exec_id);
            return false;
        }

        uint64_t kf_order_id = order_xtp_id_iter->second;
        if (not has_order(kf_order_id)) {
            SPDLOG_ERROR("no order_id {} in orders_", kf_order_id);
            return false;
        }

        add_dealt_trade(trade_info.order_xtp_id, trade_info.exec_id);
        auto &order_state = get_order(kf_order_id);

        if (has_writer(order_state.dest)) {
            auto writer = get_writer(order_state.dest);
            Trade &trade = writer->open_data<Trade>(now());
            from_xtp(trade_info, trade);
            trade.trade_id = writer->current_frame_uid();
            trade.order_id = kf_order_id;
            add_traded_volume(trade_info.order_xtp_id, trade.volume);
            SPDLOG_DEBUG("Trade: {}", trade.to_string());
            writer->close_data();
        } else {
            Trade trade{};
            from_xtp(trade_info, trade);
            trade.trade_id = get_public_writer()->current_frame_uid() xor (time::now_in_nano() & 0xFFFFFFFF);
            trade.order_id = kf_order_id;
            add_traded_volume(trade_info.order_xtp_id, trade.volume);
            SPDLOG_DEBUG("Trade: {}", trade.to_string());
            try_write_to(trade, order_state.dest);
        }

        if (not is_final_status(order_state.data.status) or order_state.data.status == OrderStatus::Lost) {
            order_state.data.volume_left = std::min<int64_t>(
                order_state.data.volume_left, order_state.data.volume - get_traded_volume(trade_info.order_xtp_id));
            if (order_state.data.volume_left > 0) {
                order_state.data.status = OrderStatus::PartialFilledActive;
            }
            order_state.data.update_time = now();
            SPDLOG_DEBUG("Order: {}", order_state.data.to_string());
            try_write_to(order_state.data, order_state.dest);
        }
        return true;
    }

    bool TraderXTP::custom_OnTradeEvent(const event_ptr &event) {
        const auto *bf_trade_info = reinterpret_cast<const BufferXTPTradeReport *>(event->data_address());
        return custom_OnTradeEvent(bf_trade_info->trade_info, bf_trade_info->session_id);
    }

    void TraderXTP::OnCancelOrderError(XTPOrderCancelInfo *cancel_info, XTPRI *error_info, uint64_t session_id) {
        if (nullptr == cancel_info) {
            SPDLOG_ERROR("XTPOrderCancelInfo is nullptr");
            return;
        }
        SPDLOG_ERROR("XTPOrderCancelInfo: {}", to_string(*cancel_info));

        auto &bf_order_cancel_info =
            get_thread_writer()->open_custom_data<BufferXTPOrderCancelInfo>(kCancelOrderErrorType, now());
        memcpy(&bf_order_cancel_info.cancel_info, cancel_info, sizeof(XTPOrderCancelInfo));
        bf_order_cancel_info.session_id = session_id;
        if (error_info != nullptr) {
            memcpy(&bf_order_cancel_info.error_info, error_info, sizeof(XTPRI));
        } else {
            memset(&bf_order_cancel_info.error_info, 0, sizeof(XTPRI));
        }
        SPDLOG_DEBUG("BufferXTPOrderInfo: {}", to_string(bf_order_cancel_info));
        get_thread_writer()->close_data();
    }

    bool TraderXTP::custom_OnCancelOrderError(const event_ptr &event) {
        const auto &bf_order_cancel_info = event->custom_data<BufferXTPOrderCancelInfo>();
        return custom_OnCancelOrderError(bf_order_cancel_info.cancel_info, bf_order_cancel_info.error_info,
                                        bf_order_cancel_info.session_id);
    }

    bool TraderXTP::custom_OnCancelOrderError(const XTPOrderCancelInfo &cancel_info, const XTPRI &error_info,
                                            uint64_t session_id) {
        SPDLOG_DEBUG("XTPOrderCancelInfo: {}", to_string(cancel_info));
        SPDLOG_DEBUG("session_id: {}, XTPRI: {}", session_id, to_string(error_info));

        uint64_t action_id = get_action_id(cancel_info.order_xtp_id);
        if (not has_order_action(action_id)) {
            SPDLOG_WARN("has not related OrderAction of {}:{}", cancel_info.order_xtp_id, action_id);
            return false;
        }

        auto action_state = get_order_action(action_id);
        auto order_id = action_state.data.order_id;
        if (not has_order(order_id)) {
            SPDLOG_WARN("order_id not in orders_ {}", order_id);
            return false;
        }

        auto order_state = get_order(order_id);
        if (has_writer(order_state.dest)) {
            OrderActionError &error = get_writer(order_state.dest)->open_data<OrderActionError>(now());
            error.order_id = order_state.data.order_id; // 订单ID
            std::string str_external_order_id = std::to_string(cancel_info.order_xtp_id);
            error.external_order_id = str_external_order_id.c_str();
            error.order_action_id = action_id;       // 订单操作ID,
            error.error_id = error_info.error_id;    // 错误ID
            error.error_msg = error_info.error_msg;  // 错误信息
            error.insert_time = time::now_in_nano(); // 写入时间
            SPDLOG_DEBUG("OrderActionError: {}", error.to_string());
            get_writer(order_state.dest)->close_data();
        } else {
            OrderActionError error{};
            error.order_id = order_state.data.order_id; // 订单ID
            std::string str_external_order_id = std::to_string(cancel_info.order_xtp_id);
            error.external_order_id = str_external_order_id.c_str();
            error.order_action_id = action_id;       // 订单操作ID,
            error.error_id = error_info.error_id;    // 错误ID
            error.error_msg = error_info.error_msg;  // 错误信息
            error.insert_time = time::now_in_nano(); // 写入时间
            SPDLOG_DEBUG("OrderActionError: {}", error.to_string());
            try_write_to(error, order_state.dest);
        }
        return true;
    }

    void TraderXTP::OnQueryPosition(XTPQueryStkPositionRsp *position, XTPRI *error_info, int request_id, bool is_last,
                                    uint64_t session_id) {
        if (nullptr == position) {
            SPDLOG_ERROR("XTPQueryStkPositionRsp is nullptr");
            return;
        }
        SPDLOG_TRACE("XTPQueryStkPositionRsp: {}", to_string(*position));

        auto &bf_position = get_thread_writer()->open_custom_data<BufferXTPQueryStkPositionRsp>(kQueryPositionType);
        memcpy(&bf_position.position, position, sizeof(XTPQueryStkPositionRsp));
        if (error_info != nullptr) {
            memcpy(&bf_position.error_info, error_info, sizeof(XTPRI));
        } else {
            memset(&bf_position.error_info, 0, sizeof(XTPRI));
        }
        bf_position.request_id = request_id;
        bf_position.is_last = is_last;
        bf_position.session_id = session_id;
        get_thread_writer()->close_data();
    }

    bool TraderXTP::custom_OnQueryPosition(const event_ptr &event) {
        const auto &bf_position = event->custom_data<BufferXTPQueryStkPositionRsp>();
        return custom_OnQueryPosition(bf_position.position, bf_position.error_info, bf_position.request_id,
                                    bf_position.is_last, bf_position.session_id);
    }

    bool TraderXTP::custom_OnQueryPosition(const XTPQueryStkPositionRsp &position, const XTPRI &error_info, int request_id,
                                        bool is_last, uint64_t session_id) {
        if (error_info.error_id != 0) {
            SPDLOG_ERROR("error_id:{}, error_msg: {}, request_id: {}, last: {}", error_info.error_id, error_info.error_msg,
                        request_id, is_last);
            return false;
        }

        SPDLOG_TRACE("XTPQueryStkPositionRsp: {}", to_string(position));
        auto writer = get_position_writer();
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
            enable_positions_sync();
        }
        return true;
    }

    void TraderXTP::OnQueryAsset(XTPQueryAssetRsp *asset, XTPRI *error_info, int request_id, bool is_last,
                                uint64_t session_id) {
        if (nullptr == asset) {
            SPDLOG_ERROR("XTPQueryAssetRsp is nullptr");
            return;
        }
        SPDLOG_TRACE("XTPQueryAssetRsp: {}", to_string(*asset));

        auto &bf_asset = get_thread_writer()->open_custom_data<BufferXTPQueryAssetRsp>(kQueryAssetType);
        memcpy(&bf_asset.asset, asset, sizeof(XTPQueryAssetRsp));
        if (error_info != nullptr) {
            memcpy(&bf_asset.error_info, error_info, sizeof(XTPRI));
        } else {
            memset(&bf_asset.error_info, 0, sizeof(XTPRI));
        }
        bf_asset.request_id = request_id;
        bf_asset.is_last = is_last;
        bf_asset.session_id = session_id;
        get_thread_writer()->close_data();
    }

    bool TraderXTP::custom_OnQueryAsset(const event_ptr &event) {
        const auto &bf_asset = event->custom_data<BufferXTPQueryAssetRsp>();
        return custom_OnQueryAsset(bf_asset.asset, bf_asset.error_info, bf_asset.request_id, bf_asset.is_last,
                                bf_asset.session_id);
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

    bool TraderXTP::req_history_order(const event_ptr &event) {
        XTPQueryOrderReq query_param{};
        int request_id = get_request_id();
        int ret = api_->QueryOrders(&query_param, session_id_, request_id);
        if (0 != ret) {
            SPDLOG_ERROR("QueryOrders False: {}", ret);
        }
        map_request_location_.emplace(request_id, event->source());
        return 0 == ret;
    }

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

    void TraderXTP::OnQueryOrder(XTPQueryOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last,
                                uint64_t session_id) {
        SPDLOG_DEBUG("request_id: {}, is_last: {}, session_id: {}", request_id, is_last, session_id);
        auto &bf_order_info = get_thread_writer()->open_custom_data<BufferXTPOrderInfo>(kQueryXTPOrderInfoType, now());
        if (order_info != nullptr) {
            memcpy(&bf_order_info.order_info, order_info, sizeof(XTPOrderInfo));
        } else {
            memset(&bf_order_info.order_info, 0, sizeof(XTPOrderInfo));
        }
        if (error_info != nullptr) {
            memcpy(&bf_order_info.error_info, error_info, sizeof(XTPRI));
        } else {
            memset(&bf_order_info.error_info, 0, sizeof(XTPRI));
        }
        bf_order_info.session_id = session_id;
        bf_order_info.request_id = request_id;
        bf_order_info.is_last = is_last;
        SPDLOG_DEBUG("BufferXTPOrderInfo: {}", to_string(bf_order_info));
        get_thread_writer()->close_frame(sizeof(BufferXTPOrderInfo));
    }

    bool TraderXTP::custom_OnQueryOrder(const event_ptr &event) {
        const auto *bf_order_info = reinterpret_cast<const BufferXTPOrderInfo *>(event->data_address());
        return custom_OnQueryOrder(bf_order_info->order_info, bf_order_info->error_info, bf_order_info->request_id,
                                bf_order_info->is_last, bf_order_info->session_id);
    }

    bool TraderXTP::custom_OnQueryOrder(const XTPOrderInfo &order_info, const XTPRI &error_info, int request_id,
                                        bool is_last, uint64_t session_id) {
        SPDLOG_DEBUG("XTPOrderInfo: {}", to_string(order_info));
        SPDLOG_DEBUG("XTPRI: {}", to_string(error_info));
        SPDLOG_DEBUG("request_id: {}, is_last: {}", request_id, is_last);

        // 查询历史流水收到nullptr, 经过journal走一圈后表现形式为 order_xtp_id == 0
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

    yijinjing::journal::writer_ptr TraderXTP::get_history_writer(uint64_t request_id) {
        return get_writer(map_request_location_.try_emplace(request_id).first->second);
    }

    void TraderXTP::OnQueryTrade(XTPQueryTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last,
                                uint64_t session_id) {
        SPDLOG_DEBUG("request_id: {}, is_last: {}, session_id: {}", request_id, is_last, session_id);
        auto &bf_trade_info = get_thread_writer()->open_custom_data<BufferXTPTradeReport>(kQueryXTPTradeReportType, now());
        if (trade_info != nullptr) {
            memcpy(&bf_trade_info.trade_info, trade_info, sizeof(XTPOrderInfo));
        } else {
            memset(&bf_trade_info.trade_info, 0, sizeof(XTPOrderInfo));
        }
        if (error_info != nullptr) {
            memcpy(&bf_trade_info.error_info, error_info, sizeof(XTPRI));
        } else {
            memset(&bf_trade_info.error_info, 0, sizeof(XTPRI));
        }
        bf_trade_info.session_id = session_id;
        bf_trade_info.request_id = request_id;
        bf_trade_info.is_last = is_last;
        SPDLOG_DEBUG("BufferXTPTradeReport: {}", to_string(bf_trade_info));
        get_thread_writer()->close_data();
    }

    bool TraderXTP::custom_OnQueryTrade(const event_ptr &event) {
        const auto *bf_trade_info = reinterpret_cast<const BufferXTPTradeReport *>(event->data_address());
        return custom_OnQueryTrade(bf_trade_info->trade_info, bf_trade_info->error_info, bf_trade_info->request_id,
                                bf_trade_info->is_last, bf_trade_info->session_id);
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

    void TraderXTP::on_recover() {
        for (auto &pair : get_orders()) {
            SPDLOG_DEBUG("Order: {}", pair.second.data.to_string());
            const std::string str_external_order_id = pair.second.data.external_order_id.to_string();
            if (not str_external_order_id.empty()) {
                uint64_t order_id = pair.first;
                uint64_t order_xtp_id = std::stoull(str_external_order_id);
                map_xtp_to_kf_order_id_.emplace(order_xtp_id, order_id);
                map_kf_to_xtp_order_id_.emplace(order_id, order_xtp_id);
            }
        }
        for (auto &pair : get_trades()) {
            SPDLOG_DEBUG("Trade: {}", pair.second.data.to_string());
            uint64_t order_xtp_id = std::stoull(pair.second.data.external_order_id);
            map_xtp_order_id_to_xtp_trader_ids_.try_emplace(order_xtp_id)
                .first->second.emplace(pair.second.data.external_trade_id.to_string());
        }
    }

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

    void TraderXTP::try_ready() {
        if (BrokerState::Ready == get_state()) {
            return;
        }

        SPDLOG_DEBUG("req_order_over_: {}, req_trade_over_: {}", req_order_over_, req_trade_over_);
        if (disable_recover_ or (req_order_over_ and req_trade_over_)) {
            update_broker_state(BrokerState::Ready);
        }
    }

    void TraderXTP::try_deal_XTPTradeReport(uint64_t xtp_order_id) {
        auto &xtp_trades = map_xtp_order_id_to_XTPTradeReports_.try_emplace(xtp_order_id).first->second;
        for (const auto &xtp_trade : xtp_trades) {
            custom_OnTradeEvent(xtp_trade, session_id_);
        }
        xtp_trades.clear();
    }

    void TraderXTP::add_XTPTradeReport(const XTPTradeReport &trade_info) {
        map_xtp_order_id_to_XTPTradeReports_.try_emplace(trade_info.order_xtp_id).first->second.push_back(trade_info);
    }

    bool TraderXTP::has_dealt_trade(uint64_t xtp_order_id, const std::string &exec_id) {
        auto &exec_ids = map_xtp_order_id_to_xtp_trader_ids_.try_emplace(xtp_order_id).first->second;
        return exec_ids.find(exec_id) != exec_ids.end();
    }

    void TraderXTP::add_dealt_trade(uint64_t xtp_order_id, const std::string &exec_id) {
        map_xtp_order_id_to_xtp_trader_ids_.try_emplace(xtp_order_id).first->second.emplace(exec_id);
    }

    bool TraderXTP::on_custom_event(const event_ptr &event) {
        SPDLOG_DEBUG("msg_type: {}", event->msg_type());
        switch (event->msg_type()) {
        case kXTPOrderInfoType:
            return custom_OnOrderEvent(event);
        case kXTPTradeReportType:
            return custom_OnTradeEvent(event);
        case kQueryXTPOrderInfoType:
            return custom_OnQueryOrder(event);
        case kQueryXTPTradeReportType:
            return custom_OnQueryTrade(event);
        case kCancelOrderErrorType:
            return custom_OnCancelOrderError(event);
        case kQueryAssetType:
            return custom_OnQueryAsset(event);
        case kQueryPositionType:
            return custom_OnQueryPosition(event);
        default:
            SPDLOG_ERROR("unrecognized msg_type: {}", event->msg_type());
            return false;
        }
    }

    void TraderXTP::add_traded_volume(uint64_t order_xtp_id, int64_t trade_volume) {
        map_xtp_order_id_to_traded_volume_.try_emplace(order_xtp_id).first->second += trade_volume;
    }

    int64_t TraderXTP::get_traded_volume(uint64_t order_xtp_id) {
        return map_xtp_order_id_to_traded_volume_.try_emplace(order_xtp_id).first->second;
    }

    void TraderXTP::add_action_id(uint64_t xtp_order_id, int64_t action_id) {
        map_xtp_order_id_to_action_ids_.try_emplace(xtp_order_id).first->second.push(action_id);
    }

    uint64_t TraderXTP::get_action_id(uint64_t xtp_order_id) {
        auto &action_ids = map_xtp_order_id_to_action_ids_.try_emplace(xtp_order_id).first->second;
        if (not action_ids.empty()) {
            uint64_t action_id = action_ids.front();
            action_ids.pop();
            SPDLOG_DEBUG("xtp_order_id:action_id = {}:{}", xtp_order_id, action_id);
            return action_id;
        } else {
            SPDLOG_ERROR("action_ids is empty");
            return 0;
        }
    }

    } // namespace kungfu::wingchun::xtp



----------------------------


marketdata_xtp.h文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

xtp的行情源头文件定义

.. code-block:: cpp
    :linenos:  

    #ifndef KUNGFU_XTP_EXT_MARKET_DATA_H
    #define KUNGFU_XTP_EXT_MARKET_DATA_H

    #include <kungfu/wingchun/broker/marketdata.h>
    #include <kungfu/yijinjing/common.h>
    #include <xtp_quote_api.h>

    namespace kungfu::wingchun::xtp {
    class MarketDataXTP : public XTP::API::QuoteSpi, public broker::MarketData {
    public:
        explicit MarketDataXTP(broker::BrokerVendor &vendor);

        ~MarketDataXTP() override;

        bool subscribe(const std::vector<longfist::types::InstrumentKey> &instrument_keys) override;

        bool subscribe_all() override;
        bool subscribe_custom(const longfist::types::CustomSubscribe &custom_sub) override;
        bool unsubscribe(const std::vector<longfist::types::InstrumentKey> &instrument_keys) override { return false; };

        /// 当客户端与行情后台通信连接断开时，该方法被调用。
        ///@param reason 错误原因，请与错误代码表对应
        ///@remark
        ///  api不会自动重连，当断线发生时，请用户自行选择后续操作。可以在此函数中调用Login重新登录。注意用户重新登录后，需要重新订阅行情
        void OnDisconnected(int reason) override;

        /// 订阅行情应答，包括股票、指数和期权
        ///@param ticker 详细的合约订阅情况
        ///@param error_info 订阅合约发生错误时的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
        ///@param is_last 是否此次订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        ///@remark 每条订阅的合约均对应一条订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
        void OnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) override;

        /// 深度行情通知，包含买一卖一队列
        ///@param market_data 行情数据
        ///@param bid1_qty 买一队列数据
        ///@param bid1_count 买一队列的有效委托笔数
        ///@param max_bid1_count 买一队列总委托笔数
        ///@param ask1_qty 卖一队列数据
        ///@param ask1_count 卖一队列的有效委托笔数
        ///@param max_ask1_count 卖一队列总委托笔数
        ///@remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
        void OnDepthMarketData(XTPMD *market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count,
                            int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count) override;

        /// 订阅逐笔行情应答，包括股票、指数和期权
        ///@param ticker 详细的合约订阅情况
        ///@param error_info 订阅合约发生错误时的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
        ///@param is_last 是否此次订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        ///@remark 每条订阅的合约均对应一条订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
        void OnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) override;

        /// 逐笔行情通知，包括股票、指数和期权
        ///@param tbt_data
        /// 逐笔行情数据，包括逐笔委托和逐笔成交，此为共用结构体，需要根据type来区分是逐笔委托还是逐笔成交，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
        void OnTickByTick(XTPTBT *tbt_data) override;

        /// 订阅全市场的股票逐笔行情应答
        ///@param exchange_id
        /// 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN，表示沪深全市场，XTP_EXCHANGE_SH表示为上海全市场，XTP_EXCHANGE_SZ表示为深圳全市场
        ///@param error_info
        /// 取消订阅合约时发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
        ///@remark 需要快速返回
        void OnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) override;

        /// 查询可交易合约的应答
        ///@param ticker_info 可交易合约信息
        ///@param error_info
        /// 查询可交易合约时发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
        ///@param is_last
        /// 是否此次查询可交易合约的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        void OnQueryAllTickers(XTPQSI *ticker_info, XTPRI *error_info, bool is_last) override;

        /// 查询合约完整静态信息的应答
        ///@param ticker_info 合约完整静态信息
        ///@param error_info
        /// 查询合约完整静态信息时发生错误时返回的错误信息，当error_info为空，或者error_info.error_id为0时，表明没有错误
        ///@param is_last
        /// 是否此次查询合约完整静态信息的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        void OnQueryAllTickersFullInfo(XTPQFI *ticker_info, XTPRI *error_info, bool is_last) override;

    protected:
        void on_start() override;

        void pre_start() override;

    private:
        XTP::API::QuoteApi *api_{};
        uint32_t entrust_band_uid_{};
        uint32_t transaction_band_uid_{};

        inline static thread_local yijinjing::journal::writer_ptr entrust_band_writer_{};
        inline static thread_local yijinjing::journal::writer_ptr transaction_band_writer_{};

        bool subscribe(const std::vector<std::string> &instruments, const std::string &exchange_id);
    };
    } // namespace kungfu::wingchun::xtp

    #endif // KUNGFU_XTP_EXT_MARKET_DATA_H
 


----------------------------


marketdata_xtp.cpp文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

xtp的行情源函数实现

.. code-block:: cpp
    :linenos:  


    #include "marketdata_xtp.h"
    #include "serialize_xtp.h"
    #include "type_convert.h"

    using namespace kungfu::yijinjing;
    using namespace kungfu::yijinjing::data;

    namespace kungfu::wingchun::xtp {
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

    MarketDataXTP::MarketDataXTP(broker::BrokerVendor &vendor) : MarketData(vendor), api_(nullptr) {
        KUNGFU_SETUP_LOG();
        SPDLOG_DEBUG("arguments: {}", get_vendor().get_arguments());
    }

    MarketDataXTP::~MarketDataXTP() {
        if (api_ != nullptr) {
            api_->Release();
        }
    }

    void MarketDataXTP::pre_start() {
        entrust_band_uid_ = request_band("market-data-band-entrust", 256);
        transaction_band_uid_ = request_band("market-data-band-transaction", 256);
    }

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

    bool MarketDataXTP::subscribe(const std::vector<InstrumentKey> &instrument_keys) {
        bool result = true;
        std::vector<std::string> sse_tickers;
        std::vector<std::string> sze_tickers;
        for (const auto &inst : instrument_keys) {
            std::string ticker = inst.instrument_id;
            if (strcmp(inst.exchange_id, EXCHANGE_SSE) == 0) {
                sse_tickers.push_back(ticker);
            } else if (strcmp(inst.exchange_id, EXCHANGE_SZE) == 0) {
                sze_tickers.push_back(ticker);
            }
        }
        if (!sse_tickers.empty()) {
            result &= subscribe(sse_tickers, EXCHANGE_SSE);
        }
        if (!sze_tickers.empty()) {
            result &= subscribe(sze_tickers, EXCHANGE_SZE);
        }
        return result;
    }

    bool MarketDataXTP::subscribe(const std::vector<std::string> &instruments, const std::string &exchange_id) {
        int size = instruments.size();
        std::vector<char *> insts;
        insts.reserve(size);
        std::transform(instruments.begin(), instruments.end(), std::back_inserter(insts),
                    [](auto &s) { return const_cast<char *>(s.c_str()); });
        XTP_EXCHANGE_TYPE exchange;
        to_xtp_exchange(exchange, exchange_id.c_str());
        int level1_result = api_->SubscribeMarketData(insts.data(), size, exchange);
        int level2_result = api_->SubscribeTickByTick(insts.data(), size, exchange);
        SPDLOG_INFO("subscribe {} from {}, l1 rtn code {}, l2 rtn code {}", size, exchange_id, level1_result,
                    level2_result);
        return level1_result == 0 and level2_result == 0;
    }

    bool MarketDataXTP::subscribe_all() {
        auto result = api_->SubscribeAllMarketData() && api_->SubscribeAllTickByTick();
        SPDLOG_INFO("subscribe all, rtn code {}", result);
        return result;
    }

    bool MarketDataXTP::subscribe_custom(const longfist::types::CustomSubscribe &custom_sub) {
        SPDLOG_INFO("custom_sub, market_type {} instrument_type {} data_type {} update_time {}",
                    int(custom_sub.market_type), long(custom_sub.instrument_type), long(custom_sub.data_type),
                    long(custom_sub.update_time));
        subscribe_all();
        return true;
    }

    void MarketDataXTP::OnDisconnected(int reason) {
        SPDLOG_ERROR("disconnected with reason {}", reason);
        update_broker_state(BrokerState::DisConnected);
    }

    void MarketDataXTP::OnSubMarketData(XTPST *ticker, XTPRI *error_info, bool is_last) {
        if (nullptr != ticker) {
            SPDLOG_DEBUG("XTPST: {}, is_last: {}", to_string(*ticker), is_last);
        }
        if (error_info != nullptr && error_info->error_id != 0) {
            SPDLOG_ERROR("failed to subscribe level 1, [{}] {}", error_info->error_id, error_info->error_msg);
        }
    }

    void MarketDataXTP::OnSubTickByTick(XTPST *ticker, XTPRI *error_info, bool is_last) {
        if (nullptr != ticker) {
            SPDLOG_DEBUG("XTPST: {}, is_last: {}", to_string(*ticker), is_last);
        }
        if (error_info != nullptr && error_info->error_id != 0) {
            SPDLOG_ERROR("failed to subscribe level 2, [{}] {}", error_info->error_id, error_info->error_msg);
        }
    }

    void MarketDataXTP::OnSubscribeAllTickByTick(XTP_EXCHANGE_TYPE exchange_id, XTPRI *error_info) {
        if (error_info != nullptr && error_info->error_id != 0) {
            SPDLOG_ERROR("failed to subscribe level 2 all, [{}] {}", error_info->error_id, error_info->error_msg);
        }
    }

    void MarketDataXTP::OnQueryAllTickers(XTPQSI *ticker_info, XTPRI *error_info, bool is_last) {
        if (nullptr != error_info && error_info->error_id != 0) {
            SPDLOG_ERROR("error_id : {} , error_msg : {}", error_info->error_id, error_info->error_msg);
            return;
        }

        if (nullptr == ticker_info) {
            SPDLOG_ERROR("ticker_info is nullptr");
            return;
        }

        Instrument &instrument = get_public_writer()->open_data<Instrument>(0);
        from_xtp(ticker_info, instrument);
        get_public_writer()->close_data();
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

    void MarketDataXTP::OnTickByTick(XTPTBT *tbt_data) {
        if (tbt_data->type == XTP_TBT_ENTRUST) {
            if (tbt_data->entrust.ord_type == 'D') {
                if (not transaction_band_writer_) {
                    while (not has_band_writer(transaction_band_uid_)) {
                        std::this_thread::sleep_for(std::chrono::milliseconds(1));
                    }
                    transaction_band_writer_ = get_band_writer(transaction_band_uid_);
                }
                Transaction &transaction = transaction_band_writer_->open_data<Transaction>(0);
                from_xtp(*tbt_data, transaction);
                transaction_band_writer_->close_data();
            } else {
                if (not entrust_band_writer_) {
                    while (not has_band_writer(entrust_band_uid_)) {
                        std::this_thread::sleep_for(std::chrono::milliseconds(1));
                    }
                    entrust_band_writer_ = get_band_writer(entrust_band_uid_);
                }
                Entrust &entrust = entrust_band_writer_->open_data<Entrust>(0);
                from_xtp(*tbt_data, entrust);
                entrust_band_writer_->close_data();
            }
        } else if (tbt_data->type == XTP_TBT_TRADE) {
            if (not transaction_band_writer_) {
                while (not has_band_writer(transaction_band_uid_)) {
                    std::this_thread::sleep_for(std::chrono::milliseconds(1));
                }
                transaction_band_writer_ = get_band_writer(transaction_band_uid_);
            }
            Transaction &transaction = transaction_band_writer_->open_data<Transaction>(0);
            from_xtp(*tbt_data, transaction);
            transaction_band_writer_->close_data();
        }
    }

    void MarketDataXTP::OnQueryAllTickersFullInfo(XTPQFI *ticker_info, XTPRI *error_info, bool is_last) {
        if (nullptr != error_info && error_info->error_id != 0) {
            SPDLOG_INFO("error_id : {} , error_msg : {}", error_info->error_id, error_info->error_msg);
            return;
        }

        if (nullptr == ticker_info) {
            SPDLOG_ERROR("ticker_info is nullptr");
            return;
        }

        Instrument &instrument = get_public_writer()->open_data<Instrument>(0);
        instrument.instrument_id = ticker_info->ticker;
        if (ticker_info->exchange_id == 1) {
            instrument.exchange_id = EXCHANGE_SSE;
        } else if (ticker_info->exchange_id == 2) {
            instrument.exchange_id = EXCHANGE_SZE;
        }

        memcpy(instrument.product_id, ticker_info->ticker_name, strlen(ticker_info->ticker_name));
        instrument.instrument_type = get_instrument_type(instrument.exchange_id, instrument.instrument_id);
        SPDLOG_TRACE("instrument {}", instrument.to_string());
        get_public_writer()->close_data();

        if (is_last) {
            record_stored_instruments_trading_day(time::strfnow("%Y%m%d"));
        }
    }
    } // namespace kungfu::wingchun::xtp


----------------------------


exports.cpp文件
^^^^^^^^^^^^^^^^^^^^^^^^^^

xtp柜台和行情源绑定到python模块

.. code-block:: cpp
    :linenos:  


    #include "marketdata_xtp.h"
    #include "trader_xtp.h"

    #include <kungfu/wingchun/extension.h>

    KUNGFU_EXTENSION() {
        KUNGFU_DEFINE_MD(kungfu::wingchun::xtp::MarketDataXTP);
        KUNGFU_DEFINE_TD(kungfu::wingchun::xtp::TraderXTP);
    }


-------------------------------

编译
----------------------

编译指令
^^^^^^^^^^^^^^^^