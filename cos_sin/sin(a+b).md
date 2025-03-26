## 说明
### 公式

$$
\boxed{\sin(a + b) = \sin a \cos b + \cos a \sin b}
$$

为了推导  $\sin(a + b)$  的展开公式，我们可以采用几何方法和余弦定理，具体步骤如下：


### **推导过程**

1. **构造单位圆上的点**：
   - 点  $P$  对应角度  $a$ ，坐标为  $(\cos a, \sin a)$ 。
   - 点  $Q$  对应角度  $\frac{\pi}{2} - b$ ，坐标为  $(\sin b, \cos b)$ 。

2. **计算点  $P$  和点  $Q$  之间的距离平方**：
   
$$
   d^2 = (\cos a - \sin b)^2 + (\sin a - \cos b)^2
   $$

   展开并简化：
   
$$
   = \cos^2 a - 2 \cos a \sin b + \sin^2 b + \sin^2 a - 2 \sin a \cos b + \cos^2 b
   $$

   
$$
   = (\cos^2 a + \sin^2 a) + (\sin^2 b + \cos^2 b) - 2 (\cos a \sin b + \sin a \cos b)
   $$

   
$$
   = 1 + 1 - 2 (\cos a \sin b + \sin a \cos b)
   $$

   
$$
   = 2 - 2 (\cos a \sin b + \sin a \cos b)
   $$


3. **使用余弦定理计算同一距离平方**：
   - 点  $P$  和  $Q$  之间的夹角为  $\frac{\pi}{2} - (a + b)$ ，因此：
   
$$
   d^2 = 2 - 2 \cos\left(\frac{\pi}{2} - (a + b)\right)
   $$

   - 根据余角关系， $\cos\left(\frac{\pi}{2} - \theta\right) = \sin \theta$ ，故：
   
$$
   d^2 = 2 - 2 \sin(a + b)
   $$


4. **将两种方法得到的距离平方等同**：
   
$$
   2 - 2 (\cos a \sin b + \sin a \cos b) = 2 - 2 \sin(a + b)
   $$

   两边同时减去 2，再除以 -2：
   
$$
   \cos a \sin b + \sin a \cos b = \sin(a + b)
   $$




### **最终公式**
因此， $\sin(a + b)$  的展开公式为：

$$
\boxed{\sin(a + b) = \sin a \cos b + \cos a \sin b}
$$




### **推导总结**
1. **几何构造**：通过单位圆上的点坐标，结合角度关系  $\frac{\pi}{2} - b$ ，引入正弦和余弦的余角恒等式。
2. **距离计算**：利用坐标展开和勾股定理简化表达式。
3. **余弦定理**：通过夹角关系将距离平方转换为正弦函数，最终导出和角公式。

这种方法与推导  $\cos(a + b)$  的几何思路一致，保持了逻辑的连贯性。