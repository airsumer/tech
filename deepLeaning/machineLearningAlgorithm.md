传统的机械学习算法
# 线性回归
## 模型的基本表示
$$
f(x;w,b)=w^Tx+b 
$$
这种形式下线性模型有个专门的偏置值`b`,通过使用**增广权重向量** $\mathbf{\hat{w}}$和**增广特征向量**$\mathbf{\hat{x}}$可以去掉这些偏置值,将线性模型变为$f(\hat{x};\hat{w}) = \hat{w}^T \hat{x}$.
$$
\begin{align*}
f(x;w,b)&=w^Tx+b \\
\because x=\begin{bmatrix}x_1\\ \vdots \\ x_D \end{bmatrix} 
\quad &\& \quad w=\begin{bmatrix}w_1 \\\vdots \\w_D\end{bmatrix}\\
\therefore f(x;w,b)&= 
    \begin{bmatrix}
    w_1 \cdots w_d
    \end{bmatrix}
    \times 
    \begin{bmatrix}
    x_1\\ \vdots \\ x_D
    \end{bmatrix}+b \\
    &=w_1x_1+\cdots+w_Dx_D+b\\

令\hat{x}&=x \oplus 1 \overset{\triangle}{=} \begin{bmatrix}
    x \\1
\end{bmatrix}=
\begin{bmatrix}
    x_1\\\vdots \\x_D\\1
\end{bmatrix} \\
又令\hat{w} &=\hat{w}\oplus b \overset{\triangle}{=}
\begin{bmatrix}
    w \\ b
\end{bmatrix}=
\begin{bmatrix}
    w_1 \\ \vdots \\w_d \\b
\end{bmatrix} \\

\therefore f(x;\hat{w}) &=\hat{w}^T\hat{x} \overset{\triangle}{=} [w_1, \cdots, w_D , b] \times \begin{bmatrix}
    x_1\\\vdots \\x_D\\1
\end{bmatrix} \\
&=w_1x_1+\cdots+w_Dx_D+b \\
&=w^T+b \\
&=f(x;w,b)\\
\end{align*}
$$

## 学习准则

由于回归问题的输出是一个连续的值,因此使用**平方损失函数**,其经验风险函数为:
$$
\begin{align*}
    \mathcal{R(w)}&= \sum_{n=1}^N\mathcal{L} \left ( y^{(n)},f(x^{(n)});w \right ) \\
    &=\frac{1}{2}\sum_{n=1}^N\mathcal{L} \left ( y^{(n)}-w^Tx^{(n)} \right )^2 \\
    &=\frac{1}{2}\parallel y-\mathbf{X}^Tw \parallel^2
\end{align*}
$$
在经验风险计算公式中,$\mathbb{y}=\left [ y^{(1)},\cdots,y^{(N)}\right ]^T \in \mathbb{R}^N$.而由于模型使用的是$f(\hat{x};\hat{w})$形式,所以输入$\mathbf{X} \in \mathbb{R}^{(D+1)\times N}$是由所有样本输入特征组成的矩阵.(该矩阵其实是一个增广矩阵).
$$
\mathbf{X}=
\begin{bmatrix}
    x_1^{(1)} &\cdots &x_1^{(N)}\\
    \vdots &\ddots &\vdots \\
     x_D^{(1)} &\cdots &x_D^{(N)}\\
     1&\cdots&1\\
\end{bmatrix}
$$

## 优化准则
机器学习模型的优化需要求解找到一个参数$w$使得模型的经验风险最小化.即:
$$
\displaystyle w \to \frac{\partial}{\partial w}\mathcal{R(w)}=0
$$
由于风险最小化问题是所有样本的损失值的均值,而每个样本的特征又是一个向量,因此模型的优化问题实质一个矩阵微积分问题.
### 矩阵微积分
#### 标量关于向量的导数
假设有函数标量$y=f(\mathbf{X})$,其中$\mathbf{X}=[x_1 \cdots x_m]$.则标量`y`关于向量$\mathbf{X}$的导数也可以写成向量的形式.
$$
\frac{\partial y}{\partial \mathbf{X}}=\left [ \frac{\partial y}{\partial x_1},\cdots,\frac{\partial y}{\partial x_m} \right]^T
$$

#### 向量关于向量的导数
向量$\mathbf Y=[y_1,\cdots,y_N]$关于向量$\mathbf{X}=[x_1,\cdots,x_M]^T$的导数是一个矩阵,其中每一列都是一个$w$对向量$y$的偏导数.
$$
\frac{\partial f(x)}{\partial x}=\begin{bmatrix}
    &\frac{\partial y_1}{\partial x_1}   &\cdots   &\frac{\partial y_N}{\partial x_1}\\
    &\vdots  &\ddots  &\vdots \\
    &\frac{\partial y_1}{\partial x_M}  &\cdots  &\frac{\partial y_N}{\partial x_M}\\
\end{bmatrix}
$$

#### 特殊的关于向量的导数
有几个特殊的向量的导数:
$$
\begin{align}
    \frac{\partial x}{\partial x} &= I \\
    \frac{\partial Ax}{\partial x}&=A^T\\
    \frac{\partial x^TA}{\partial x}&=A\\
    \frac{\partial X^TX}{\partial X}&=2X
