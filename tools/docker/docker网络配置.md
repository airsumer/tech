

docker的网络配置类型：
  | 模式          | 命令                         | 特点                                            |
  | ------------- | ---------------------------- | ----------------------------------------------- |
  | `bridge模式`    | `--net=bridge`               | 桥接模式（默认设置，自己创建也使用bridge 模式） |
  | `host`模式      | `--net=host`                 | 和宿主即共享网络                                |
  | `container`模式 | `--net=container:NAME_or_ID` | 容器网络连通!(很少用，局限性很大！)             |
  | `none`模式      | `--net=none 不配置网络`      |                                                 |

  使用`docker network`命令查看网络配置：
  ``` bash
  Usage:  docker network COMMAND

Manage networks

Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks
  ```

  关于容器运行时的网络配置过程，推荐查看：[Docker 创建网络步骤](https://jiajially.gitbooks.io/dockerguide/content/chapter_network_pro/pro_network_step.html)

# host
`host`模式下，宿主机和docker容器使用同一个网络。这样的好处是方便，可能存在的问题就是宿主机和容器没有隔离性。
``` docker
docker run --rm -d --network host --name my_nginx nginx
```

# container模式
在container模式下，不同的容器共用一个网络。而host模式下则是容器和宿主机公用一个网络。

# `bridge`网桥模式

Docker安装启动后会在宿主机上创建一个名为`docker0`的虚拟网桥，处于七层网络模型的数据链路层。

后续每当我们创建一个新的`docker`容器，在不指定容器网络模式的情况下，`docker`会通过`docker0`与主机的网络连接，`docker0` 相当于网桥。

使用`bridge`模式新创建的容器，容器内部都会有一个虚拟网卡，名为`eth0`，容器之间可以通过容器内部的IP相互通信。

## 宿主机和容器的网络配置

### 宿主机`docker0`

``` bash
$ifconfig
docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 82:89:de:78:8b:04  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### 创建ubuntu1
``` shell
# 使用桥接模式创建容器1
$sudo docker run -itd --name="ubuntu1" ubuntu:24.04 /bin/bash
$sudo docker exec -it ubuntu1 /bin/bash
$ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
        ether e2:1c:a0:91:8e:b2  txqueuelen 0  (Ethernet)
        RX packets 3069  bytes 35100580 (35.1 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2759  bytes 189968 (189.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### 创建ubuntu2
``` bash
$sudo docker run -itd --name="ubuntu2" ubuntu:24.04 /bin/bash
$sudo docker exec -it ubuntu2 /bin/bash
$ifconfig
$ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.3  netmask 255.255.0.0  broadcast 172.17.255.255
        ether aa:2b:91:f2:bf:42  txqueuelen 0  (Ethernet)
        RX packets 4279  bytes 35180276 (35.1 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3717  bytes 249584 (249.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

## 宿主机、容器间的通信

### 容器间的相互通信
容器间通过bridge进行通信，宿主机（bridge）也可以通过容器的`eth0`网卡访问到容器。
``` bash
$ping 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.062 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.035 ms
64 bytes from 172.17.0.2: icmp_seq=3 ttl=64 time=0.048 ms
64 bytes from 172.17.0.2: icmp_seq=4 ttl=64 time=0.029 ms
64 bytes from 172.17.0.2: icmp_seq=5 ttl=64 time=0.030 ms
64 bytes from 172.17.0.2: icmp_seq=6 ttl=64 time=0.026 ms
```

### 外网访问容器
容器和外部网络的通信方法可以参考：[容器与外部网络通信](https://jiajially.gitbooks.io/dockerguide/content/chapter_network_pro/pro_link_containers.html)
#### 端口映射
如果在互联网想要访问容器内部署的服务，则只有通过**端口映射**的方式。如：
``` bash
# -p <宿主机端口>:<容器端口>
# -P：随机映射到宿主机的端口上
$sudo docker run -d -p 47.108.145.191:8080:80 myapp
```
此命令意为将容器内部内部的80端口映射到宿主机的8080端口上。当然，ip地址可以指定也可以不指定，如果服务器上是多网卡，且docker只需要绑定某一个特定网卡，那么可以指定ip地址，否则默认是`0.0.0.0`。

不过需要注意的是，如果需要让外网成功访问容器内的服务，需要满足以下几个要求：
|要求|示例|原理
-|-|-
容器监听所有地址|`server.listen(80,"0.0.0.0")`|如果只监听`127.0.0.1`，则其他容器和宿主机的消息就收不到
宿主机端口未被占用||宿主机端口被占用会报错
宿主机会转发流量||宿主机会转发流量，外网才能访问docker容器
云服务器端口放行||需要确保服务器端口放行


#### NAT转发
如果是通过端口映射，则必须在创建创建时指定。但是如果是已经`run`起来的容器，那么就可以通过`iptable`来转发。

具体的方法可以参考：[Docker 增加端口映射与管理端口转发教程](https://github.com/whunt1/docker_manage_port)

# Ref
1. [Docker容器内部端口映射到外部宿主机端口 - 运维笔记](https://www.cnblogs.com/kevingrace/p/9453987.html)
2. [docker基础网络配置](https://yeasy.gitbook.io/docker_practice/advanced_network/quick_guide)
3. [docker网络配置：bridge模式、host模式、container模式、none模式
](https://www.cnblogs.com/xiongzaiqiren/p/18177383/docker-network)

# TODO:
1. docker创建自定义网络：https://www.cnblogs.com/zhangchao0515/p/15322851.html
2. 使用`--link`选项实现容器间通信：https://doc.yonyoucloud.com/doc/docker_practice/network/linking.html
3. 自己创建docker网络：https://yeasy.gitbook.io/docker_practice/network/linking