## 说明

罗德里格斯公式是一种用于描述三维旋转的数学公式。它基于向量的分解和旋转的基本原理，用于将一个向量绕一个旋转轴旋转一定的角度。


下面给出罗德里格斯公式的详细推导过程。假设我们有一个三维向量 **v**，以及一个单位旋转轴 **k**（满足 ‖**k**‖ = 1），我们希望将 **v** 绕 **k** 旋转一个角度 θ，得到旋转后的向量 **v′**。最终结果是


$$
\mathbf{v}' = \mathbf{v} \cos\theta + (\mathbf{k} \times \mathbf{v}) \sin\theta + \mathbf{k} (\mathbf{k} \cdot \mathbf{v}) (1-\cos\theta).
$$


下面详细推导这一公式的关键步骤：

---

### 1. 分解向量

任意向量 **v** 可分解为平行于旋转轴 **k** 的分量和垂直于 **k** 的分量。记：

- 平行分量：

$$
  \mathbf{v}_\parallel = (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k}.
  $$


- 垂直分量：

$$
  \mathbf{v}_\perp = \mathbf{v} - \mathbf{v}_\parallel = \mathbf{v} - (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k}.
  $$


注意：旋转时平行分量保持不变，而垂直分量将在平面内旋转。

---

### 2. 在垂直平面内旋转

令垂直分量 **v⊥** 在以 **k** 为法向量的平面内旋转。由于 **v⊥** 与 **k** 垂直，可以在此平面内构造一个正交基。令

- 第一基向量：

$$
  \mathbf{u} = \frac{\mathbf{v}_\perp}{\|\mathbf{v}_\perp\|}.
  $$


- 第二基向量：

$$
  \mathbf{w} = \mathbf{k} \times \mathbf{u}.
  $$


在该正交平面中，**v⊥** 的旋转可以写成：

$$
\mathbf{v}_\perp' = \mathbf{v}_\perp \cos\theta + (\mathbf{k} \times \mathbf{v}_\perp) \sin\theta.
$$

这里利用了二维旋转公式，注意到  $\mathbf{k} \times \mathbf{v}_\perp = \|\mathbf{v}_\perp\| \, \mathbf{w}$ 。

---

### 3. 整体旋转的组合

由于平行分量不变，旋转后的向量为：

$$
\mathbf{v}' = \mathbf{v}_\parallel + \mathbf{v}_\perp'.
$$

将上面表达式代入：

$$
\mathbf{v}' = (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k} + \left[\mathbf{v}_\perp \cos\theta + (\mathbf{k} \times \mathbf{v}_\perp) \sin\theta\right].
$$


---

### 4. 进一步简化

首先注意到：
-  $\mathbf{v}_\perp = \mathbf{v} - (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k}$ ；

其次，利用向量恒等式，有：

$$
\mathbf{k} \times \mathbf{v}_\perp = \mathbf{k} \times \left[\mathbf{v} - (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k}\right].
$$

而由于  $\mathbf{k} \times (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k} = (\mathbf{k} \cdot \mathbf{v}) (\mathbf{k} \times \mathbf{k}) = \mathbf{0}$ （因为  $\mathbf{k} \times \mathbf{k} = \mathbf{0}$ ），所以：

$$
\mathbf{k} \times \mathbf{v}_\perp = \mathbf{k} \times \mathbf{v}.
$$


因此，上式可以写成：

$$
\mathbf{v}' = (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k} + \left[\left(\mathbf{v} - (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k}\right)\cos\theta + (\mathbf{k} \times \mathbf{v}) \sin\theta\right].
$$


整理后得到：

$$
\mathbf{v}' = \mathbf{v} \cos\theta + (\mathbf{k} \times \mathbf{v}) \sin\theta + \mathbf{k} (\mathbf{k} \cdot \mathbf{v}) (1 - \cos\theta).
$$


这正是罗德里格斯公式。

---

### 5. 小结

推导过程中，我们利用了以下关键思想：
- **向量分解**：将待旋转向量分解为平行和垂直于旋转轴的部分，其中平行部分保持不变。
- **二维旋转**：在垂直平面内应用标准二维旋转公式。
- **向量恒等式**：利用  $\mathbf{k} \times (\mathbf{k} \cdot \mathbf{v}) \, \mathbf{k} = \mathbf{0}$  简化交叉乘积。

最终，我们得到了描述绕任意单位轴 **k** 旋转 θ 后向量变换的罗德里格斯公式：

$$
\boxed{\mathbf{v}' = \mathbf{v} \cos\theta + (\mathbf{k} \times \mathbf{v}) \sin\theta + \mathbf{k} (\mathbf{k} \cdot \mathbf{v}) (1 - \cos\theta).}
$$


这种公式在计算机图形学、机器人学以及物理学中都具有重要应用。
