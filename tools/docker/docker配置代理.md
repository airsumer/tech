

`docker`需要设置代理，否则`docker pull`慢地怀疑人生。

`docker`的代理需要记住两点:

1. `docker` 的代理并不能通过`export https_proxy`来设置!

2. ` docker pull / docker push` 和` docker build/docker run` 使用代理的方式不一样！

# `docker pull`代理设置



## 创建配置文件

`docker pull /push` 的代理被 `systemd `接管，所以需要设置 `systemd`。

``` bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```

## 写入配置

在`http-proxy.conf`文件中写入：

``` bash
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
```

## 重启`docker`服务

需要重启服务才可以实现。

``` bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

重启完成后应该就可以通过代理进行`docker pull`了，如果不放心就用下面的命令看看环境变量设置设置成功。

``` bash
sudo systemctl show --property=Environment docker
```



# `docker build`代理设置



# Ref

1. [docker 设置代理，以及国内加速镜像设置](https://neucrack.com/p/286)