伯努利分布:
$p(x)=\mu^x(1-\mu)^(1-x)$
- $\mu$:事件A出现的概率
- $x \in {0,1}$:表示出现或不出现
二项分布:

n次伯努利分布,以X表示A出现的次数,$x \in {0,...,n}$
则其分布为:$P(X=k)=(\begin{matrix}
    n\\
    k
\end{matrix}) \mu^k(1-u)^{(n-k)},k \in {0,1,...,n}$

连续随机变量

使用概率密度函数(Probability Density Function,PDF)$p(x)$来描述,PDF的形式要求为:$\int_{-\infty}^{+\infty}p(x)dx=1$

常见的连续随机变量分布

高斯分布(Gaussian Distribution):
  
$X \sim N(\mu,\sigma^2)$

$p(x)=\frac{1}{\sqrt{2\pi}\sigma}exp(-\frac{(x-u)^2}{2\sigma^2})$

累计分布函数(Cumulative Distribution Function,CDF)