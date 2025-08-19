import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

# 定义lambda参数
lambda_param = 1

# 生成x轴数据
x = np.linspace(0, 5, 100)

# 计算生存函数 S(x) = 1 - CDF(x)
survival_function = 1 - expon.cdf(x, scale=1 / lambda_param)

# 计算x=1时的生存函数值
x1_point = 1
y1_point = 1 - expon.cdf(x1_point, scale=1 / lambda_param)

# 计算x=1.2时的生存函数值
x2_point = 1.2
y2_point = 1 - expon.cdf(x2_point, scale=1 / lambda_param)

# 绘制生存函数
plt.plot(x, survival_function, label="Survival Function")

# 绘制从 (1, 0) 到 (1, S(1)) 的垂直线，标记为S(1)
plt.plot(
    [x1_point, x1_point],
    [0, y1_point],
    color="r",
    linestyle="--",
    label=f"S({x1_point})",
)

# 绘制从 (1.2, 0) 到 (1.2, S(1.2)) 的垂直线，标记为S(1.2)
plt.plot(
    [x2_point, x2_point],
    [0, y2_point],
    color="g",
    linestyle="--",
    label=f"S({x1_point}+Δ)",
)

# 计算通过点(1.2, 0)和(1.2, 30)的垂线
plt.plot([x1_point, x2_point], [y2_point, y2_point], color="b", linestyle="-.")

# 标记 (1, y1_point) 点，显示 S(1)
plt.scatter(x1_point, y1_point, color="red", zorder=5)
plt.text(x1_point - 0.1, y1_point, f"S(1)", color="red")

# 标记 (1.2, y2_point) 点，显示 S(1+Δ)
plt.scatter(x2_point, y2_point, color="green", zorder=5)
plt.text(x2_point + 0.1, y2_point, f"S(1+Δ))", color="green")

# 标记 (1, y2_point) 点，显示 ΔS
plt.scatter(x1_point, y2_point, color="red", zorder=5)
plt.text(x1_point - 0.1, y2_point, f"ΔS)", color="red")

# 设置标签和标题
plt.xlabel("x")
plt.ylabel("S(x)")
plt.title("Survival Function with Vertical Lines and Comparison")

# 显示图例
plt.legend()

# 显示图形
plt.show()
