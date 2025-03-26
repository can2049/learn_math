## 说明
cos(a + b)是一个数学公式，用于计算两个角度a和b的和的余弦值。这个公式可以通过展开cos(a + b)的表达式来得到。

## 推导过程

为了推导cos(a + b)的展开公式，我们可以使用几何方法、旋转矩阵或欧拉公式。这里我们使用几何方法和欧拉公式进行推导：

### 几何方法（余弦定理）
1. 在单位圆上，考虑两个点A和B，分别对应角度a和-b。它们的坐标分别为：
   - 点A：(cos a, sin a)
   - 点B：(cos b, -sin b)

2. 计算点A和点B之间的距离平方：

$$
   (\cos a - \cos b)^2 + (\sin a + \sin b)^2
   $$

   展开并简化：

$$
   \cos^2 a - 2 \cos a \cos b + \cos^2 b + \sin^2 a + 2 \sin a \sin b + \sin^2 b
   $$

   利用恒等式$`\cos^2 x + \sin^2 x = 1`$：

$$
   1 + 1 - 2 \cos a \cos b + 2 \sin a \sin b = 2 - 2 (\cos a \cos b - \sin a \sin b)
   $$


3. 根据余弦定理，点A和点B之间的夹角为a + b，距离平方为：

$$
   2 - 2 \cos(a + b)
   $$


4. 比较两个表达式：

$$
   2 - 2 (\cos a \cos b - \sin a \sin b) = 2 - 2 \cos(a + b)
   $$

   解得：

$$
   \cos(a + b) = \cos a \cos b - \sin a \sin b
   $$


### 欧拉公式（复数方法）
1. 利用欧拉公式$`e^{i\theta} = \cos \theta + i \sin \theta`$：

$$
   e^{i(a + b)} = e^{ia} \cdot e^{ib} = (\cos a + i \sin a)(\cos b + i \sin b)
   $$


2. 展开乘积：

$$
   (\cos a \cos b - \sin a \sin b) + i (\cos a \sin b + \sin a \cos b)
   $$


3. 比较实部和虚部：

$$
   \cos(a + b) = \cos a \cos b - \sin a \sin b
   $$


$$
   \sin(a + b) = \cos a \sin b + \sin a \cos b
   $$


### 最终答案

$$
\boxed{\cos(a + b) = \cos a \cos b - \sin a \sin b}
$$
