# 注意力就是你所需要的一切

> **原文标题**: Attention Is All You Need
> **作者**: Ashish Vaswani\*, Noam Shazeer\*, Niki Parmar\*, Jakob Uszkoreit\*, Llion Jones\*, Aidan N. Gomez\*†, Łukasz Kaiser\*, Illia Polosukhin\*‡ （\*共同第一作者）
> **机构**: Google Brain, Google Research, University of Toronto
> **发表/来源**: NeurIPS 2017 (原 NIPS 2017), arXiv:1706.03762 (2017年6月)

---

## 摘要

主流的序列转换（Sequence Transduction）模型基于复杂的循环神经网络（Recurrent Neural Network, RNN）或卷积神经网络（Convolutional Neural Network, CNN），采用编码器-解码器（Encoder-Decoder）架构。表现最优的模型还通过注意力机制（Attention Mechanism）连接编码器和解码器。我们提出了一种新的简洁网络架构——**Transformer**，完全基于注意力机制，彻底摒弃了循环和卷积结构。在两个机器翻译任务上的实验表明，该模型在翻译质量上更优，同时具备更强的并行化能力，所需训练时间也显著更少。我们的模型在 WMT 2014 英德翻译任务上达到 28.4 BLEU，超越此前所有最佳结果（包括集成模型）2 个 BLEU 以上。在 WMT 2014 英法翻译任务上，我们的模型在 8 块 GPU 上训练 3.5 天后，取得 41.0 的单模型 BLEU 新纪录，训练成本仅为文献中最佳模型的一小部分。

> **阅读批注**：这篇论文的核心贡献在于证明了纯注意力机制就足以构建强大的序列转换模型，不需要 RNN 或 CNN。这一架构后来成为 GPT、BERT、ViT 等一系列里程碑模型的基石，被认为是深度学习领域最具影响力的论文之一。

---

## 1 引言

循环神经网络，特别是长短期记忆网络（Long Short-Term Memory, LSTM）[12] 和门控循环单元（Gated Recurrent Unit, GRU）[7]，在序列建模和序列转换问题（如语言建模和机器翻译 [29, 2, 5]）中已被确立为最先进的方法。此后众多研究持续推进循环语言模型和编码器-解码器架构的发展 [31, 21, 13]。

循环模型通常沿输入和输出序列的符号位置分解计算。将各位置对齐到计算时间步，模型生成一系列隐藏状态 $ h_t $，作为前一隐藏状态 $ h_{t-1} $ 和位置 $ t $ 的输入的函数。这种固有的**顺序性**使得训练样本内部无法并行化，当序列较长时这一问题尤为严重，因为内存限制了跨样本的批处理能力。近期工作通过分解技巧 [18] 和条件计算 [26] 实现了计算效率的显著提升，同时后者还提高了模型性能。然而，顺序计算的根本约束依然存在。

注意力机制已成为各种任务中序列建模和转换模型的核心组成部分，它允许对依赖关系进行建模，而不受输入或输出序列中距离的限制 [2, 16]。但在绝大多数情况下 [22]，此类注意力机制仍然是与循环网络配合使用的。

在本文中，我们提出了 **Transformer**——一种摒弃循环结构、完全依赖注意力机制来捕获输入与输出之间全局依赖关系的模型架构。Transformer 允许更大程度的并行化，仅在 8 块 P100 GPU 上训练约 12 小时就能达到翻译质量的新水平。

---

## 2 背景

减少顺序计算的目标同样是 Extended Neural GPU [20]、ByteNet [15] 和 ConvS2S [8] 的基础，它们都使用卷积神经网络作为基本构建模块，对所有输入和输出位置并行地计算隐藏表示。在这些模型中，将两个任意输入或输出位置的信号关联起来所需的操作数量随位置间距离增长——ConvS2S 中线性增长，ByteNet 中对数增长。这使得学习远距离依赖变得更加困难 [11]。在 Transformer 中，这被减少到**常数级别**的操作数量，尽管代价是由于对注意力加权位置求平均而降低了有效分辨率——我们通过多头注意力（Multi-Head Attention，详见第 3.2 节）来抵消这一效应。

**自注意力**（Self-Attention），有时也称为内部注意力（Intra-Attention），是一种将单个序列中不同位置相互关联以计算该序列表示的注意力机制。自注意力已在多种任务中成功应用，包括阅读理解、抽象式摘要、文本蕴含和学习与任务无关的句子表示 [4, 22, 23, 19]。

端到端记忆网络（End-to-End Memory Networks）基于循环注意力机制而非序列对齐的循环，已被证明在简单语言问答和语言建模任务上表现良好 [28]。

据我们所知，Transformer 是第一个完全依赖自注意力来计算其输入和输出表示的转换模型，不使用序列对齐的 RNN 或卷积。在接下来的章节中，我们将描述 Transformer，阐述自注意力的动机，并讨论其相对于 [14, 15] 和 [8] 等模型的优势。

---

## 3 模型架构

