# gcc/g++手动编译

gcc通常用来编译c文件,g++通常用来编译c++文件.gcc/g++的常用选项的含义


| 选项      | 功能                                                                                   |
| --------- | -------------------------------------------------------------------------------------- |
| -o        | 指定生成的可执行文件的文件名                                                           |
| -c        | 仅仅编译，但是不进行链接，如果文件没有定义main函数就需要使用该选项                     |
| -llibrary | library表示要搜索的库文件名称.该选项用于指定手动链接环节中需要调用的库文件,如libcrypto |
| -Llibdic  | dic表示库文件的目录                                                                    |
| -Ihdic    | hdic表示要导入的头文件所在的目录                                                       |
| -share    | 尽量使用动态库                                                                         |
| -static   | 禁止使用动态库                                                                         |
| -w        | 不生成任何警告信息                                                                     |
| -Wall     | 显示所有的警告信息                                                                     |
| -g        | 编译时添加调试信息                                                                     |



- 编译时，链接顺序很重要

- 先输出还是先链接，这个顺序也有点意思

  ​		

  > ‘g++ $^ -lcrypto -lpthread -lgtest -o $@ ’ :报错：
  >
  > g++ key_manager.c crypto.c key_manager_test.cpp -lcrypto -lpthread -lgtest -o key_manager_test.o 
  > /usr/bin/ld: /usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/libgtest.a(gtest-all.cc.o): undefined reference to symbol 'pthread_getspecific@@GLIBC_2.2.5'
  > /usr/bin/ld: /usr/lib/gcc/x86_64-linux-gnu/9/../../../x86_64-linux-gnu/libpthread.so: error adding symbols: DSO missing from command line
  > collect2: error: ld returned 1 exit status
  > make: *** [Makefile:2: key_manager_test.o] Error 1

  把pthread库放到后面就可以了：

  `g++ $^ -o $@  -lcrypto -lgtest -lpthread`

解释：gtest库依赖于pthread库，在链接时，首先链接gtest，gtest要使用的再去找pthread库，因此写命令时，需要将gtest写再pthread前面。

# makefile文件进行编译

如果用gcc，需要手动的进行编译，如果有成百上千个c文件，那么手动输入命令十分麻烦。因此一个思路是，通过在一个文本文件中说明对哪些需要执行什么操作，需要使用到哪些以来，然后根据这个文件自动的生成命令区编译c文件。根据这种思路，我们把这种写明了编译信息的文件就称为`makefie`,通过`make`命令就根据目录下的`makefile`文件自动生成编译命令进行编译.

## makefile文件的基本结构

### 规则的基本组成

makefile文件由规则组成,每条规则明确:

1. 构建目标的前置条件
2. 如何构建

```bash
<target> : <prerequisites> 
[tab]  <commands>
```

| 部件          | 含义                                                   | 可选值                                                                                                         | Example                                              |
| ------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| target        | 指明Make命令要构建的对象                               | 文件名,如果目标是多个文件名,文件名之间用**空格**隔开                                                           |                                                      |
|               |                                                        | 操作名,成为伪目标(phony target),如clean操作。<br />通常需要使用`.PHONY:OP`命令表示,OP是一个操作,而不是一个文件 | .PHONY: clean <br />clean:  <br />       rm *.o temp |
| prerequisites | 指明了目标是否需要重新构建。如果依赖有更新就重新构建。 | 一组文件，有空格隔开                                                                                           |                                                      |
| commands      | 表示如何更新目标文件，由一行或多行shell命令组成        | shell命令前需要使用一个***Tab**键。每行命令在一个单独的shell中执行，shell之间没有继承关系。                    |                                                      |

### 顺序执行命令的三种方式

command默认是并行执行的,没有继承关系,如果要让命令顺序执行,可以采用以下三种方式

| 方式                        | 示例                                                                               |
| --------------------------- | ---------------------------------------------------------------------------------- |
| 合并写，用分号隔开          | var-kept: <br />    export foo=bar; echo "foo=[$$foo]"                             |
| 用分号,在换行符号前加转义符 | var-kept:<br />     export foo=bar; \ <br />     echo "foo=[$$foo]"                |
| 前置`ONESHELL`命令          | .ONESHELL: <br />var-kept:<br />     export foo=bar; <br />     echo "foo=[$$foo]" |



## makefile的基本语法

