奇异值分解（Singular Value Decomposition, SVD）是矩阵分解中非常重要的一种工具，它可以将任意  $m \times n$  矩阵  $A$  分解为三个矩阵的乘积，即


$$
A = U \Sigma V^T,
$$


其中：
-  $U$  是一个  $m \times m$  的正交矩阵（或单位酉矩阵），其列向量被称为左奇异向量；
-  $\Sigma$  是一个  $m \times n$  的对角矩阵（通常写成“伪对角矩阵”），对角元  $\sigma_1, \sigma_2, \ldots, \sigma_r$ （ $r = \operatorname{rank}(A)$ ）非负且按降序排列，这些数称为奇异值；
-  $V$  是一个  $n \times n$  的正交矩阵，其列向量被称为右奇异向量。

下面详细推导 SVD 的分解过程，并给出相关的几何意义说明。

---

## 一、推导过程

### 1. 考察矩阵  $A^T A$
由于  $A^T A$  是对称矩阵，且对于任意  $x$  有

$$
x^T A^T A x = (Ax)^T (Ax) = \|Ax\|^2 \ge 0,
$$

因此  $A^T A$  是半正定的。根据谱定理，存在一个正交矩阵  $V$  和一个对角矩阵  $\Lambda$ （对角元为非负数）使得：

$$
A^T A = V \Lambda V^T.
$$

记  $\Lambda = \operatorname{diag}(\lambda_1, \lambda_2, \ldots, \lambda_n)$  且  $\lambda_i \ge 0$ 。定义奇异值为：

$$
\sigma_i = \sqrt{\lambda_i}, \quad i=1,2,\ldots,n.
$$

为了简便，我们假设  $\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_n \ge 0$ 。

### 2. 定义右奇异向量
矩阵  $V$  的列向量  $v_1, v_2, \ldots, v_n$  就是  $A^T A$  的一组正交归一的特征向量。它们满足

$$
A^T A v_i = \lambda_i v_i = \sigma_i^2 v_i.
$$


### 3. 构造左奇异向量
对于非零奇异值  $\sigma_i > 0$ ，定义

$$
u_i = \frac{1}{\sigma_i} A v_i.
$$

验证：

$$
\|u_i\| = \frac{1}{\sigma_i} \|A v_i\| = \frac{1}{\sigma_i} \sqrt{v_i^T A^T A v_i} = \frac{1}{\sigma_i} \sqrt{\sigma_i^2} = 1,
$$

即  $u_i$  为单位向量。同时，利用  $A v_i = \sigma_i u_i$ ，可以验证  $u_i$  之间的正交性。若  $\sigma_i = 0$ ，我们可以任意选取一组与前面选出的  $u_i$  互相正交的单位向量补全  $U$  的正交基底。

### 4. 表达  $A$  的作用
对于任意向量  $x \in \mathbb{R}^n$ ，可以写成  $x = \sum_{i=1}^n \alpha_i v_i$ 。那么，

$$
A x = A\left(\sum_{i=1}^n \alpha_i v_i\right) = \sum_{i=1}^n \alpha_i A v_i = \sum_{i=1}^r \alpha_i \sigma_i u_i,
$$

其中  $r$  是  $A$  的秩，注意对于  $\sigma_i = 0$  的部分贡献为 0。

### 5. 写成矩阵形式
令
-  $U = \begin{bmatrix} u_1 & u_2 & \cdots & u_m \end{bmatrix}$ （其中前  $r$  列由上式定义，剩余的列补全正交基）；
-  $\Sigma$  为  $m \times n$  的矩阵，其前  $r$  个对角元为  $\sigma_1, \sigma_2, \ldots, \sigma_r$ ，其他位置为 0；
-  $V = \begin{bmatrix} v_1 & v_2 & \cdots & v_n \end{bmatrix}$ 。

则有

$$
A = U \Sigma V^T.
$$


---

## 二、几何意义

SVD 的几何解释非常直观。考虑  $A$  作为一个从  $\mathbb{R}^n$  映射到  $\mathbb{R}^m$  的线性变换，其作用可以分解为三个几何步骤：

1. **右正交变换  $V^T$**：
   这个变换将原始坐标系中的任意向量  $x$  旋转到一个新的正交坐标系中。由于  $V$  是正交矩阵，其作用仅仅是旋转和反射，不改变向量长度。

2. **缩放变换  $\Sigma$**：
   在新的坐标系中，矩阵  $\Sigma$  对各个坐标方向进行独立的伸缩。奇异值  $\sigma_i$  就是这些伸缩因子。特别地，单位球在这个变换下会变成一个椭球，其半轴长度正是对应的奇异值。

3. **左正交变换  $U$**：
   最后，通过  $U$  的正交变换将椭球进一步旋转到最终的位置。这个变换同样不改变向量的长度。

总的来说，SVD 告诉我们：任意线性变换  $A$  都可以看成是“先旋转—再缩放—再旋转”的过程。也就是说，对于任意向量  $x$ ，其变换过程为：

$$
x \xrightarrow{V^T} \text{旋转后得到 } y \xrightarrow{\Sigma} \text{伸缩后得到 } z \xrightarrow{U} \text{旋转后得到 } A x.
$$


这种分解方式不仅在理论上提供了对矩阵结构的深刻理解，而且在许多实际应用中（如数据降维、噪声过滤、图像压缩、信号处理等）都有重要应用。

---

## 三、小结

- **分解形式**：
  任意矩阵  $A$  都可以分解为  $A = U \Sigma V^T$ ，其中  $U$  和  $V$  分别是左、右正交矩阵， $\Sigma$  包含奇异值。

- **推导过程**：
  利用  $A^T A$  的正定性与谱分解，求出右奇异向量和奇异值，再由  $A v_i = \sigma_i u_i$  得到左奇异向量，进而写出完整的分解。

- **几何意义**：
  SVD 把线性变换看作是“旋转—缩放—旋转”的过程，单位球经由该变换变成椭球，奇异值表示椭球的半轴长度，而正交矩阵  $U$  与  $V$  描述了旋转方向。

这种清晰的结构和直观的几何解释，使得 SVD 成为理解和处理矩阵问题的有力工具。