大多数具有竞争力的神经序列转换模型都采用编码器-解码器结构 [5, 2, 29]。编码器将输入符号表示序列 $ (x_1, \ldots, x_n) $ 映射为连续表示序列 $ \mathbf{z} = (z_1, \ldots, z_n) $。给定 $ \mathbf{z} $，解码器逐个生成输出符号序列 $ (y_1, \ldots, y_m) $。在每一步中，模型都是**自回归的**（Auto-Regressive）[9]，在生成下一个符号时将先前生成的符号作为额外输入。

Transformer 遵循这一总体架构，其编码器和解码器均使用堆叠的自注意力层和逐位置（Point-Wise）全连接层构建。

### 3.1 编码器和解码器堆栈

**编码器**：编码器由 $ N = 6 $ 个相同的层堆叠而成。每层包含两个子层：第一个是**多头自注意力机制**，第二个是简单的**逐位置全连接前馈网络**。我们在每个子层周围使用**残差连接**（Residual Connection）[10]，之后进行**层归一化**（Layer Normalization）[1]。即每个子层的输出为：

$$
\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))
$$

其中 $ \mathrm{Sublayer}(x) $ 是该子层本身实现的函数。为便于使用残差连接，模型中所有子层和嵌入层的输出维度均为 $ d_{\text{model}} = 512 $。

**解码器**：解码器同样由 $ N = 6 $ 个相同的层堆叠而成。除编码器每层的两个子层外，解码器**插入第三个子层**，该子层对编码器堆栈的输出执行多头注意力。与编码器类似，我们在每个子层周围使用残差连接和层归一化。解码器还**修改了自注意力子层**，以防止每个位置关注后续位置。这种掩码（Masking）机制加上输出嵌入偏移一个位置的事实，确保了位置 $ i $ 的预测只能依赖于位置小于 $ i $ 的已知输出。

> **架构要点总结**：
>
> - 编码器每层：多头自注意力 → 残差+层归一化 → 前馈网络 → 残差+层归一化
> - 解码器每层：掩码多头自注意力 → 残差+层归一化 → 编码器-解码器注意力 → 残差+层归一化 → 前馈网络 → 残差+层归一化
> - 统一维度 $ d_{\text{model}} = 512 $ 是实现残差连接的关键设计选择

### 3.2 注意力

注意力函数可以描述为将一个查询（Query）和一组键-值（Key-Value）对映射到一个输出，其中查询、键、值和输出均为向量。输出是值的加权和，每个值的权重由查询与对应键的兼容性函数计算得到。

#### 3.2.1 缩放点积注意力

我们将本文的特定注意力称为"缩放点积注意力"（Scaled Dot-Product Attention）。输入由维度为 $ d_k $ 的查询和键、维度为 $ d_v $ 的值组成。我们计算查询与所有键的点积，将每个点积除以 $ \sqrt{d_k} $，然后应用 softmax 函数以获得值的权重。

在实践中，我们同时对一组查询进行计算，将其打包成矩阵 $ Q $。键和值也分别打包成矩阵 $ K $ 和 $ V $。输出矩阵的计算公式为：

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

> **数学原理详解——缩放点积注意力**：
>
> **符号含义**：
> - $ Q \in \mathbb{R}^{n \times d_k} $：查询矩阵，$ n $ 个查询向量，每个维度 $ d_k $
> - $ K \in \mathbb{R}^{m \times d_k} $：键矩阵，$ m $ 个键向量，每个维度 $ d_k $
> - $ V \in \mathbb{R}^{m \times d_v} $：值矩阵，$ m $ 个值向量，每个维度 $ d_v $
> - $ QK^T \in \mathbb{R}^{n \times m} $：查询与键的点积矩阵，元素 $ (i, j) $ 衡量第 $ i $ 个查询与第 $ j $ 个键的相似度
> - $ \sqrt{d_k} $：缩放因子，用于控制点积的数量级
>
> **推导过程**：
> 1. 计算 $ QK^T $：每个元素 $ q_i \cdot k_j = \sum_{l=1}^{d_k} q_{il} \cdot k_{jl} $，得到原始注意力得分
> 2. 缩放：除以 $ \sqrt{d_k} $，得到 $ \frac{QK^T}{\sqrt{d_k}} $
> 3. Softmax 归一化：对每行应用 softmax，使权重和为 1
> 4. 加权求和：用归一化后的权重对 $ V $ 加权，得到输出
>
> **为什么要缩放？** 假设 $ q $ 和 $ k $ 的各分量是均值为 0、方差为 1 的独立随机变量，则它们的点积 $ q \cdot k = \sum_{i=1}^{d_k} q_i k_i $ 的均值为 0，**方差为 $ d_k $**。当 $ d_k $ 较大时，点积的绝对值会很大，导致 softmax 的输入被推到极端区域（接近 one-hot），梯度变得极小。除以 $ \sqrt{d_k} $ 后，点积的方差被归一化为 1，softmax 输出分布更加平滑，梯度信号更健康。
>
> **直觉理解**：可以类比为"考试阅卷"——查询是"评分标准"，键是"各答案的特征"，值是"各答案的内容"。点积衡量每个答案与标准的匹配程度，softmax 将匹配度转化为概率分布，最后按概率混合各答案内容作为输出。缩放因子确保不会因为维度太高而让某个答案"一家独大"。

