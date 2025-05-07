好的！我们来**详细展开高斯-牛顿法（Gauss-Newton Method）的完整推导过程**，包括：

1. **问题定义**
2. **目标函数的梯度和 Hessian 的详细推导**
3. **高斯-牛顿法的迭代方向推导**
4. **线搜索策略说明**
5. **终止条件**
6. **具体求解示例（曲线拟合）**
7. **算法步骤总结**

---

## 🧠 一、问题定义：非线性最小二乘优化

我们要解决如下形式的优化问题：

$$
\min_{\mathbf{x} \in \mathbb{R}^n} f(\mathbf{x}) = \frac{1}{2} \sum_{i=1}^m r_i(\mathbf{x})^2 = \frac{1}{2} \| \mathbf{r}(\mathbf{x}) \|^2
$$

其中：
- $ \mathbf{x} \in \mathbb{R}^n $ 是待优化的参数向量
- $ \mathbf{r}(\mathbf{x}) = [r_1(\mathbf{x}), r_2(\mathbf{x}), \dots, r_m(\mathbf{x})]^T \in \mathbb{R}^m $ 是残差函数（residual function）
- 每个 $ r_i(\mathbf{x}) $ 是关于 $ \mathbf{x} $ 的非线性函数
- 目标是使所有残差平方和的一半最小化（方便后续求导）

---

## 📘 二、目标函数的梯度和 Hessian 推导

### 1. 定义目标函数

$$
f(\mathbf{x}) = \frac{1}{2} \mathbf{r}(\mathbf{x})^T \mathbf{r}(\mathbf{x}) = \frac{1}{2} \sum_{i=1}^m r_i(\mathbf{x})^2
$$

### 2. 计算梯度（Gradient）

使用链式法则对每个变量 $ x_j $ 求偏导：

$$
\frac{\partial f}{\partial x_j} = \sum_{i=1}^m r_i(\mathbf{x}) \cdot \frac{\partial r_i}{\partial x_j}
$$

写成向量形式：

$$
\nabla f(\mathbf{x}) =
\begin{bmatrix}
\frac{\partial f}{\partial x_1} \\
\frac{\partial f}{\partial x_2} \\
\vdots \\
\frac{\partial f}{\partial x_n}
\end{bmatrix}
=
\begin{bmatrix}
\sum_i r_i \frac{\partial r_i}{\partial x_1} \\
\sum_i r_i \frac{\partial r_i}{\partial x_2} \\
\vdots \\
\sum_i r_i \frac{\partial r_i}{\partial x_n}
\end{bmatrix}
= J(\mathbf{x})^T \mathbf{r}(\mathbf{x})
$$

其中：
- $ J(\mathbf{x}) \in \mathbb{R}^{m \times n} $ 是雅可比矩阵，定义为：
  $$
  J(\mathbf{x}) =
  \begin{bmatrix}
  \frac{\partial r_1}{\partial x_1} & \cdots & \frac{\partial r_1}{\partial x_n} \\
  \vdots & \ddots & \vdots \\
  \frac{\partial r_m}{\partial x_1} & \cdots & \frac{\partial r_m}{\partial x_n}
  \end{bmatrix}
  $$

所以最终得到：

$$
\boxed{
\nabla f(\mathbf{x}) = J(\mathbf{x})^T \mathbf{r}(\mathbf{x})
}
$$

---

### 3. 计算 Hessian 矩阵

继续对梯度求导：

$$
H_f(\mathbf{x}) = \nabla^2 f(\mathbf{x}) = \frac{\partial}{\partial \mathbf{x}} (J(\mathbf{x})^T \mathbf{r}(\mathbf{x}))
$$

利用乘积法则展开：

$$
H_f(\mathbf{x}) = \sum_{i=1}^m \left[ \nabla r_i(\mathbf{x}) \cdot \nabla r_i(\mathbf{x})^T + r_i(\mathbf{x}) \cdot \nabla^2 r_i(\mathbf{x}) \right]
$$

即：

$$
H_f(\mathbf{x}) = J(\mathbf{x})^T J(\mathbf{x}) + \sum_{i=1}^m r_i(\mathbf{x}) \cdot \nabla^2 r_i(\mathbf{x})
$$

但高斯-牛顿法的核心思想是**忽略二阶项**（也就是含 $ \nabla^2 r_i(\mathbf{x}) $ 的项），得到近似 Hessian：

$$
\boxed{
H_f(\mathbf{x}) \approx J(\mathbf{x})^T J(\mathbf{x})
}
$$

---

## 🔁 三、高斯-牛顿法的迭代公式

在每一步迭代中，我们用当前点 $ \mathbf{x}_k $ 处的目标函数进行二次近似：

$$
f(\mathbf{x}) \approx f(\mathbf{x}_k) + \nabla f(\mathbf{x}_k)^T (\mathbf{x} - \mathbf{x}_k) + \frac{1}{2} (\mathbf{x} - \mathbf{x}_k)^T H_f(\mathbf{x}_k) (\mathbf{x} - \mathbf{x}_k)
$$

代入近似梯度和 Hessian：

$$
f(\mathbf{x}) \approx f(\mathbf{x}_k) + \mathbf{r}_k^T J_k (\mathbf{x} - \mathbf{x}_k) + \frac{1}{2} (\mathbf{x} - \mathbf{x}_k)^T J_k^T J_k (\mathbf{x} - \mathbf{x}_k)
$$

令 $ \mathbf{p} = \mathbf{x} - \mathbf{x}_k $，目标是最小化这个模型：

$$
\min_{\mathbf{p}} m_k(\mathbf{p}) = \mathbf{r}_k^T J_k \mathbf{p} + \frac{1}{2} \mathbf{p}^T J_k^T J_k \mathbf{p}
$$

