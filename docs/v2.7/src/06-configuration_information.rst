package.json配置信息
=====================

1. 简介
--------

kfs 构建功夫插件的时候, 需要根据 package.json 文件提供的描述信息来进行构建, 我们要求每一个插件的开发目录根目录都存在一个package.json文件



2. package.json 范例
---------------------

.. code-block:: python
    :linenos:

        {
            "name": "@kungfu-trader/examples-strategy-python",
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


1. 字段说明
------------


name 
~~~~~~
 - 插件仓库的名字（任意自定义字符）


description
~~~~~~~~~~~~~

    插件的描述信息, 在功夫插件模块内会将此字段读取


kungfuBuild
~~~~~~~~~~~~~

为 cpp, python 插件打包指定依赖以及版本

.. code-block:: python
    :linenos:

        "kungfuBuild": {
            "python": {
                "dependencies": {
                    "dotted_dict": "~=1.1.0",
                    "recordclass": "~=0.18.0",
                    "sortedcontainers": "~=2.4.0"
                }
            }
        }


kungfuConfig
~~~~~~~~~~~~~

主要配置项, 针对strategy(策略/算法), td(交易柜台), md(行情柜台)分场景配置

.. code-block:: json
    :linenos:

        "kungfuConfig": {
            "key": "ConditionOrder",
            "name": "条件单",
            "ui_config": {
                "position": "make_order"
            },
            "config": {
                "strategy": {
                    "type": "trade",
                    "settings": [
                        {
                            "key": "priceCondition",
                            "name": "priceCondition",
                            "type": "table",
                            "columns": [
                                {
                                    "key": "currentPrice",
                                    "name": "currentPrice",
                                    "type": "select",
                                    "options": [
                                        {
                                            "label": "currentPrice_0",
                                            "value": "0"
                                        },
                                        {
                                            "label": "currentPrice_1",
                                            "value": "1"
                                        },
                                        {
                                            "label": "currentPrice_2",
                                            "value": "2"
                                        }
                                    ]
                                },
                            ],
                        }
                    ]
                }
            }
        }






key:
^^^^^^^

:: 

    key: 唯一key, 例如功夫app中存在十个插件, 这十个插件的key不能重复, 且对于柜台与交易任务，该key与目录结构存在对应关系

name:
^^^^^^^^
:: 


    name: 插件名称，会在功夫插件列表与对应入口进行展示



config说明:
^^^^^^^^^^^^^

:: 

    config: 插件表单主要配置项（插件表单是指通过功夫app或者cli添加柜台/算法时所需填写的配置表单）, 下级对应 strategy, md, td 三个选择，分别对应算法插件，行情接口插件，与交易柜台插件


不同插件配置下级说明
+++++++++++++++++++++


对于算法插件
'''''''''''''

    config 下级为 strategy

:: 
    
    "config": {
        "strategy": {

        }
    }

举例说明 : 

.. code-block:: python
    :linenos:

        "config": {
            "strategy": {
                "type": "trade",
                "settings": [
                    {
                        "key": "accountId",
                        "name": "twap.accountId",
                        "type": "td",
                        "required": true,
                        "primary": true
                    }
                ]
            }
        }


对于 行情/交易插件
''''''''''''''''''

    一般柜台接口同时提供行情交易接口，开发者可在config下同时配置行情交易（td），（md）配置项

:: 
    
    "config": {

        "td": {

        },

        "md": {

        }
    }


举例说明 :   

.. code-block:: python
    :linenos:

        "config": {
            "td": {
                "type": [ "stock" ],
                "settings": [
                    {
                        "key": "account_name",
                        "name": "account_name",
                        "type": "str", 
                        "tip": "account_name_tip"
                    },
                    {
                        "key": "account_id",
                        "name": "account_id",
                        "type": "str",
                        "required": true,
                        "primary": true,
                        "tip": "account_id_tip"
                    },
                    {
                        "key": "password",
                        "name": "password",
                        "type": "password",
                        "required": true,
                        "tip": "password_tip"
                    },
                    {
                        "key": "td_port",
                        "name": "td_port",
                        "type": "int",
                        "required": true,
                        "tip": "td_port_tip"
                    },
                ]
            },
            "md": {
                "type": [ "stock" ],
                "settings": [
                    {
                        "key": "account_id",
                        "name": "account_id",
                        "type": "str",
                        "required": true,
                        "tip": "account_id_tip",
                        "default": "15011218"
                    },
                    {
                        "key": "password",
                        "name": "password",
                        "type": "password",
                        "required": true,
                        "tip": "password_tip",
                    },
                    {
                        "key": "md_ip",
                        "name": "md_ip",
                        "type": "str",
                        "required": true,
                        "tip": "md_ip_tip",
                        "default": "119.3.103.38"
                    },
                    {
                        "key": "md_port",
                        "name": "md_port",
                        "type": "int",
                        "required": true,
                        "tip": "md_port_tip",
                        "default": 6002
                    },
                ]
            }
        }


type说明: 
++++++++++

type: 对于柜台有效，标记柜台支持的交易类型，可选项为

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - stock
     - 股票
   * - stockoption
     - 股票期权
   * - techstock
     - 科技股
   * - Future
     - 期货
   * - bond
     - 债券
   * - fund
     - 基金
   * - index
     - 指数
   * - repo
     - 回购
   * - crypto
     - 加密货币
   * - cryptofuture
     - 加密货币合约
   * - cryptoufuture
     - 加密货币u本位合约
   * - multi
     - 多品种



settings: 对应表单配置项
+++++++++++++++++++++++++
 
key
''''''
::

    key: 表单项的key


name
''''''''
::

    name: 表单项的name

type
''''''''
::

    type表单项的类型: 可选项
    

.. list-table::
   :width: 600px

   * - 属性
     - 说明
   * - str
     - 字符串
   * - password
     - 密码
   * - file
     - 文件
   * - files
     - 多选文件
   * - directory
     - 目录
   * - folder
     - 文件夹
   * - rangePicker
     - 时间范围选择器
   * - dateTimePicker
     - 日期时间选择器
   * - datePicker
     - 日期选择器
   * - timePicker
     - 时间选择器
   * - select
     - 选择框
   * - multiSelect
     - 多选框
   * - radio
     - 单选栏
   * - checkbox
     - 复选框
   * - bool
     - 布尔类型  
   * - int
     - 整型              
   * - float
     - 浮点型                   
   * - percent
     - 百分比 
   * - td
     - 选择交易账户
   * - md
     - 选择行情源
   * - operator
     - 选择算子
   * - instrument
     - 选择标的
   * - instruments
     - 选择多个标的
   * - side
     - 选择买卖
   * - offset
     - 选择开平

                  

options
''''''''
::

    options: 其中当type字段类型为 select/checkbox/multiSelect/radio 时有效，对应结构如下: 

.. code-block:: python
    :linenos:

        {
            "value": # string | number, 选项值;
            "label": # string, 选项显示内容;
        }

tips
''''''''
::

    tips: 备注信息


errMsg
''''''''
::

    errMsg: 报错信息


default
''''''''
::

    default: 默认值，类型需和 type 一致，目前只支持对一些基础类型设置（int/float/str/bool/percent/select/checkbox/multiSelect/radio）


required
''''''''
::

    required: true/false, 该项是否必填


primary
''''''''
::

    primary: true/false, 该项是否为主键