两种最常用的注意力函数是**加性注意力**（Additive Attention）[2] 和**点积（乘性）注意力**（Dot-Product / Multiplicative Attention）。点积注意力与我们的算法相同，只是缺少缩放因子 $ \frac{1}{\sqrt{d_k}} $。加性注意力使用一个带单隐藏层的前馈网络来计算兼容性函数。虽然两者的理论复杂度相近，但点积注意力在实践中**快得多且空间效率更高**，因为它可以利用高度优化的矩阵乘法代码。

对于较小的 $ d_k $，两种机制表现类似；但当 $ d_k $ 较大时，不带缩放的点积注意力性能不如加性注意力 [3]。如前所述，我们怀疑大 $ d_k $ 使得点积值变大，将 softmax 函数推入梯度极小的区域。因此我们用 $ \frac{1}{\sqrt{d_k}} $ 对点积进行缩放。

#### 3.2.2 多头注意力

我们发现，与其用 $ d_{\text{model}} $ 维的键、值和查询执行单一注意力函数，不如将查询、键和值分别用 $ h $ 组不同的、可学习的线性投影映射到 $ d_k $、$ d_k $ 和 $ d_v $ 维度。然后在每组投影后的查询、键和值上并行执行注意力函数，得到 $ d_v $ 维的输出。将这些输出拼接后再进行一次线性投影，得到最终输出。

$$
\mathrm{MultiHead}(Q, K, V) = \mathrm{Concat}(\mathrm{head}_1, \ldots, \mathrm{head}_h) W^O
$$

$$
\text{其中} \quad \mathrm{head}_i = \mathrm{Attention}(Q W_i^Q, K W_i^K, V W_i^V)
$$

> **数学原理详解——多头注意力**：
>
> **符号含义**：
> - $ W_i^Q \in \mathbb{R}^{d_{\text{model}} \times d_k} $：第 $ i $ 个头的查询投影矩阵
> - $ W_i^K \in \mathbb{R}^{d_{\text{model}} \times d_k} $：第 $ i $ 个头的键投影矩阵
> - $ W_i^V \in \mathbb{R}^{d_{\text{model}} \times d_v} $：第 $ i $ 个头的值投影矩阵
> - $ W^O \in \mathbb{R}^{h d_v \times d_{\text{model}}} $：输出投影矩阵
> - $ h = 8 $：注意力头的数量
> - $ d_k = d_v = d_{\text{model}} / h = 64 $：每个头的维度
>
> **计算流程**：
> 1. 对于第 $ i $ 个头，将输入分别投影：$ Q W_i^Q $、$ K W_i^K $、$ V W_i^V $
> 2. 在投影后的低维空间中计算缩放点积注意力
> 3. 拼接 $ h $ 个头的输出（维度 $ h \times d_v = 512 $）
> 4. 通过 $ W^O $ 投影回 $ d_{\text{model}} $ 维
>
> **为什么用多头？** 单个注意力头进行的是加权平均，会抑制模型同时关注不同表示子空间中不同位置信息的能力。多头注意力让模型可以在不同头中学习不同类型的关注模式——例如，一个头可能关注句法关系，另一个头关注语义相似性，还有头可能捕捉位置相邻性。
>
> **计算代价**：由于每个头的维度从 $ d_{\text{model}} = 512 $ 降低到 $ d_k = 64 $，$ h $ 个头的总计算量与全维度单头注意力相当。这是一个"分而治之"的策略——同样的计算预算，获得更丰富的表示能力。

本文使用 $ h = 8 $ 个并行注意力头，每个头 $ d_k = d_v = d_{\text{model}} / h = 64 $。由于每个头的维度降低，总计算成本与全维度单头注意力相当。

#### 3.2.3 注意力在模型中的应用

Transformer 以三种不同方式使用多头注意力：

1. **编码器-解码器注意力层**：查询来自前一个解码器层，键和值来自编码器的输出。这使解码器的每个位置都能关注输入序列的所有位置，模拟了序列到序列模型中典型的编码器-解码器注意力机制 [31, 2, 8]。

2. **编码器自注意力层**：键、值和查询都来自同一位置——即编码器前一层的输出。编码器中的每个位置都能关注前一层中的所有位置。

3. **解码器掩码自注意力层**：解码器中的自注意力层允许每个位置关注解码器中直到并包括该位置的所有位置。为保持自回归特性，需要防止向左的信息流动。实现方式是在 softmax 的输入中将对应非法连接的位置设为 $ -\infty $（即掩码机制）。

### 3.3 逐位置前馈网络

除注意力子层外，编码器和解码器的每一层还包含一个全连接前馈网络，该网络分别且相同地应用于每个位置。它由两个线性变换组成，中间有 ReLU 激活函数：

$$
\mathrm{FFN}(x) = \max(0, xW_1 + b_1) W_2 + b_2
$$

