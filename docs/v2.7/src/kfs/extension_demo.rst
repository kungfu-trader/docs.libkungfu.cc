Python策略范例
^^^^^^^^^^^^^^^^^^^^^^

源码目录结构::

    strategy-python-101/
    ├── src/
    │   └── python
    |       └── KungfuStrategy101Python
    |           └── __init__.py                 # python策略代码
    └── package.json                            # 编译配置信息


编译后文件目录结构::

    strategy-python-101/
    ├── src/
    │   └── python
    |       └── KungfuStrategy101Python
    |           └── __init__.py
    ├── package.json         
    ├── __pypackages__/                                         # Python模块库, 自动生成
    ├── dist/                                                   # 编译打包出来的二进制文件
    |   └── KungfuStrategy101Python
    |       └── KungfuStrategy101Python.cp39-win_amd64.pyd      # 二进制文件
    ├── pdm.lock                                                # build后下载依赖库自动生成的文件
    └── pyproject.toml                                          # build后下载依赖库自动生成的文件


package.json::

    {
        "name": "@kungfu-trader/examples-strategy-python",
        "author": {
            "name": "Kungfu Trader",
            "email": "info@kungfu.link"
        },
        "description": "KungFu Strategy 101 - Python Demo",
        "license": "Apache-2.0",
        "kungfuBuild": {
            "python": {
                "dependencies": {}
            }
        },
        "kungfuConfig": {
            "key": "KungfuStrategy101Python"
        }
    }


.. code-block:: python
    :linenos:


    # __init__.py

    import random
    from kungfu.wingchun.constants import *
    import kungfu

    lf = kungfu.__binding__.longfist
    wc = kungfu.__binding__.wingchun
    yjj = kungfu.__binding__.yijinjing

    source = "sim"  # 目标交易账户的柜台名称
    account = "fill"  # 目标交易账户的账户号, 需添加 sim 柜台的账户号为 simTest 的账户
    md_source = "sim"  # 目标行情源的柜台名称, 需添加 sim 行情源


    def pre_start(context):
        context.log.info("pre start")
        context.add_account(source, account)  # 添加交易账户
        context.subscribe(md_source, ["600000", "600004", "600009"], Exchange.SSE)  # 订阅行情
        context.subscribe(md_source, ["300033", "300059"], Exchange.SZE)  # 订阅行情
        context.subscribe(md_source, ["rb2401"], Exchange.SHFE)  # 订阅行情
        context.subscribe(md_source, ["sc2401"], Exchange.INE)  # 订阅行情
        # context.subscribe_operator("bar", "123") # 需从算子入口添加bar插件, 并定义bar的id为123
        context.throttle_insert_order = {}


    def post_start(context):
        account_uid = context.get_account_uid(source, account)
        context.log.info(f"account {source} {account}, account_uid: {account_uid}")


    def on_quote(context, quote, location, dest):
        # insert order interval 10s
        if context.now() - context.throttle_insert_order.get(quote.instrument_id, 0) < 10000000000:
            return
        context.throttle_insert_order[quote.instrument_id] = context.now()

        side = random.choice([Side.Buy, Side.Sell])
        offset = random.choice([Offset.Open, Offset.Close])
        side = random.choice([Side.Buy, Side.Sell])
        price = quote.ask_price[0] if side == Side.Buy else quote.bid_price[0]
        price_type = random.choice([PriceType.Any, PriceType.Limit])
        volume = 3 if quote.instrument_type == InstrumentType.Future else 300
        order_id = context.insert_order(
            quote.instrument_id,
            quote.exchange_id,
            source,
            account,
            price,
            volume,
            price_type,
            side,
            offset,
        )
        context.log.info(f"insert order: {order_id}")


    # 监听算子广播信息
    def on_synthetic_data(context, synthetic_dataa, location, dest):
        context.log.info("on_synthetic_data: {}".format(synthetic_dataa))


    def on_order(context, order, location, dest):
        context.log.info(f"on_order: {order}, from {location} to {dest}")

        if not wc.utils.is_final_status(order.status):
            context.cancel_order(order.order_id)


    def on_trade(context, trade, location, dest):
        context.log.info(f"on_trade: {trade}, from {location} to {dest}")

    


