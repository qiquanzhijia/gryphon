# mysql-python 模块安装 MySQL-python==1.2.5

fatal error C1083: Cannot open include file: ‘config-win.h’: No such file or directory，
这时候需要到mysql的官网下载mysql connector/c，注意是Connector/C，不是Connector/Python，选择64位下载，地址：https://dev.mysql.com/downloads/connector/c/

mklink /d "C:\Program Files (x86)\MySQL\MySQL Connector C 6.0.2\include" "C:\Program Files\MySQL\MySQL Connector C 6.0.2\include"

# pylibmc>=1.5.2,<2  python-memcached

# gryphon-decimal==2.3 

http://www.bytereef.org/mpdecimal/doc/decimal/index.html

https://www.lfd.uci.edu/~gohlke/pythonlibs/#decimal 

https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python

```cython
from decimal import *
c = getcontext()               # Global (thread-local) context

c.traps[Inexact] = True        # Trap the Inexact signal
c.traps[Inexact] = False       # Clear the Inexact signal

c._traps |= DecInexact         # Trap the Inexact signal
c.traps[Inexact]
# True
c._traps &= ~DecInexact        # Clear the Inexact signal
c.traps[Inexact]
# False

```
http://blog.codebase.co.jp/memcached%E3%82%92windows%E3%81%AB%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%99%E3%82%8B
net start "memcached"

框架采用Tornado,有循环引用问题

scoop config aria2-enabled false

https://www.cnblogs.com/fangbei/p/8432891.html  概念