> **数学原理详解——前馈网络**：
>
> **符号含义**：
> - $ x \in \mathbb{R}^{d_{\text{model}}} $：某个位置的输入向量（维度 512）
> - $ W_1 \in \mathbb{R}^{d_{\text{model}} \times d_{ff}} $：第一层权重（$ 512 \times 2048 $）
> - $ b_1 \in \mathbb{R}^{d_{ff}} $：第一层偏置
> - $ W_2 \in \mathbb{R}^{d_{ff} \times d_{\text{model}}} $：第二层权重（$ 2048 \times 512 $）
> - $ b_2 \in \mathbb{R}^{d_{\text{model}}} $：第二层偏置
> - $ d_{ff} = 2048 $：内层维度
>
> **计算流程**：输入 → 线性变换升维（512→2048）→ ReLU 激活 → 线性变换降维（2048→512）
>
> **直觉理解**：注意力层的作用是"在不同位置间聚合信息"，而 FFN 的作用是"对每个位置独立地进行非线性变换"。可以类比为：注意力是"开会讨论"，FFN 是"各自消化思考"。升维（4倍）后再降维的设计类似于 bottleneck 的逆操作，为模型提供更大的中间表示空间进行复杂变换。
>
> 另一种理解方式：该 FFN 等价于两个核大小为 1 的卷积层。虽然线性变换跨位置共享参数（同一层内），但不同层之间参数不同。

输入和输出维度均为 $ d_{\text{model}} = 512 $，内层维度为 $ d_{ff} = 2048 $。

### 3.4 嵌入和 Softmax

与其他序列转换模型类似，我们使用可学习的嵌入（Learned Embeddings）将输入和输出 token 转换为维度 $ d_{\text{model}} $ 的向量。我们还使用常规的可学习线性变换和 softmax 函数将解码器输出转换为预测的下一 token 概率。在本模型中，我们在两个嵌入层和预 softmax 线性变换之间**共享相同的权重矩阵**，类似于 [24]。在嵌入层中，我们将这些权重乘以 $ \sqrt{d_{\text{model}}} $。

> **设计动机——权重共享与缩放**：
>
> 三处共享权重（输入嵌入、输出嵌入、预 softmax 线性变换）减少了参数量并引入了隐式正则化，使得输入和输出的表示空间对齐。乘以 $ \sqrt{d_{\text{model}}} $ 是为了补偿嵌入维度对向量范数的影响：嵌入向量的各分量通常较小（受权重初始化影响），乘以 $ \sqrt{d_{\text{model}}} $ 后与位置编码的量级匹配，避免位置信息在相加后淹没语义信息。

### 3.5 位置编码

由于模型不含循环和卷积，为了利用序列的顺序信息，我们必须注入关于 token 在序列中相对或绝对位置的信息。为此，我们将**位置编码**（Positional Encoding）加到编码器和解码器堆栈底部的输入嵌入上。位置编码的维度与嵌入相同（ $ d_{\text{model}} $ ），使两者可以相加。

本文使用不同频率的正弦和余弦函数：

$$
PE_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i / d_{\text{model}}}}\right)
$$

$$
PE_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i / d_{\text{model}}}}\right)
$$

> **数学原理详解——正弦位置编码**：
>
> **符号含义**：
> - $ pos $：token 在序列中的位置（0, 1, 2, ...）
> - $ i $：维度索引（$ 0 \le i < d_{\text{model}} / 2 $）
> - $ PE_{(pos, 2i)} $：位置编码向量的第 $ 2i $ 个分量（偶数维用 sin）
> - $ PE_{(pos, 2i+1)} $：位置编码向量的第 $ 2i+1 $ 个分量（奇数维用 cos）
>
> **波长设计**：各维度对应的波长构成从 $ 2\pi $ 到 $ 10000 \cdot 2\pi $ 的**几何级数**。低维度的波长短（变化快，编码细粒度位置信息），高维度的波长长（变化慢，编码粗粒度位置信息）。
>
> **关键特性——相对位置的线性可表达性**：对于任意固定偏移 $ k $，$ PE_{pos+k} $ 可以表示为 $ PE_{pos} $ 的线性函数。具体地，利用三角函数的和差化积公式：
>
> $$
> \begin{pmatrix} \sin(pos \cdot \omega + k\omega) \\ \cos(pos \cdot \omega + k\omega) \end{pmatrix} = \begin{pmatrix} \cos(k\omega) & \sin(k\omega) \\ -\sin(k\omega) & \cos(k\omega) \end{pmatrix} \begin{pmatrix} \sin(pos \cdot \omega) \\ \cos(pos \cdot \omega) \end{pmatrix}
> $$
>
> 其中 $ \omega = 1 / 10000^{2i/d_{\text{model}}} $。旋转矩阵只依赖于偏移 $ k $，不依赖于绝对位置 $ pos $。这意味着模型可以通过学习线性变换来"解码"两个位置之间的相对距离。
>
> **直觉理解**：可以类比为**二进制计数器的连续版本**。在二进制中，最低位每步翻转一次，次低位每两步翻转一次……位置编码的低维度"振荡快"，高维度"振荡慢"，每个位置都有唯一的"频率指纹"。
>
> **相较于可学习位置嵌入**：实验表明两者效果几乎一致（见 Table 3 行 (E)），但正弦版本的潜在优势是可以**外推**到训练时未见过的更长序列——因为正弦函数对任意 $ pos $ 都有定义。

