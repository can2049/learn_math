## 说明
二维旋转是指在二维平面上对一个点进行旋转操作，改变其位置和方向。旋转操作可以通过旋转矩阵或欧拉公式来实现。

## 推导过程


为了推导二维旋转公式，我们考虑一个点  $P(x, y)$  绕原点逆时针旋转角度  $\theta$  后的新坐标  $P'(x', y')$ 。

1. **极坐标转换**：
   假设点  $P$  的极坐标为  $(r, \alpha)$ ，其中  $r$  是到原点的距离， $\alpha$  是相对于 x 轴的夹角。原坐标可以表示为：
   
$$
   x = r \cos \alpha
   $$

   
$$
   y = r \sin \alpha
   $$

   旋转  $\theta$  角度后，新角度变为  $\alpha + \theta$ ，新坐标为：
   
$$
   x' = r \cos(\alpha + \theta)
   $$

   
$$
   y' = r \sin(\alpha + \theta)
   $$


2. **三角函数加法公式**：
   使用三角函数的加法公式展开：
   
$$
   \cos(\alpha + \theta) = \cos \alpha \cos \theta - \sin \alpha \sin \theta
   $$

   
$$
   \sin(\alpha + \theta) = \sin \alpha \cos \theta + \cos \alpha \sin \theta
   $$

   代入原坐标  $x$  和  $y$ ：
   
$$
   x' = r (\cos \alpha \cos \theta - \sin \alpha \sin \theta) = x \cos \theta - y \sin \theta
   $$

   
$$
   y' = r (\sin \alpha \cos \theta + \cos \alpha \sin \theta) = y \cos \theta + x \sin \theta
   $$


3. **向量分解**：
   将原向量分解为基向量  $\mathbf{i}$  和  $\mathbf{j}$  旋转后的结果。基向量旋转后的新坐标为：
   
$$
   \mathbf{i}' = (\cos \theta, \sin \theta)
   $$

   
$$
   \mathbf{j}' = (-\sin \theta, \cos \theta)
   $$

   旋转后的向量  $P'$  表示为：
   
$$
   x' \mathbf{i}' + y' \mathbf{j}' = x (\cos \theta, \sin \theta) + y (-\sin \theta, \cos \theta)
   $$

   得到：
   
$$
   x' = x \cos \theta - y \sin \theta
   $$

   
$$
   y' = x \sin \theta + y \cos \theta
   $$


4. **验证**：
   通过特殊角度（如  $0^\circ$ 、 $90^\circ$ 、 $180^\circ$ ）验证公式的正确性，结果均符合预期。

最终，二维旋转后的坐标公式为：

$$
\boxed{
\begin{cases}
x' = x \cos \theta - y \sin \theta \\
y' = x \sin \theta + y \cos \theta
\end{cases}
}
$$



5. **矩阵形式表示**
将上述公式写成矩阵乘法形式：

$$
\begin{pmatrix} x' \\ y' \end{pmatrix} = 
\begin{pmatrix} 
\cos \theta & -\sin \theta \\ 
\sin \theta & \cos \theta 
\end{pmatrix}
\begin{pmatrix} x \\ y \end{pmatrix}
$$

其中，旋转矩阵 $R(\theta)$ 为：

$$
R(\theta) = \begin{pmatrix} 
\cos \theta & -\sin \theta \\ 
\sin \theta & \cos \theta 
\end{pmatrix}
$$

6. **验证**
通过矩阵乘法验证：

$$
x' = \cos \theta \cdot x - \sin \theta \cdot y \\
y' = \sin \theta \cdot x + \cos \theta \cdot y
$$

与之前推导的公式一致。

7. **性质**
旋转矩阵 $R(\theta)$ 是正交矩阵，满足：
- $R^T R = I$（转置等于逆矩阵）
- $\det(R) = 1$（行列式为1）

8. 总结
二维旋转的矩阵形式为：

$$
\boxed{
\begin{pmatrix} x' \\ y' \end{pmatrix} = 
\begin{pmatrix} 
\cos \theta & -\sin \theta \\ 
\sin \theta & \cos \theta 
\end{pmatrix}
\begin{pmatrix} x \\ y \end{pmatrix}
}
$$