| 写法                                                                             | 含义                                                                                                                               |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| @command                                                                         | 关闭回声测试(echo),即终端不会打印各条要执行的命令                                                                                  |
| %.o : %.c                                                                        | 等同于`f1.o : f1.c`,`%`表示一个相同的部件                                                                                          |
| txt = Hello World <br />test:<br />     @echo $(txt); \ <br/>     @echo \$\$HOME | 使用`$`引用自定义的变量.使用`$$`引用shell变量                                                                                      |
| `$@`                                                                             | 指代当前的`target`                                                                                                                 |
| `$<`                                                                             | 指代第一个prerequisity.(前置条件)                                                                                                  |
| `$^`                                                                             | 指代所有前置条件                                                                                                                   |
| `$*`                                                                             | 指代`%`表示的内容                                                                                                                  |
| `$(@D) 和 $(@F)`                                                                 | `$(@D)` 和 `$(@F)` 分别指向 `$@` 的目录名和文件名。比如，`$@`是 `src/input.c`，那么`$(@D)` 的值为 `src` ，`$(@F)` 的值为 `input.c` |
| D和F                                                                             | 放在目标后,表示对象所在文件夹和文件名                                                                                              |



Makefile中调用`shell`中的各种函数,其语法为

```bash
$(function arguments)
# 或者
${function arguments}
```

| 常用函数 | 作用             | 示例                                                    |
| -------- | ---------------- | ------------------------------------------------------- |
| shell    | 执行shell命令    | `srcfiles := $(shell echo src/{00..99}.txt)`            |
| wildcard | 替换Bash的通配符 | `srcfiles := $(wildcard src/*.txt)`                     |
| subst    | 进行文本替换     | `$(subst from,to,text)`,在text文本中,将`from`替换成`to` |
| patsubst | 模式匹配的替换   | `$(patsubst pattern,replacement,text)`                  |



## make的常用命令

``` shell
make VERBOSE=1 # 详细打印make过程中的各种命令，目录等信息，verbose：冗长的
```



# 使用cmake生成Makefile文件

## CMakeLists.txt 的一般结构和编译的一般过程

不同平台,`makefile`文件不同,`cmake`就是使用同一文件,生成不同平台的`makefile`文件的工具。`cmake`需要`CMakeLists.txt`文件。（注意：名字只能是这个，不能叫其他）

``` cmake
#要求的cmake的最小版本
cmake_minimum_required(VERSION 3.10)

#项目名称
project(hello) # ${PROJECT_NAME}

#include

#link

#执行规则:指定生成的可执行文件的名称和相关源文件
add_executable(hello.o main.cpp printhello.cpp)
```

一般的编译过程：

1. 因为使用**`cmake`**进行编译会生成很多中间文件，因此一般需要建立一个`build`目录来存放：
2. 使用`cmake ..`命令，在父目录寻找`CMakeLists.txt`, 在当前目录生成`Makefile`文件
3. 使用`make`命令进行编译和链接

``` shell
mkdir build && cd build
cmake ..
make
```



## include



``` cmake
#set(SOURCES
#    src/Hello.cpp
#    src/main.cpp
#)
file(GLOB SOURCES "src/*.cpp") # 替代上面的内容，glob命令：使用正则表达式查找文件
```

``` cmake
# target_include_directories()函数将头文件所在目录转意成 -I/path的形式
target_include_directories(target
    PRIVATE
        ${PROJECT_SOURCE_DIR}/include
)
```

## 链接库

``` cmake
# 添加一个静态链接库，名字叫做hello_library,使用src/hello.cpp来生成
add_library(hello_library STATIC
    src/Hello.cpp
)
```

``` cmake
# 添加一个共享链接库
add_library(hello_library SHARED
    src/Hello.cpp
)
```

``` cmake
#  给链接库起别名
add_library(hello::library ALIAS hello_library)
```

``` cmake
# 将链接库链接到可执行文件
target_link_libraries(hello_binary
    PRIVATE
        hello::library
)
```

| 规则                                   | 含义                                                                                   | 类比           |
| -------------------------------------- | -------------------------------------------------------------------------------------- | -------------- |
| `add_library(libmy.a mylib.cpp)`       | 使用`mylib.cpp`生成一个叫做`libmy.a`的库                                               | 相当于`gcc -c` |
| `add_executable(main.o main.cpp)`      | 使用`main.cpp`生成一个叫做`main.o`的可执行文件                                         | 相当于`gcc -o` |
| `add_subdirectory(subModuleDir)`       | 表示添加一个子模块,子模块中包含`CMakeLists.txt`和源代码,子模块的路径为`./subModuleDir` |                |
| `target_link_libraries(target source)` |                                                                                        |                |
| `target_include_directories`           |                                                                                        |                |
| `set（key value）`                     | 定义一个变量                                                                           |                |

## `link`和`include`中关`PUBLIC`和`PRIVATE`的含义

假设`A→B→C`，如果编译B的可执行文件写的是：`target_link_libraries(B PUBLIC C)`,则表示C是B的public成员,提供对外访问服务.即A也能调用C中定义的函数.

PRIVATE:表示被链接的库是私有属性,因此不提供对外接口,只能B使用,A不能使用

## 静态库与共享库（动态链接库）

共享库其实就是动态链接库

## cmake中的一些变量

