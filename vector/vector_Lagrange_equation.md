### 拉格朗日恒等式的详细推导

**拉格朗日恒等式**是向量叉积与点积之间的重要关系，其形式为：

$$
\|\mathbf{u} \times \mathbf{v}\|^2 + (\mathbf{u} \cdot \mathbf{v})^2 = \|\mathbf{u}\|^2 \|\mathbf{v}\|^2
$$

以下从代数角度逐步推导该恒等式。

---

#### **步骤 1：展开叉积的模平方**
设三维向量  $\mathbf{u} = [u_x, u_y, u_z]$  和  $\mathbf{v} = [v_x, v_y, v_z]$ ，叉积定义为：

$$
\mathbf{u} \times \mathbf{v} = \begin{bmatrix} u_y v_z - u_z v_y \\ u_z v_x - u_x v_z \\ u_x v_y - u_y v_x \end{bmatrix}
$$

叉积的模平方为：

$$
\|\mathbf{u} \times \mathbf{v}\|^2 = (u_y v_z - u_z v_y)^2 + (u_z v_x - u_x v_z)^2 + (u_x v_y - u_y v_x)^2
$$


**展开每一项：**
1. **第一项**：

$$
   (u_y v_z - u_z v_y)^2 = u_y^2 v_z^2 + u_z^2 v_y^2 - 2 u_y u_z v_y v_z
   $$

2. **第二项**：

$$
   (u_z v_x - u_x v_z)^2 = u_z^2 v_x^2 + u_x^2 v_z^2 - 2 u_z u_x v_x v_z
   $$

3. **第三项**：

$$
   (u_x v_y - u_y v_x)^2 = u_x^2 v_y^2 + u_y^2 v_x^2 - 2 u_x u_y v_x v_y
   $$


**合并后叉积模平方：**

$$
\|\mathbf{u} \times \mathbf{v}\|^2 = \sum_{\text{循环}} \left( u_i^2 v_j^2 + u_j^2 v_i^2 - 2 u_i u_j v_i v_j \right)
$$

其中  $i, j$  循环取  $(y,z), (z,x), (x,y)$ 。

---

#### **步骤 2：展开点积的平方**
点积  $\mathbf{u} \cdot \mathbf{v}$  定义为：

$$
\mathbf{u} \cdot \mathbf{v} = u_x v_x + u_y v_y + u_z v_z
$$

其平方为：

$$
(\mathbf{u} \cdot \mathbf{v})^2 = (u_x v_x + u_y v_y + u_z v_z)^2 = u_x^2 v_x^2 + u_y^2 v_y^2 + u_z^2 v_z^2 + 2(u_x u_y v_x v_y + u_x u_z v_x v_z + u_y u_z v_y v_z)
$$


---

#### **步骤 3：将叉积模平方与点积平方相加**
将  $\|\mathbf{u} \times \mathbf{v}\|^2$  和  $(\mathbf{u} \cdot \mathbf{v})^2$  相加：


$$
\|\mathbf{u} \times \mathbf{v}\|^2 + (\mathbf{u} \cdot \mathbf{v})^2 = \left[ \sum_{\text{循环}} (u_i^2 v_j^2 + u_j^2 v_i^2 - 2 u_i u_j v_i v_j) \right] + \left[ u_x^2 v_x^2 + u_y^2 v_y^2 + u_z^2 v_z^2 + 2(u_x u_y v_x v_y + u_x u_z v_x v_z + u_y u_z v_y v_z) \right]
$$


**展开叉积部分的求和：**

$$
\sum_{\text{循环}} (u_i^2 v_j^2 + u_j^2 v_i^2) = u_y^2 v_z^2 + u_z^2 v_y^2 + u_z^2 v_x^2 + u_x^2 v_z^2 + u_x^2 v_y^2 + u_y^2 v_x^2
$$


$$
\sum_{\text{循环}} (-2 u_i u_j v_i v_j) = -2(u_y u_z v_y v_z + u_z u_x v_z v_x + u_x u_y v_x v_y)
$$


**合并所有项：**

$$
\begin{aligned}
&\|\mathbf{u} \times \mathbf{v}\|^2 + (\mathbf{u} \cdot \mathbf{v})^2 \\
&= \left[ u_y^2 v_z^2 + u_z^2 v_y^2 + u_z^2 v_x^2 + u_x^2 v_z^2 + u_x^2 v_y^2 + u_y^2 v_x^2 \right] \\
&\quad + \left[ u_x^2 v_x^2 + u_y^2 v_y^2 + u_z^2 v_z^2 \right] \\
&\quad - 2(u_y u_z v_y v_z + u_z u_x v_z v_x + u_x u_y v_x v_y) \\
&\quad + 2(u_x u_y v_x v_y + u_x u_z v_x v_z + u_y u_z v_y v_z) \\
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
&\left[ u_y^2 v_z^2 + u_z^2 v_y^2 + u_z^2 v_x^2 + u_x^2 v_z^2 + u_x^2 v_y^2 + u_y^2 v_x^2 \right] + \left[ u_x^2 v_x^2 + u_y^2 v_y^2 + u_z^2 v_z^2 \right] \\
&= u_x^2 v_x^2 + u_y^2 v_y^2 + u_z^2 v_z^2 + u_x^2 v_y^2 + u_x^2 v_z^2 + u_y^2 v_x^2 + u_y^2 v_z^2 + u_z^2 v_x^2 + u_z^2 v_y^2 \\
\end{aligned}
$$


**整理成平方和形式：**

$$
= u_x^2 (v_x^2 + v_y^2 + v_z^2) + u_y^2 (v_x^2 + v_y^2 + v_z^2) + u_z^2 (v_x^2 + v_y^2 + v_z^2)
$$


$$
= (u_x^2 + u_y^2 + u_z^2)(v_x^2 + v_y^2 + v_z^2)
$$


$$
= \|\mathbf{u}\|^2 \|\mathbf{v}\|^2
$$


---

#### **步骤 4：总结**
通过展开叉积模平方和点积平方，并合并同类项后，所有交叉项相互抵消，剩余部分正好是两向量模长平方的乘积，即：

$$
\|\mathbf{u} \times \mathbf{v}\|^2 + (\mathbf{u} \cdot \mathbf{v})^2 = \|\mathbf{u}\|^2 \|\mathbf{v}\|^2
$$

**证毕。**

---

### **几何解释**
拉格朗日恒等式反映了向量空间中正交分解的思想：
- 若将  $\mathbf{v}$  分解为与  $\mathbf{u}$  平行和垂直的分量，则：

$$
  \|\mathbf{v}\|^2 = \|\text{平行分量}\|^2 + \|\text{垂直分量}\|^2
  $$

- 对应点积和叉积的平方和，体现了勾股定理在向量空间的推广。

### **应用**
该恒等式在物理学和工程学中用于简化涉及向量长度和角度的计算，例如验证向量的正交性或计算旋转系统的能量。