通过主面板的 **策略进程->添加->策略路径** 选择 KungfuStrategy101Python.cp39-win_amd64.pyd, 点击启动就可以运行Python编译后的策略代码


------------------------------


CPP策略范例
^^^^^^^^^^^^^^^^^^^^^^

源码目录结构::

    strategy-cpp-101/
    ├── src/
    │   └── cpp
    |       └── strategy.cpp                    # cpp策略代码
    └── package.json                            # 编译配置信息


编译后文件目录结构::

    strategy--101/
    ├── src/
    │   └── cpp
    |       └── strategy.cpp                                # cpp策略代码
    ├── package.json         
    ├── dist/                                               # 编译打包出来的二进制文件
    |   └── KungfuStrategy101Cpp
    |       └── KungfuStrategy101Cpp.cp39-win_amd64.pyd     # 二进制文件
    └── build                                               # build 编译生成中间文件


package.json::

    {
        "name": "@kungfu-trader/examples-strategy-cpp",
        "author": "kungfu-trader",
        "description": "KungFu Strategy 101 - C++ Demo",
        "license": "Apache-2.0",
        "kungfuConfig": {
            "key": "KungfuStrategy101Cpp"
        },
        "kungfuBuild": {
            "cpp": {
            "target": "bind/python"
            }
        }
    }



.. code-block:: cpp
    :linenos:


    // strategy.cpp
    #include <kungfu/wingchun/extension.h>
    #include <kungfu/wingchun/strategy/context.h>
    #include <kungfu/wingchun/strategy/strategy.h>

    using namespace kungfu::longfist::enums;
    using namespace kungfu::longfist::types;
    using namespace kungfu::wingchun::strategy;
    using namespace kungfu::yijinjing::data;

    KUNGFU_MAIN_STRATEGY(KungfuStrategy101) {
    public:
    KungfuStrategy101() = default;
    ~KungfuStrategy101() = default;

    void pre_start(Context_ptr & context) override {
        SPDLOG_INFO("preparing strategy");
        SPDLOG_INFO("arguments: {}", context->get_arguments());

        context->add_account("sim", "fill");
        context->subscribe("sim", {"600000"}, {"SSE"});
    }

    void post_start(Context_ptr & context) override { SPDLOG_INFO("strategy started"); }

    void on_quote(Context_ptr & context, const Quote &quote, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("Quote: {}  location: {}", quote.to_string(), location->to_string());
        context->insert_order(quote.instrument_id, quote.exchange_id, "sim", "fill", quote.last_price, 200,
                            PriceType::Limit, Side::Buy, Offset::Open);
    }

    void on_order(Context_ptr & context, const Order &order, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("Order: {}", order.to_string());
    }

    void on_trade(Context_ptr & context, const Trade &trade, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("Trade: {}", trade.to_string());
    }

    void on_tree(Context_ptr & context, const Tree &tree, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("on tree: {}", tree.to_string());
    }

    void on_synthetic_data(Context_ptr & context, const SyntheticData &synthetic_data, const location_ptr &location,
                            uint32_t dest) override {
        SPDLOG_INFO("on_synthetic_data: {} ", synthetic_data.to_string());
    }

    void on_broker_state_change(Context_ptr & context, const BrokerStateUpdate &broker_state_update,
                                const location_ptr &location) override {
        SPDLOG_INFO("on broker state changed: {}", broker_state_update.to_string());
    }

    void on_operator_state_change(Context_ptr & context, const OperatorStateUpdate &operator_state_update,
                                    const location_ptr &location) override {
        SPDLOG_INFO("on operator state changed: {}", operator_state_update.to_string());
    }
    };


    


通过主面板的 **策略进程->添加->策略路径** 选择 KungfuStrategy101Cpp.cp39-win_amd64.pyd, 点击启动就可以运行Python编译后的策略代码




------------------------------


CPP策略可执行程序范例
^^^^^^^^^^^^^^^^^^^^^^