\end{align}
$$

### 经验风险最小化

$$
\begin{align*}
&\frac{\partial}{\partial w}\mathcal{R(w)}\\
=&\frac{\partial \frac{1}{2} \parallel y-X^Tw  \parallel ^2}{\partial w}\\
=&\frac{1}{2} \times 2 \times (y-X^Tw) \times \frac{\partial(y-X^Tw)}{\partial w} \\
\because &   \frac{\partial Ax}{\partial x}=A^T\\
\therefore& 上式=-X \times(y-X^Tw) \\
&=XX^Tw-Xy\\
&要使得\frac{\partial}{\partial w}\mathcal{R(w)}=0\\
\Rightarrow &XX^Tw-Xy=0 \\
\Rightarrow& XX^Tw=Xy \\
&若 XX^T可逆\\
\Rightarrow &[XX^T]^{-1} \times XX^Tw=[XX^T]^{-1} \times Xy\\
\Rightarrow & w=[XX^T]^{-1} \times Xy \\
& 根据最小二乘法可求解w
\end{align*}
$$

### 结构风险最小化
#### 结构风险最小化的引入-经验风险的局限性
要求经验风险最小化的前提假设是$XX^T$为可逆矩阵,
但是$XX^T$未必有逆矩阵.只有当$XX^T$为满秩矩阵时其才为可逆矩阵.
- $XX^T$不可逆,则不能直接求出经验风险最小化
<!-- TODO:矩阵非满秩矩阵时的问题 -->
- 非满秩时说明特征之间存在**共线性**(特征冗余,存在线性相关).特征冗余:
$$
假设x_i=-x_j \\
f(w,x)=w_ix_i+w_jx_j \\
$$

为了约束$w$的取值,不让其取值过大,所以引入一个约束项(也叫做正则化项),构成一个新的风险函数,叫做**结构风险最小化(structure risk minimization,srm)**.
$$
\mathcal{R(w)} =\frac{1}{2} \parallel y-\mathbf{X}^Tw \parallel ^2+\frac{1}{2}\lambda\parallel w\parallel^2\\
\begin{cases}
    \lambda:&正则化系数,是一个超参 \\
    \frac{1}{2}\lambda\parallel w\parallel^2:&正则化项
\end{cases}
$$

#### 结构风险最小化
对结构风险函数的偏导数就行化简,得到$w^*=(XX^T+\lambda I)^{-1}Xy$.这种方法在统计学上叫做**岭回归(Ridge Regression)**

# 概率论中的线性回归

# 多项式回归-曲线拟合
对于曲线就需要使用多项式函数,对应的模型为:
$$
\begin{align*}
f(x,w)&=w_0 + w_1x+w_2x^2+\cdots + w_Mx^M \\
&=w^T\Phi(x) \begin{cases}
    w:m+1维的向量,\mathbb{R^{m+1}} \\
    m:x的最高次数,是一个超参 \\
    \Phi(x):\left [ 1,x,\cdots,x^M \right]
\end{cases}
\end{align*}
$$
在上面模型中,模型的非线性是通过**基函数**$\Phi(x)$来实现的,如果把$\Phi(x)$看成一个整体的话,非线性模型和线性模型的形式没区别,因此非线性模型也可以使用线性模型的推导思路.

## 学习准则
多项式回归仍然使用平方损失函数.
$f(x,w)=w^T\Phi(x)$可以看成一种特殊的线性模型,因此多项式回归的平方损失函数为:
$$
\mathcal{R(w)}=\frac{1}{2}\sum_{n=1}^N \left ( y^{(n)}-w^T\Phi(x^{(n)}) \right )^2
$$
而求解经验风险最小化的过程也和线性回归类似,但是要注意链式法则.

控制过拟合的方法:
- 添加正则化
- 增加样本数量,令经验风险更接近期望风险

### 多项式次数(Degree)的选择
<!-- TODO:可以整理分类讨论,例如degree=10时,若x^9一般x<1,则w需要很大才不会让这个特征消失,因为x<1,所以x^9特别小,梯度下降时这个特征对梯度的影响微乎其微,为了不让特征小时,对应系数需要特别大.而这样的话,一旦x>1了,只要x增加了一点点,而本身系数又比较大,则将会引起很大的误差 -->
多形式次数的选择是一个**模型选择问题(model selection problem)**.
Degeree过大则导致模型过于复杂,容易发生过拟合.这就导致高次项随便变化一点,损失值就会变化很多,为了缓解这种问题,可以加入正则化来对参数$w$进行约束,**惩罚大的系数**.(TODO:可以理解成让系数和高次项相互抵消?).

加入正则化后,模型的经验风险函数为:
$$
\hat{\mathcal{R}}(w)=\frac{1}{2}\sum_{n=1}^N \left ( y^{(n)} - w^T\Phi(x^{(n)}) \right)^2 + \frac{\lambda}{2}w^Tw \\
\begin{cases}
    \frac{\lambda}{2}w^Tw:正则化项\\ 
    \lambda:正则化系数\\
\end{cases}
$$