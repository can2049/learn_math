
四元数（Quaternions）是复数的扩展，由**实数**和三个**虚数单位**  $\mathbf{i}, \mathbf{j}, \mathbf{k}$  构成，广泛应用于三维空间的旋转表示、计算机图形学、机器人学等领域。以下是其核心内容和特性：

---

### **1. 四元数的定义**
四元数的一般形式为：

$$
q = a + b\mathbf{i} + c\mathbf{j} + d\mathbf{k}
$$

其中：
-  $a, b, c, d \in \mathbb{R}$  是实数部分。
-  $\mathbf{i}, \mathbf{j}, \mathbf{k}$  是虚数单位，满足以下乘法规则：

$$
  \mathbf{i}^2 = \mathbf{j}^2 = \mathbf{k}^2 = \mathbf{i}\mathbf{j}\mathbf{k} = -1
  $$


$$
  \mathbf{i}\mathbf{j} = \mathbf{k}, \quad \mathbf{j}\mathbf{k} = \mathbf{i}, \quad \mathbf{k}\mathbf{i} = \mathbf{j}
  $$


$$
  \mathbf{j}\mathbf{i} = -\mathbf{k}, \quad \mathbf{k}\mathbf{j} = -\mathbf{i}, \quad \mathbf{i}\mathbf{k} = -\mathbf{j}
  $$


---

### **2. 四元数的表示**
- **标量-向量形式**： $q = (a, \mathbf{v})$ ，其中  $\mathbf{v} = (b, c, d)$  为三维向量。
- **极坐标形式**：若  $q$  为单位四元数（模为1），可表示为：

$$
  q = \cos\left(\frac{\theta}{2}\right) + \mathbf{u} \sin\left(\frac{\theta}{2}\right)
  $$

  其中  $\mathbf{u}$  是单位旋转轴， $\theta$  是旋转角度。

---

### **3. 基本运算**
- **加法**：逐项相加。
- **乘法**（格拉斯曼积）：

$$
  q_1 q_2 = (a_1a_2 - \mathbf{v}_1 \cdot \mathbf{v}_2, \, a_1\mathbf{v}_2 + a_2\mathbf{v}_1 + \mathbf{v}_1 \times \mathbf{v}_2)
  $$

  乘法不满足交换律（ $q_1 q_2 \neq q_2 q_1$ ）。
- **共轭四元数**： $q^* = a - b\mathbf{i} - c\mathbf{j} - d\mathbf{k}$ 。
- **模长**： $\|q\| = \sqrt{a^2 + b^2 + c^2 + d^2}$ 。
- **逆四元数**： $q^{-1} = \frac{q^*}{\|q\|^2}$ 。

---

### **4. 关键特性**
1. **非交换性**
   四元数乘法不满足交换律，但满足结合律和分配律。

2. **旋转表示**
   三维向量  $\mathbf{v}$  绕单位轴  $\mathbf{u}$  旋转  $\theta$  角，可通过四元数实现：

$$
   \mathbf{v}' = q \mathbf{v} q^{-1}, \quad \text{其中} \quad q = \cos\left(\frac{\theta}{2}\right) + \mathbf{u} \sin\left(\frac{\theta}{2}\right)
   $$

   此方法避免了欧拉角的万向节锁问题。

3. **单位四元数与旋转群**
   所有单位四元数构成三维旋转群  $\text{SO}(3)$  的双覆盖（每个旋转对应两个四元数  $q$  和  $-q$ ）。

4. **插值平滑性**
   四元数的球面线性插值（Slerp）能生成平滑的旋转路径，适用于动画和路径规划。

5. **与矩阵的对比**
   - 存储更高效（4个数 vs. 矩阵的9个数）。
   - 计算更快速，避免矩阵的奇异性问题。

---

### **5. 应用场景**
- **计算机图形学**：角色动画、相机朝向控制。
- **机器人学**：无人机、机械臂的姿态控制。
- **物理学**：角速度、陀螺仪数据的处理。
- **游戏开发**：Unity/Unreal引擎中常用四元数表示旋转。

---

### **6. 示例**
**旋转一个点**：
将点  $\mathbf{p} = (1, 0, 0)$  绕  $\mathbf{u} = (0, 1, 0)$  旋转  $90^\circ$ ：
1. 构造四元数： $q = \cos(45^\circ) + \mathbf{u} \sin(45^\circ) \approx 0.707 + 0.707\mathbf{j}$ 。
2. 旋转计算： $\mathbf{p}' = q \mathbf{p} q^{-1} = (0, 0, -1)$ 。

---

### **总结**
四元数通过紧凑的形式和高效的运算，解决了三维旋转中的诸多问题（如万向节锁），成为现代工程和计算机科学中不可或缺的工具。其核心优势在于**几何直观性**、**计算效率**和**插值平滑性**。
