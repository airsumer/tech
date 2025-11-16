使用`dockerfile`可以实现用一个脚本文件构建镜像。

以构建一个基础的c++开发环境为例：

``` dockerfile
# 基础镜像
FROM ubuntu:24.04

# 设置非交互模式，避免安装 tzdata 时卡住(各种yes or no的选择)
ENV DEBIAN_FRONTEND=noninteractive

# 更新系统并安装常用开发工具，使用install -y同样也是为了避免各种交互选择
RUN apt update && apt install -y build-essential cmake git\
    && apt clean

# 默认启动 bash
CMD ["/bin/bash"]
```

# 语法
语句|用法 |例子| 含义
-|-|-|-
`FROM <image>`|用于指定基础镜像，我们的定制镜像就在基础镜像之上构建|FROM ubuntu:22.04|表示使用版本为 22.04 的 ubuntu 镜像来定制我们的镜像。
`RUN <command>`|用于执行命令，是 Dockerfile 中最常用的指令之一，用法也十分简单|`RUN echo -e "hello world!" > test.txt`|表示向文件 test.txt 中写入内容 hello world!。
`COPY <src_paths>... <dest_path>`|用于将主机上的src复制到容器内的dest_path|`COPY package.json config.json /usr/src/app/`|表示将构建上下文目录中的 package.json 和 config.json 两个文件复制到新一层镜像内的 /usr/src/app/ 目录下


字典形式
- `WORKDIR <dir_path>`:
        
        设置docker容器内的以后各层的目录。因为docker是分层构建的，每一个run就是一行，因此直接用`cd`命令只是作用与当前层，而设置工作目录可以作用与所有层。
- `ENV <key1>=<value1> <key2>=<value2> ...`:
  
        用于设置环境变量，其后的 RUN 等命令和所运行的应用都可以使用设定好的环境变
- `EXPOSE <ports>`:
  
        用于声明容器暴露的端口，主要用处是帮助镜像使用者理解这个镜像服务打算使用什么端口，方便配置端口映射。注意，这只是一个声明，并未自动进行端口映射，使用者仍需在运行时使用`-p <host_port>:<container_port>`进行端口映射。
- `CMD <command>`:
  
        作为容器启动命令，即创建容器并启动时立刻执行的命令，可以被 `docker run <image> <command>`中提供的命令替换。

注意：像是`run`和`cmd`命令都可有两种写法，一种是直接写命令，一种是通过字典形式
- shell形式： `RUN pip install -r requirement.text`
- exec形式：`RUN ["pip", "install", "-r", "requirements.txt"]`


# 镜像的构建
## 镜像的构建过程
构建容器需要使用`docker build`命令。其最基本的用法为：
``` bash
$docker build .
```
- `-t，--tag`：指定要构建的镜像的名称和版本，如`docker build -t app:1.0`
- `-f，--file`:指定`dockerfile`文件的路径，默认是当前路径下

镜像是分层的，每一层都是在上一层的基础上做修改，有点类型继承关系。对某一层的修改不影响上层，只会影响当前层和以后的所有层。为了控制镜像的大小，应该控制`dockerifle`的行数。

容器也是分层的，其在镜像的基础上添加了一个容器扩展层，这个层的生命周期和容器相同，因此说容器是易失的，因此这个扩展层在容器销毁后也就不存在了。

## 镜像的上下文
`docker build .`命令最后有一个`.`，表示**上下文路径**

在文件系统中，`.` 表示当前目录，但是在`docker`中`.`指的并不是`Dockerfile`所在的目录（因为 `Dockerfile` 往往在当前目录下），而且`Dockerfile`的路径是由前面的`-f` 参数来指定的。实际上，这个 `.` 指定的是**上下文路径**。

`Docker` 在运行时分为 `Docker Engine` 和**客户端工具**，我们在本地使用各种 `Docker` 命令时，实际上是在使用客户端工具，它与 `Docker Engine` 交互来完成各种功能。
在使用 `docker build` 进行构建时，该命令会将**构建镜像上下文目录**下的**所有内容**打包上传给 `Docker Engine`，`Docker Engine` 展开这个上下文包，获得镜像构建所需的所有文件，完成构建过程。

因此，`docker build` 命令的最后一项表示的就是这个上下文目录。比如，命令 `docker build ./content` 表示以 `./content` 目录作为构建镜像的上下文，那么 `./content` 目录下的所有文件将会被打包用于镜像构建。
并且，`Dockerfile` 中的 `COPY` 等命令往往使用相对路径，
其中源路径就是相对于上下文的（镜像外），
目标路径是相对于工作目录的（镜像内），比如 `COPY ./package.json .` 表示将 `./content/package.json` 复制至镜像内的工作目录下。

还要特别提醒的是，由于只有构建镜像上下文目录下的文件会被上传用于构建，所以，诸如` COPY ../package.json . `或 `COPY /usr/xxx . `这样的命令是无法工作的，前者因为使用了上下文的父目录中的文件，后者因为使用绝对路径，它们对应的文件都超出了上下文的范围，无法被 `Docker Engine` 获得，构建也就无法完成。

# Ref
1. https://summer25.net9.org/backend/docker/note/#_7
2. https://yeasy.gitbook.io/docker_practice/image/build