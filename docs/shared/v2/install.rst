Windows平台
------------

正常安装即可

Linux平台
----------

Kungfu-version.rpm 安装包，安装命令为

::

    yum install Kungfu-version.rpm
    # 比如 : yum install Kungfu-1.0.12-linux-x86_64-latest.rpm


Kungfu-version.AppImage 安装包
    需要将 appimage 抽出，生成 squashfs-root 文件夹（该文件夹名称以系统生成为准），再将其内容复制到 /opt/Kungfu (如果opt下面没有Kungfu文件夹,需要先创建)目录下

::

    ./Kungfu-version.AppImage --appimage-extract
    # 比如 : ./Kungfu-1.0.12-linux-x86_64-latest.AppImage --appimage-extract
    cp -R squashfs-root/* /opt/Kungfu


安装成功后，需要把kungfu/resources/kfc/extensions下的文件权限改为777，对应命令为

::

    chmod 777 -R /opt/Kungfu/resources/kfc/extensions


卸载

::

    # 对于 .rpm 版本卸载
    yum remove Kungfu

    # 对于 .AppImage 版本
    直接删除 /opt/Kungfu 即可


Mac平台
----------

正常安装即可


注意事项
---------

功夫量化交易系统不支持自动换日，使用系统时，需要每天重启系统。