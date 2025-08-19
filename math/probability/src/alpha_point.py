import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 设置标准正态分布的参数
mu = 0  # 均值
sigma = 1  # 标准差

# 定义α值的范围
alpha_values = np.linspace(0.01, 0.99, 100)

# 计算标准正态分布的α分位点，使用累积分布函数（CDF）
quantiles = norm.ppf(alpha_values, mu, sigma)

# 绘制图像
plt.figure(figsize=(8, 6))
plt.plot(alpha_values, quantiles, label=r"$\alpha$ 分位点", color="b")
plt.title("Standard Normal Distribution Alpha Quantiles", fontsize=16)
plt.xlabel(r"$\alpha$", fontsize=14)
plt.ylabel("Quantiles", fontsize=14)
plt.grid(True)
plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)

# 添加图例
plt.legend()

# 显示图片
plt.show()
