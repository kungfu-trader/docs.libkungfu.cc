算子面板
-------------------

.. image:: _images/算子面板-25.png

.. image:: _images/算子-27.png

.. hint:: 
   - 算子计算的结果可被其他算子、策略订阅，算子间可进行嵌套计算。
   - 因此算子的使用可减少重复计算，提高策略运行效率。

算子主要分为 **算子插件** 和 **算子文件** 两种类型；

 -  **算子插件** 为官方封装好的算子内容，可输入参数直接调用 。
 -  **算子文件** 为用户自己编写的python文件。



.. note:: **算子使用场景举例**

    1.计算开销过高（如使用了机器学习等情况），计算在策略中发生可能导致数据拥塞;使用算子可将计算与策略分为两个进程运行，减少数据拥塞。
    
    2.算子结果可被复用（如生成K线，或生成因子），因此重复计算可由算子执行，多个策略或算子同时订阅算子结果以减少重复计算。





.. note::  
   - **算子合成数据的用途** 算子合成数据在诊断工具的标识为“SyntheticData（合成数据）”。

   - 算子输出结果主要用途：

    1.合成k线或其他数据 (如根据Quote行情，可以合成分钟/秒k线)。
    2.作为因子（可通过合成数据做出对未来价格的预测：例如各类量价因子）。
    3.计算目标仓位（策略可通过多个因子组合优化或使用机器学习模型，获得最优目标仓位，并应用到实际下单中）。


-----

添加算子
~~~~~~~~~~~~~

(1) 点击“添加”按钮。

.. image:: _images/添加算子.png


.. image:: _images/添加算子-27.png


(2) 选择要添加的算子类型。


.. image:: _images/算子2-25.png

请根据要添加的算子类型（文件/插件），查看下方对应的引导文档。

-----


添加算子插件-bar数据
~~~~~~~~~~~~~~~~~~~~~~~~~~

(1) 选择算子类型窗口选择“插件”。

.. image:: _images/选择插件-25.png


点击 "确认"，完成选择。

(2) 填写参数

.. image:: _images/算子-bar-25.png


.. image:: _images/添加bar算子-27.png

.. note:: 填写算子信息，请参考以下表格。

.. list-table::
   :header-rows: 1

   * - 字段
     - 字段含义
   * - Bar ID
     - bar行情的id，其他算子/策略订阅本算子时的判断标识，不允许重复
   * - 数据源
     - 选择数据的行情源（ctp、xtp、sim……）
   * - 标的
     - 填写要合成bar数据的标的，允许多选
   * - 周期
     - 单位为秒。作为该算子的计算周期、推送频率。如：计算周期为5s，行情源1s推送一组行情，则算子将把5s内收到的五组行情数据处理成一组合成数据（5s内的高开低收），每5s推送一次


-----

添加算子文件
~~~~~~~~~~~~~~~~~~~~~~~

(1) 选择算子类型窗口选择“文件”。

.. image:: _images/选择文件-25.png


点击 "确认",完成选择。

(2) 填写算子id，指定算子文件路径。填写完毕后点击确认创建算子


.. image:: _images/添加算子文件-27.png


.. list-table::
   :header-rows: 1

   * - 字段
     - 字段含义
   * - 算子 ID
     - 填写算子的id
   * - 算子路径
     - 选择本地算子 .py 文件


-----

调用算子代码示例
~~~~~~~~~~~~~~~~~~~~
详细内容可参考 **算子API文档** 。

.. attention:: 

  1.策略订阅算子后，仍然需要在策略文件代码中订阅行情源才能正常执行下单。

  2.若算子与其他算子实现了嵌套计算，需要确保开启的顺序同依赖关系一致。如算子op2依赖算子op1的计算结果，如果实操中先开启算子op2，则由于未收到op1的数据，算子op2会出现报错。

  3.当策略中使用算子数据，但算子未运行时，策略将保持监听，直到算子成功上线才会进行下单，不会报错。

  4.当策略中同时使用算子、行情并行作为下单依据时，若算子下线，其他能够正常工作的数据源进程将继续指导下单。如策略同时使用算子op1、算子op2、行情源md1作为下单依据，当op1未上线，op2、md1正常运行时，策略将使用op2、md1的数据下单，当op1上线时，策略将同时使用三个数据源进行下单。

-----

K线合成：订阅指定标的行情，并在收到行情时广播行情数据
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

:: 
    
    # -*- coding: UTF-8 -*-
    from kungfu.wingchun.constants import *

    # 设置行情源为sim，交易所为上交所
    source = "sim"
    exchange = Exchange.SSE

    # 订阅标的'600420','600000'行情
    def pre_start(context):
        context.log.info("pre start")
        context.subscribe(source,['600420','600000'], exchange)

    def post_start(context):
        context.log.info("post start")

    def on_quote(context, quote, location, dest):
        context.log.info("on quote: {}".format(quote.instrument_id))
        #  广播发布key标识为'op'的行情数据
        context.publish_synthetic_data('op', "{}".format(quote))



-----

在策略/算子中订阅其他算子发布的数据
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

:: 

    # 订阅2种类型算子的方法
    # 1.使用算子插件时，group=bar，name=添加算子时填写的算子ID，如bar1或mybar  
    def pre_start(context):
        context.subscribe_operator("bar","my-bar")

    # 2.使用算子文件时，group=default，name=添加算子时填写的算子ID，如op2  
    def pre_start(context):
        context.subscribe_operator("default","op2")

    # 算子的广播会自动触发本方法的调用，将获取所订阅算子广播的数据
    def on_synthetic_data(context, synthetic_data, location, dest):
        context.log.info("on_synthetic_data: {}".format(synthetic_data))

- 需要订阅算子状态变化回调、了解算子相关参数的填写细则请参考算子API文档。

-----

