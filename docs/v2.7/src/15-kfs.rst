================
模块功能
================

|   kfs是基于Python和JavaScript封装的可执行程序, 其作用是辅助管理插件的编译, 
    只需要写好package.json文件的配置信息, 执行kfs extension build就可以自动识别插件的代码类型是cpp还是python, 
    自动生成CMakeLists.txt文件, 根据配置编译生成CPython模块或可执行程序.


==========================================



kfs模块功能
==============


kfs文件路径
------------------


::

    Windows: {kungfu安装目录}/resources/kfc/kfs.exe

    Linux: {kungfu安装目录}/resources/kfc/kfs

    MacOS: {kungfu安装目录}/Contents/Resources/kfc/kfs


通过图形化界面的菜单栏, **文件->打开功夫安装目录**, 可以直接打开 **{kungfu安装目录}/resources** 目录


------------------



extension模块
----------------

.. include:: kfs/extension_module.rst
