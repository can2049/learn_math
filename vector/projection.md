## 说明
本文介绍如何得到一个向量在另一个向量上的投影，或者说是平行分量。

## 推导过程

假设有两个向量  $\mathbf{v}$  和  $\mathbf{u}$ （其中  $\mathbf{u}$  非零），我们希望找出  $\mathbf{v}$  在  $\mathbf{u}$  方向上的平行分量，也称为  $\mathbf{v}$  在  $\mathbf{u}$  上的投影。记该平行分量为  $\mathbf{v}_\parallel$ ，它必定是  $\mathbf{u}$  的一个标量倍数，即存在一个标量  $\lambda$  使得


$$
\mathbf{v}_\parallel = \lambda \mathbf{u}.
$$


下面是详细推导步骤：

---

### 1. 投影的几何意义

直观上，投影操作就是将  $\mathbf{v}$  的尾部垂直“落”到  $\mathbf{u}$  的直线上，得到一个新的向量  $\mathbf{v}_\parallel$ ，它与  $\mathbf{u}$  同向。

---

### 2. 正交分解

由于  $\mathbf{v}$  可以分解为在  $\mathbf{u}$  方向上的分量和平面（垂直于  $\mathbf{u}$ ）上的分量，我们有


$$
\mathbf{v} = \mathbf{v}_\parallel + \mathbf{v}_\perp,
$$


其中  $\mathbf{v}_\parallel = \lambda \mathbf{u}$  为平行分量，而  $\mathbf{v}_\perp$  为垂直分量，其特点是和  $\mathbf{u}$  正交，即


$$
\mathbf{v}_\perp \cdot \mathbf{u} = 0.
$$


---

### 3. 利用正交条件确定  $\lambda$

由分解式，两边同时与  $\mathbf{u}$  点乘，有


$$
\mathbf{v} \cdot \mathbf{u} = (\mathbf{v}_\parallel + \mathbf{v}_\perp) \cdot \mathbf{u}.
$$


利用正交性条件  $\mathbf{v}_\perp \cdot \mathbf{u} = 0$ ，可得


$$
\mathbf{v} \cdot \mathbf{u} = \mathbf{v}_\parallel \cdot \mathbf{u}.
$$


又因为  $\mathbf{v}_\parallel = \lambda \mathbf{u}$ ，所以


$$
\mathbf{v}_\parallel \cdot \mathbf{u} = (\lambda \mathbf{u}) \cdot \mathbf{u} = \lambda (\mathbf{u} \cdot \mathbf{u}).
$$


因此


$$
\mathbf{v} \cdot \mathbf{u} = \lambda (\mathbf{u} \cdot \mathbf{u}).
$$


解得


$$
\lambda = \frac{\mathbf{v} \cdot \mathbf{u}}{\mathbf{u} \cdot \mathbf{u}}.
$$


---

### 4. 得到平行分量

将  $\lambda$  代入  $\mathbf{v}_\parallel = \lambda \mathbf{u}$  得到


$$
\boxed{\mathbf{v}_\parallel = \frac{\mathbf{v} \cdot \mathbf{u}}{\mathbf{u} \cdot \mathbf{u}} \, \mathbf{u}}.
$$


如果  $\mathbf{u}$  是单位向量（即  $\|\mathbf{u}\|=1$ ），那么  $\mathbf{u} \cdot \mathbf{u}=1$ ，公式就简化为


$$
\boxed{\mathbf{v}_\parallel = (\mathbf{v} \cdot \mathbf{u}) \, \mathbf{u}}.
$$


---

### 5. 小结

整个推导的关键在于：
- 假设平行分量为  $\lambda \mathbf{u}$ ；
- 利用正交分解的性质： $\mathbf{v} = \lambda \mathbf{u} + \mathbf{v}_\perp$ ，其中  $\mathbf{v}_\perp \cdot \mathbf{u} = 0$ ；
- 通过点乘消去垂直分量，求出  $\lambda$ 。

最终得到了  $\mathbf{v}$  在  $\mathbf{u}$  上的投影公式，即


$$
\mathbf{v}_\parallel = \frac{\mathbf{v} \cdot \mathbf{u}}{\mathbf{u} \cdot \mathbf{u}} \, \mathbf{u}.
$$


这种投影公式在工程、物理、计算机图形学等领域中都有广泛应用。
