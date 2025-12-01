
# for语句
<font color=red>**python**中的`for`语句不同与C中的`for`语句.</font>

## C和Python中的for循环风格差异
C中的for语句一般是程序员手动定义迭代步骤和终止条件,如:
``` c
for(int i=0;i<10;i++>){
    printf("%d\n",i);
}
```
python中的`for`语句在任意的**sequence**类型的元素上进行迭代,其风格完全不同c系列的编程语言,其标准的`for`循环风格如下:
``` python
numbers = [1, 2, 3, 4, 5] 
for n in numbers:
    print(n)
```
python的`for`循环不依靠索引,因此不需要对索引变量进行初始化,不需要递增索引,不需要边界检查.
在python中,`for`通常用于循环**迭代器**.

## python关于for的定义
`for`主要用于迭代各种迭代器.其定义为:
``` python
for_stmt: "for" target_list "in" starred_expression_list ":" suite
          ["else" ":" suite]
```

`starred_expression_list` 表达式会被**求值一次**；它应当产生一个 `iterable` 对象。 将针对该可迭代对象创建一个`iterator`。随后`iterator`被赋值给循环变量。每次迭代都会发生循环变量的赋值,如:
``` python
for i in range(10):
    print(i)
    i = 5             # 这不会影响 for 循环
                      # 因为它将被 range 对象中的下一个索引
                      # 所覆盖
```

TODO:
或者也可以将python中的`iterator`看成一个先入先出的**队列**,在`for`每迭代一次,`iterator`就将队首元素赋值给循环变量.

ref:
1. https://docs.python.org/zh-cn/dev/reference/compound_stmts.html#for
2. https://www.freecodecamp.org/chinese/news/loops-and-iterations-in-python/

## for与range()函数
内置的`range()`函数可以用于生成等差数列,其也是可以可迭代对象,因此也常用于for循环中.例如
``` python
for nv in range(10):
    print(nv)
>>> 输出0-9(不包括10)
```

ref:
1. https://docs.python.org/zh-cn/dev/tutorial/controlflow.html#the-range-function

# `match`语句
<font color=red>python中的`match`语句作用类似`c`中的`switch`,但是机制不同,更像是模式匹配</font>
如果有多个`case`语句同时匹配,只会执行第一个`case`,而在c语言中,如果有多个`case`符合且没有break,那么所有的匹配项都会执行.

## `C`中的`switch`语句
C中的switch语句有几个特点:
- `switch`中的类型只支持**整数**类型
- `case`分支中的值<font color=red><em>只能是常量</em></font>
- 多个`case`分支中的值不能重复
- 只要没有break,就会执行该分支以及后面**所有**分支的语句;
    ``` c
    #include <stdio.h>

    void http_error(int code){
    switch(code){
            case 400:
                    printf("Bad request\n");
            case 404:
                    printf("Not found\n");
            case 418:
                    printf("I'm a teapot\n");
            default:
                    printf("Something's wrong with the internet\n");
    }
    }
    int main(){
            http_error(400);
    }

    <!-- 输出 -->
    /**
    $ ./test.exe
    Bad request
    Not found
    I'm a teapot
    Something's wrong with the internet
    */
    ```
ref:
1. https://blog.csdn.net/weixin_44488341/article/details/131253343
## `Python`中的`switch`语句
`python`中的`match`语句相对于c中的switch,逻辑不同,支持的数据类型不同.
- python中的match语句,如果有多个`case`同时匹配成功,则只会执行一次.且支持`|`逻辑或运算符.
    ``` python
    def http_error(status):
        match status:
            # 可以使用|运算符将多个字面值组合到一个模式
            case 400|403:
                return "Bad request"
            case 400|404:
                return "Not found"
            case 418:
                return "I'm a teapot"
            # _符号表示通配符,代表必然会匹配成功
            case _:
                return "Something's wrong with the internet"

    print(http_error(400))
    >>> Bad request
    ```
- `match`不仅支持整数类型,还支持`tuple`等复合数据类型,以及其他更复杂的模式匹配具体支持的匹配模式,详细可以参考:https://docs.python.org/zh-cn/dev/reference/compound_stmts.html#the-match-statement 8.6.4节

# pass语句
 pass 语句不执行任何动作。语法上需要一个语句，但程序毋需执行任何动作时，可以使用该语句。说白了就是一个占位符.例如：
- 用于占位等待
    ``` python
    while True:
        pass  # 无限等待键盘中断 (Ctrl+C)
    ```
- 用于创建类
    ``` python
    class MyEmptyClass:
        pass
    ```
- 用于定义函数声明:pass 还可用作函数或条件语句体的占位符，让你保持在更抽象的层次进行思考。pass 会被默默地忽略：
    ``` python
    def initlog(*args):
        pass   # 此处相当于...,记得实现这个！
    ```