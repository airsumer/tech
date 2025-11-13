
https://www.debian.org/doc/manuals/debian-reference/ch03.zh-cn.html
# 启动过程概述
计算机从上电到运行完整操作系统所经过的步骤：
典型的启动过程像是一个四级的火箭。每一级火箭将系统控制权交给下一级。

- “第一阶段：UEFI”
- “第二阶段：引载加载程序”
- “第三阶段：迷你 Debian 系统”
- “第四阶段：常规 Debian 系统

## UEFI

**Unified Extensible Firmware Interface (UEFI) 统一可扩展固件接口**定义了**启动管理器**作为 UEFI 规范的一部分。
当一个计算机打开电源，启动管理器是启动流程的第一阶段，它检查**启动配置**并基于启动配置的设置，**执行特定的操作系统引导加载程序或操作系统内核（通常是引导加载程序）**。
启动配置通过变量存储在 NVRAM，变量包括指示操作系统引导加载程序或操作系统内核的文件系统路径的变量。

可以把 UEFI 和 BIOS 都理解成一种固件，其主要功能是为计算机提供最底层的、最直接的硬件设置和控制（包括启动操作系统），而 UEFI 是传统 BIOS 升级替代品，功能更强，并兼容传统 BIOS。

EFI system partition (ESP) EFI 系统分区 是一个数据存储设备分区，在计算机里用来遵照 UEFI 规范。当计算机打开电源时，由 UEFI 固件来访问，它存储了 UEFI 应用程序和这些应用程序运行所需要的文件，包括操作系统的引导加载程序。（在老的 PC 系统，存放在 MBR 里的 BIOS 可以用来代替。）

BIOS启动时做的事：

- 通电：CPU 初始化，并执行 BIOS 程序；

- 自检：BIOS 程序启动开始 POST 自检，进行更完整的硬件（检查 CPU、RAM、键盘、鼠标等）检测；

- 此阶段无法屏幕显示，只能通过主板扬声器报警。

- 其他初始化：初始化显卡和其他设备并显示到屏幕；

- 加载 MBR：BIOS 提供中断服务，读取 CMOS 设置，读取第一个启动磁盘的 MBR 到内存让 CPU 执行（此后 BIOS 就撒手不管了），然后由 MBR 引导代码启动操作系统。

## 第二阶段：引导加载程序

引导加载程序是启动过程的第二阶段，由 UEFI 启动。引导加载程序将系统内核映像和 **initrd 映像**加载到内存并将控制权交给它们。initrd 映像是根文件系统映像，其支持程度依赖于所使用的引导加载程序。

Debian 系统通常使用 Linux 内核作为默认的系统内核。当前的 5.x Linux 内核的 initrd 映像在技术上是 initramfs（初始 RAM 文件系统）映像。

有许多引导加载程序和配置选项存在。

对于 UEFI 系统，GRUB2 首先读取 ESP 分区，使用 `"/boot/efi/EFI/debian/grub.cfg"`里面`search.fs_uuid`指定的`UUID`来确定`GRUB2`菜单配置文件`"/boot/grub/grub.cfg"`所在的分区。

## 第三阶段：迷你系统
迷你 Debian 系统是启动流程的第三阶段，由引导加载程序启动。它会在内存中运行系统内核和根文件系统。这是启动流程的一个可选准备阶段。这个系统通常被称为 initrd 或 initramfs 系统。

/init 程序是内存中的根文件系统上执行的第一个程序。这个程序在用户空间把内核初始化，并把控制权交给下一阶段。迷你 Debian 系统能够在主引导流程之前添加内核模块或以加密形式挂载根文件系统，使引导流程更加灵活。

## 第四阶段：常规系统

常规 Debian 系统是启动流程的第四阶段，由迷你 Debian 系统启动。迷你 Debian 系统的内核在此环境下继续运行。根文件系统将由内存切换到实际的硬盘文件系统上。

init 程序是系统执行的第一个程序（PID=1），它启动其它各种程序以完成主引导流程。init 程序的默认路径是 ”/usr/sbin/init“，但可通过内核启动参数修改，例如 ”init=/path/to/init_program"。

在 Debian 8 jessie（2015 年发布）版本后，"/usr/sbin/init" 是一个到 "/lib/systemd/systemd" 的符号链接。

