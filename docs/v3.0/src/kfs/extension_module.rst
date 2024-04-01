
install
^^^^^^^^^^^

下载package.json里面配置的依赖项目

::

    $ kfs extension install

-----------------------------------


compile
^^^^^^^^^^^^^^^^^^

编译代码生成二进制文件，

如果是cpp代码，根据package.json配置编译生成CPython模块或可执行程序。

如果是Python代码，使用Nuitka编译生成二进制库文件。

::

    $ kfs extension compile


-----------------------------------


build
^^^^^^^^^^^

先检测依赖的库文件是否已经下载，若没下载则进行下载。如果package.json配置的是cpp代码项目，会自动生成CMakeLists.txt配置文件。然后在执行kfs extension compile的操作生成二进制文件。

::

    $ kfs extension build


package.json文件字段范例::

    "kungfuDependencies": {
        "xtp": "v2.2.37.4"
    },
    "kungfuBuild": {
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
    }

    这是xtp柜台的编译配置信息，执行 kfs extension build 之后，会先下载xtp的v2.2.37.4版本的API头文件和库文件，生成的CMakeLists.txt的配置文件中，设置编译输出为CPython模块，链接库xtptraderapi和xtptraderapi。



.. tip::

    注: 如果曾经在下载过程中被打断，导致目录下有依赖的库目录但是文件不全，此时检测结果会视为已下载，需要删除 __kungfulibs__ 和 __pypackages__  目录再执行kfs extension build 命令。


-----------------------------------



package
^^^^^^^^^^^

将dist目录中编译生成的文件打包到压缩包中

::

    $ kfs extension package


-----------------------------------


clean
^^^^^^^^^^^

删除build目录和dist目录中编译生成的文件

::

    $ kfs extension clean


-----------------------------------



format
^^^^^^^^^^^

格式化代码::

    cpp的代码使用clang-format进行格式化
    Python的代码使用black进行格式化

::

    $ kfs extension format



-----------------------------------


list
^^^^^^^^^^^

展示kungfu云环境里支持的柜台API列表，列表中的API版本只需要加到package.json的kungfuDependencies字段中，
在执行build的时候就可以自动下载API的头文件和库文件，并且自动配置CMakeLists.txt配置信息。

如果列表中没有您需要的柜台版本，可以联系我们进行添加。

::

    $ kfs extension list


package.json文件字段范例::

    "kungfuDependencies": {
        "xtp": "v2.2.37.4",
        "ctp": "v6.6.8"
    }

    kfs extension install 时会将xtp的v2.2.37.4版本的API头文件和库文件下载到__kungfulibs__/xtp/v2.2.37.4目录下，将ctp的v6.6.8版本的API头文件和库文件下载到__kungfulibs__/ctp/v6.6.8。