---

## 4 为什么使用自注意力

本节从三个维度比较自注意力层与循环层和卷积层：

1. **每层总计算复杂度**
2. **可并行化的计算量**（以所需最少顺序操作数衡量）
3. **长距离依赖的路径长度**

**Table 1：不同层类型的复杂度对比**

| 层类型 | 每层复杂度 | 顺序操作数 | 最大路径长度 |
|--------|-----------|-----------|------------|
| 自注意力 | $ O(n^2 \cdot d) $ | $ O(1) $ | $ O(1) $ |
| 循环层 | $ O(n \cdot d^2) $ | $ O(n) $ | $ O(n) $ |
| 卷积层 | $ O(k \cdot n \cdot d^2) $ | $ O(1) $ | $ O(\log_k(n)) $ |
| 受限自注意力 | $ O(r \cdot n \cdot d) $ | $ O(1) $ | $ O(n/r) $ |

> **数学原理详解——复杂度分析**：
>
> - **自注意力** $ O(n^2 \cdot d) $：$ n $ 个位置两两之间计算注意力（$ n^2 $ 对），每对涉及 $ d $ 维的点积。当 $ n < d $ 时（机器翻译中通常如此），自注意力比循环层更快。顺序操作数为 $ O(1) $ 意味着所有位置可完全并行计算。最大路径长度为 $ O(1) $，即任意两个位置之间只需一步即可直接交互。
>
> - **循环层** $ O(n \cdot d^2) $：每步涉及 $ d \times d $ 的矩阵乘法，共 $ n $ 步。顺序操作数为 $ O(n) $ 是其致命缺陷——必须逐步串行计算。最大路径长度为 $ O(n) $，远距离信号必须经过多步传播。
>
> - **卷积层** $ O(k \cdot n \cdot d^2) $：单层核宽 $ k < n $ 无法连接所有位置对，需要 $ O(n/k) $ 层（连续核）或 $ O(\log_k(n)) $ 层（膨胀卷积），增加了最大路径长度。
>
> **核心论点**：自注意力在路径长度上的 $ O(1) $ 优势使其更容易学习长距离依赖关系。

自注意力层用常数级别的顺序操作连接所有位置，而循环层需要 $ O(n) $ 个顺序操作。当序列长度 $ n $ 小于表示维度 $ d $ 时（机器翻译中常见情况），自注意力层比循环层更快。

对于涉及极长序列的任务，自注意力可以被限制为仅考虑以输出位置为中心、大小为 $ r $ 的邻域，这将最大路径长度增加到 $ O(n/r) $。

自注意力还带来了**可解释性**方面的附加好处。各注意力头明显学会了执行不同的任务，许多表现出与句子句法和语义结构相关的行为。

---

## 5 训练

### 5.1 训练数据和分批

- **英德翻译**：标准 WMT 2014 英德数据集，约 450 万句对。使用字节对编码（Byte-Pair Encoding, BPE）[3]，共享源-目标词表约 37000 个 token。
- **英法翻译**：WMT 2014 英法数据集，3600 万句对，32000 个 word-piece 词表 [31]。
- 句对按近似序列长度分批，每个训练批次包含约 25000 个源 token 和 25000 个目标 token。

### 5.2 硬件和训练计划

在一台配备 8 块 NVIDIA P100 GPU 的机器上训练：
- **基础模型**：每步约 0.4 秒，共训练 100,000 步（约 12 小时）
- **大模型**：每步约 1.0 秒，共训练 300,000 步（约 3.5 天）

### 5.3 优化器

使用 Adam 优化器 [17]，参数为 $ \beta_1 = 0.9 $，$ \beta_2 = 0.98 $，$ \epsilon = 10^{-9} $。学习率按以下公式在训练过程中变化：

$$
lrate = d_{\text{model}}^{-0.5} \cdot \min(step\_num^{-0.5}, \ step\_num \cdot warmup\_steps^{-1.5})
$$

> **数学原理详解——学习率调度**：
>
> **两段式调度**：
> - **预热阶段**（前 $ warmup\_steps = 4000 $ 步）：学习率线性增长。此阶段 $ step\_num < warmup\_steps $，因此 $ step\_num \cdot warmup\_steps^{-1.5} < step\_num^{-0.5} $，学习率主要由 $ step\_num \cdot warmup\_steps^{-1.5} $ 决定，与步数成正比。
> - **衰减阶段**（4000 步后）：学习率按步数的平方根倒数衰减。此阶段 $ step\_num^{-0.5} < step\_num \cdot warmup\_steps^{-1.5} $，学习率正比于 $ step\_num^{-0.5} $。
>
> **峰值学习率**：在 $ step\_num = warmup\_steps $ 时达到最大值 $ d_{\text{model}}^{-0.5} \cdot warmup\_steps^{-0.5} = 512^{-0.5} \cdot 4000^{-0.5} \approx 6.96 \times 10^{-4} $。
>
> **乘以 $ d_{\text{model}}^{-0.5} $ 的意义**：使学习率与模型维度自适应匹配——维度越大，学习率越小，有助于稳定训练。
>
> **预热的动机**：训练初期参数随机，梯度方向不稳定且方差大。较小的学习率避免参数剧烈震荡。随着梯度统计量（Adam 的一阶和二阶矩估计）逐渐稳定，逐步增大学习率以加速收敛。

