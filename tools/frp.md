
使用frp来反向代理ssh服务。
客户端：
1. 下载并配置openssh-server
2. 配置frpc
服务端：
配置frps

# 服务端配置frps

`frp`下载地址：`https://github.com/fatedier/frp`

## 配置文件填写

下载frp并解压，配置`frps.toml`
``` toml
bindAddr = "0.0.0.0"
bindPort = 7000
#web dashboard配置
webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "xxx"
webServer.password = "xxx"
#启用prometheus监控指标
enablePrometheus = true
#token权限验证，需与客户端配置一致
auth.method = "token"
auth.token = "xxx"
#日志配置
log.to = "/home/airsumer/app/frp_0.65.0_linux_amd64/log"
log.level = "info"
log.maxDays = 3
```

配置文件写完后运行：`./frps -c ./frps.toml`(运行前记得开放相关的端口)

## 使用`systemctl`运行`frps`

其中service配置文件如下：
``` toml
[Unit]
Description=FRP Server
After=network.target syslog.target
Wants=network.target
 
[Service]
Type=simple
User=sumer
Group=sumer
 WorkingDirectory=XXX
ExecStart=${WorkingDirectory}/frpc -c ${WorkingDirectory}frpc.toml
ExecReload=${WorkingDirectory}/frpc reload -c ${WorkingDirectory}/frpc.toml
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```


# 客户端配置frp
## 下载ssh-server
客户端需要下载`openssh-server`,否则只能当ssh客户端而不能当服务器。

``` shell
sudo apt update
sudo apt install openssh-server
```

下载完成之后，在`/etc/ssh/sshd_config`文件中进行自定义，可以：
- 更改ssh默认端口号
- 设置可以公钥登录

## 配置frpc.toml

``` toml
# 服务器配置
serverAddr = "XXXX" # 服务器公网ip
serverPort = 7000 # 服务器开放的监听端口
auth.token ="XXXX" # 密码

#代理配置
[[proxies]]
name = "ssh" # 作为一个id，同一个frps不支持创建两个相同name的代理
type = "tcp"
localIP = "127.0.0.1"
localPort = 6000 # 本地的ssh端口，默认值是22
remotePort = 6001 # frps服务器上的端口
```

## 配置systemd服务
`sudo vim /etc/systemd/system/frpc.service`
注意，service文件里面,user和 group这两个需要是需要的。

``` toml
[Unit]
Description=Frpc Client Service
After=network.target
wants=network-online.target
[Service]
Type=simple
User=XXX
Group=XXX
DynamicUser=yes
Restart=on-failure
RestartSec=5s
WorkingDirectory=XXX
ExecStart=${WorkingDirectory}/frpc -c ${WorkingDirectory}frpc.toml
ExecReload=${WorkingDirectory}/frpc reload -c ${WorkingDirectory}/frpc.toml
LimitNOFILE=1048576
# 标准输出和错误重定向
StandardOutput=append:/var/log/frpc.log
StandardError=append:/var/log/frpc.log
[Install]
WantedBy=multi-user.target
```