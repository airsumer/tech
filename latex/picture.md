插图的方法可以查看：https://cn.overleaf.com/learn/latex/Inserting_Images

# 基本的插图方法

## 基本插图方法

`latex`中插入图片的方法。

1. `\usepackage{graphix}`
2. `\includegraphics[]{PATH}`:通过`width`参数可以设置图片的大小，通过`scale`设置图片的缩放，`angle`设置图片的翻转角度

### 图片尺寸的调整

#### `scale`参数设置大小

使用`scale`参数可以控制图片的缩放比例，从而调整图片的大小。基本的用法为：

``` latex
\includegraphics[scale=1.5]{overleaf-logo}
```

在`scale`参数中可以指定图像的缩放比例。



#### `width`参数设置大小

`\includegraphics`命令提供各种参数以设置图片的大小,主要是通过`width\height`参数。

``` latex
\includegraphics[width=5cm, height=4cm]{overleaf-logo}
```

直接使用`width`、`height`等参数来设置图像的尺寸，参数的值可以是`dafault latex length`中的任意一个。这几个单位的介绍为：https://cn.overleaf.com/learn/latex/Inserting_Images#Reference_guide

| Abbreviation   | Definition                                          |
| :------------- | :-------------------------------------------------- |
| `pt`           | A point, is the default length unit. About 0.3515mm |
| `mm`           | a millimetre                                        |
| `cm`           | a centimetre                                        |
| `in`           | an inch                                             |
| `ex`           | the height of an **x** in the current font          |
| `em`           | the width of an **m** in the current font           |
| `\columnsep`   | distance between columns                            |
| `\columnwidth` | width of the column                                 |
| `\linewidth`   | width of the line in the current environment        |
| `\paperwidth`  | width of the page                                   |
| `\paperheight` | height of the page                                  |
| `\textwidth`   | width of the text                                   |
| `\textheight`  | height of the text                                  |
| `\unitlength`  | units of length in the *picture* environment.       |

### 图像旋转

使用`angle`参数可以旋转图像。

``` latex
\includegraphics[scale=1.2, angle=45]{overleaf-logo}
```

参数的值代表旋转的角度。

## 浮动体插图

主要用于将图片或表格这种放在合适的位置，不然的话图片和文字就是绝对布局，如果图片过大，一页放不下，那么图片就会到下一页，出现大段大段的空白。

浮动体：让图片脱离绝对位置，自己找合适的位置放。

创建浮动体使用`figure`环境。

```latex
\begin{figure}[htbp]
	\centering
	\includegraphics[]{}
	\caption{title}
	\label{id}
\end{figure}
```

在浮动体环境中，图片的位置可以改变，但是不能完全改变，有些很复杂的限制规则，可以在参数中使用`!`强制忽略这些规则。

| 参数        | 作用                 |
| ----------- | -------------------- |
| `h(here)`   | 代码在哪，图片就在哪 |
| `t(top)`    | 将图片放在页面的顶部 |
| `b(bottom)` | 放在页面的底部       |
| `p(page)`   | 使用一个新页放图片   |

一般都是直接用`htbp`，使用这个参数告诉系统自动从`htbp`中选一个位置放，将放哪的问题交给系统来解决。

# 图片排版

## 两图并排

两图并排可以在页面中使用`minipage`盒子完成。一个`minipage`可以放一张图，每张图都有各自的`caption`和`label`

``` latex
\begin{figure}
	\centering
	\begin{minipage}{0.4\linewidth}
		\includegraphics[width=\linewidth]{}
	\end{minipage}
	\hfill
	\begin{minipage}{0.4\linewidth}
		\includegraphics[width=\linewidth]{}
	\end{minipage}
\end{figure}
```





## 多张子图

像论文里面会使用多张子图，这种要复杂一些。多张子图共有一个大标题，然后每个子图又有各自的小标题。这种排版效果需要使用`subcaption`宏包。子图需要使用`subfigure`环境。

``` latex
\begin{figure}
	\centering
	\begin{subfigure}{0.4\linewidth}
		\includegraphics[width=\linewidth{}
		\caption{}
		\label
	\end{subfigure}
	\hfill
	\begin{subfigure}{0.4\linewidth}
		\includegraphics[width=\linewidth]{}
		\caption
		\label
	\end{subfigure}
	\caption{}
	\label{}
\end{figure}
```



# TODO

1. 使用`\begin{figure*}`实现分栏排版
2. 使用`hyperref`宏包中`\autoref`取代`\ref`命令，自动根据图、表、公式的类型进行引用，例如`图\ref{fig:pic}=\autoref{fig:pic}`。