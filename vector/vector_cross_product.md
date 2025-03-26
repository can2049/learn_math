### **向量叉积（Cross Product）的定义**
向量叉积（又称**向量积**或**外积**）是三维空间中两个向量的一种二元运算，其结果是一个**新的向量**，而不是标量（与点积不同）。叉积仅适用于 **ℝ³**（三维空间），在更高维度需要推广到**外代数**或**楔积**。

给定两个三维向量：

$$
\mathbf{u} = \begin{bmatrix} u_x \\ u_y \\ u_z \end{bmatrix}, \quad \mathbf{v} = \begin{bmatrix} v_x \\ v_y \\ v_z \end{bmatrix}
$$

它们的叉积定义为：

$$
\mathbf{u} \times \mathbf{v} = \begin{bmatrix} u_y v_z - u_z v_y \\ u_z v_x - u_x v_z \\ u_x v_y - u_y v_x \end{bmatrix}
$$

或者用行列式表示：

$$
\mathbf{u} \times \mathbf{v} = \begin{vmatrix}
\mathbf{i} & \mathbf{j} & \mathbf{k} \\
u_x & u_y & u_z \\
v_x & v_y & v_z \\
\end{vmatrix}
$$

其中 **i, j, k** 是标准单位基向量。

---

## **1. 叉积的几何性质**
### **(1) 方向：右手定则**
- 叉积结果 **$\mathbf{u} \times \mathbf{v}$** 是一个垂直于 **$\mathbf{u}$** 和 **$\mathbf{v}$** 的向量。
- 方向由**右手定则**确定：
  - 右手四指从 **$\mathbf{u}$** 转向 **$\mathbf{v}$**，大拇指指向 **$\mathbf{u} \times \mathbf{v}$** 的方向。
- 如果 **$\mathbf{u}$** 和 **$\mathbf{v}$** 平行或反平行，叉积为零向量。

### **(2) 模长（大小）**

$$
\|\mathbf{u} \times \mathbf{v}\| = \|\mathbf{u}\| \|\mathbf{v}\| \sin \theta
$$

其中：
-  $\theta$  是 **$\mathbf{u}$** 和 **$\mathbf{v}$** 的夹角。
- 几何意义：叉积的模等于 **$\mathbf{u}$** 和 **$\mathbf{v}$** 张成的**平行四边形的面积**。

### **(3) 正交性**

$$
\mathbf{u} \times \mathbf{v} \perp \mathbf{u} \quad \text{且} \quad \mathbf{u} \times \mathbf{v} \perp \mathbf{v}
$$

即，叉积结果与两个输入向量都垂直。

---

## **2. 代数性质**
### **(1) 反交换律（不满足交换律）**

$$
\mathbf{u} \times \mathbf{v} = - (\mathbf{v} \times \mathbf{u})
$$

因此，叉积**不满足交换律**，交换顺序会改变方向。

### **(2) 分配律**

$$
\mathbf{u} \times (\mathbf{v} + \mathbf{w}) = \mathbf{u} \times \mathbf{v} + \mathbf{u} \times \mathbf{w}
$$


### **(3) 结合律（标量乘法）**

$$
(k \mathbf{u}) \times \mathbf{v} = k (\mathbf{u} \times \mathbf{v}) = \mathbf{u} \times (k \mathbf{v})
$$

其中  $k$  是标量。

### **(4) 零向量**

$$
\mathbf{u} \times \mathbf{0} = \mathbf{0}
$$


### **(5) 自叉积**

$$
\mathbf{u} \times \mathbf{u} = \mathbf{0}
$$

因为  $\sin 0° = 0$ 。

### **(6) 拉格朗日恒等式**

$$
\|\mathbf{u} \times \mathbf{v}\|^2 + (\mathbf{u} \cdot \mathbf{v})^2 = \|\mathbf{u}\|^2 \|\mathbf{v}\|^2
$$


---

## **3. 叉积的应用**
### **(1) 计算法向量**
- 在计算机图形学中，叉积用于计算**三角形或多边形的法向量**（用于光照计算）。
- 例如，给定三角形三个顶点  $A, B, C$ ，法向量：

$$
  \mathbf{n} = (B - A) \times (C - A)
  $$

  然后归一化  $\hat{\mathbf{n}} = \frac{\mathbf{n}}{\|\mathbf{n}\|}$ 。

