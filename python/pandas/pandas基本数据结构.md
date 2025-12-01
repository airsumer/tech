

两种基本数据结构：

1. `DataFrame`可以看成一个**矩形表格**（比如`m`行`n`列的数据）甚至是整个表格，存储的是二维的数据。
2. `Series`则是`DataFrame`中的**一列**，存储的是一维的数据![db86fd2ccc0a36ab68604c834be73a08](./asset/db86fd2ccc0a36ab68604c834be73a08.png)数据。

# Series

`Series`本质上是一个**带标签的一维数组**，可以看成是**numpy一维数组+字典**的结合体。

## Series数据结构的定义

Series类的实例属性包含：`data(序列值)、index（行索引）、dtype（存储类型）、name（序列名）`四部分属性。

``` python
# https://github.com/pandas-dev/pandas/blob/main/pandas/core/series.py
class Series():
    """
      Parameters
    ----------
    data : array-like, Iterable, dict, or scalar value
        Contains data stored in Series. If data is a dict, argument order is
        maintained. Unordered sets are not supported.
    index : array-like or Index (1d)
        Values must be hashable and have the same length as `data`.
        Non-unique index values are allowed. Will default to
        RangeIndex (0, 1, 2, ..., n) if not provided. If data is dict-like
        and index is None, then the keys in the data are used as the index. If the
        index is not None, the resulting Series is reindexed with the index values.
    dtype : str, numpy.dtype, or ExtensionDtype, optional
        Data type for the output Series. If not specified, this will be
        inferred from `data`.
        See the :ref:`user guide <basics.dtypes>` for more usages.
        If ``data`` is Series then is ignored.
    name : Hashable, default None
        The name to give to the Series.
    copy : bool, default False
        Copy input data. Only affects Series or 1d ndarray input. See examples.

    """
   def __init__(
        self,
        data=None,
        index=None,
        dtype: Dtype | None = None,
        name=None,
        copy: bool | None = None,
   		) -> None:
```

以一个例子说明series的各个属性的含义：

``` python
import pandas as pd
s = pd.Series(data = [102,103,104,105],
          index = ['小明','小强','小红','小兰'],
          dtype = 'int',
          name = '语文')
print(s)
```

运行的结果为：

![image-20250519083305586](./asset/image-20250519083305586.png)

## series的核心用途





可以通过列表或字典创建

``` python
    >>> d = {"a": 1, "b": 2, "c": 3}
    >>> ser = pd.Series(data=d, index=["a", "b", "c"])
    >>> ser
    a   1
    b   2
    c   3
    dtype: int64
```

## DataFrame

``` python
# 、https://github.com/pandas-dev/pandas/blob/main/pandas/core/frame.py
class DataFrame(NDFrame, OpsMixin):
    """
    Two-dimensional, size-mutable, potentially heterogeneous tabular data.

    Data structure also contains labeled axes (rows and columns).
    Arithmetic operations align on both row and column labels. Can be
    thought of as a dict-like container for Series objects. The primary
    pandas data structure.

    Parameters
    ----------
    data : ndarray (structured or homogeneous), Iterable, dict, or DataFrame
        Dict can contain Series, arrays, constants, dataclass or list-like objects. If
        data is a dict, column order follows insertion-order. If a dict contains Series
        which have an index defined, it is aligned by its index. This alignment also
        occurs if data is a Series or a DataFrame itself. Alignment is done on
        Series/DataFrame inputs.

        If data is a list of dicts, column order follows insertion-order.

    index : Index or array-like
        Index to use for resulting frame. Will default to RangeIndex if
        no indexing information part of input data and no index provided.
    columns : Index or array-like
        Column labels to use for resulting frame when data does not have them,
        defaulting to RangeIndex(0, 1, 2, ..., n). If data contains column labels,
        will perform column selection instead.
    dtype : dtype, default None
        Data type to force. Only a single dtype is allowed. If None, infer.
        If ``data`` is DataFrame then is ignored.
    copy : bool or None, default None
        Copy data from inputs.
        For dict data, the default of None behaves like ``copy=True``.  For DataFrame
        or 2d ndarray input, the default of None behaves like ``copy=False``.
        If data is a dict containing one or more Series (possibly of different dtypes),
        ``copy=False`` will ensure that these inputs are not copied.

        .. versionchanged:: 1.3.0
       """
     def __init__(
        self,
        data=None,
        index: Axes | None = None,
        columns: Axes | None = None,
        dtype: Dtype | None = None,
        copy: bool | None = None,
    ) -> None:
```

DataFrame的主要特点是：

- `DataFrame`的属性在`eries`的基础上增加了列索引`columns`，减少了name属性。

- `DataFrame`的设置数据类型`dtype`时，表示要强制的数据类型，但只允许使用一种数据类型。

	如果没有定义强制的数据类型，就会自行推断

构造函数有：