| Variable                 | Info                                                                                      |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| `CMAKE_SOURCE_DIR`       | The root source directory                                                                 |
| CMAKE_CURRENT_SOURCE_DIR | The current source directory if using sub-projects and directories.                       |
| PROJECT_SOURCE_DIR       | The source directory of the current cmake project.                                        |
| CMAKE_BINARY_DIR         | The root binary / build directory. This is the directory where you ran the cmake command. |
| CMAKE_CURRENT_BINARY_DIR | The build directory you are currently in.                                                 |
| PROJECT_BINARY_DIR       | The build directory for the current project.                                              |



## make install设置

install()函数的一般使用方法：

``` cmake
install(TARGETS targets... [EXPORT <export-name>]
        [RUNTIME_DEPENDENCIES args...|RUNTIME_DEPENDENCY_SET <set-name>]
        [[ARCHIVE|LIBRARY|RUNTIME|OBJECTS|FRAMEWORK|BUNDLE|
          PRIVATE_HEADER|PUBLIC_HEADER|RESOURCE|FILE_SET <set-name>|CXX_MODULES_BMI]
         [DESTINATION <dir>]
         [PERMISSIONS permissions...]
         [CONFIGURATIONS [Debug|Release|...]]
         [COMPONENT <component>]
         [NAMELINK_COMPONENT <component>]
         [OPTIONAL] [EXCLUDE_FROM_ALL]
         [NAMELINK_ONLY|NAMELINK_SKIP]
        ] [...]
        [INCLUDES DESTINATION [<dir> ...]]
        )
```

使用cmake进行安装的一般语法：

注意：cmake_install_prifix前缀需要加在顶层cmakelists.txt文件中

``` cmake
# 设置安装路径，Linux下默认是/usr/local
SET(CMAKE_INSTALL_PREFIX ${PROJECT_BINARY_DIR})


# Install
############################################################

# Binaries
install (TARGETS cmake_examples_inst_bin DESTINATION bin)

# Library
# Note: may not work on windows
install (TARGETS cmake_examples_inst
    LIBRARY DESTINATION lib)

# Header files
install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/ DESTINATION include)

# Config
install (FILES cmake-examples.conf DESTINATION etc)
```



卸载安装：

在当前目录（即使用make install命令的当前路径下），输入`sudo xargs rm < install_manifest.txt`命令即可从路径中删除安装的库

## build type

### 通过命令手动设置构建类型

通过cmake命令的`-DCMAKE_BUILD_TYPE=XXX`参数手动设置编译的4种类型。

- Release 
- Debug 
- MinSizeRel 
- RelWithDebInfo 

``` cmake
cmake .. -DCMAKE_BUILD_TYPE=Release
```

### 设置默认的build  type

通过在`CMakeLists.txt`中添加下列语句设置默认的build type

``` cmake
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message("Setting build type to 'RelWithDebInfo' as none was specified.")
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()
```

​     

## 第三方库

使用`find()`函数在`${CMAKE_MODULE_PATH}`下查找第三方库。`CMAKE_MODULE_PATH`的默认值在Linux下为`/usr/share/cmake/Modules`         

# 关于编译时的一些注意事项

## 关于c和c++混合编程

c和c++混合编程的时候，需要注意由此引发的文件链接问题。即cpp文件调用c文件时，出现未定义的问题。例如有：`a.h`,`a.c`,`b.cpp`三个文件，如果`b.cpp`使用了` #include "a.h" `调用`a.h`，在使用cmake和make进行编译的时候有可能报错为：

![image-20230302153822082](https://qingbin.oss-cn-chengdu.aliyuncs.com/img/2023/20230302153924.png)

解决方法，

1. 如果是cpp文件调用c文件，则直接将c的后缀名改成cpp就行

2. 使用`extern "c"`语句，使用c语言的规范导入头文件，如

   ``` c
   #ifdef _cplusplus
   // _cplusplus宏是c++标准中定义的一个宏，用于表示c++的版本
   extern "c"{
       #include "a.h";
   }
   #endif
   ```

   



## 关于文件main函数

#### 1. 没有main函数的文件编译

- gcc编译器编译时报错：/usr/lib/gcc/x86_64-linux-gnu/5/…/…/…/x86_64-linux-gnu/crt1.o：在函数‘_start’中：(.text+0x20)：对‘main’未定义的引用

- gcc默认编译并链接成可执行文件,如果c文件中没有写main方法的话,表示这是一个静态库而是一个可执行文件.此时可以添加`-c`参数表明要生成一个库

#### 2. 多文件调用的编译

假如`a.h`和`a.cpp`,`b.cpp`调用了`a.h`,则在编译的时候,`b.cpp`就需要添加`a.cpp`的依赖。此外，还需要注意，`a.cpp`和`b.cpp`中只能有一个main函数,否则会报错：链接失败。
