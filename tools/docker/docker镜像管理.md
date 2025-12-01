



# 镜像与导入

## `docker commit`命令

将`Docker`容器通过`commit`命令保存成镜像

``` bash
$docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]
```

例如：

``` bash
$ docker commit \
    --author "Tao Wang <twang2218@gmail.com>" \
    --message "修改了默认网页" \
    webserver \
    nginx:v2
```

但是不建议直接使用`docker commit`命令，因为文件会变得很大。

## `docker save`命令

使用`docker save`命令可以将一个或多个镜像保存为`tar`存档。

``` bash
$docker image save [OPTIONS] IMAGE [IMAGE...]
```

通常的用法是使用`docker save -o`将镜像写入一个归档文件里。

``` bash
$docker save -o ubuntu.tar ubuntu:22.04
```

## `docker load`

使用`docker load`命令可以从`tar`文件中载入镜像。例如：

``` bash
$docker load -i ubuntu.tar
```

`-i`表示从文件导入镜像及相关的元数据，如`tag`等。

1. [利用 commit 理解镜像构成](https://yeasy.gitbook.io/docker_practice/image/commit)