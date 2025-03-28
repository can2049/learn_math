### 引言

最小二乘法（Least Squares Method）是一种数学优化技术，它通过最小化误差的平方和来寻找数据的最佳函数匹配。在统计学和机器学习中，最小二乘法广泛应用于线性回归问题。本文将详细推导最小二乘法的矩阵表示，并展开各个公式的详细步骤。

### 问题描述

假设我们有一组观测数据 $(x_1, y_1), (x_2, y_2), \ldots, (x_n, y_n)$，我们希望找到一个线性模型 $y = \beta_0 + \beta_1 x$ 来拟合这些数据。在矩阵表示中，可以扩展到多个自变量的情况，即：

$$
\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}
$$

其中：
- $\mathbf{y}$ 是一个 $n \times 1$ 的观测值向量，
- $\mathbf{X}$ 是一个 $n \times (p+1)$ 的设计矩阵（包括截距项），
- $\boldsymbol{\beta}$ 是一个 $(p+1) \times 1$ 的参数向量，
- $\boldsymbol{\epsilon}$ 是一个 $n \times 1$ 的误差向量。

我们的目标是通过最小化残差平方和来估计参数 $\boldsymbol{\beta}$。

### 残差平方和

残差（误差）向量为：

$$
\boldsymbol{\epsilon} = \mathbf{y} - \mathbf{X}\boldsymbol{\beta}
$$

残差平方和（RSS）为：

$$
\text{RSS} = \boldsymbol{\epsilon}^T \boldsymbol{\epsilon} = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})
$$

### 展开残差平方和

让我们展开 RSS：

$$
\begin{align*}
\text{RSS} &= (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) \\
&= \mathbf{y}^T\mathbf{y} - \mathbf{y}^T\mathbf{X}\boldsymbol{\beta} - \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{y} + \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{X}\boldsymbol{\beta}
\end{align*}
$$

注意到 $\mathbf{y}^T\mathbf{X}\boldsymbol{\beta}$ 是一个标量（因为结果是 $1 \times 1$ 的矩阵），而标量的转置等于自身，即：

$$
\mathbf{y}^T\mathbf{X}\boldsymbol{\beta} = (\mathbf{y}^T\mathbf{X}\boldsymbol{\beta})^T = \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{y}
$$

因此，RSS 可以简化为：

$$
\text{RSS} = \mathbf{y}^T\mathbf{y} - 2\boldsymbol{\beta}^T\mathbf{X}^T\mathbf{y} + \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{X}\boldsymbol{\beta}
$$

### 最小化 RSS

为了找到 $\boldsymbol{\beta}$ 的最小值，我们对 RSS 关于 $\boldsymbol{\beta}$ 求导，并令导数等于零。

首先，回顾一些矩阵微分的规则：

1. $\frac{\partial \mathbf{a}^T\boldsymbol{\beta}}{\partial \boldsymbol{\beta}} = \mathbf{a}$
2. $\frac{\partial \boldsymbol{\beta}^T\mathbf{A}\boldsymbol{\beta}}{\partial \boldsymbol{\beta}} = (\mathbf{A} + \mathbf{A}^T)\boldsymbol{\beta}$ （如果 $\mathbf{A}$ 对称，则为 $2\mathbf{A}\boldsymbol{\beta}$）

在我们的情况下，$\mathbf{X}^T\mathbf{X}$ 是对称的，因为 $(\mathbf{X}^T\mathbf{X})^T = \mathbf{X}^T\mathbf{X}$。

因此，对 RSS 关于 $\boldsymbol{\beta}$ 求导：

$$
\begin{align*}
\frac{\partial \text{RSS}}{\partial \boldsymbol{\beta}} &= \frac{\partial}{\partial \boldsymbol{\beta}} \left( \mathbf{y}^T\mathbf{y} - 2\boldsymbol{\beta}^T\mathbf{X}^T\mathbf{y} + \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{X}\boldsymbol{\beta} \right) \\
&= 0 - 2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\boldsymbol{\beta}
\end{align*}
$$

令导数等于零：

$$
-2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = 0 \\
\Rightarrow \mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = \mathbf{X}^T\mathbf{y}
$$

### 正规方程

上述方程称为正规方程（Normal Equation）：

$$
\mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = \mathbf{X}^T\mathbf{y}
$$

如果 $\mathbf{X}^T\mathbf{X}$ 是可逆的（即满秩），则我们可以解出 $\boldsymbol{\beta}$：

