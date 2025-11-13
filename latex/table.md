
# 表格过宽或越界的解决方法
## 缩小字体
在表格前加一个`\small`命令，缩小字号（一个命令的作用域是以后的一个段落）。

## 使用graphicx::resizebox
使用`graphicx`包中的`resizebox`命令自动调整字号。

``` latex
\usepackage{graphicx}
...
\begin{table}
\resizebox{\textwidth}{!}{
    \begin{tabular}
    ...
    \end{tabular}
}
\end{table}
```

## 手动断行
使用`\makecell`命令手动设置单元格，单元格内可以设置手动换行和对齐。通过手动换行来控制表格的宽度。要使用`\makecell`命令需要手动导入`makecell`包。

`\makecell`命令默认是**居中对齐**，可以在参数中使用`[t|b|r|l|c]`参数来调整对齐位置。