对其求导并令导数为零：

$$
\nabla_{\mathbf{p}} m_k(\mathbf{p}) = J_k^T \mathbf{r}_k + J_k^T J_k \mathbf{p} = 0
$$

解得：

$$
\boxed{
\mathbf{p}_k = - (J_k^T J_k)^{-1} J_k^T \mathbf{r}_k
}
$$

然后更新：

$$
\boxed{
\mathbf{x}_{k+1} = \mathbf{x}_k + \alpha_k \mathbf{p}_k
}
$$

其中 $ \alpha_k > 0 $ 是步长，通常通过线搜索确定。

---

## 📊 四、算法步骤总结

给定初始点 $ \mathbf{x}_0 $，重复以下步骤直到收敛：

1. **计算残差向量：**
   $$
   \mathbf{r}_k = \mathbf{r}(\mathbf{x}_k)
   $$

2. **计算雅可比矩阵：**
   $$
   J_k = J(\mathbf{x}_k)
   $$

3. **构建线性系统：**
   $$
   J_k^T J_k \mathbf{p}_k = - J_k^T \mathbf{r}_k
   $$

4. **求解搜索方向：**
   $$
   \mathbf{p}_k = - (J_k^T J_k)^{-1} J_k^T \mathbf{r}_k
   $$

5. **线搜索找到最优步长 $ \alpha_k $**（如 Armijo 准则）

6. **更新参数：**
   $$
   \mathbf{x}_{k+1} = \mathbf{x}_k + \alpha_k \mathbf{p}_k
   $$

7. **检查是否满足终止条件：**
   - 梯度足够小：$ \| \nabla f(\mathbf{x}_k) \| < \varepsilon $
   - 或者函数值变化很小：$ |f(\mathbf{x}_{k+1}) - f(\mathbf{x}_k)| < \varepsilon $

---

## ✅ 五、具体求解例子：指数曲线拟合

### 1. 已知数据点：

| $ x_i $ | 0 | 1 | 2 | 3 |
|----------|---|----|----|----|
| $ y_i $ | 2 | 5 | 15 | 40 |

我们要拟合模型：
$$
y = a e^{bx}
$$

定义残差函数：
$$
r_i(a, b) = y_i - a e^{b x_i}
$$

设：
$$
\mathbf{x} = \begin{bmatrix} a \\ b \end{bmatrix}, \quad
\mathbf{r}(\mathbf{x}) = \begin{bmatrix}
y_1 - a e^{b x_1} \\
y_2 - a e^{b x_2} \\
y_3 - a e^{b x_3} \\
y_4 - a e^{b x_4}
\end{bmatrix}
$$

### 2. 雅可比矩阵：

$$
J =
\begin{bmatrix}
-e^{b x_1} & -a x_1 e^{b x_1} \\
-e^{b x_2} & -a x_2 e^{b x_2} \\
-e^{b x_3} & -a x_3 e^{b x_3} \\
-e^{b x_4} & -a x_4 e^{b x_4}
\end{bmatrix}
$$

### 3. 初始猜测：

设初始参数：
$$
\mathbf{x}_0 = \begin{bmatrix} a_0 \\ b_0 \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}
$$

### 4. 第一次迭代：

- 计算残差：
  $$
  \mathbf{r}_0 = \begin{bmatrix}
  2 - 1 \cdot e^{0} = 1 \\
  5 - 1 \cdot e^{1} \approx 5 - 2.718 = 2.282 \\
  15 - 1 \cdot e^{2} \approx 15 - 7.389 = 7.611 \\
  40 - 1 \cdot e^{3} \approx 40 - 20.085 = 19.915
  \end{bmatrix}
  $$

- 雅可比矩阵（带入 $ a=1, b=1 $）：
  $$
  J_0 =
  \begin{bmatrix}
  -1 & 0 \\
  -e^1 & -1 \cdot 1 \cdot e^1 \\
  -e^2 & -1 \cdot 2 \cdot e^2 \\
  -e^3 & -1 \cdot 3 \cdot e^3
  \end{bmatrix}
  \approx
  \begin{bmatrix}
  -1 & 0 \\
  -2.718 & -2.718 \\
  -7.389 & -14.778 \\
  -20.085 & -60.255
  \end{bmatrix}
  $$

- 计算搜索方向：
  $$
  \mathbf{p}_0 = - (J_0^T J_0)^{-1} J_0^T \mathbf{r}_0
  $$

- 假设解出 $ \mathbf{p}_0 = \begin{bmatrix} 0.5 \\ 0.3 \end{bmatrix} $

- 更新参数：
  $$
  \mathbf{x}_1 = \mathbf{x}_0 + \alpha \mathbf{p}_0
  $$

选择合适步长 $ \alpha = 1 $，得到：

$$
\mathbf{x}_1 = \begin{bmatrix} 1.5 \\ 1.3 \end{bmatrix}
$$

重复上述过程，直到收敛。

---

## 📝 六、总结

| 内容 | 说明 |
|------|------|
| 基本思想 | 忽略 Hessian 中的二阶项，用 $ J^T J $ 近似 Hessian |
| 核心公式 | $ \mathbf{p}_k = - (J_k^T J_k)^{-1} J_k^T \mathbf{r}_k $ |
| 收敛速度 | 接近极小点时为二阶 |
| 优点 | 实现简单、不需要二阶导数 |
| 缺点 | 对初始点敏感、可能出现数值不稳定 |
| 应用场景 | 曲线拟合、参数估计、机器学习等最小二乘问题 |

---

如果你希望我帮你用 Python 实现该算法，并可视化拟合过程，也可以告诉我。欢迎继续提问！