源码目录结构::

    strategy-cpp-101-exe/
    ├── src/
    │   └── cpp
    |       └── strategy.cpp                    # cpp策略代码
    └── package.json                            # 编译配置信息


编译后文件目录结构::

    strategy-cpp-101-exe/
    ├── src/
    │   └── cpp
    |       └── strategy.cpp                    # cpp策略代码
    ├── package.json         
    ├── dist/                                   # 编译打包出来的二进制文件
    |   └── KungfuStrategy101CppExe
    |       └── KungfuStrategy101CppExe.exe     # 可执行文件
    └── build                                   # build 编译生成中间文件


package.json::

    {
    "name": "@kungfu-trader/examples-strategy-cpp",
    "author": "kungfu-trader",
    "description": "KungFu Strategy 101 - C++ Demo",
    "license": "Apache-2.0",
    "kungfuConfig": {
        "key": "KungfuStrategy101CppExe"
    },
    "kungfuBuild": {
        "cpp": {
            "target": "exe"
        }
    }
    }



.. code-block:: cpp
    :linenos:


    // strategy.cpp
    #include <kungfu/wingchun/strategy/context.h>
    #include <kungfu/wingchun/strategy/runner.h>
    #include <kungfu/wingchun/strategy/strategy.h>

    using namespace kungfu::longfist::enums;
    using namespace kungfu::longfist::types;
    using namespace kungfu::wingchun::strategy;
    using namespace kungfu::yijinjing::data;

    class KungfuStrategy101 : public Strategy {
    public:
    KungfuStrategy101() = default;
    ~KungfuStrategy101() = default;

    void pre_start(Context_ptr &context) override {
        SPDLOG_INFO("preparing strategy");
        SPDLOG_INFO("arguments: {}", context->get_arguments());

        context->add_account("sim", "fill");
        context->subscribe("sim", {"600000"}, {"SSE"});
    }

    void post_start(Context_ptr &context) override { SPDLOG_INFO("strategy started"); }

    void on_quote(Context_ptr &context, const Quote &quote, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("Quote: {}  location: {}", quote.to_string(), location->to_string());
        context->insert_order(quote.instrument_id, quote.exchange_id, "sim", "fill", quote.last_price, 200,
                            PriceType::Limit, Side::Buy, Offset::Open);
    }

    void on_order(Context_ptr &context, const Order &order, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("Order: {}", order.to_string());
    }

    void on_trade(Context_ptr &context, const Trade &trade, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("Trade: {}", trade.to_string());
    }

    void on_tree(Context_ptr &context, const Tree &tree, const location_ptr &location, uint32_t dest) override {
        SPDLOG_INFO("on tree: {}", tree.to_string());
    }

    void on_synthetic_data(Context_ptr &context, const SyntheticData &synthetic_data, const location_ptr &location,
                            uint32_t dest) override {
        SPDLOG_INFO("on_synthetic_data: {} ", synthetic_data.to_string());
    }

    void on_broker_state_change(Context_ptr &context, const BrokerStateUpdate &broker_state_update,
                                const location_ptr &location) override {
        SPDLOG_INFO("on broker state changed: {}", broker_state_update.to_string());
    }

    void on_operator_state_change(Context_ptr &context, const OperatorStateUpdate &operator_state_update,
                                    const location_ptr &location) override {
        SPDLOG_INFO("on operator state changed: {}", operator_state_update.to_string());
    }
    };

    int main(int argc, char **argv) {
        SPDLOG_INFO("runner1 add strategy1");
        Runner runner(std::make_shared<locator>(), "CppStrategy", "demo01exe", mode::LIVE, false);
        SPDLOG_INFO("runner");
        runner.add_strategy(std::make_shared<KungfuStrategy101>());
        runner.run();
        SPDLOG_INFO("Over");
        return 0;
    }


    


直接运行 KungfuStrategy101CppExe.exe 程序就可以运行以上策略



------------------------------


Python交易任务范例
^^^^^^^^^^^^^^^^^^^^^^

