# AutoXHS 服务器后端

## 一、功能特性

- 对接基于 `requests` 开发的 [**Auto XHS** 前端](https://github.com/gupingan/auto-xhs-frontend)；

- 提供一系列前端对应的`登录`、`创建`、`搜索`、`评论`等接口；

- 配备了`日志存储`、`查阅进程配置`等功能，方便维护。


## 二、技术栈

- Flask
- MySQL Ver 14.14 Distrib 5.7.43
- NodeJS v18.17.1

## 三、服务器部署

**部署环境**： 腾讯云轻量级应用服务器 + CentOS 7.6 64bit

**项目目录**：`/projects/auto-xhs` 存放 Flask 项目的所有源码（当前仓库）

### 3.1 安装 `Git`

1. 安装 git

   ```bash
   yum update
   yum install -y git
   ```

2. 克隆项目

   ```bash
   mkdir /projects
   cd /projects
   git clone git@github.com:gupingan/auto-xhs-backend.git
   # 克隆后续需要的一些工具
   git clone git@gitee.com:xiaogugyx/server-deployment-kit.git
   ```
   
3. 调整文件名称

   ```bash
   mv auto-xhs-backend/ auto-xhs
   mv server-deployment-kit/ serverkit
   ```

### 3.2 安装 `node.js`

  此处顶级大坑，无力吐槽~~

  1. 安装 nodejs

     ```bash
     cd /projects/serverkit/nodejs
     tar xvf node-v18.17.1-linux-x64.tar.xz 
     mv node-v18.17.1-linux-x64 ~
     ln -s /root/node-v18.17.1-linux-x64/bin/node /usr/local/bin/node
     ln -s /root/node-v18.17.1-linux-x64/bin/npm /usr/local/bin/npm
     # 以上来源于 腾讯云 官方的文档 https://cloud.tencent.com/document/product/213/38237
     # 不出意外的话就要出意外了
     node -v
     """ error：
     node: /lib64/libm.so.6: version `GLIBC_2.27' not found (required by node)
     node: /lib64/libc.so.6: version `GLIBC_2.25' not found (required by node)
     node: /lib64/libc.so.6: version `GLIBC_2.28' not found (required by node)
     node: /lib64/libstdc++.so.6: version `CXXABI_1.3.9' not found (required by node)
     node: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found (required by node)
     node: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by node)
     """
     ```

  2. 安装 gcc-8

     ```bash
     yum install centos-release-scl
     yum install -y devtoolset-8-gcc devtoolset-8-gcc-c++ devtoolset-8-binutils
     echo "source /opt/rh/devtoolset-8/enable" >> /etc/profile
     source /etc/profile
     ```

  3. 安装 make4.3

     ```bash
     cd /projects/serverkit/nodejs
     # 或者 wget https://ftp.gnu.org/gnu/make/make-4.3.tar.gz
     tar -xzvf make-4.3.tar.gz && cd make-4.3/
     ./configure  --prefix=/usr/local/make
     make && make install
     cd /usr/bin/ && mv make make.bak
     ln -sv /usr/local/make/bin/make /usr/bin/make
     ```

  4. 安装 glibc-2.28

     ```bash
     cd /projects/serverkit/nodejs
     # 或者 wget http://ftp.gnu.org/gnu/glibc/glibc-2.28.tar.gz
     tar xf glibc-2.28.tar.gz 
     cd glibc-2.28/ && mkdir build  && cd build
     ../configure --prefix=/usr --disable-profile --enable-add-ons --with-headers=/usr/include --with-binutils=/usr/bin
     ```

  5. 安装 libstdc++.so.6

     ```bash
     yum install libstdc++.so.6 -y
     cd /projects/serverkit/nodejs
     # 或者 wget http://ftp.de.debian.org/debian/pool/main/g/gcc-8/libstdc++6_8.3.0-6_amd64.deb
     ar -x libstdc++6_8.3.0-6_amd64.deb
     tar -xvf data.tar.xz
     cp usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.25 /usr/lib64/
     rm -rf /usr/lib64/libstdc++.so.6
     ll /usr/lib64/libstd*
     ln -s /usr/lib64/libstdc++.so.6.0.25 /usr/lib64/libstdc++.so.6
     ```

  6. Done.

     ```bash
     node -v
     npm -v
     ```

     但是，压根没有必要照着上面的做，可以运行我提供的两个 .sh 文件中的任意一个，`setup-nodejs1.sh` 是利用了 nodejs 官方自动安装的脚本，`setup-nodejs2.sh` 则是上述手动安装补坑的脚本文件，执行 sh 文件前务必记得修改好权限。

     ```bash
     # 接下来不要忘记安装依赖哦
     cd /projects/auto-xhs
     npm install jsdom
     ```

### 3.3 安装 `Python3.10`

1. 安装 gcc

   ```bash
   yum install -y gcc
   ```

2. 安装 openssl

   ```bash
   yum remove openssl
   cd /opt
   yum install -y wget
   wget https://www.openssl.org/source/openssl-1.1.1n.tar.gz --no-check-certificate
   tar -zxf openssl-1.1.1n.tar.gz
   cd openssl-1.1.1n
   ./config --prefix=/usr/local/openssl shared zlib 
   make && make install
   echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/openssl/lib" >>  /etc/profile
   source /etc/profile
   ```
   
3. 下载其他依赖

   ```bash
   yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
   yum install -y libffi-devel zlib1g-dev
   yum install zlib* -y
   ```

4. 下载 Python 源码

   ```bash
   cd /projects/serverkit/python
   # 或者 wget https://www.python.org/ftp/python/3.10.10/Python-3.10.10.tgz
   ```
   
5. 解压 & 编译 & 安装

   ```bash
   # 解压 tgz 包
   tar -zxf Python-3.10.10.tgz
   # 编译并安装
   cd Python-3.10.10
   ./configure --prefix=/usr/local//python3 --with-openssl=/usr/local//openssl 
   make && make install
   # 链接
   ln -s /usr/local/python3/bin/pip3  /usr/bin/pip
   ln -s /usr/local/python3/bin/python3  /usr/bin/python
   ln -s /usr/local/python3/bin/python3  /usr/bin/python3    
   # 验证
   cd ..
   python
   # 输入以下代码 无报错则完成
   import ssl
   import _ssl
   ```

### 3.4 安装虚拟环境

1. 安装

   ```bash
   pip install virtualenv
   ```

2. 创建

   ```bash
   mkdir /envs
   virtualenv /envs/xhs --python=python3.10
   ```

3. 激活

   ```bash
   source /envs/xhs/bin/activate
   ```

- 安装项目的依赖项

  ```bash
  # 务必按上述方式激活虚拟环境
  cd /projects/auto-xhs
  pip install -r requirements.txt  
  # 当然，还有一个 xhsAPI 是我自己写的包，通过此途径无法直接安装
  ```

- 安装 xhsAPI 包（温馨提醒：之前的 jsdom 是否安装了？）

  ~~[点击我跳转](https://github.com/gupingan/xhsAPI)，下载发行版到服务器端，在虚拟环境下通过 pip 本地安装。~~

  因某些缘故不可公开，请在 [Issues](https://github.com/gupingan/auto-xhs-backend/issues) 中留下您的邮箱，免费发送 `xhsAPI` 包给您

### 3.5 安装 `MySQL`

  1. 安装 MySQL 的分支

     ```bash
     yum install -y mariadb-server
     ```

  2. 设置开机启动并启动服务

     ```bash
     systemctl enable mariadb
     systemctl start mariadb
     # 查看
     systemctl status mariadb
     # 出现 Active: active (running) 即可
     ```

  3. 账号初始化并执行sql

     ```sql
     cd /projects/auto-xhs
     mysql -u root -p
     # 导入项目数据库
     source auto_xhs_db.sql;
     # 更新root密码
     UPDATE mysql.user SET password=password('<your-password>') WHERE mysql.user='root';
     FLUSH PRIVILEGES;
     # 创建用户
     INSERT INTO mysql.user(user, host, password) values ('normal', '%', password('<your-password>')); 
     FLUSH PRIVILEGES;
     # 赋予权限
     GRANT ALL PRIVILEGES ON auto_xhs_db.* to normal@'%';
     FLUSH PRIVILEGES;
     ```

     完成以上操作后你会发现，创建的用户 `normal` 在本地无需密码就能登录，为了安全性考虑，我们需要删除某些本地用户。

     ```sql
     SELECT User, Host, Password FROM mysql.user;
     """ input
     +--------+---------------+-------------------------------------------+
     | User   | Host          | Password                                  |
     +--------+---------------+-------------------------------------------+
     | root   | localhost     | *1880C4770E85923D54E015CA6FBCE031713FFC4A |
     | root   | vm-0-4-centos | *1880C4770E85923D54E015CA6FBCE031713FFC4A |
     | root   | 127.0.0.1     | *1880C4770E85923D54E015CA6FBCE031713FFC4A |
     | root   | ::1           | *1880C4770E85923D54E015CA6FBCE031713FFC4A |
     |        | localhost     |                                           |
     |        | vm-0-4-centos |                                           |
     | normal | %             | *1880C4770E85923D54E015CA6FBCE031713FFC4A |
     +--------+---------------+-------------------------------------------+
     """
     DELETE FROM mysql.user WHERE User='' and Password='';
     FLUSH PRIVILEGES;
     ```
     
     你还需要在 `config.py` 中写上你设置的密码。

![截图_20231116193300](https://gitee.com/xiaogugyx/drawing-bed/raw/master/%E6%88%AA%E5%9B%BE_20231116193300.png)

### 3.6 安装 `uwsgi`

  1. 安装

     ```bash
     source /envs/xhs/bin/activate
     pip install uwsgi
     ```

  2. 基于 `uwsgi` 运行

     ```sh
     cd /projects/serverkit/
     vim uwsgi-tool.sh
     # 修改 INI="/projects/xhsweb/backend/xhs_uwsgi.ini" 对应的值
     # 改为 /projects/auto-xhs/xhs_uwsgi.ini
     chmod 777 uwsgi-tool.sh
     ./uwsgi-tool.sh start
     ```

  3. 将来你可能需要重启或者关闭↓

     ```bash
     ./uwsgi-tool.sh restart
     ./uwsgi-tool.sh stop
     ```

## 四、本地运行

**拉取项目后：**

- 确保安装好所有 python 包（requirements.txt 和 xhsAPI）
- 确保安装了 nodejs 环境，最好和我的版本一致，然后在项目文件夹的 cmd 命令行中安装 jsdom
- 确保你的系统安装得有 mysql 服务，最好版本和我一致，进入数据库中导入执行项目中 .sql 文件，并且 config.py 中的用户名和密码能够对得上你所设置的
- 并不需要虚拟环境以及 uwsgi，保证以上三点都是满足的后，运行项目

## 五、初始管理员

无论你是经过[三](#三服务器部署)还是[四](#四本地运行)，你都需要进行管理员账号的初始化，至于如何注册和管理更多的账号，请参考另一个终端项目 [auto-xhs-admin](https://github.com/gupingan/auto-xhs-admin)（设置好服务端地址后，尽量打包成 exe）。

**回到正题**：启动好服务器后，通过访问接口 **/api/admin/init**

提示如下后，你就已经获得了专属的管理员账号（默认账号：`adminer` + 默认密码：`123456`）

```bash
{
  "success": true,
  "msg": "初始化管理员账号成功",
  "data": {}
}
```

这个账号可以登录在管理员端，也可以登录在客户端，但是请不要同时登录，token 在登录时会生成新的值，导致前一登录状态失效！建议管理员账号请通过管理员端修改密码和账号，在客户端尽量使用普通用户的账号，避免去使用管理员账号。

## 六、接口文档

[点击我跳转查看本项目的路由接口](https://github.com/gupingan/auto-xhs-backend/blob/main/docs/API.md)