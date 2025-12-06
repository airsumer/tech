



可以通过如下命令启动`oracle`的`docker`容器。

``` bash
sudo docker run -d \
	--name oracle \
    -p 1521:1521 \
    -p 5500:5500\
    -e ORACLE_SID=ORCLCDB\
    -e ORACLE_PDB=ORCLPDB1\
    -e ORACLE_PWD=Password123\
    -e ORACLE_CHARACTERSET=AL32UTF8\
    container-registry.oracle.com/database/enterprise:19.3.0.0
```

下面对参数进行说明

参数|含义
-|-
`oracle_sid`|`SID`是一个数据库的唯一标识符。通常中是环境变量：`ORACLE_SID`。每个`Oracle`数据库实例都有一个唯一的`SID`，它用于在操作系统层面标识和区分不同的`Oracle`实例。通常用`JDBC`连接数据库时指定的`SID`即为此值。
`oracle_cdb`|容器数据库，是整个实例的“壳”。用于实现实例和数据库的一对多关系。
`oracle_pdb`|`Pluggable Database`，即可插拔数据库，可以实现从一个`CDB`拔出，插入到另一个`CDB`中。`pdb`是真正用于存放表，用户和应用数据的地方。
`oracle_pwd`|用于设置`sys`用户的密码



``` bash
docker run -d --name <container_name> \
 -p <host_port>:1521 -p <host_port>:5500 \
 -e ORACLE_SID=<your_sid> \
 -e ORACLE_PDB=<your_pdbname> \
 -e ORACLE_PWD=<your_database_password> \
 -e INIT_SGA_SIZE=<your_database_sga_memory_mb> \
 -e INIT_PGA_SIZE=<your_database_pga_memory_mb> \
 -e ORACLE_EDITION=<your_database_edition> \
 -e ORACLE_CHARACTERSET=<your_character_set> \
 -e ENABLE_ARCHIVELOG=true \
 -v [<host_mount_point>:]/opt/oracle/oradata \
container-registry.oracle.com/database/enterprise:21.3.0.0

Parameters:
 --name:                 The name of the container (default: auto generated
 -p:                     The port mapping of the host port to the container port.
                         Two ports are exposed: 1521 (Oracle Listener), 5500 (OEM Express)
 -e ORACLE_SID:          The Oracle Database SID that should be used (default:ORCLCDB)
 -e ORACLE_PDB:          The Oracle Database PDB name that should be used (default: ORCLPDB1)
 -e ORACLE_PWD:          The Oracle Database SYS, SYSTEM and PDBADMIN password (default: auto generated)
 -e INIT_SGA_SIZE:       The total memory in MB that should be used for all SGA components (optional)
 -e INIT_PGA_SIZE:       The target aggregate PGA memory in MB that should be used for all server processes attached to the instance (optional)
 -e ORACLE_EDITION:      The Oracle Database Edition (enterprise/standard, default: enterprise)
 -e ORACLE_CHARACTERSET: The character set to use when creating the database (default: AL32UTF8)
 -e ENABLE_ARCHIVELOG:   To enable archive log mode when creating the database (default: false). Supported 19.3 onwards.
 -v /opt/oracle/oradata
                         The data volume to use for the database. Has to be writable by the Unix "oracle" (uid: 54321) user inside the container
                         If omitted the database will not be persisted over container recreation.
 -v /opt/oracle/scripts/startup | /docker-entrypoint-initdb.d/startup
                         Optional: A volume with custom scripts to be run after database startup.
                         For further details see the "Running scripts after setup and on
                         startup" section below.
 -v /opt/oracle/scripts/setup | /docker-entrypoint-initdb.d/setup
                         Optional: A volume with custom scripts to be run after database setup.
                         For further details see the "Running scripts after setup and on startup" section below.
```

The supported configuration options are:

- `ORACLE_SID`

  This parameter changes the Oracle system identifier (SID) of the 
  database. This parameter is optional and the default value is set to 
  `ORCLCDB`.

- `ORACLE_PDB`

  This parameter modifies the name of the `pluggable database (PDB)`. 
  This parameter is optional and the default value is set to `ORCLPDB1`.

- `ORACLE_PWD`

  This parameter modifies the password for the `SYS, SYSTEM and 
  PDBADMIN users`. This parameter is optional and the default value is 
  randomly generated. This password can be changed later as described 
  in the section titled “Changing the Default Password for SYS User”.

- `INIT_SGA_SIZE`

  This parameter modifies the memory in MB that should be used for all 
  SGA components. This parameter is optional, and the default value is 
  calculated during database creation if it isn¿t provided. The user can 
  refer to the section titled ¿Setting the SGA and PGA memory¿ for more details.

- `INIT_PGA_SIZE`

  This parameter modifies the target aggregate memory in MB that should 
  be used for all server processes attached to the instance. This parameter 
  is optional, and the default value is calculated during database creation 
  if it isn¿t provided. The user can refer to the section titled 
  Setting the SGA and PGA memory¿ for more details.

- `ORACLE_EDITION`

  This parameter modifies the edition of the database when the container 
  is started for the first time. This parameter is optional and the two 
  values are enterprise or standard. The default value is enterprise.

- `ORACLE_CHARACTERSET`

  This parameter modifies the character set of the database. This 
  parameter is optional and the default value is set to AL32UTF8.

- `ENABLE_ARCHIVELOG`

  This parameter enables the ARCHIVELOG mode while creating the database for the first time. 
  Default value of this parameter is false.

# 使用idea连接

![image-20251129123509734](./asset/image-20251129123509734.png)
