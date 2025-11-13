
docker是一种虚拟化技术，将其简单当成虚拟机来用。

# docker介绍

docker有几个产品：
- docker engine：docker的核心部件，用于虚拟化
- docker build：一个根据dockerfile生成可运行的镜像的工具
- docker compose：用于管理多个镜像，如 oracle数据库镜像和java镜像，使用docker compose将两个整合起来运行。

docker的架构为：
![docker的架构设计](./assets/docker_structure.png)

虚拟机在宿主机上运行一个完成的虚拟操作系统，而docker则是直接使用宿主机的操作系统内核，也没有进行硬件虚拟，较虚拟机更高效。

镜像没有系统内核，但是镜像是一个特殊的文件系统，提供容器运行时所需的程序、库、资源和配置参数等（如环境变量）。

# 管理镜像

### 拉取镜像

从仓库拉取镜像的命令为：
``` bash
docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
```

- Docker 镜像仓库地址：地址的格式一般是 <域名/IP>[:端口号]。默认地址是 Docker Hub(docker.io)。
- 仓库名：两段式名称，即 <用户名>/<软件名>。对于 Docker Hub，如果不给出用户名，则默认为 library，也就是官方镜像

如`docker pull ubuntu:18.04`命令的完整形式其实就是：`docker pull docker.io/library/ubuntu:18.04`



如果是私有的仓库，那么拉取前还需要登录。这时需要使用`docker login`命令，基本命令形式为：

``` bash
# 语法
docker login [OPTIONS] [SERVER]

Options:
  -p, --password string   Password 密码
      --password-stdin    Take the password from stdin 标准输出
  -u, --username string   Username 用户名
```

同样，`Server`的默认值仍然是`docker hub（docker.io）`

### 查看镜像

通过`docker image`命令可以可以管理下载下来的镜像，常见的操作包括镜像查看和删除等。

``` bash
Usage:  docker image ls [OPTIONS] [REPOSITORY[:TAG]]

List images

Aliases:
  docker image ls, docker image list, docker images

Options:
  -a, --all             Show all images (default hides intermediate images)
      --digests         Show digests
  -f, --filter filter   Filter output based on conditions provided
      --format string   Format output using a custom template:
                        'table':            Print output in table format
                        with column headers (default)
                        'table TEMPLATE':   Print output in table format
                        using the given Go template
                        'json':             Print in JSON format
                        'TEMPLATE':         Print output using the given
                        Go template.
                        Refer to https://docs.docker.com/go/formatting/
                        for more information about formatting output with
                        templates
      --no-trunc        Don't truncate output
  -q, --quiet           Only show image IDs
      --tree            List multi-platform images as a tree (EXPERIMENTAL)
```

使用`docker system df`命令可以查看各个容器的占用大小。


# 运行镜像

通过`docker run`命令可以以镜像为基础启动并运行一个容器。以`ubuntu18.4`为例，运行改系统的命令为：
``` bash
docker run -it --rm ubuntu:18.04 bash
```
- it：交互式运行
- rm：退出容器后将其删除，也可以手动使用`docker rm`命删除容器
- ubuntu：18.4： 以`ubuntu18.4`镜像为基础运行该容器
- bash：因为使用的是交互式启动运行，因此使用`bash`这一个交互式`shell`



# Ref

1. [docker:login和logout登录与登出](https://www.cnblogs.com/hider/p/17043224.html)
