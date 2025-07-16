
# 列表
## 基本特性
列表是用方括号标注，逗号分隔的一组值。可以包含不同类型的元素，但一般情况下，各个元素的类型相同.
``` python
squares = [1, 4, 9, 16, 25]
squares
>>> [1, 4, 9, 16, 25]
```
特性:
- 是sequence类型,支持索引和切片
    ``` python
    squares[0]  # 索引操作将返回条目

    squares[-1]

    squares[-3:]  # 切片操作将返回一个新列表
    ```
- 是mutable类型,数据内容可变
- 构造函数是浅拷贝而不是深拷贝,用`operator =`赋值一个变量时该变量将**引用**现有列表.
    ``` python
    rgb = ["Red", "Green", "Blue"]
    rgba = rgb
    id(rgb) == id(rgba)  # 它们指向同一个对象

    rgba.append("Alph")
    rgb
    ```
## 基本API
列表数据类型支持很多方法，列表对象的所有方法所示如下：

list.append(x)

    在列表末尾添加一项。 类似于 a[len(a):] = [x]。

list.extend(iterable)

    通过添加来自 iterable 的所有项来扩展列表。 类似于 a[len(a):] = iterable。

list.insert(i, x)

    在指定位置插入元素。第一个参数是插入元素的索引，因此，a.insert(0, x) 在列表开头插入元素， a.insert(len(a), x) 等同于 a.append(x) 。

list.remove(x)

    从列表中删除第一个值为 x 的元素。未找到指定元素时，触发 ValueError 异常。

list.pop([i])

    移除列表中给定位置上的条目，并返回该条目。 如果未指定索引号，则 a.pop() 将移除并返回列表中的最后一个条目。 如果列表为空或索引号在列表索引范围之外则会引发 IndexError。

list.clear()

    移除列表中的所有项。 类似于 del a[:]。

list.index(x[, start[, end]])

    返回列表中第一个值为 x 的元素的零基索引。未找到指定元素时，触发 ValueError 异常。

    可选参数 start 和 end 是切片符号，用于将搜索限制为列表的特定子序列。返回的索引是相对于整个序列的开始计算的，而不是 start 参数。

list.count(x)

    返回列表中元素 x 出现的次数。

list.sort(*, key=None, reverse=False)

    就地排序列表中的元素（要了解自定义排序参数，详见 sorted()）。

list.reverse()

    翻转列表中的元素。

list.copy()

    返回列表的浅拷贝。 类似于 a[:]。

## 列表与列表推导式
### 列表推导式的使用场景
通过使用**列表推导式**可以快捷创建列表,算是一个语法糖.列表推导式的常见用法为:对**序列或可迭代对象**中的**每个元素**应用某种操作，**用生成的结果创建新的列表**；或用满足特定条件的元素创建子序列。
``` python
#  创建平方值的列表
squares = []
for x in range(10):
    squares.append(x**2)
print(x)
>>> 9 #这也是和c不同的地方,这里for中创建的变量后面也可以接着用
>>>squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
这种写法等同于
``` python
squares = [x**2 for x in range(10)]
```

ref:
1. https://docs.python.org/zh-cn/dev/tutorial/datastructures.html#more-on-lists 第5.1.3节

# 元组

元组的创建和输入特点为:
``` python
# 创建元组时,多个元素可不加`()`符号
t = 12345, 54321, 'hello!'

>>> t[0]:12345
>>>t:(12345, 54321, 'hello!')

# 元组可以嵌套：

u = (t, (1, 2, 3, 4, 5))

# 元组输出时一定有`()`
>>>u:((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))

# 元组是不可变对象,但是子元素的子元素的值可变：
t[0] = 88888
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```
- 列表和元组都是序列类型,但是元组是**不可变数据类型**,而列表是可变数据类型;
- 元组通常包含不同类型数据,列表通常是相同类型
- 元组可以通过解包或索引访问,列表可迭代访问

ref:
1. https://docs.python.org/zh-cn/dev/tutorial/datastructures.html#more-on-lists 5.3