### 拉格朗日恒等式的详细推导

**拉格朗日恒等式** （Lagrange's Identity）在向量代数中表述为：

$$
(\mathbf{a} \cdot \mathbf{b})^2 + \|\mathbf{a} \times \mathbf{b}\|^2 = \|\mathbf{a}\|^2 \|\mathbf{b}\|^2
$$

其中， $\mathbf{a}$  和  $\mathbf{b}$  是三维空间中的向量， $\cdot$  表示点积， $\times$  表示叉积， $\|\cdot\|$  表示向量的模。

以下从代数角度逐步推导该恒等式。

---

#### **步骤 1：展开叉积的模平方**
设三维向量  $\mathbf{a} = [a_x, a_y, a_z]$  和  $\mathbf{b} = [b_x, b_y, b_z]$ ，叉积定义为：

$$
\mathbf{a} \times \mathbf{b} = \begin{bmatrix} a_y b_z - a_z b_y \\ a_z b_x - a_x b_z \\ a_x b_y - a_y b_x \end{bmatrix}
$$

叉积的模平方为：

$$
\|\mathbf{a} \times \mathbf{b}\|^2 = (a_y b_z - a_z b_y)^2 + (a_z b_x - a_x b_z)^2 + (a_x b_y - a_y b_x)^2
$$


**展开每一项：**
1. **第一项**：

$$
   (a_y b_z - a_z b_y)^2 = a_y^2 b_z^2 + a_z^2 b_y^2 - 2 a_y a_z b_y b_z
   $$

2. **第二项**：

$$
   (a_z b_x - a_x b_z)^2 = a_z^2 b_x^2 + a_x^2 b_z^2 - 2 a_z a_x b_x b_z
   $$

3. **第三项**：

$$
   (a_x b_y - a_y b_x)^2 = a_x^2 b_y^2 + a_y^2 b_x^2 - 2 a_x a_y b_x b_y
   $$


**合并后叉积模平方：**

$$
\|\mathbf{a} \times \mathbf{b}\|^2 = \sum_{\text{循环}} \left( a_i^2 b_j^2 + a_j^2 b_i^2 - 2 a_i a_j b_i b_j \right)
$$

其中  $i, j$  循环取  $(y,z), (z,x), (x,y)$ 。

---

#### **步骤 2：展开点积的平方**
点积  $\mathbf{a} \cdot \mathbf{b}$  定义为：

$$
\mathbf{a} \cdot \mathbf{b} = a_x b_x + a_y b_y + a_z b_z
$$

其平方为：

$$
(\mathbf{a} \cdot \mathbf{b})^2 = (a_x b_x + a_y b_y + a_z b_z)^2 = a_x^2 b_x^2 + a_y^2 b_y^2 + a_z^2 b_z^2 + 2(a_x a_y b_x b_y + a_x a_z b_x b_z + a_y a_z b_y b_z)
$$


---

#### **步骤 3：将叉积模平方与点积平方相加**
将  $\|\mathbf{a} \times \mathbf{b}\|^2$  和  $(\mathbf{a} \cdot \mathbf{b})^2$  相加：


$$
\|\mathbf{a} \times \mathbf{b}\|^2 + (\mathbf{a} \cdot \mathbf{b})^2 = \left[ \sum_{\text{循环}} (a_i^2 b_j^2 + a_j^2 b_i^2 - 2 a_i a_j b_i b_j) \right] + \left[ a_x^2 b_x^2 + a_y^2 b_y^2 + a_z^2 b_z^2 + 2(a_x a_y b_x b_y + a_x a_z b_x b_z + a_y a_z b_y b_z) \right]
$$


**展开叉积部分的求和：**

$$
\sum_{\text{循环}} (a_i^2 b_j^2 + a_j^2 b_i^2) = a_y^2 b_z^2 + a_z^2 b_y^2 + a_z^2 b_x^2 + a_x^2 b_z^2 + a_x^2 b_y^2 + a_y^2 b_x^2
$$


$$
\sum_{\text{循环}} (-2 a_i a_j b_i b_j) = -2(a_y a_z b_y b_z + a_z a_x b_z b_x + a_x a_y b_x b_y)
$$


**合并所有项：**