使用 $ warmup\_steps = 4000 $。

### 5.4 正则化

训练过程中采用三种正则化方式：

**残差 Dropout**：在每个子层的输出上应用 Dropout [27]，在其与子层输入相加并归一化之前执行。此外，在编码器和解码器堆栈中，对嵌入和位置编码的求和结果也应用 Dropout。基础模型的 Dropout 率 $ P_{drop} = 0.1 $。

**标签平滑**（Label Smoothing）：训练时使用 $ \epsilon_{ls} = 0.1 $ 的标签平滑 [30]。这会损害困惑度（Perplexity），因为模型学习变得更"不确定"，但提高了准确率和 BLEU 分数。

> **标签平滑的直觉**：传统 one-hot 标签对正确类别赋概率 1、其余为 0，要求模型过度自信。标签平滑将正确类别的概率降为 $ 1 - \epsilon_{ls} $，其余类别均分 $ \epsilon_{ls} $。这迫使模型不再追求极端的 logit 差异，起到防过拟合作用，同时使 softmax 输出更为校准。

---

## 6 结果

### 6.1 机器翻译

**Table 2：与现有最优模型的对比**

| 模型 | EN-DE BLEU | EN-FR BLEU | EN-DE FLOPs | EN-FR FLOPs |
|------|-----------|-----------|-------------|-------------|
| ByteNet [15] | 23.75 | — | — | — |
| Deep-Att + PosUnk [32] | — | 39.2 | — | $ 1.0 \times 10^{20} $ |
| GNMT + RL [31] | 24.6 | 39.92 | $ 2.3 \times 10^{19} $ | $ 1.4 \times 10^{20} $ |
| ConvS2S [8] | 25.16 | 40.46 | $ 9.6 \times 10^{18} $ | $ 1.5 \times 10^{20} $ |
| MoE [26] | 26.03 | 40.56 | $ 2.0 \times 10^{19} $ | $ 1.2 \times 10^{20} $ |
| Deep-Att + PosUnk Ensemble [32] | — | 40.4 | — | $ 8.0 \times 10^{20} $ |
| GNMT + RL Ensemble [31] | 26.30 | 41.16 | $ 1.8 \times 10^{20} $ | $ 1.1 \times 10^{21} $ |
| ConvS2S Ensemble [8] | 26.36 | 41.29 | $ 7.7 \times 10^{19} $ | $ 1.2 \times 10^{21} $ |
| **Transformer (base)** | **27.3** | **38.1** | $ 3.3 \times 10^{18} $ | — |
| **Transformer (big)** | **28.4** | **41.0** | $ 2.3 \times 10^{19} $ | — |

在 WMT 2014 英德翻译任务上，大 Transformer 模型超越此前所有已报告模型（包括集成模型）2.0 个 BLEU 以上，建立了 **28.4 BLEU** 的新纪录。训练在 8 块 P100 GPU 上仅用 3.5 天。即使是基础模型也超越了所有已发布的模型和集成模型，且训练成本仅为竞争模型的一小部分。

在 WMT 2014 英法翻译任务上，大模型取得 **41.0 BLEU**，超越所有已发布的单模型，训练成本不到此前最优模型的 1/4。

推理设置：基础模型取最后 5 个检查点的平均；大模型取最后 20 个检查点的平均。使用束搜索（Beam Search），束宽 4，长度惩罚 $ \alpha = 0.6 $。

### 6.2 模型变体

**Table 3 关键消融实验结果**（在 newstest2013 开发集上）

| 配置 | $ N $ | $ d_{\text{model}} $ | $ d_{ff} $ | $ h $ | $ d_k $ | $ d_v $ | $ P_{drop} $ | $ \epsilon_{ls} $ | PPL | BLEU | 参数量 |
|------|-------|---------------------|-----------|-------|---------|---------|-------------|-------------------|-----|------|--------|
| base | 6 | 512 | 2048 | 8 | 64 | 64 | 0.1 | 0.1 | 4.92 | 25.8 | 65M |
| (A) $ h=1 $ | | | | 1 | 512 | 512 | | | 5.29 | 24.9 | |
| (A) $ h=16 $ | | | | 16 | 32 | 32 | | | 4.91 | 25.8 | |
| (A) $ h=32 $ | | | | 32 | 16 | 16 | | | 5.01 | 25.4 | |
| (E) 可学习位置嵌入 | | | | | | | | | 4.92 | 25.7 | |
| big | 6 | 1024 | 4096 | 16 | — | — | 0.3 | — | 4.33 | 26.4 | 213M |

