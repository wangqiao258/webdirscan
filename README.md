# 简介

`webdirscan`是一个超级简单的多线程Web目录扫描工具。

# 安装

使用Python语言编写

第三方模块只用了`requests`,所以`clone`以后只需要安装`requests`,`re`模块即可。

```
git clone https://github.com/Strikersb/webdirscan.git
pip install requests
pip install re
```

安装完成。

# 使用方法

```
usage: webdirscan.py [-h] [-d SCANDICT] [-o SCANOUTPUT] [-t THREADNUM]
                     scanSite

positional arguments:
  scanSite              The website to be scanned

optional arguments:
  -h, --help            帮助信息
  -d SCANDICT, --dict SCANDICT
                        选择字典
  -o SCANOUTPUT, --output SCANOUTPUT
                        输出结果
  -t THREADNUM, --thread THREADNUM
                        线程数
```

# 关于

原项目地址：https://github.com/TuuuNya/webdirscan

本项目在该基础上重构，改为python3，修改了其中一些代码和注释。