``` python

import pandas as pd
# 使用二维列表创建
data = [[102,98,106,78,86],
        [103,107,89,84,78],
        [104,78,88,91,94],
        [105,110,99,69,79]]
df = pd.DataFrame(data=data,
            index = ['小明','小强','小红','小兰'],
            columns = ['语文','数学','英语','历史','地理'])

# 使用字典创建
data = {'语文':[102,103,104,105],
        '数学':[98,107,78,110],
        '英语':[106,89,88,99],
        '历史':[78,84,91,69],
        '地理':[86,78,94,79]}
 
df = pd.DataFrame(data=data,index = ['小明','小强','小红','小兰'])
```

运行的结果为：![image-20250519085915564](./asset/image-20250519085915564.png)

# 数据读取

| **文件类型**  | **文件后缀名**      | **读取文件函数** |
| ------------- | ------------------- | ---------------- |
| **CSV**文件   | **.csv**            | read_csv()       |
| **Excel**文件 | **.xlsx**或**.xls** | read_excel()     |
| **TXT**文件   | **.txt**            | read_table()     |

**上述三个读取文件的函数有一些公共参数。常见的公用参数含义如下表：**

| **参数名**    | **参数含义** | **详解**                                                     |
| ------------- | ------------ | ------------------------------------------------------------ |
| `header`      | 文件首行     | 默认首行为表头，即列名设置为None表示第一行不作为列名         |
| `index_col`   | 索引列       | 默认第一列为索引列index_col=['姓名','语文']，表示将姓名及语文成绩这两列设置为索引列设置为None表示无索引列 |
| `useclos`     | 读取列       | 默认读取所有列，useclos=['姓名','语文']，表示只读取姓名及语文成绩这两列 |
| `parse_dates` | 时间列       | 需要转化为时间的列parse_dates=['XX','YY']，表示将 "XX","YY"这两列转换成时间格式 |
| `nrows`       | 读取行数     | 默认全部读取nrows=100，表示读取前100行数据                   |

以`read_excel`为例，其函数的定义为：

``` python
@doc(storage_options=_shared_docs["storage_options"])
@Appender(_read_excel_doc)
def read_excel(
    io,
    sheet_name: str | int | list[IntStrT] | None = 0,
    *,
    header: int | Sequence[int] | None = 0,# 文件首行，默认首行为表头
    names: SequenceNotStr[Hashable] | range | None = None,
    index_col: int | str | Sequence[int] | None = None,# 索引列，指定以哪列为索引
    usecols: int
    | str
    | Sequence[int]
    | Sequence[str]
    | Callable[[str], bool]
    | None = None,
    dtype: DtypeArg | None = None,
    engine: Literal["xlrd", "openpyxl", "odf", "pyxlsb", "calamine"] | None = None,
    converters: dict[str, Callable] | dict[int, Callable] | None = None,
    true_values: Iterable[Hashable] | None = None,
    false_values: Iterable[Hashable] | None = None,
    skiprows: Sequence[int] | int | Callable[[int], object] | None = None,
    nrows: int | None = None,
    na_values=None,
    keep_default_na: bool = True,
    na_filter: bool = True,
    verbose: bool = False,
    parse_dates: list | dict | bool = False,
    date_parser: Callable | lib.NoDefault = lib.no_default,
    date_format: dict[Hashable, str] | str | None = None,
    thousands: str | None = None,
    decimal: str = ".",
    comment: str | None = None,
    skipfooter: int = 0,
    storage_options: StorageOptions | None = None,
    dtype_backend: DtypeBackend | lib.NoDefault = lib.no_default,
    engine_kwargs: dict | None = None,
) -> DataFrame | dict[IntStrT, DataFrame]:
```

# 数据操作

## 遍历

[DataFrame](https://zhida.zhihu.com/search?content_id=163628731&content_type=Article&match_order=1&q=DataFrame&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NDgxMzA1MDQsInEiOiJEYXRhRnJhbWUiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoxNjM2Mjg3MzEsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.F2vX7JZoyYhWZSstg6sU5P050uGJo3fPpoGrd0WKCj4&zhida_source=entity)的遍历方式主要有三种

|                          |                                |
| ------------------------ | ------------------------------ |
| `DataFrame.iterrows()`   | 按行顺序优先，接着依次按列迭代 |
| `DataFrame.iteritems()`  | 按列顺序优先，接着依次按行迭代 |
| `DataFrame.itertuples()` | 按行顺序优先，接着依次按列迭代 |

以`iterrows()`为例，其用法为：DataFrame.**iterrows**()[source\]](https://github.com/pandas-dev/pandas/blob/v2.2.3/pandas/core/frame.py#L1505-L1557)

Iterate over DataFrame rows as (index, Series) pairs.

## 数据清洗

| 函数                              | 作用                                                         |
| --------------------------------- | ------------------------------------------------------------ |
| `drop_duplicates()`               | 自动把重复的行去掉。                                         |
| `df2['Chinese'].astype(np.int64)` | 规范数据格式,统一每一个series的数据类型                      |
| `str.strip`                       | 使用 `strip `函数删除某些特殊符号，比如`df2['Chinese'].str.strip('$')` |



## 数据统计

