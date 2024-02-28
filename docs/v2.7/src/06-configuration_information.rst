package.json配置信息
=====================

1. 简介
--------

kfs 构建功夫插件的时候, 需要根据 package.json 文件提供的描述信息来进行构建, 我们要求每一个插件的开发目录根目录都存在一个package.json文件

.. code-block:: python
    :linenos:

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

2. 字段
--------


name 
~~~~~~
插件仓库的 name（任意自定义字符）


description
~~~~~~~~~~~~~

插件的描述信息, 在功夫插件模块内会将此字段读取


kungfuBuild
~~~~~~~~~~~~~

[重要] 为 cpp, python 插件打包指定依赖

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

[重要] 主要配置项, 针对strategy(策略/算法), td(交易柜台), md(行情柜台)分场景配置

key: 唯一key, 例如功夫app中存在十个插件, 这十个插件的key不能重复, 且对于柜台与交易任务，该key与目录结构存在对应关系

name: 插件名称，会在功夫插件列表与对应入口进行展示

config: 插件表单主要配置项（插件表单是指通过功夫app或者cli添加柜台/算法时所需填写的配置表单）, 下级对应 strategy, md, td 三个选择，分别对应算法插件，行情接口插件，与交易柜台插件


对于算法插件, config 下级为 strategy

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

对于 行情/交易插件，一般柜台接口同时提供行情交易接口，开发者可在config下同时配置行情（md），交易（td）配置项

.. code-block:: python
    :linenos:

        "config": {
            "td": {
                "type": [ "stock" ],
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
                        "key": "td_port",
                        "name": "xtp.td_port",
                        "type": "int",
                        "required": true,
                        "tip": "xtp.td_port_tip"
                    },
                ]
            },
            "md": {
                "type": [ "stock" ],
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
                ]
            }
        }

