## 说明
三维旋转是指在三维空间中对一个点进行旋转操作，改变其位置和方向。旋转操作可以通过旋转矩阵或欧拉公式来实现。

## 推导过程
为了推导三维旋转公式，我们考虑一个点  $P(x, y, z)$  绕原点逆时针旋转角度  $\theta$  后的新坐标  $P'(x', y', z')$ 。

下面给出在三维空间中绕  $x$ 、 $y$  和  $z$  轴旋转的推导过程及对应的旋转矩阵。

---

### 1. 绕  $x$  轴的旋转

假设有一点  $P(x,y,z)$ 。当绕  $x$  轴旋转角度  $\theta$  时， $x$  坐标保持不变，而  $y$  和  $z$  坐标发生变化。直观上，旋转可以看成在  $yz$  平面内的二维旋转。

二维旋转公式为：

$$
\begin{cases}
y' = y \cos\theta - z \sin\theta,\\
z' = y \sin\theta + z \cos\theta.
\end{cases}
$$

因此，绕  $x$  轴的旋转矩阵可以写为

$$
R_x(\theta) = \begin{bmatrix}
1 & 0 & 0 \\
0 & \cos\theta & -\sin\theta \\
0 & \sin\theta & \cos\theta
\end{bmatrix}.
$$

应用此矩阵于向量  $\begin{bmatrix} x \\ y \\ z \end{bmatrix}$  得到新坐标  $\begin{bmatrix} x \\ y' \\ z' \end{bmatrix}$ 。

---

### 2. 绕  $y$  轴的旋转

同理，考虑绕  $y$  轴旋转角度  $\theta$ 。此时  $y$  坐标不变，旋转发生在  $xz$  平面内。二维旋转公式在  $xz$  平面中写作：

$$
\begin{cases}
x' = x \cos\theta + z \sin\theta,\\
z' = -x \sin\theta + z \cos\theta.
\end{cases}
$$


对应的旋转矩阵为

$$
R_y(\theta) = \begin{bmatrix}
\cos\theta & 0 & \sin\theta \\
0 & 1 & 0 \\
-\sin\theta & 0 & \cos\theta
\end{bmatrix}.
$$


---

### 3. 绕  $z$  轴的旋转

对于绕  $z$  轴旋转角度  $\theta$ ， $z$  坐标保持不变，旋转发生在  $xy$  平面。二维旋转公式为：

$$
\begin{cases}
x' = x \cos\theta - y \sin\theta,\\
y' = x \sin\theta + y \cos\theta.
\end{cases}
$$


因此，旋转矩阵写作：

$$
R_z(\theta) = \begin{bmatrix}
\cos\theta & -\sin\theta & 0 \\
\sin\theta & \cos\theta & 0 \\
0 & 0 & 1
\end{bmatrix}.
$$


---

### 4. 综合旋转

如果需要同时绕三个轴旋转，可以将单轴旋转矩阵按一定顺序相乘。例如，如果设绕  $x$ 、 $y$  和  $z$  轴的旋转角分别为  $\theta_x$ 、 $\theta_y$  和  $\theta_z$ ，那么常见的组合旋转矩阵（注意矩阵乘法的顺序不可交换）为：

$$
R = R_z(\theta_z) \, R_y(\theta_y) \, R_x(\theta_x).
$$

这表示先绕  $x$  轴旋转，再绕  $y$  轴，最后绕  $z$  轴。不同的顺序会得到不同的结果，具体应用时需根据问题情景确定旋转顺序。

---

### 总结

- **绕  $x$  轴：**

$$
  R_x(\theta) = \begin{bmatrix}
  1 & 0 & 0 \\
  0 & \cos\theta & -\sin\theta \\
  0 & \sin\theta & \cos\theta
  \end{bmatrix}
  $$

- **绕  $y$  轴：**

$$
  R_y(\theta) = \begin{bmatrix}
  \cos\theta & 0 & \sin\theta \\
  0 & 1 & 0 \\
  -\sin\theta & 0 & \cos\theta
  \end{bmatrix}
  $$

- **绕  $z$  轴：**

$$
  R_z(\theta) = \begin{bmatrix}
  \cos\theta & -\sin\theta & 0 \\
  \sin\theta & \cos\theta & 0 \\
  0 & 0 & 1
  \end{bmatrix}
  $$


通过以上步骤，我们推导出三维空间中绕所有坐标轴旋转的基本公式。若有其他问题或需要更详细的证明过程，请继续提问。
