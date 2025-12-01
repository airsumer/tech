# 用户登录

- 除sys外，都应该登录pdb而不是cdb

## sys用户登录

使用`sqlplus`工具进行登录。如果是刚安装好数据库，可以使用`sys`用户进行登录。注意：使用`sys`用户进行登录时，要使用`sys as sysdba`

``` bash
$sqlplus

SQL*Plus: Release 19.0.0.0.0 - Production on Sat Nov 29 09:42:56 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.

Enter user-name: sys as sysdba
Enter password: 

Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0
```



# 用户管理

## 创建用户

使用`CREATE USER`命令可以创建一个新用户，如：

``` sql
SQL>CREATE USER summer IDENTIFIED BY password;
```

上面的语句创建了一个名为`summer`的新用户，并通过`IDENTIFIED BY`命令指定新用户的密码是`password`。

（注意：创建用户应该在pdb模式下，而不是cdb模式。在cdb模式下创建用户会报错）

## 用户授权

使用`GRANT right TO user;`命令可以将权限授予用户。

 在创建用户后，如果没有给用户授予相应的系统权限，则用户不能连接到数据库，因为该用户缺少创建会话的权限。向用户授予权限的语句为 GRANT，其语法格式为:

``` sql
GRANT 系统权限 TO {PUBLIC | role | username} [WITH ADMIN OPTION]
```

- `WITH ADMIN OPTION` 选项：表示该用户可以将其所有权限再授权给其他用户，也可以将权限再收回。
- `PUBLIC` ：表示将该权限授予数据库中全体用户。
- `role` ：给指定某一角色授权。
- `username` ：给指定用户授权。

常见的系统权限：

| 权限               | 功能                   |
| ------------------ | ---------------------- |
| `CREATE SESSION`   | 允许用户登录到数据库。 |
| `CREATE TABLE`     | 允许用户创建表。       |
| `REATE VIEW`       | 允许用户创建视图。     |
| `CREATE INDEX`     | 允许用户创建索引。     |
| `CREATE PROCEDURE` | 允许用户创建存储过程。 |
| `SELECT ANY TABLE` | 允许用户查询任意表。   |
| `LTER ANY TABLE`   | 允许用户修改任意表。   |
| `DROP ANY TABLE`   | 允许用户删除任意表。   |
| `SYSDBA`           | 系统管理员权限         |
| `SYSOPER`          | 系统操作员权限         |



- 将系统管理员权限授予zhangsan用户
``` sql
	GRANT sysdba To zhangsan;
```

- 授予stu用户 登录、连接的系统权限
``` sql
GRANT create session TO stu;
```

通常创建用户可以授予：

``` sql
grant connect,resource,dba to 用户名;
```



# Ref

- [Oracle用户授权篇](https://www.cnblogs.com/luler/p/17960916)