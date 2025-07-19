latex中两种算法和伪代码的插入方法:
1. 使用`algpseudocode OR algcompatible OR algorithmic`中的任一一个包输入算法主体,使用`algorithm`包来生成标题
2. 直接使用`algorithm2e`包
两种方法互斥,一个文档中只能选一种,不能两种都用.

# algorithm2e
`algorithm`是一个**浮动环境**,类似与表格和图片.使用`algorithm2e`写伪代码只有两步:
1. 在导言区导入`algorithm2e`包
2. 在正文区的`\algorithm`环境中编写伪代码

除了while,if等语句外,每一行都应该以`\;`结尾
## 伪代码基本命令

`\For{}{}`
`\While{}{}`