使用`docker run --mount`可以在创建容器时将宿主机上的文件挂载到`docker`容器的指定目录上。
# 数据卷
## 数据卷的介绍
`docker`容器是易失的，因此非常不建议用容器来进行数据的持久化。因此想要`在docker`中实现数据的存储，就需要将数据保存在宿主机上，这种方式在`docker`中叫做**数据卷**。

**数据卷** 是一个可供**一个或多个容器**使用的特殊目录。其保存在宿主机上，但是可以通过`docker run --mout`将宿主机上保存的**volume**挂载到`docker`容器中，从而实现数据的持久化。它绕过 **nionFS**，可以提供很多有用的特性：
- **数据卷**可以在容器之间共享和重用
- 对 **数据卷**的修改会立马生效
- 对**数据卷**的更新，不会影响镜像
- **数据卷**默认会一直存在，即使容器被删除
注意：数据卷 的使用，类似于 `Linux` 下对目录或文件进行`mount`，镜像中的被指定为挂载点的目录中的文件会复制到数据卷中（仅数据卷为空时会复制）。

## 数据卷管理
可以使用`docker volume`命令可以完成数据卷的相关管理。
``` bash
Usage:  docker volume COMMAND

Manage volumes

Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove unused local volumes
  rm          Remove one or more volumes
  update      Update a volume (cluster volumes only)

Run 'docker volume COMMAND --help' for more information on a command.
```

### 数据卷的创建- create命令
创建数据卷的基本命令为`docker volume create [VOLUME]`.该命令的说明为：

``` bash
Usage:  docker volume create [OPTIONS] [VOLUME]

Create a volume

Options:
      --availability string       Cluster Volume availability ("active", "pause", "drain") (default "active")
  -d, --driver string             Specify volume driver name (default "local")
      --group string              Cluster Volume group (cluster volumes)
      --label list                Set metadata for a volume
      --limit-bytes bytes         Minimum size of the Cluster Volume in bytes
  -o, --opt map                   Set driver specific options (default map[])
      --required-bytes bytes      Maximum size of the Cluster Volume in bytes
      --scope string              Cluster Volume access scope ("single", "multi") (default "single")
      --secret map                Cluster Volume secrets (default map[])
      --sharing string            Cluster Volume access sharing ("none", "readonly", "onewriter", "all") (default "none")
      --topology-preferred list   A topology that the Cluster Volume would be preferred in
      --topology-required list    A topology that the Cluster Volume must be accessible from
      --type string               Cluster Volume access type ("mount", "block") (default "block")
```

命令示例：`docker volume create fpp_data`:创建一个名为`fpp_data`的数据卷。

### 数据卷信息的查看- ls&inspect命令
使用`docker volume ls`命令可以查看当前拥有哪些`volume`。如：
``` bash
$sudo docker volume ls
DRIVER    VOLUME NAME
local     fpp_data
```

如果要查看具体某一个`volume`的信息，就可以使用`docker volume inspect`命令。
``` bash
$sudo docker volume inspect fpp_data
[
    {
        "CreatedAt": "2025-11-15T08:15:21+08:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/fpp_data/_data",
        "Name": "fpp_data",
        "Options": null,
        "Scope": "local"
    }
]
```

## 数据卷的使用- `docker run --mount`选项
`docker run --mount`可以在运行容器时挂载数据卷。例如：
``` bash
$ docker run -d -P \
    --name web \
    # -v my-vol:/usr/share/nginx/html \
    --mount source=fpp_data,target=/usr/share/nginx/html \
    nginx:alpine
```
下面创建一个名为 web 的容器，并加载一个 数据卷 到容器的 `/usr/share/nginx/html` 目录。

# 宿主机文件挂载
通过`docker run --mount`命令也可以将宿主机的本地文件目录挂载到容器中去。如：
``` bash
$docker run -d -P \
    --name web \
    # -v /src/webapp:/usr/share/nginx/html \
    --mount type=bind,source=/src/webapp,target=/usr/share/nginx/html \
    nginx:alpine

```
上面的命令加载主机的 `/src/webapp`目录到容器的`/usr/share/nginx/html`目录。这个功能在进行测试的时候十分方便，比如用户可以放置一些程序到本地目录中，来查看容器是否正常工作。本地目录的路径必须是绝对路径，以前使用 `-v`参数时如果本地目录不存在 `docker` 会自动为你创建一个文件夹，现在使用`--mount`参数时如果本地目录不存在，Docker 会报错。

`Docker`挂载主机目录的默认权限是`读写`，用户也可以通过增加`readonly`指定为`只读`。

``` bash
$docker run -d -P \
    --name web \
    # -v /src/webapp:/usr/share/nginx/html:ro \
    --mount type=bind,source=/src/webapp,target=/usr/share/nginx/html,readonly \
    nginx:alpine
```
加了`readonly` 之后，就挂载为 `只读` 了。如果你在容器内 `/usr/share/nginx/html` 目录新建文件，会显示如下错误
``` bash
/usr/share/nginx/html # touch new.txt
touch: new.txt: Read-only file system
```

注：
因为`Linux`中一切都是文件，目录也是文件，因此通过`mount`命令不仅可以挂文件，也可以挂目录

# 总结
使用`docker run --mount`可以在创建容器时指定要访问的数据。`--mount`有几种类型：
- [default]：挂载数据卷，需要配合`docker volume`命令使用
- `type=bind`:绑定一个或多个宿主机上的文件到容器中去