$$
\begin{aligned}
&\|\mathbf{a} \times \mathbf{b}\|^2 + (\mathbf{a} \cdot \mathbf{b})^2 \\
&= \left[ a_y^2 b_z^2 + a_z^2 b_y^2 + a_z^2 b_x^2 + a_x^2 b_z^2 + a_x^2 b_y^2 + a_y^2 b_x^2 \right] \\
&\quad + \left[ a_x^2 b_x^2 + a_y^2 b_y^2 + a_z^2 b_z^2 \right] \\
&\quad - 2(a_y a_z b_y b_z + a_z a_x b_z b_x + a_x a_y b_x b_y) \\
&\quad + 2(a_x a_y b_x b_y + a_x a_z b_x b_z + a_y a_z b_y b_z) \\
\end{aligned}
$$


**观察交叉项的抵消：**
- 第三行的负交叉项与第四行的正交叉项完全抵消：

$$
  -2(\cdots) + 2(\cdots) = 0
  $$


**剩余项为：**

$$
\begin{aligned}
&\left[ a_y^2 b_z^2 + a_z^2 b_y^2 + a_z^2 b_x^2 + a_x^2 b_z^2 + a_x^2 b_y^2 + a_y^2 b_x^2 \right] + \left[ a_x^2 b_x^2 + a_y^2 b_y^2 + a_z^2 b_z^2 \right] \\
&= a_x^2 b_x^2 + a_y^2 b_y^2 + a_z^2 b_z^2 + a_x^2 b_y^2 + a_x^2 b_z^2 + a_y^2 b_x^2 + a_y^2 b_z^2 + a_z^2 b_x^2 + a_z^2 b_y^2 \\
\end{aligned}
$$


**整理成平方和形式：**

$$
= a_x^2 (b_x^2 + b_y^2 + b_z^2) + a_y^2 (b_x^2 + b_y^2 + b_z^2) + a_z^2 (b_x^2 + b_y^2 + b_z^2)
$$


$$
= (a_x^2 + a_y^2 + a_z^2)(b_x^2 + b_y^2 + b_z^2)
$$


$$
= \|\mathbf{a}\|^2 \|\mathbf{b}\|^2
$$


---

#### **步骤 4：总结**
通过展开叉积模平方和点积平方，并合并同类项后，所有交叉项相互抵消，剩余部分正好是两向量模长平方的乘积，即：

$$
\|\mathbf{a} \times \mathbf{b}\|^2 + (\mathbf{a} \cdot \mathbf{b})^2 = \|\mathbf{a}\|^2 \|\mathbf{b}\|^2
$$






### 几何含义
1. **点积与夹角的关系**：
   - 点积  $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\| \|\mathbf{b}\| \cos \theta$  反映了两个向量的平行程度（ $\theta$  为它们的夹角）。
   - 叉积的模  $\|\mathbf{a} \times \mathbf{b}\| = \|\mathbf{a}\| \|\mathbf{b}\| \sin \theta$  则反映了垂直程度。

2. **恒等式的几何解释**：
   将点积和叉积的表达式代入拉格朗日恒等式，得到：

$$
   (\|\mathbf{a}\| \|\mathbf{b}\| \cos \theta)^2 + (\|\mathbf{a}\| \|\mathbf{b}\| \sin \theta)^2 = \|\mathbf{a}\|^2 \|\mathbf{b}\|^2
   $$

   化简后即为三角恒等式：

$$
   \cos^2 \theta + \sin^2 \theta = 1
   $$

   因此，拉格朗日恒等式本质上是 **三角恒等式在向量运算中的体现**，表明两个向量的平行分量和垂直分量的平方和等于它们模的平方积。

3. **几何意义总结**：
   - 恒等式说明，无论两个向量的夹角如何，它们的“平行贡献”（点积）和“垂直贡献”（叉积）的组合始终满足勾股定理。
   - 从几何上看， $\mathbf{a}$  和  $\mathbf{b}$  张成的平行四边形的面积（由叉积决定）与它们投影的重叠程度（由点积决定）共同构成了一个“不变量”，即  $\|\mathbf{a}\|^2 \|\mathbf{b}\|^2$ 。

### 推广与应用
- 在更高维空间或抽象内积空间中，拉格朗日恒等式推广为 **柯西-施瓦茨不等式**（ $\|\mathbf{a} \cdot \mathbf{b}\| \leq \|\mathbf{a}\| \|\mathbf{b}\|$ ），其几何意义仍然是向量投影关系的体现。
- 在物理学中，这一恒等式可用于分析力的分解或电磁场中场的正交性。

简而言之，拉格朗日恒等式揭示了向量的“平行”与“垂直”分量的内在平衡关系，是勾股定理在向量空间中的自然延伸。
