# mysql-python 模块安装 MySQL-python==1.2.5

fatal error C1083: Cannot open include file: ‘config-win.h’: No such file or directory，
这时候需要到mysql的官网下载mysql connector/c，注意是Connector/C，不是Connector/Python，选择64位下载，地址：https://dev.mysql.com/downloads/connector/c/

mklink /d "C:\Program Files (x86)\MySQL\MySQL Connector C 6.0.2\include" "C:\Program Files\MySQL\MySQL Connector C 6.0.2\include"

# pylibmc>=1.5.2,<2

# gryphon-cdecimal==2.3