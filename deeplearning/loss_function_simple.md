在深度学习中，损失函数（Loss Function）是衡量模型预测结果与真实值之间差异的核心工具，直接影响模型的优化方向和性能。根据任务类型和数据特点，损失函数可分为以下几大类：

---

### **1. 按任务类型分类**
#### **(1) 回归任务（连续值预测）**
- **均方误差（Mean Squared Error, MSE）**
  - 公式： $L = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y}_i)^2$
  - 特点：对异常值敏感（因平方放大误差），输出为无符号标量。
  - 应用：房价预测、温度预测等连续值任务。

- **平均绝对误差（Mean Absolute Error, MAE）**
  - 公式： $L = \frac{1}{N}\sum_{i=1}^{N}|y_i - \hat{y}_i|$
  - 特点：对异常值鲁棒，但梯度不连续（优化速度较慢）。

- **Huber Loss**
  - 结合MSE和MAE，对异常值鲁棒且梯度平滑：

$$
    L = \begin{cases}
    \frac{1}{2}(y_i - \hat{y}_i)^2 & \text{if } |y_i - \hat{y}_i| \leq \delta \\
    \delta(|y_i - \hat{y}_i| - \frac{1}{2}\delta) & \text{otherwise}
    \end{cases}
    $$

  - 应用：需要平衡MSE和MAE的场景（如自动驾驶中的距离预测）。

---

#### **(2) 分类任务（离散标签预测）**
- **交叉熵损失（Cross-Entropy Loss）**
  - **二分类（Binary Cross-Entropy）**：

$$
    L = -\frac{1}{N}\sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i) \right]
    $$

  - **多分类（Categorical Cross-Entropy）**：

$$
    L = -\frac{1}{N}\sum_{i=1}^{N} \sum_{c=1}^{C} y_{i,c} \log(\hat{y}_{i,c})
    $$

  - 特点：与Softmax激活函数配合使用，擅长处理概率分布差异。
  - 应用：图像分类（如ResNet）、文本分类。

- **合页损失（Hinge Loss）**
  - 公式： $L = \sum_{i=1}^{N} \max(0, 1 - y_i \cdot \hat{y}_i)$
  - 特点：用于支持向量机（SVM），鼓励“边界清晰”的分类。

- **Focal Loss**
  - 改进交叉熵，解决类别不平衡问题：

$$
    L = -\alpha (1-\hat{y}_i)^\gamma \log(\hat{y}_i)
    $$

  - 参数： $\gamma$  抑制易分类样本的权重， $\alpha$  平衡类别。
  - 应用：目标检测（如RetinaNet）。

---

#### **(3) 排序任务（如推荐系统）**
- **对比损失（Contrastive Loss）**
  - 公式： $L = \sum_{i,j} \left[ y_{ij} d(\mathbf{x}_i, \mathbf{x}_j) + (1-y_{ij}) \max(0, \alpha - d(\mathbf{x}_i, \mathbf{x}_j)) \right]$
  - 特点：拉近相似样本，推开不相似样本（ $d$ 为距离函数，如欧氏距离）。

- **Triplet Loss**
  - 公式： $L = \sum_{i} \max(0, d(\mathbf{x}_a, \mathbf{x}_p) - d(\mathbf{x}_a, \mathbf{x}_n) + \alpha)$
  - 组成：锚点（Anchor）、正样本（Positive）、负样本（Negative）。
  - 应用：人脸识别（如FaceNet）、商品相似度排序。

---

### **2. 按损失函数性质分类**
#### **(1) 基于概率的损失**
- **KL散度（Kullback-Leibler Divergence）**
  - 衡量两个概率分布的差异，常用于生成模型（如VAE）。

#### **(2) 基于边界的损失**
- **Margin Loss**
  - 强调分类边界宽度（如支持向量机）。

#### **(3) 鲁棒性损失**
- **Huber Loss**、**Log-Cosh Loss**
  - 减少异常值影响，适用于噪声数据。

---

### **3. 特殊任务与复合损失**
- **感知损失（Perceptual Loss）**
  - 在图像生成中，基于特征层（如VGG网络）的差异计算损失。
- **Dice Loss**
  - 用于图像分割，处理类别不平衡：

$$
    L = 1 - \frac{2\sum y_i \hat{y}_i}{\sum y_i + \sum \hat{y}_i}
    $$

- **复合损失**
  - 例如：目标检测中的 **Multi-Task Loss**（分类损失+回归损失+置信度损失）。

---

### **选择损失函数的关键因素**
1. **任务类型**：回归、分类、生成等。
2. **数据分布**：是否平衡、有无异常值。
3. **模型输出**：概率值、置信度得分或连续值。
4. **优化难度**：梯度是否平滑、是否存在局部最优。

---

### **代码示例（PyTorch）**
```python
import torch.nn as nn

# 回归任务
mse_loss = nn.MSELoss()
mae_loss = nn.L1Loss()

# 分类任务
bce_loss = nn.BCELoss()  # 需配合Sigmoid
ce_loss = nn.CrossEntropyLoss()  # 直接输入logits（无需Softmax）

# 排序任务
triplet_loss = nn.TripletMarginLoss(margin=1.0)
```

理解不同损失函数的适用场景和数学特性，是设计高效深度学习模型的关键一步！
