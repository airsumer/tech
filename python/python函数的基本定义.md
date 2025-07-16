关于`python`的一些基础操作.

# 函数定义
## 函数声明
### 函数声明示例
函数参数类型和返回值类型指定:
``` python
def load_iris(
    *, # 特殊参数,限制参数的传递方式
    return_X_y: bool = False, # 限定参数return_X_y的类型为bool,默认值为False
     as_frame: bool = False
    ) -> tuple[Bunch, tuple]: # 返回值类型注解
    ... # 表示这是一个函数声明,这是一种合法的空函数体,可以将...替换成pass
``` 
### 特殊参数
ref:https://docs.python.org/zh-cn/3.13/tutorial/controlflow.html#defining-functions 4.9.3
python中函数参数的传递有三种方式,分别是:
- 仅按位置传递:在仅限位置形参前加使用`/`分隔符
- 尽限关键字传参数:在参数列表中第一个仅限关键字形参前使用`*`
- 按照位置或关键字传递:[default]

``` python
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
    位置或关键字     仅位置             仅关键字
```

如果仅限制使用位置传参,但是实际上又使用了关键字传参,此时编译器就会报错.如:
``` python
def pos_only_arg(arg, /):
    print(arg)

# 使用位置传参,正确执行
pos_only_arg(1)
>>> 1

# 使用关键字传参,编译器报错
pos_only_arg(arg=1)

>>> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: pos_only_arg() got some positional-only arguments passed as keyword arguments: 'arg'

```

### 可变参数列表
使用可变参数列表在编程时比较使用少,因为使用可变参数列表语义不清晰,同时在C系语言中,可变参数列表使用宏实现,没有做类型检查.参考:[C/C++可变参数列表实现原理与缺陷](https://kevins.pro/va_list.html)
``` python
# 限制位置的可变参数列表
def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))

# 限制关键字的可变参数列表
def write_multiple_items(file, separator, **args):
    file.write(separator.join(args))
```
可变参数列表形参后的任何形式参数只能限为**关键字参数**,不用用作位置参数.如果可变参数列表后还要接其他参数,需要类似:
``` python
def concat(*args, sep="/"):
    return sep.join(args)

concat("earth", "mars", "venus")

concat("earth", "mars", "venus", sep=".")
```
但是,这种写法我个人觉得其实没啥必要,多弊无益.

### 解包实参列表
有时候实参的格式与要求的格式不同,需要做一下转换,除了做格式转换外,python还可以执行**解包实参列表**.如内置的`range`函数的形参为独立的`start`和`stop`,但是你也可以通过`*`运算符将实参从列表或元组中解包出来,如:
``` python
# *解包列表或元组
list(range(3, 6))            # 附带两个参数的正常调用

args = [3, 6]
list(range(*args))            # 附带从一个列表解包的参数的调用

# **解包字典
def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)

```

与**解包**相对应的还有**封包**

### 函数传参的过程
常见的函数参数传递方式有3种:**值传递**,**指针传递**和**引用传递**.
在python中,函数的参数传递方式为**引用传递**.也就是说实参传递给函数的其实是值的引用.
在传递实参时,实参的引用会被调入函数的**局部符号表**中.

当函数A调用函数B时,无论函数A的函数体内调用了多少次函数B,都只会给函数B创建一个新的局部符号表.
## 函数体定义

``` python
def fib(n):    # 打印小于 n 的斐波那契数列
    # 函数体中第一段注释称为docstring,用于生成文档
    """Print a Fibonacci series less than n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
```