源码目录结构::

    kfx-task-excel-demo/
    ├── src/
    │   └── python
    |       └── Excel
    |           └── __init__.py                 # python交易任务策略代码
    ├── README.md                               # 交易任务说明
    └── package.json                            # 编译配置信息


编译后文件目录结构::

    kfx-task-excel-demo/
    ├── src/
    │   └── python
    |       └── Excel
    |           └── __init__.py                 
    ├── README.md                               
    ├── package.json         
    ├── __pypackages__/                                         # Python模块库, 自动生成
    ├── dist/                                                   # 编译打包出来的二进制文件
    |   └── Excel
    |       └── Excel.cp39-win_amd64.pyd                        # 二进制文件
    ├── pdm.lock                                                # build后下载依赖库自动生成的文件
    └── pyproject.toml                                          # build后下载依赖库自动生成的文件


package.json::
    
    {
        "name": "@kungfu-trader/kfx-task-excel",
        "description": "Kungfu Extension - Excel",
        "author": "kungfu-trader",
        "license": "Apache-2.0",
        "kungfuBuild": {
            "python": {
                "dependencies": {
                    "openpyxl": ">=3.0.10"
                }
            }
        },
        "kungfuConfig": {
            "key": "Excel",
            "name": "Excel下单",
            "ui_config": {},
            "language": {
                "zh-CN": {
                    "accountId": "账户",
                    "marketSource": "行情",
                    "taskExcel": "下单Excel",
                    "taskExcelTip": "Excel文件目前只支持一个sheet表.\n表格第一行为字段名, 皆为英文, 需要包括以下字段: \ntime: 下单时间, 字符串, 格式为 HH: mm: ss (24小时制, 时分秒皆占两位), 例: 01: 02: 03.\ninstrument_id: 标的ID, 字符串.\nexchange_id: 交易所ID, 字符串.\nlimit_price: 限价, 浮点数.\nvolume: 下单量, 整数.\nprice_type: 报单类型, 字符串, 可填 Limit、Any、FakBest5、ForwardBest、ReverseBest、Fak、Fok.\nside: 买卖, 字符串, 可填 Buy、Sell、Lock、Unlock、Exec、Drop、MarginTrade、ShortSell、RepayMargin、RepayStock.\noffset: 开平, 字符串, 可填 Open、Close、CloseToday、CloseYesterday.\nhedge_flag: 投机套保标识, 字符串, 目前只可填Speculation, 也可不填, 默认为该值.\nis_swap: 互换, 布尔值字符串, 可填 True 或 False, 也可不填, 默认为False."
                },
                "en-US": {
                    "excel": "Excel Task",
                    "accountId": "Account ID",
                    "marketSource": "Market Source",
                    "taskExcel": "Excel File",
                    "taskExcelTip": "Only one sheet is currently supported.\nThe first row of the form contains the following fields: \ntime: place order time, string, the format is HH: mm: ss (In 24-hour system, time, minutes and seconds occupy two places), like: 01: 02: 03.\ninstrument_id: instrument ID, string.\nexchange_id: exchange ID, string.\nlimit_price: limit price, float.\nvolume: place order volume, int.\nprice_type: order price type, string, allow: Limit、Any、FakBest5、ForwardBest、ReverseBest、Fak、Fok.\nside: side, string, allow: Buy、Sell、Lock、Unlock、Exec、Drop、MarginTrade、ShortSell、RepayMargin、RepayStock.\noffset: offset, string, allow: Open、Close、CloseToday、CloseYesterday.\nhedge_flag: hedge flag, string, current only allow 'Speculation', also can be empty, default is this value.\nis_swap: whether swap open or not, boolean, allow: True or False, also can be empty, default is False."
                }
            },
            "config": {
                "strategy": {
                    "type": "trade",
                    "settings": [
                    {
                        "key": "accountId",
                        "name": "Excel.accountId",
                        "type": "td",
                        "required": true,
                        "showArg": true
                    },
                    {
                        "key": "taskExcel",
                        "name": "Excel.taskExcel",
                        "type": "file",
                        "required": true,
                        "showArg": true,
                        "tip": "Excel.taskExcelTip"
                    }
                    ]
                }
            }
        }
    }