**关键发现**：
- **(A) 注意力头数**：单头注意力比最佳设置差 0.9 BLEU；头数过多（32）也略有下降。$ h = 8 $ 是最优平衡点。
- **(B) 键维度**：减小 $ d_k $ 会损害模型质量，说明确定兼容性并非简单任务，可能需要比点积更复杂的兼容性函数。
- **(C) 模型规模**：更大的模型更好。
- **(D) Dropout**：Dropout 对避免过拟合非常关键。
- **(E) 位置编码**：正弦位置编码与可学习位置嵌入效果几乎相同。

---

## 7 结论

本文提出了 Transformer——第一个完全基于注意力的序列转换模型，用多头自注意力取代了编码器-解码器架构中最常用的循环层。

对于翻译任务，Transformer 的训练速度显著快于基于循环或卷积层的架构。在 WMT 2014 英德和英法翻译任务上均达到了新的最优水平。在英德任务上，最佳模型甚至超越了所有先前报告的集成模型。

作者对基于注意力的模型的未来充满期待，计划将其应用于其他任务，包括涉及文本以外的输入输出模态（如图像、音频和视频）的问题，以及研究局部受限注意力机制以高效处理大规模输入输出。使生成过程不那么顺序化也是研究目标之一。

---

## 核心数学公式汇总