$$
\boldsymbol{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$

### 步骤总结

1. **模型表示**：$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$
2. **残差平方和**：$\text{RSS} = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})$
3. **展开 RSS**：$\text{RSS} = \mathbf{y}^T\mathbf{y} - 2\boldsymbol{\beta}^T\mathbf{X}^T\mathbf{y} + \boldsymbol{\beta}^T\mathbf{X}^T\mathbf{X}\boldsymbol{\beta}$
4. **对 $\boldsymbol{\beta}$ 求导**：$\frac{\partial \text{RSS}}{\partial \boldsymbol{\beta}} = -2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\boldsymbol{\beta}$
5. **令导数为零**：$-2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = 0 \Rightarrow \mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = \mathbf{X}^T\mathbf{y}$
6. **求解 $\boldsymbol{\beta}$**：$\boldsymbol{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$

### 示例验证

为了验证我们的推导，考虑一个简单的线性回归例子：

假设有以下数据点：
$(1, 1), (2, 2), (3, 2)$

模型：$y = \beta_0 + \beta_1 x$

设计矩阵 $\mathbf{X}$ 和观测向量 $\mathbf{y}$：

$$
\mathbf{X} = \begin{bmatrix}
1 & 1 \\
1 & 2 \\
1 & 3 \\
\end{bmatrix}, \quad
\mathbf{y} = \begin{bmatrix}
1 \\
2 \\
2 \\
\end{bmatrix}
$$

计算 $\mathbf{X}^T\mathbf{X}$ 和 $\mathbf{X}^T\mathbf{y}$：

$$
\mathbf{X}^T\mathbf{X} = \begin{bmatrix}
1 & 1 & 1 \\
1 & 2 & 3 \\
\end{bmatrix}
\begin{bmatrix}
1 & 1 \\
1 & 2 \\
1 & 3 \\
\end{bmatrix} =
\begin{bmatrix}
3 & 6 \\
6 & 14 \\
\end{bmatrix}
$$

$$
\mathbf{X}^T\mathbf{y} = \begin{bmatrix}
1 & 1 & 1 \\
1 & 2 & 3 \\
\end{bmatrix}
\begin{bmatrix}
1 \\
2 \\
2 \\
\end{bmatrix} =
\begin{bmatrix}
5 \\
11 \\
\end{bmatrix}
$$

解正规方程：

$$
\begin{bmatrix}
3 & 6 \\
6 & 14 \\
\end{bmatrix}
\begin{bmatrix}
\beta_0 \\
\beta_1 \\
\end{bmatrix} =
\begin{bmatrix}
5 \\
11 \\
\end{bmatrix}
$$

计算 $(\mathbf{X}^T\mathbf{X})^{-1}$：

行列式 $= 3 \times 14 - 6 \times 6 = 42 - 36 = 6$

逆矩阵：

$$
(\mathbf{X}^T\mathbf{X})^{-1} = \frac{1}{6} \begin{bmatrix}
14 & -6 \\
-6 & 3 \\
\end{bmatrix} =
\begin{bmatrix}
\frac{14}{6} & -1 \\
-1 & \frac{3}{6} \\
\end{bmatrix} =
\begin{bmatrix}
\frac{7}{3} & -1 \\
-1 & \frac{1}{2} \\
\end{bmatrix}
$$

因此：

$$
\begin{bmatrix}
\beta_0 \\
\beta_1 \\
\end{bmatrix} =
\begin{bmatrix}
\frac{7}{3} & -1 \\
-1 & \frac{1}{2} \\
\end{bmatrix}
\begin{bmatrix}
5 \\
11 \\
\end{bmatrix} =
\begin{bmatrix}
\frac{35}{3} - 11 \\
-5 + \frac{11}{2} \\
\end{bmatrix} =
\begin{bmatrix}
\frac{35}{3} - \frac{33}{3} \\
-\frac{10}{2} + \frac{11}{2} \\
\end{bmatrix} =
\begin{bmatrix}
\frac{2}{3} \\
\frac{1}{2} \\
\end{bmatrix}
$$

所以，最佳拟合直线为：

$$
y = \frac{2}{3} + \frac{1}{2}x
$$

### 几何解释

从几何上看，最小二乘法的解是在 $\mathbf{X}$ 的列空间中找到 $\mathbf{y}$ 的投影。$\mathbf{X}\boldsymbol{\beta}$ 是 $\mathbf{y}$ 在 $\mathbf{X}$ 列空间上的投影，残差 $\boldsymbol{\epsilon} = \mathbf{y} - \mathbf{X}\boldsymbol{\beta}$ 与 $\mathbf{X}$ 的列空间正交，即：

$$
\mathbf{X}^T \boldsymbol{\epsilon} = 0 \\
\Rightarrow \mathbf{X}^T (\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) = 0 \\
\Rightarrow \mathbf{X}^T\mathbf{y} - \mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = 0 \\
\Rightarrow \mathbf{X}^T\mathbf{X}\boldsymbol{\beta} = \mathbf{X}^T\mathbf{y}
$$

这与我们之前得到的正规方程一致。

### 多元线性回归的推广

对于多元线性回归，即 $y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_p x_p$，设计矩阵 $\mathbf{X}$ 的形式为：

$$
\mathbf{X} = \begin{bmatrix}
1 & x_{11} & x_{12} & \cdots & x_{1p} \\
1 & x_{21} & x_{22} & \cdots & x_{2p} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_{n1} & x_{n2} & \cdots & x_{np} \\
\end{bmatrix}
$$

参数向量 $\boldsymbol{\beta}$ 和观测向量 $\mathbf{y}$ 的形式不变。最小二乘解仍然为：

$$
\boldsymbol{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$

### 假设和性质

1. **$\mathbf{X}$ 满列秩**：$\mathbf{X}^T\mathbf{X}$ 可逆的前提是 $\mathbf{X}$ 是满列秩的，即 $\text{rank}(\mathbf{X}) = p + 1$。如果 $\mathbf{X}$ 不是满列秩（存在多重共线性），则 $\mathbf{X}^T\mathbf{X}$ 不可逆，需要使用广义逆或其他方法。

2. **无偏性**：在经典线性回归假设下（如误差均值为零，同方差，无自相关等），最小二乘估计量是无偏的。

3. **方差**：$\text{Var}(\hat{\boldsymbol{\beta}}) = \sigma^2 (\mathbf{X}^T\mathbf{X})^{-1}$，其中 $\sigma^2$ 是误差的方差。

### 结论

通过上述详细的推导，我们得到了最小二乘法的矩阵表示：

$$
\boldsymbol{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$

这一公式不仅适用于简单线性回归，也适用于多元线性回归。关键在于构造设计矩阵 $\mathbf{X}$ 和观测向量 $\mathbf{y}$，然后通过矩阵运算求解参数估计。
