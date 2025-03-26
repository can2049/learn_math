## 基于四元数的旋转公式推导
下面给出基于四元数的三维空间旋转公式的详细推导过程。设需要旋转的向量为

$$
\mathbf{v} = (v_x, v_y, v_z)
$$

我们将它看作一个纯虚四元数

$$
\mathbf{V} = 0 + v_x \mathbf{i} + v_y \mathbf{j} + v_z \mathbf{k}.
$$


### 1. 构造旋转四元数

设旋转角为  $\theta$ ，旋转轴为单位向量

$$
\mathbf{u} = (u_x, u_y, u_z),
$$

旋转四元数定义为

$$
q = \cos\frac{\theta}{2} + \sin\frac{\theta}{2} \,(u_x \mathbf{i} + u_y \mathbf{j} + u_z \mathbf{k}).
$$


对应的共轭（反四元数）为

$$
q^{-1} = q^* = \cos\frac{\theta}{2} - \sin\frac{\theta}{2} \,(u_x \mathbf{i} + u_y \mathbf{j} + u_z \mathbf{k}).
$$


### 2. 四元数旋转公式

旋转后的向量对应的四元数为

$$
\mathbf{V}' = q\, \mathbf{V}\, q^{-1}.
$$


我们的目标是从这个表达式推导出向量旋转的具体公式。

### 3. 推导过程

记

$$
s = \cos\frac{\theta}{2}, \quad \mathbf{r} = \sin\frac{\theta}{2}\,(u_x, u_y, u_z).
$$

则

$$
q = s + \mathbf{r}, \quad q^{-1} = s - \mathbf{r}.
$$


注意四元数的乘法满足：
- 标量部分和向量部分分别计算，且两个纯虚四元数的乘积与三维向量叉乘有关。
- 对于任意两个四元数  $A = a_0 + \mathbf{a}$  与  $B = b_0 + \mathbf{b}$ ，它们的乘积为

$$
  A B = a_0 b_0 - \mathbf{a} \cdot \mathbf{b} + a_0 \mathbf{b} + b_0 \mathbf{a} + \mathbf{a} \times \mathbf{b}.
  $$


首先计算  $q\,\mathbf{V}$ ：

$$
q\,\mathbf{V} = (s + \mathbf{r})(0 + \mathbf{v}) = s\,\mathbf{v} + \mathbf{r}\,\mathbf{v}.
$$

其中

$$
\mathbf{r}\,\mathbf{v} = -\mathbf{r} \cdot \mathbf{v} + \mathbf{r} \times \mathbf{v}.
$$

因此

$$
q\,\mathbf{V} = s\,\mathbf{v} - (\mathbf{r} \cdot \mathbf{v}) + \mathbf{r} \times \mathbf{v}.
$$

这个结果可以看作一个四元数，其标量部分为

$$
-s_1 = -(\mathbf{r} \cdot \mathbf{v})
$$

（这里注意： $s\,\mathbf{v}$ 没有标量部分，而  $-(\mathbf{r} \cdot \mathbf{v})$ 是标量），而向量部分为

$$
s\,\mathbf{v} + \mathbf{r} \times \mathbf{v}.
$$


接下来将  $q\,\mathbf{V}$  与  $q^{-1} = s - \mathbf{r}$  相乘：

$$
\mathbf{V}' = (q\,\mathbf{V})(s - \mathbf{r}).
$$


我们令  $q\,\mathbf{V} = A_0 + \mathbf{A}$ ，其中

$$
A_0 = -\mathbf{r} \cdot \mathbf{v}, \quad \mathbf{A} = s\,\mathbf{v} + \mathbf{r} \times \mathbf{v}.
$$

则

$$
\mathbf{V}' = (A_0 + \mathbf{A})(s - \mathbf{r}) = A_0 s - A_0\,\mathbf{r} + s\,\mathbf{A} - \mathbf{A}\,\mathbf{r}.
$$


其中，注意  $\mathbf{A}\,\mathbf{r}$  的乘积公式为

$$
\mathbf{A}\,\mathbf{r} = -\mathbf{A}\cdot \mathbf{r} + \mathbf{A} \times \mathbf{r}.
$$


我们只关注最终的虚部（向量部分），经过一些代数整理，利用纯量部分必为0（因为旋转后的四元数是纯虚的），可得：

$$
\mathbf{v}' = \mathbf{v} + 2\,\mathbf{r} \times (s\,\mathbf{v} + \mathbf{r} \times \mathbf{v}).
$$

进一步利用三重积公式：

$$
\mathbf{r} \times (\mathbf{r} \times \mathbf{v}) = \mathbf{r} (\mathbf{r} \cdot \mathbf{v}) - \|\mathbf{r}\|^2\, \mathbf{v},
$$

且注意  $\|\mathbf{r}\|^2 = \sin^2\frac{\theta}{2}$  和  $2s\,\mathbf{r} = 2\cos\frac{\theta}{2}\sin\frac{\theta}{2}$ , 我们可以整理出经典的罗德里格公式形式：

$$
\mathbf{v}' = \mathbf{v}\cos\theta + (\mathbf{u} \times \mathbf{v})\sin\theta + \mathbf{u} (\mathbf{u} \cdot \mathbf{v}) (1 - \cos\theta).
$$


### 4. 结论

综上所述，利用四元数  $q = \cos\frac{\theta}{2} + \sin\frac{\theta}{2}\,(u_x \mathbf{i} + u_y \mathbf{j} + u_z \mathbf{k})$  对纯虚四元数  $\mathbf{V} = 0 + v_x\mathbf{i}+v_y\mathbf{j}+v_z\mathbf{k}$  进行旋转，即

$$
\mathbf{V}' = q\,\mathbf{V}\,q^{-1},
$$

可以推出旋转后的向量为

$$
\mathbf{v}' = \mathbf{v}\cos\theta + (\mathbf{u}\times\mathbf{v})\sin\theta + \mathbf{u}(\mathbf{u}\cdot\mathbf{v})(1-\cos\theta).
$$


这就是基于四元数的三维空间旋转公式的推导过程。