| 编号 | 名称 | 公式 | 作用 |
|------|------|------|------|
| (1) | 缩放点积注意力 | $ \mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V $ | 核心注意力计算，通过缩放防止大维度下梯度消失 |
| — | 多头注意力 | $ \mathrm{MultiHead}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1, \ldots, \mathrm{head}_h) W^O $ | 并行多组注意力，捕获不同子空间的信息 |
| — | 注意力头 | $ \mathrm{head}_i = \mathrm{Attention}(QW_i^Q, KW_i^K, VW_i^V) $ | 投影到低维子空间后执行注意力 |
| (2) | 前馈网络 | $ \mathrm{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2 $ | 逐位置非线性变换，升维后降维 |
| — | 位置编码 (sin) | $ PE_{(pos,2i)} = \sin(pos / 10000^{2i/d_{\text{model}}}) $ | 编码绝对位置，支持相对位置的线性表达 |
| — | 位置编码 (cos) | $ PE_{(pos,2i+1)} = \cos(pos / 10000^{2i/d_{\text{model}}}) $ | 与 sin 配合形成旋转编码 |
| (3) | 学习率调度 | $ lrate = d_{\text{model}}^{-0.5} \cdot \min(step^{-0.5}, step \cdot warmup^{-1.5}) $ | 预热后衰减，自适应模型维度 |
| — | 残差连接 | $ \mathrm{LayerNorm}(x + \mathrm{Sublayer}(x)) $ | 缓解深层网络梯度问题 |

---

## 方案演进对比

| 维度 | Transformer (本文, 2017) | Seq2Seq + Attention (Bahdanau, 2014) | ConvS2S (Gehring, 2017) | GNMT (Wu et al., 2016) | BERT (Devlin, 2018) | GPT-2/3 (Radford/Brown, 2019/2020) |
|------|------------------------|--------------------------------------|------------------------|----------------------|---------------------|--------------------------------------|
| 核心思路 | 纯注意力，无循环无卷积 | RNN + 加性注意力 | 全卷积 + 注意力 | 深层 LSTM + 注意力 + RL | Transformer 编码器，掩码语言模型 | Transformer 解码器，自回归语言模型 |
| 输入/输出 | 序列→序列 | 序列→序列 | 序列→序列 | 序列→序列 | 序列→表示 | 前缀→续写 |
| 关键技术 | 多头自注意力、位置编码、残差+层归一化 | 双向 RNN + 对齐模型 | 门控卷积 + 多步注意力 | 8层 LSTM + 残差 + RL微调 | MLM + NSP 预训练 | 大规模自回归预训练、上下文学习 |
| 数学框架 | 缩放点积注意力 | 加性注意力（MLP 兼容性函数） | 点积注意力 + 位置嵌入 | 加性注意力 | 与 Transformer 相同 | 与 Transformer 相同 |
| 并行化能力 | 高（$ O(1) $ 顺序操作） | 低（$ O(n) $ 顺序操作） | 高（$ O(1) $ 顺序操作） | 低（$ O(n) $ 顺序操作） | 高（继承 Transformer） | 高（继承 Transformer） |
| 长距离依赖 | $ O(1) $ 路径长度 | $ O(n) $ 路径长度 | $ O(\log_k(n)) $ 路径长度 | $ O(n) $ 路径长度 | $ O(1) $ 路径长度 | $ O(1) $ 路径长度 |
| 实验规模 | WMT 2014, 8 GPU × 3.5天 | WMT 2014/15 | WMT 2014, 多 GPU | WMT 2014, 96 GPU | BookCorpus+Wikipedia, 64 TPU × 4天 | WebText/Internet, 数百 GPU/TPU |
| 优势 | 训练快、BLEU 高、可解释性 | 首次在 NMT 中引入注意力 | 并行训练高效 | 强工程优化 | 双向上下文、通用预训练 | 零/少样本学习、生成能力强 |
| 局限 | 自注意力 $ O(n^2) $ 对长序列不友好 | 训练慢、难并行 | 长距离依赖仍需多层 | 训练成本极高 | 仅编码器，不直接做生成 | 训练成本极高，单向注意力 |

> **演进趋势总结**：序列建模经历了从 RNN 主导（Seq2Seq, GNMT）→ CNN 尝试替代（ConvS2S, ByteNet）→ 纯注意力突破（Transformer）→ 大规模预训练（BERT, GPT）的发展脉络。Transformer 论文是这一演进中的**关键转折点**：它证明了注意力机制本身就足够强大，不需要循环或卷积作为"骨架"。此后，几乎所有主流 NLP 模型都采用 Transformer 架构，并通过增大规模和改变预训练策略（MLM vs. 自回归）衍生出两大路线——以 BERT 为代表的理解路线和以 GPT 为代表的生成路线。Transformer 的影响远不止 NLP，已扩展到计算机视觉（ViT）、语音（Whisper）、多模态（GPT-4V）、科学计算（AlphaFold 2）等领域。

---

## 参考文献

[1] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. *arXiv:1607.06450*, 2016.

[2] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. Neural machine translation by jointly learning to align and translate. *CoRR, abs/1409.0473*, 2014.

[3] Denny Britz, Anna Goldie, Minh-Thang Luong, and Quoc V. Le. Massive exploration of neural machine translation architectures. *CoRR, abs/1703.03906*, 2017.

[4] Jianpeng Cheng, Li Dong, and Mirella Lapata. Long short-term memory-networks for machine reading. *arXiv:1601.06733*, 2016.

[5] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, et al. Learning phrase representations using RNN encoder-decoder for statistical machine translation. *CoRR, abs/1406.1078*, 2014.

[6] François Chollet. Xception: Deep learning with depthwise separable convolutions. *arXiv:1610.02357*, 2016.

[7] Junyoung Chung, Çaglar Gülçehre, Kyunghyun Cho, and Yoshua Bengio. Empirical evaluation of gated recurrent neural networks on sequence modeling. *CoRR, abs/1412.3555*, 2014.

[8] Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolutional sequence to sequence learning. *arXiv:1705.03122*, 2017.

[9] Alex Graves. Generating sequences with recurrent neural networks. *arXiv:1308.0850*, 2013.

[10] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In *CVPR*, pages 770–778, 2016.

[11] Sepp Hochreiter, Yoshua Bengio, Paolo Frasconi, and Jürgen Schmidhuber. Gradient flow in recurrent nets: the difficulty of learning long-term dependencies, 2001.

[12] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. *Neural Computation*, 9(8):1735–1780, 1997.

[13] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring the limits of language modeling. *arXiv:1602.02410*, 2016.

[14] Łukasz Kaiser and Ilya Sutskever. Neural GPUs learn algorithms. In *ICLR*, 2016.

[15] Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, et al. Neural machine translation in linear time. *arXiv:1610.10099*, 2017.

[16] Yoon Kim, Carl Denton, Luong Hoang, and Alexander M. Rush. Structured attention networks. In *ICLR*, 2017.

[17] Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In *ICLR*, 2015.

[18] Oleksii Kuchaiev and Boris Ginsburg. Factorization tricks for LSTM networks. *arXiv:1703.10722*, 2017.

[19] Zhouhan Lin, Minwei Feng, et al. A structured self-attentive sentence embedding. *arXiv:1703.03130*, 2017.

[20] Samy Bengio, Łukasz Kaiser. Can active memory replace attention? In *NeurIPS*, 2016.

[21] Minh-Thang Luong, Hieu Pham, and Christopher D Manning. Effective approaches to attention-based neural machine translation. *arXiv:1508.04025*, 2015.

[22] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention model. In *EMNLP*, 2016.

[23] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive summarization. *arXiv:1705.04304*, 2017.

[24] Ofir Press and Lior Wolf. Using the output embedding to improve language models. *arXiv:1608.05859*, 2016.

[25] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words with subword units. *arXiv:1508.07909*, 2015.

[26] Noam Shazeer, Azalia Mirhoseini, et al. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. *arXiv:1701.06538*, 2017.

[27] Nitish Srivastava, Geoffrey E Hinton, et al. Dropout: a simple way to prevent neural networks from overfitting. *JMLR*, 15(1):1929–1958, 2014.

[28] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In *NeurIPS*, pages 2440–2448, 2015.

[29] Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural networks. In *NeurIPS*, pages 3104–3112, 2014.

[30] Christian Szegedy, Vincent Vanhoucke, et al. Rethinking the inception architecture for computer vision. *CoRR, abs/1512.00567*, 2015.

[31] Yonghui Wu, Mike Schuster, Zhifeng Chen, et al. Google's neural machine translation system: Bridging the gap between human and machine translation. *arXiv:1609.08144*, 2016.

[32] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu. Deep recurrent models with fast-forward connections for neural machine translation. *CoRR, abs/1606.04199*, 2016.