.. code-block:: python
    :linenos:
        
    # -*- coding: UTF-8 -*-
    from multiprocessing import context
    import time
    import datetime
    import json
    import pandas as pd
    import numpy as np
    import kungfu
    from kungfu.wingchun.constants import *

    TIMER_DELAY = 1000000

    lf = kungfu.__binding__.longfist


    def update_strategy_state(state, value, context):
        strategy_state = lf.types.StrategyStateUpdate()

        if state == lf.enums.StrategyState.Normal:
            strategy_state.value = str(value)
            context.log.info(str(value))
        elif state == lf.enums.StrategyState.Warn:
            strategy_state.value = str(value)
            context.log.warn(str(value))
        else:
            strategy_state.value = str(value)
            context.log.error(str(value))

        strategy_state.state = state

        context.update_strategy_state(strategy_state)


    def deal_key(key):
        return key.upper() if isinstance(key, str) else key


    def deal_instrument_id(value):
        return str(value)


    def deal_exchange_id(value):
        all_exchange_id = ["BSE","SSE","SZE","SHFE","DCE","CZCE","CFFEX","INE","GFEX"]
        resolved_exchange_id = deal_key(value)

        if resolved_exchange_id in all_exchange_id:
            return resolved_exchange_id

        return None


    def deal_limit_price(value):
        return float(value)


    def deal_volume(value):
        return int(value)


    def deal_price_type(key):
        switcher = {
            "LIMIT": PriceType.Limit,
            "ANY": PriceType.Any,
            "FAKBEST5": PriceType.FakBest5,
            "FORWARDBEST": PriceType.ForwardBest,
            "REVERSEBEST": PriceType.ReverseBest,
            "FAK": PriceType.Fak,
            "FOK": PriceType.Fok,
        }
        key = deal_key(key)
        return switcher.get(key)


    def deal_side(key):
        switcher = {
            "BUY": Side.Buy,
            "SELL": Side.Sell,
            "LOCK": Side.Lock,
            "UNLOCK": Side.Unlock,
            "EXEC": Side.Exec,
            "DROP": Side.Drop,
            "MARGINTRADE": Side.MarginTrade,
            "SHORTSELL": Side.ShortSell,
            "REPAYMARGIN": Side.RepayMargin,
            "REPAYSTOCK": Side.RepayStock,
        }
        key = deal_key(key)
        return switcher.get(key)


    def deal_offset(key):
        switcher = {
            "OPEN": Offset.Open,
            "CLOSE": Offset.Close,
            "CLOSETODAY": Offset.CloseToday,
            "CLOSEYESTERDAY": Offset.CloseYesterday,
        }
        key = deal_key(key)
        return switcher.get(key)


    def deal_hedge_flag(key):
        switcher = {
            "SPECULATION": HedgeFlag.Speculation,
        }

        if isinstance(key, str):
            key = deal_key(key)
            return switcher.get(key)

        if np.isnan(key):
            return switcher["SPECULATION"]

        return None


    def deal_is_swap(key):
        switcher = {
            "TRUE": True,
            "FALSE": False,
        }

        if isinstance(key, str):
            key = deal_key(key)
            return switcher.get(key)

        if np.isnan(key):
            return switcher["FALSE"]

        return None


    def validator_switcher(key, value, context):
        parser_switcher = {
            "instrument_id": deal_instrument_id,
            "exchange_id": deal_exchange_id,
            "limit_price": deal_limit_price,
            "volume": deal_volume,
            "price_type": deal_price_type,
            "side": deal_side,
            "offset": deal_offset,
            "hedge_flag": deal_hedge_flag,
            "is_swap": deal_is_swap,
        }

        parser = parser_switcher.get(key)

        if parser is not None:
            resolved_value = parser(value)
            if resolved_value is not None:
                return resolved_value
            else:
                update_strategy_state(
                    lf.enums.StrategyState.Error, f"列 '{key}' 的值 {value} 解析异常.", context
                )
                context.has_parse_error = True
                context.req_deregister()
        else:
            return value


    def validate_exchange_instrument(task, instruments_map, context):
        instrument_id = task.get("instrument_id")
        exchange_id = task.get("exchange_id")
        cur_map_key = str(exchange_id).lower() + str(instrument_id).lower()

        return instruments_map.get(cur_map_key)


    def parse_tasks(tasks_df, context):
        tasks = tasks_df.to_dict("records")
        resolved_tasks = []
        for index, task in enumerate(tasks):
            resolved = {k: validator_switcher(k, v, context) for k, v in task.items()}
            cur_instrument = validate_exchange_instrument(
                resolved, context.instruments_map, context
            )
            if cur_instrument is not None:
                resolved["instrument_id"] = cur_instrument.instrument_id
                resolved["exchange_id"] = cur_instrument.exchange_id
            else:
                context.log.warn(
                    f"第 {str(index + 1)} 单 instrument_id {resolved.get('instrument_id')} 或 exchange_id {resolved.get('exchange_id')} 填写错误, 请确认."
                )
            resolved_tasks.append(resolved)
            context.log.info(
                f"第 {str(index + 1)} 单: {' '.join([f'{str(k)}: {str(v)}' for k, v in resolved.items()])}"
            )
        return resolved_tasks


    def time_parser(time_strs):
        return pd.to_datetime(time_strs, format="%H:%M:%S").dt.time


    def load_excel(excel_path, context):
        if not (excel_path.endswith(".xlsx") or excel_path.endswith(".xls")):
            update_strategy_state(
                lf.enums.StrategyState.Error, "文件格式不是Excel,解析失败.", context
            )
            context.req_deregister()
            return False
        tasks_df = pd.read_excel(excel_path, dtype=str)
        tasks_df["time"] = time_parser(tasks_df["time"])
        tasks_count = tasks_df.shape[0]
        context.tasks_df = tasks_df
        context.tasks = parse_tasks(tasks_df, context)
        context.tasks_count = tasks_count
        context.counts_to_fill = tasks_count
        if not context.has_parse_error:
            context.log.info("Excel文件加载完成.")
            return True
        else:
            context.log.error("Excel文件解析失败.")
            context.req_deregister()
            return False


    def check_all_task_time(context):
        now = datetime.datetime.now()
        for task in context.tasks:
            task_time = task["time"]
            if (
                not task.get("order_status")
                and task_time.hour == now.hour
                and task_time.minute == now.minute
                and task_time.second == now.second
            ):
                task["order_status"] = make_order(context, task)
                if task["order_status"]:
                    context.counts_to_fill -= 1

        if context.counts_to_fill == 0:
            context.log.info("所有任务完成.")
            context.req_deregister()


    def start_timer(context):
        global TIMER_DELAY

        def cb(ctx, event):
            check_all_task_time(ctx)
            context.add_timer(time.time_ns() + TIMER_DELAY, cb)

        context.add_timer(time.time_ns() + TIMER_DELAY, cb)


    def set_instruments_map(context):
        book = context.get_account_book(context.SOURCE, context.ACCOUNT)
        instruments = book.instruments
        context.instruments_map = {}
        for key in instruments:
            instrument = instruments[key]
            map_key = (
                str(instrument.exchange_id).lower() + str(instrument.instrument_id).lower()
            )
            context.instruments_map[map_key] = instrument


    def pre_start(context):
        context.SOURCE = ""
        context.ACCOUNT = ""
        context.has_parse_error = False
        context.quote_map = {}
        context.log.info("参数 {}".format(context.arguments))
        args = json.loads(context.arguments)
        sourceAccountList = args["accountId"].split("_")
        context.tasks_excel_path = args["taskExcel"]

        if len(sourceAccountList) == 2:
            context.SOURCE = sourceAccountList[0]
            context.ACCOUNT = sourceAccountList[1]
            context.add_account(context.SOURCE, context.ACCOUNT)
        else:
            update_strategy_state(lf.enums.StrategyState.Error, "账户解析异常.", context)
            context.req_deregister()

        context.log.info(f"SOURCE {context.SOURCE} ACCOUNT {context.ACCOUNT}")


    def post_start(context):
        set_instruments_map(context)
        if not load_excel(context.tasks_excel_path, context):
            return

        update_strategy_state(
            lf.enums.StrategyState.Normal,
            "所有任务开始.",
            context,
        )
        start_timer(context)


    def make_order(context, task):
        now_nano = time.time_ns()
        context.insert_order(
            task.get("instrument_id"),
            task.get("exchange_id"),
            context.SOURCE,
            context.ACCOUNT,
            task.get("limit_price"),
            task.get("volume"),
            task.get("price_type"),
            task.get("side"),
            task.get("offset"),
            task.get("hedge_flag", HedgeFlag.Speculation),
            task.get("is_swap", False),
        )
        date_time_for_nano = datetime.datetime.fromtimestamp(now_nano / (10**9))
        time_str = date_time_for_nano.strftime("%Y-%m-%d %H:%M:%S.%f")
        count = context.tasks_count - context.counts_to_fill + 1
        context.log.info(
            "-------------------- [第{}单] 时间 {} --------------------".format(count, time_str)
        )
        context.log.info(
            "标的 {} 交易所 {} 账户 {} 价格 {} 数量 {} 方向 {} 开平 {} 投机套保标识 {} 互换 {}".format(
                task["instrument_id"],
                task["exchange_id"],
                context.ACCOUNT,
                task["limit_price"],
                task["volume"],
                task["side"],
                task["offset"],
                task.get("hedge_flag", HedgeFlag.Speculation),
                task.get("is_swap", False),
            )
        )
        return True



