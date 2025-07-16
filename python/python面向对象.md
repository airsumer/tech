ref:
1. https://brinnatt.com/programming/python_tech/17%e3%80%81python3-%e9%9d%a2%e5%90%91%e5%af%b9%e8%b1%a1/
2. https://pythonhowto.readthedocs.io/zh-cn/latest/object.html#id2
# 类的定义
ref:
1. https://brinnatt.com/programming/python_tech/17%e3%80%81python3-%e9%9d%a2%e5%90%91%e5%af%b9%e8%b1%a1/
## 成员变量的定义
与C++之类的不同,在C++中,类定义中的`static`修饰的成员是归类所有的,而非`static`成员是实例所拥有的.

### C++中的类定义
``` c++
class student{
    private:
        uint8_t _age;
        bool _sex;
    protected:
        uint8_t major;
    
    public:
        static uint8_t _type=1;
        string _name

        student(string name,uint8_t age,bool sex):_name(name),_age(age),_sex(sex){}

        // 定义一个静态函数
        static void classMethod(){};
        
}

int main(void){
    student zhangsan("zhangsan",20,1);
    std::cout <<zhangsan::_type <<std::endl;
}
```

### python中的类定义
在python的类中,一共有两种成员属性:
- 类属性:定义在类中,类似于C++中的`static`成员
- 对象属性:类的某一个实例自身所拥有的属性

如果实例想调用类属性,需要通过`INSTANCE.class.ATTRIBUTE`的形式调用,如cpp中的static成员一样,这个成员是所有实例共享的,如果一个实例修改了该属性的值,那么其他实例查看该变量的值时也会得到修改后的值.
``` python
class student:
    # 在类中定义类成员
    _type=1
    
    # 在构造函数中定义实例属性:python中显式添加self,c++中隐式自动添加this
    def __init__(self,name,age,sex,major):
        # 默认public类型变量
        self.name=name
        # 通过`__`定义`private`变量
        self.__age=age
        self.__sex=sex
        # 通过`_`定义`protected`变量
        self._major=major

    # 通过@classmethod装饰器表明这是类函数,相似于c++中的静态函数
    @classmethod
    def classMethod();
        pass

student zhangsan('zhangsan',20,1)
# 实例访问类属性
print(zhang.class._type)
```

PS:
- 无论是成员变量还是成员方法,如果想要设置为private,只需要将其名字设置为`__`就行,protected的需要将名字设置为`_`
- 类名必须是**大驼峰命名**
- 构造函数中第一参数`self`表示类的某一个实例,而在c++中同样的`this`关键字会自动绑定到对象中.但是在cpp中,类中定义的非static函数只有实例化了才能调用,因为cpp默认会将函数绑定到对象,因此不需显式传入this关键字.但是在python中,其理念是显式大于隐式,因此如果函数不手动传入self,其就类似面向过程的普通函数,或者说可以像cpp中的static函数一样被调用.


## 类的继承
ref:
1. https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/125012990
### cpp中的类继承规则
cpp中不同的继承方式对应的对父类成员的访问规则:
| 继承方式  | 父类权限  | 子类权限  |
| --------- | --------- | --------- |
| public    | public    | public    |
|           | protected | protected |
|           | private   | 不能继承  |
| protected | public    | protected |
|           | protected | protected |
|           | private   | 不能继承  |
| private   | public    | private   |
|           | protected | private   |
|           | private   | 不能继承  |

在cpp的继承中,子类对象的成员包括两部分:
- 继承自父类的成员
- 子类自己定义的成员
因此内存模型中有一部分是父类对象.构造子类对象时其实是先构造了一个父类对象,然后再构造子类的其他成员.子类会保存父类的private成员,但是不能访问,如果要访问需要父类提供的`getter/setter`函数.

``` c++
#include <iostream>

class Base {
private:
    int baseSecret = 42;
public:
    int basePub = 1;
    int getSecret();
    int setSecret(int value);

    Base(int _sec,int _pub):secret(_sec),pub(_pub){};
    ~Base(){};
};

class Derived : public Base {
private:
    int child_secret = 99;
public:
    int child_pub = 2;
    //  子类的构造函数需要先调用父类的构造函数
    Derived(int baseSecret,int basePub,int childSecret,int child_pub):Base(baseSecret,basePub),child_secret(childSecret),child_pub(childPub){}:
    ~Derived(){
        child_secret=0;
        child_pub=0;
        // 最后会自动调用父类的析构函数,但是子类中手动调用父类的析构函数编译器会报错.
    };
};
```

### python中的继承规则

python的类继承相比c中的类继承没有public和private的继承区别,同时继承的写法也不同.规则为:
- 子类继承父类的成员变量和成员方法
- 子类不继承父类的构造方法，能够继承父类的析构方法
- 子类不能删除父类的成员，但可以重定义父类成员
- 子类可以增加自己的成员

``` python
class Base:
    def __init__(self,secret,pub):
        self.__baseSecret=secret
        self._basePub=pub

# 继承父类的方式不同
class Derive(Base):
    def __init__(self,secret,pub,childSecret,childPub):
        # 手动调用父类的构造函数
        super(Derive,self).__init__(secret,pub)
        self._baseSecret=childSecret
        self._basePub=childPub
```

# 对象的内存管理
在python中,一个对象在内存中的大概结构为
``` c
struct class{
    int id;// 每个对象的id,实际上也可以算地址
    int type;// 每个对象的类型
    int count;//对象的引用计数器,用于垃圾回收
    struct object value;// 对象所存储的值
}
```

此外,每个对象都还有一些相关的内置成员,这些内置的属性或者函数在命名上都以`__`开始和结尾,如构造函数`__init__()`就是一个内置的函数,但是这个内置函数需要程序员手动重载.

python提供一些内置函数可以读取一个对象的这些基本属性.
| 方法                      | 作用                                             |
| ------------------------- | ------------------------------------------------ |
| `id()`                    | 一个类函数,获取对象的唯一编号,通常是一个内存地址 |
| `type()`或`__class__`属性 | 可获取对象的类型                                 |
| `__base__`                | 对象的一个属性,查看其基类                        |

此外,所有的对象都会继承`object`类,就算没有明确定义继承的基类,也会默认继承`object`类.`object`类的成员和属性参考:https://pythonhowto.readthedocs.io/zh-cn/latest/object.html#id14 13.3节.这里提供一个简单摘要:
| 成员               | 作用                                                                          |
| ------------------ | ----------------------------------------------------------------------------- |
| __delattr__        |
| __dir__()          | 用于获取类的所有属性和方法名,是一个字典,内置的`dir()`函数调用的就是他         |
| __doc__            | 指向当前类的描述字符串,描述字符串不会被继承                                   |
| __format__         |
| __getattribute__   |
| __hash__           |
| __init__           |
| __init__subclass__ |
| __repr__           |
| __setattr__        |
| __sizeof__         |
| __str__            | 用于`str()`函数中                                                             |
| __call__           | 可以将一个对象名函数化,有点类似cpp中的重载`()`运算符?装饰器基于`__call__`实现 |