### **(2) 计算面积**
- 两个向量 **$\mathbf{u}$** 和 **$\mathbf{v}$** 张成的**平行四边形面积**：

$$
  A = \|\mathbf{u} \times \mathbf{v}\|
  $$

- **三角形面积**是其一半：

$$
  A_{\triangle} = \frac{1}{2} \|\mathbf{u} \times \mathbf{v}\|
  $$


### **(3) 判断向量方向**
- 叉积可用于判断两个向量的**相对方向**（顺时针/逆时针）：
  - 在 2D 中（虽然严格来说 2D 没有叉积，但可以扩展）：

$$
    \mathbf{u} \times \mathbf{v} = u_x v_y - u_y v_x
    $$

- 如果  $> 0$ ，**$\mathbf{v}$** 在 **$\mathbf{u}$** 的**逆时针**方向。
- 如果  $< 0$ ，**$\mathbf{v}$** 在 **$\mathbf{u}$** 的**顺时针**方向。
- 如果  $= 0$ ，两向量共线。

### **(4) 物理学中的力矩**
- 力矩（扭矩） $\mathbf{\tau}$  是位置向量 **$\mathbf{r}$** 和力 **$\mathbf{F}$** 的叉积：

$$
  \mathbf{\tau} = \mathbf{r} \times \mathbf{F}
  $$

  方向表示旋转方向（右手定则）。

### **(5) 电磁学中的洛伦兹力**
- 带电粒子在磁场中的受力：

$$
  \mathbf{F} = q (\mathbf{v} \times \mathbf{B})
  $$

  其中：
  -  $q$  是电荷，
  -  $\mathbf{v}$  是速度，
  -  $\mathbf{B}$  是磁场。

### **(6) 计算旋转轴**
- 在 3D 旋转中，叉积可用于计算**旋转轴**。例如，给定两个方向向量 **$\mathbf{u}$** 和 **$\mathbf{v}$**，旋转轴是它们的叉积：

$$
  \mathbf{axis} = \mathbf{u} \times \mathbf{v}
  $$


---

## **4. 叉积的特殊情况**
### **(1) 标准基向量的叉积**

$$
\begin{aligned}
\mathbf{i} \times \mathbf{j} &= \mathbf{k}, \\
\mathbf{j} \times \mathbf{k} &= \mathbf{i}, \\
\mathbf{k} \times \mathbf{i} &= \mathbf{j}, \\
\mathbf{i} \times \mathbf{i} &= \mathbf{0}, \quad \text{（同理 } \mathbf{j} \times \mathbf{j} = \mathbf{0}, \mathbf{k} \times \mathbf{k} = \mathbf{0} \text{）}
\end{aligned}
$$


### **(2) 平行向量的叉积**
如果 **$\mathbf{u}$** 和 **$\mathbf{v}$** 平行（即  $\theta = 0°$  或  $180°$ ），则：

$$
\mathbf{u} \times \mathbf{v} = \mathbf{0}
$$


---

## **5. 叉积 vs. 点积**
| 性质          | 点积（Dot Product） | 叉积（Cross Product） |
|-------------|----------------|----------------|
| **结果类型**   | 标量（Scalar）   | 向量（Vector）   |
| **计算方式**   |  $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos \theta$  |  $\mathbf{u} \times \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \sin \theta \cdot \hat{\mathbf{n}}$  |
| **交换律**    | 满足（ $\mathbf{u} \cdot \mathbf{v} = \mathbf{v} \cdot \mathbf{u}$ ） | 不满足（ $\mathbf{u} \times \mathbf{v} = - \mathbf{v} \times \mathbf{u}$ ） |
| **正交性**    | 点积为零表示正交 | 叉积为零表示平行 |
| **几何意义**  | 投影、夹角计算 | 面积、旋转方向 |

---

## **6. 总结**
- **叉积**适用于 **3D 向量**，结果是**垂直于输入向量的新向量**。
- **几何意义**：叉积的模等于**平行四边形的面积**，方向由**右手定则**决定。
- **应用**：
  - 计算法向量（计算机图形学）。
  - 计算面积（平行四边形、三角形）。
  - 判断方向（2D/3D）。
  - 物理学中的力矩和电磁学中的洛伦兹力。
- **与点积的区别**：
  - 点积是**标量**，用于计算投影、夹角。
  - 叉积是**向量**，用于计算垂直方向、面积、旋转。

理解叉积的性质和应用，对于**计算机图形学、物理学、机器人学**等领域至关重要！