将dist目录下的Excel拷贝到以下目录, 


::

    Windows: {kungfu安装目录}/resources/resources/app/kungfu-extensions/Excel

    Linux: {kungfu安装目录}/resources/resources/app/kungfu-extensions/Excel

    MacOS: {kungfu安装目录}/Contents/Resources//app/kungfu-extensions/Excel


重启Kungfu前端界面, 就可以在 **策略进程->添加->根据具体交易任务的配置设置**, 交易任务添加后表现行为与策略相似    



.. ----------------------


.. Broker对接范例
.. ^^^^^^^^^^^^^^^^^^^^^^

.. 源码目录结构:

..     kfx-broker-xtp-demo/
..     ├── src/
..     │   └── cpp
..     |       └── ....    # cpp柜台对接相关代码
..     └── package.json    # 编译配置信息


.. 编译后文件目录结构:

..     kfx-broker-xtp-demo/
..     ├── src/
..     │   └── cpp
..     |       └── ....                              # cpp策略代码
..     ├── package.json         
..     ├── __kungfulibs__
..     |   └── xtp
..     |       └── v2.2.37.4                                   # 使用的柜台API库
..     |           ├── doc                                     # 柜台API的文档
..     |           ├── include                                 # 柜台API的头文件
..     |           └── lib                                     # 依赖库文件
..     ├── dist/                                               # 编译打包出来的二进制文件
..     |   └── xtp
..     |       ├── KungfuStrategy101Cpp.cp39-win_amd64.pyd     # 二进制文件
..     |       └── ....                                        # 相关的依赖库文件
..     └── build                                               # build 编译生成中间文件


.. 相关代码文件在  `kfs-extension-demo`_

.. .. _kfs-extension-demo: https://github.com/kungfu-trader/kungfu


.. 将dist目录下的xtp目录拷贝到以下目录, 

.. ::

..     Windows: {kungfu安装目录}/resources/resources/app/kungfu-extensions/xtp

..     Linux: {kungfu安装目录}/resources/resources/app/kungfu-extensions/xtp

..     MacOS: {kungfu安装目录}/Contents/Resources//app/kungfu-extensions/xtp

.. 重启Kungfu前端界面, 
.. 在 **交易账户->添加->选择XTP**, 添加对应配置信息就可以添加xtp柜台交易账户
.. 在 **行情源->添加->选择XTP**, 添加对应配置信息就可以添加xtp行情源