[提示]	提示
你的系统中实际使用的 init 命令可以使用 “ps --pid 1 -f” 命令确认。

# systend初始化
## systemd的启动过程

当 Debian 系统启动，`/usr/sbin/init` 符号链接到的 `/usr/lib/systemd` 作为初始系统进程 (PID=1) 启动，该进程由 root (UID=0)所有。

systemd 初始化进程基于`unit`文件（如.service就是一种unit文件）来并行派生进程，有如下的unit类型：

|单元类型	|文件后缀	|描述
-|-|-
Service	|.service	|定义了系统服务，包括启动，重启，关闭服务的相关指令
Target	|.target	|定义了一组单元的集合，通常作为单元启动的同步点，某个target启动成功就意味着一组相关的service启动成功


### target
target文件夹用于管理一组unit文件，启动级别有：

init架构中系统运行级别|systemd架构中Target Unit	|备注
-|-|-|
0	|runlevel0.target / poweroff.target|	关闭系统
1	|runlevel1.target / rescue.target	|单用户模式
2, 4	|runlevel2.target / runlevel4.target / multi-user.target	|用户自定义的运行级别。不同于Init架构中提供的离线多用户模式，systemd架构默认只提供联网多用户模式，也就是对应Init架构数字为3的运行级别。
3	|runlevel3.target / multi-user.target	|联网多用户模式，不带有图形化界面
5	|runlevel5.target / graphical.target|	联网多用户模式且带有图形化界面

派生的进程被放在一个单独的 `Linux control groups`，在单元后命名，它们属于一个私有的 systemd 层级结构.


### unit文件启动顺序

`unit`是按照下列优先权顺序：

1. `"/etc/systemd/system/*"`: 管理员创建的系统单元文件
1. `"/run/systemd/system/*"`: 运行时单元文件
1. `"/lib/systemd/system/*"`: 发行版软件包管理器安装的系统单元文件

他们的相互依赖关系通过`"Wants=", "Requires=", "Before=", "After=", … `等指示来配置。

## unit文件结构

- 每个字段的官方详细介绍：https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
- 第三方文档：https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html

一个`unit`文件主要分成三个大的部分。
- `unit`:定义一个`unit`的元数据、配置以及和其他`unit`的关系
  - `description`:描述一下这个`unit`文件用来干嘛的
  - `Document`:用来表示查阅说明文档的命令
  - `wants/before/after/require`:此`unit`和其他`unit`之间的关系
    - require:当前的unit的依赖，如果依赖未运行，则次unit不会运行
    - wants：当前unit配合其他unit运行，如果他们未运行，则当前unit不会启动
    - before：指定必须在此unit执行前执行的unit
    - assert：当亲啊unit执行必须要满足的条件
- `service`:定义服务的具体动作
  - ExexStart：服务启动时的命令
  - ExecAtartPre：启动当前服务之前的命令
  - ExecStartPos：启动服务之后执行的命令
  - ExecStop：停止服务所用的命令
- `install`：定义如何启动unit，以及是否开机启动
  - alias：给当前unit定义一个别名
  - WantedBy：它的值是一个或多个 Target，当前 Unit 激活时（enable）符号链接会放入/etc/systemd/system目录下面以 `Target 名 + .wants`后缀构成的子目录中


一份简单的service unit文件的模版
``` service
[Unit]
Description=My Simple HTTP Service

[Service]
ExecStart=/usr/bin/python -m SimpleHTTPServer 8888
Restart=on-failure

[Install]
WantedBy=multi-user.target # 被multi-user.target依赖，即系统以联网多用户模式启动时，自定义的服务会优先于multi-user.target就绪。（尤其是sshd服务需要先于多用户模式启动）

```

## systemctl管理systemd

使用`systemctl`命令提供通用的系统管理操作。

- `systemctl daemon-reload`：systemctl不支持热添加，因此需要用此命令手动加载配置文件
- `systemctl status daemon` : 查看一个服务的状态
- `systemctl start/stop/restart XX`:启动/停止/重启一个服务


# Ref

1. [systemd入门教程：命令篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)
2. [systemd入门教程：实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)
3. [debian-系统初始化](https://www.debian.org/doc/manuals/debian-reference/ch03.zh-cn.html)
4. [《一篇搞懂》系列之三——systemd 祁祁不正经](https://zhuanlan.zhihu.com/p/643259265)