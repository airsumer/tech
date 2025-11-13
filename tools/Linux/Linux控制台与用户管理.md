学习材料：

https://www.debian.org/doc/manuals/debian-reference/ch01.zh-cn.html#_console_basics

# 控制台基础
##  unix命令格式标准
通过`man`命令可以查看某个命令的帮助文档。
以`shutdown`命令为例，介绍命令的说明文档的格式。

### 例1:`shutdown`命令
``` shell
NAME
     shutdown – close down the system at a given time

SYNOPSIS
     shutdown [-] [-h [-u] | -r | -s | -k] [-o [-n]] time
              [warning-message ...]
```

| 符号  | 含义                                       | 举例                                   |                                       |                                  |
| ----- | ------------------------------------------ | -------------------------------------- | ------------------------------------- | -------------------------------- |
| `[]`  | **可选项**，可以省略                       | `[-r]` 表示 `-r` 可有可无              |                                       |                                  |
| `{}`  | **必须选一个**                             | `{start\| stop\| restart}` 表示三者必选其一 |
| `...` | **可重复项**，可以写多个                   | `[file ...]` 表示可以跟多个文件        |                                       |                                  |
| `[-]` | 旧式写法，表示选项前可以加 `-`，也可以不加 | `[−]time` 表示可以写 `-time` 或 `time` |                                       |                                  |


例如`shutdown`命令中的`[-h[-u]]`表示可选`-h`作为参数，同时如果使用了`-h`参数，也可以跟着用`-u`参数，如`shutdown -hu`

### 例2:`{}`符号的含义
使用`tar`命令为例，介绍`{}`符号的意义。
``` shell
NAME
       tar - an archiving utility

SYNOPSIS
   Traditional usage
       tar {A|c|d|r|t|u|x}[GnSkUWOmpsMBiajJzZhPlRvwo] [ARG...]
```
在此例中，`{A|c|d|r|t|u|x}`表示`tar`命令必须要从`{A|c|d|r|t|u|x}`中必须选一个。

## 用户登录：`root shell`提示符

可以进入`root`账户的方法

| 序号 | 方法                               | 特点                       |
| ---- | ---------------------------------- | -------------------------- |
| 1    | 使用`root`作为用户名登录             |
| 2    | 任何用户的的`shell`提示符下输入`su`  | 保留当前用户的一些环境设定 |
| 3    | 任意用户的`shell`提示符下输入`su -l` | 不保存当前用户的环境设定   |

## 进入和退出控制台的方法
### 退出控制台
使用`ctrl+D`快捷键可以关闭shell活动。如果正处于字符控制台，将会返回到登录提示行。

也可以使用`exit`命令退出命令行

### 清空控制台
使用`clear`命令可以清除已经输出的内容。

使用`reset`命令可以重置控制台。

### 关闭系统

普通多用户模式下，可以使用`shutdown -h now`命令关闭系统。该命令的基本格式为：`shutdown [-] [-h] `
- `-h`代表`halted`，意思是停止
- `-r`表示重启系统
- `-c`表示取消已计划的关机任务
- `now`表示立即关机，也可以换成具体的时间，如`14:00`表示在`14:00`关机

## 用户管理


|command | usage|
|-|-|
|`adduser`|**交互式**创建用户
|`useradd`|**非交互式**创建用户
|`passwd`|设置或更改用户的密码
|`usermod`|对用户的属性进行更改，如用户所属的组，或给用户添加`sudo`权限
`deluser`|删除一个用户

### 创建用户
可以使用`adduser`交互式创建用户，或者用`useradd`来非交互式创建用户。

#### `adduser`交互式创建用户
该命令简介为：
``` shell
adduser [-c comment] [-d home_dir] [-e expire_date] [-f inactive_time] [-g initial_group] [-G group[,...]] [-m [-k skeleton_dir] | -M] [-p passwd] [-s shell] [-u uid [ -o]] [-n] [-r] loginid
```

基本用法为：`sudo adduser alice`,如：
``` shell
sumer@Aliyun:~$ sudo adduser alice
info: Adding user `alice' ...
info: Selecting UID/GID from range 1000 to 59999 ...
info: Adding new group `alice' (1002) ...
info: Adding new user `alice' (1002) with group `alice (1002)' ...
info: Creating home directory `/home/alice' ...
info: Copying files from `/etc/skel' ...
New password: 
Retype new password: 
passwd: password updated successfully
Changing the user information for alice
Enter the new value, or press ENTER for the default
	Full Name []: 
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] 
info: Adding new user `alice' to supplemental / extra groups `users' ...
info: Adding user `alice' to group `users' ...
```

相应的如果要删除用户可以使用`deluser`命令，如`deluser --remove-home alice`

#### `useradd`：非交互式创建用户
该命令可以在创建时指定用户所在的**组**，`shell`类型，`home`目录路径等。算是`adduser`的进阶版。

``` shell
sudo useradd -m -s /bin/bash 用户名  # -m: 创建家目录，-s: 指定shell
```

- 指定`home`目录
``` shell
sudo useradd -m -d /path/to/home 用户名
```
- 指定`用户组`
``` shell
sudo useradd -m -G 组名 用户名  # 如 sudo,adm
```

### `sudo`授权

1. 将用户添加到`sudo`组：`sudo usermod -aG sudo username`
2. 将用户添加到`/etc/sudoers`文件:在文件中添加`用户名   ALL=(ALL:ALL) NOPASSWD:ALL`

## 控制台常用快捷键

|快捷键	|描述|
-|-
Ctrl-U|删除光标前到行首的字符
Ctrl-H|删除光标前的一个字符
Ctrl-D|终止输入（如果你在使用 shell，则退出 shell）
Ctrl-C|终止一个正在运行的程序
Ctrl-Z|通过将程序移动到后台来暂停程序
Ctrl-S	|停止屏幕输出
Ctrl-Q	|激活屏幕输出
Ctrl-Alt-Del|	重启/关闭系统，参见 inittab(5)
左 Alt 键（可选择同时按下 Windows-key）|	Emacs 和相似 UI 的元键（meta-key）
Up-arrow 向上方向键	|开始在bash 中查看命令历史
Ctrl-R	|开始在 bash 的增量命令历史中搜索
Tab	|在 bash 命令行中补全文件名
Ctrl-V Tab	|在 bash 命令行中输入 Tab 而不是进行补全
