简介
=====

功夫核心 Kungfu-core 是一套为开发者提供的集 sdk, api 于一体的, 专注在量化交易, 高性能实时计算领域的工具包
Kungfu-core 内封装了高性能的共享内存通信框架, 以及打包应用所需插件的手脚架工具, 支持 python, cpp, javascript 的插件构建与开发
我们提供 kfs, kfc 以及 python api 等要素来构建应用, 功夫的核心产品功夫量化交易系统也是基于此套工具构建


  - kfs: 用于功夫插件的构建, 可用于:
  
      - 构建算法插件
      - 构建broker柜台插件
      - 构建算子插件
      - 构建ui插件

  - kfc: 用于启动功夫功夫进程

  - kungfu api: 可内嵌入开发者自身进程, 运行回测, 获取因子, 以及在python脚本内对进程的启动做更细粒度的控制




功夫在系统设计上支持任意柜台的对接 (涵盖中国所有股票、期货市场) , 目前功夫开源版仅提供 XTP 柜台对接的实现。

如果需要接入更多柜台请通过 `咨询页面 <https://www.kungfu-trader.com/index.php/about-us>`_ 联系我们。

了解更多请通过 `官网 <https://www.kungfu-trader.com>`
