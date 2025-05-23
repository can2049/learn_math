在线更新高斯分布的均值和方差是一个经典的统计学习问题，通常用于流式数据或实时处理场景。
在计算时，只保存当前的均值和方差，而不需要保存所有的历史数据。
以下是详细的数学原理和步骤：

---

### **问题描述**
假设已有前  $n$  个观测数据  $\{x_1, x_2, \dots, x_n\}$ ，当前高斯分布的参数为：
- 均值  $\mu_n$
- 方差  $\sigma_n^2$ （或标准差平方）

当新观测值  $x_{n+1}$  到达时，如何更新均值和方差？

---

### **1. 均值的在线更新**
均值的定义是所有观测值的算术平均。更新公式为：

$$
\mu_{n+1} = \mu_n + \frac{x_{n+1} - \mu_n}{n+1}
$$


**数学原理**：
1. 旧均值  $\mu_n = \frac{1}{n} \sum_{i=1}^n x_i$ 。
2. 加入新数据后，新均值：

$$
   \mu_{n+1} = \frac{1}{n+1} \left( \sum_{i=1}^n x_i + x_{n+1} \right) = \frac{n \mu_n + x_{n+1}}{n+1}
   $$

3. 重新整理得到增量形式：

$$
   \mu_{n+1} = \mu_n + \frac{x_{n+1} - \mu_n}{n+1}
   $$


**直观解释**：新均值是旧均值加上新数据与旧均值的偏差的加权（权重为  $\frac{1}{n+1}$ ）。

---

### **2. 方差的在线更新**
方差的定义是数据与均值平方差的期望。在线更新需要同时跟踪**二阶矩（平方和）**或使用**Welford算法**（更数值稳定）。

#### **方法一：基于二阶矩**
1. 维护二阶矩  $M_{2,n} = \sum_{i=1}^n (x_i - \mu_n)^2$ ，则方差为  $\sigma_n^2 = \frac{M_{2,n}}{n}$ （或  $\frac{M_{2,n}}{n-1}$  无偏估计）。
2. 更新步骤：
   - 计算均值增量  $\delta = x_{n+1} - \mu_n$ 。
   - 更新均值  $\mu_{n+1} = \mu_n + \frac{\delta}{n+1}$ 。
   - 更新二阶矩：

$$
     M_{2,n+1} = M_{2,n} + \delta \cdot (x_{n+1} - \mu_{n+1})
     $$

   - 新方差：

$$
     \sigma_{n+1}^2 = \frac{M_{2,n+1}}{n+1}
     $$


**数学原理**：
- 二阶矩的递推关系利用了：

$$
  \sum_{i=1}^{n+1} (x_i - \mu_{n+1})^2 = \sum_{i=1}^n (x_i - \mu_{n+1})^2 + (x_{n+1} - \mu_{n+1})^2
  $$

- 通过代数展开可证明递推公式（详见Welford算法推导）。

#### **方法二：Welford算法（数值稳定）**
1. 初始化： $\mu_0 = 0$ ,  $M_{2,0} = 0$ 。
2. 对每个新数据  $x_{n+1}$ ：
   - 计算均值增量：

$$
     \mu_{n+1} = \mu_n + \frac{x_{n+1} - \mu_n}{n+1}
     $$

   - 更新二阶矩：

$$
     M_{2,n+1} = M_{2,n} + (x_{n+1} - \mu_n)(x_{n+1} - \mu_{n+1})
     $$

3. 最终方差：

$$
   \sigma_{n+1}^2 = \frac{M_{2,n+1}}{n+1} \quad \text{(有偏)} \quad \text{或} \quad \frac{M_{2,n+1}}{n} \quad \text{(无偏)}
   $$


**优势**：避免大数相减导致的数值误差。

---

### **3. 协方差矩阵的扩展（多元高斯分布）**
对于  $d$ -维数据，均值  $\bm{\mu}_n$  和协方差矩阵  $\bm{\Sigma}_n$  的更新类似：
1. 均值：

$$
   \bm{\mu}_{n+1} = \bm{\mu}_n + \frac{\bm{x}_{n+1} - \bm{\mu}_n}{n+1}
   $$

2. 协方差：

$$
   \bm{\Sigma}_{n+1} = \frac{n}{n+1} \bm{\Sigma}_n + \frac{n}{(n+1)^2} (\bm{x}_{n+1} - \bm{\mu}_n)(\bm{x}_{n+1} - \bm{\mu}_n)^T
   $$


---

### **总结步骤**
1. **初始化**：设  $n = 0$ ,  $\mu_0 = 0$ ,  $M_{2,0} = 0$ 。
2. **对于每个新数据  $x_{n+1}$**：
   - 计算  $\delta = x_{n+1} - \mu_n$ 。
   - 更新均值  $\mu_{n+1} = \mu_n + \frac{\delta}{n+1}$ 。
   - 更新二阶矩  $M_{2,n+1} = M_{2,n} + \delta \cdot (x_{n+1} - \mu_{n+1})$ 。
3. **计算方差**：

$$
   \sigma_{n+1}^2 = \frac{M_{2,n+1}}{n+1}
   $$


---

### **数学直觉**
- **均值更新**：新数据对旧均值的修正量与其偏差成正比，权重随数据量减小。
- **方差更新**：二阶矩的递推通过分离新旧均值的差异保持数值稳定性。

这种方法广泛应用于实时滤波、传感器数据处理和机器学习（如在线学习算法）。
