# GAIA-1：面向自动驾驶的生成式世界模型

> **原文标题**: GAIA-1: A Generative World Model for Autonomous Driving
> **作者**: Anthony Hu\*, Lloyd Russell\*, Hudson Yeo\*, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, Gianluca Corrado (\*共同第一作者)
> **机构**: Wayve
> **arXiv**: 2309.17080 (2023年9月)

---

## 摘要

自动驾驶有望为交通运输带来变革性的改进，但构建能够在现实世界非结构化复杂场景中安全导航的系统仍然充满挑战。一个核心问题在于：如何有效地预测随着世界演变、车辆采取不同动作后可能出现的各种潜在结果。

为了应对这一挑战，我们提出了 GAIA-1（"Generative AI for Autonomy"，生成式自主智能），这是一个生成式世界模型，利用**视频、文本和动作**三种输入来生成逼真的驾驶场景，同时提供对自车（ego-vehicle）行为和场景特征的细粒度控制。我们的方法将世界建模转化为一个**无监督序列建模**问题，通过将输入映射为离散 token，然后预测序列中的下一个 token 来实现。我们模型展现出的涌现特性（emerging properties）包括：学习高层结构和场景动态、上下文感知、泛化能力以及对几何结构的理解。GAIA-1 学习到的表征能够捕获对未来事件的预期，结合其生成逼真样本的能力，为自动驾驶技术的增强和加速训练提供了新的可能。

---

## 1 引言

预测未来事件是自主系统的一项基本而关键的能力。准确的未来预测使自动驾驶车辆能够预见和规划其行动，从而提高道路安全性和效率。为实现这一目标，构建一个健壮的世界模型至关重要 [1]，过去已有大量工作致力于为自动驾驶构建这样的预测性世界模型 [2, 3, 4, 5, 6]。世界模型 [7, 8] 学习环境的结构化表征和理解，可用于在驾驶时做出明智的决策。

然而，当前的方法存在重大局限性。世界模型已成功应用于模拟环境 [9, 10, 11, 12, 13] 和真实世界机器人任务 [14, 15] 中的控制问题。这些方法通常依赖于标注数据——而大规模标注数据的获取极具挑战性——且在模拟数据上有效的模型可能无法完全捕捉真实世界场景的复杂性。此外，由于使用低维表征，这些模型在生成未来事件的高度逼真样本方面可能力不从心，这为在自动驾驶等复杂现实应用中实现高保真预测带来了困难。

与此同时，生成式图像和视频生成领域的进展已经利用自监督学习的力量，从大量真实世界数据中学习并生成极为逼真的视频样本 [16, 17, 18]。然而，该领域仍存在一个重大挑战：难以学习到能够捕捉预期未来事件的表征。虽然此类生成模型擅长生成视觉上令人信服的内容，但在学习对于精确未来预测和复杂场景中稳健决策至关重要的世界演化动态表征方面可能不足。

在这项工作中，我们提出了 GAIA-1，一种旨在兼顾世界模型和生成式视频生成双重优势的方法。它将生成式视频模型的**可扩展性和逼真度**与世界模型学习**有意义的未来演化表征**的能力相结合。GAIA-1 的工作方式如下：首先，我们将模型划分为两个组件：**世界模型**和**视频扩散解码器**。世界模型负责对场景的高层组件和动态进行推理，而扩散模型负责将潜在表征转化回具有逼真细节的高质量视频。

对于世界模型，我们使用视频帧的向量量化（vector-quantized）表征将每一帧离散化，转换为 token 序列。随后，我们将预测未来的挑战重新表述为预测序列中的下一个 token [10, 19]。这一方法近年来被广泛用于训练大语言模型 [20, 21, 22, 23]，并且以通过扩大模型规模和数据量来提升模型性能而著称。可以通过自回归生成在世界模型的潜在空间中生成样本。

第二个组件是一个多任务视频扩散解码器，能够执行高分辨率视频渲染以及时间上采样，从世界模型自回归生成的信息中生成流畅的视频。与大语言模型类似，视频扩散模型也展现了训练规模与整体性能之间的明确相关性，使 GAIA-1 的两个组件都适合于有效的复合扩展（compound scaling）。

GAIA-1 被设计为多模态系统，允许使用视频、文本和动作作为提示来生成多样且逼真的驾驶场景。通过在大规模英国城市驾驶真实数据上进行训练，GAIA-1 学会了理解和解耦（disentangle）重要概念，如静态和动态元素，包括汽车、公共汽车、行人、骑行者、道路布局、建筑物甚至红绿灯。此外，它通过动作和语言条件提供对自车行为和其他场景特征的细粒度控制。

GAIA-1 展示了展现真实世界生成规则的能力。**涌现特性**如学习高层结构、泛化、创造力和上下文感知表明，该模型能够理解和再现世界的规则与行为。此外，GAIA-1 展示了对 3D 几何的理解，例如有效地捕捉因路面不平（如减速带）引起的俯仰和横滚之间的复杂相互作用。它展示了其他智能体的反应性行为，证明了理解道路使用者决策中因果关系的能力。出人意料的是，它展现了成功外推到训练数据之外的能力，例如驾驶超出道路边界的场景。

GAIA-1 学习到的表征预测未来事件的能力，加上对自车动力学和场景元素的控制，是一个激动人心的进展，为改进具身智能和提供合成数据以加速训练和验证铺平了道路。世界模型（如 GAIA-1）是预测下一步可能发生什么的基础，这对于自动驾驶中的决策制定具有根本性的重要意义。

---

## 2 模型

本节描述 GAIA-1 中可训练组件的模型架构。总体架构如图 2 所示。

### 2.1 编码视频、文本和动作

GAIA-1 可以利用三种不同的输入模态（视频、文本、动作），它们被编码到一个共享的 $d$ 维空间中。

#### 图像 Token

每个视频帧被表示为离散 token。为此，我们使用预训练的图像分词器进行离散化（预训练细节见第 2.2 节）。

形式化地，考虑一个由 $T$ 张图像组成的序列 $(x_1, \ldots, x_T)$，其中每张图像 $x_t$ 使用预训练图像分词器离散化为 $n = 576$ 个离散 token。我们得到一个序列 $(z_1, \ldots, z_T)$，其中每个 $\mathbf{z}_t = (z_{t,1}, \ldots, z_{t,n}) \in \mathbb{R}^n$ 对应 $n = \frac{H}{D} \times \frac{W}{D}$ 个离散 token。这里 $H$ 和 $W$ 分别表示输入图像的高度和宽度，$D$ 表示图像分词器的下采样因子。这些离散 token 随后通过一个与世界模型一起训练的嵌入层映射到 $d$ 维空间。

> **数学原理解读**：
>
> 图像分词的核心思想是**空间压缩**。一张尺寸为 $H \times W$ 的图像，经过下采样因子 $D=16$ 后，变为 $\frac{H}{D} \times \frac{W}{D}$ 个 token。对于本文使用的 $288 \times 512$ 图像：
>
> $$
> n = \frac{288}{16} \times \frac{512}{16} = 18 \times 32 = 576
> $$
>
> 每个 token 不再是一个像素，而是一个**语义单元**——它代表了 $16 \times 16 = 256$ 个像素区域的离散化表示。这类似于 NLP 中的分词（tokenization）：像素类比于字符，而图像 token 类比于词。通过向量量化（VQ），连续的图像特征被映射到一个有限大小的码本（codebook）中最近的向量，从而实现离散化。

#### 文本 Token

在每个时间步 $t$，我们同时纳入文本和动作信息。文本输入使用预训练的 T5-large 模型 [24] 编码，产生每个时间步 $m = 32$ 个文本 token。这些 token 通过一个与世界模型联合训练的线性层映射到 $d$ 维空间。此过程产生的文本表征记为：

$$
\mathbf{c}_t = (c_{t,1}, \ldots, c_{t,m}) \in \mathbb{R}^{m \times d}
$$

#### 动作 Token

对于动作，我们考虑 $l = 2$ 个标量值（分别表示速度和曲率）。每个标量通过一个与世界模型联合训练的线性层独立映射到 $d$ 维空间。因此，时间步 $t$ 的动作表示为：

$$
\mathbf{a}_t = (a_{t,1}, \ldots, a_{t,l}) \in \mathbb{R}^{l \times d}
$$

#### Token 交错排列与位置编码

对于每个时间步，输入 token 按以下顺序交错排列：**文本 - 图像 - 动作**。世界模型的最终输入因此为：

$$
(\mathbf{c}_1, \mathbf{z}_1, \mathbf{a}_1, \ldots, \mathbf{c}_T, \mathbf{z}_T, \mathbf{a}_T)
$$

为了编码输入 token 的位置，我们使用**分解的时空位置嵌入**（factorized spatio-temporal positional embedding）：

1. **时间嵌入**：一个可学习的时间嵌入在给定时间步的所有 token 之间共享，共有 $T$ 个时间嵌入。
2. **空间嵌入**：一个可学习的空间嵌入指示 token 在一个时间步内的位置，共有 $m + n + l = 32 + 576 + 2 = 610$ 个空间嵌入，维度为 $d = 4096$。

> **数学原理解读**：
>
> 分解的时空位置编码是一种高效的位置表示方式。如果不进行分解，对于总序列长度 $T \times 610 = 15860$ 个 token，需要 15860 个独立的位置嵌入。通过分解为时间维度 $T$ 个嵌入和空间维度 610 个嵌入，参数量从 $O(T \times 610)$ 降低到 $O(T + 610)$，并且这种分解自然地反映了数据的时空结构——相同时间步的 token 共享时间信息，相同位置类型的 token（如第 3 个图像 token）在不同时间步间共享空间语义。
>
> 每个 token 的最终位置嵌入是其时间嵌入和空间嵌入的叠加：
>
> $$
> PE(t, i) = TemporalEmb(t) + SpatialEmb(i)
> $$
>
> 其中 $t$ 是时间步索引，$i$ 是该 token 在一个时间步内的位置索引。

### 2.2 图像分词器

在使用序列模型建模离散输入数据时，存在**序列长度**和**词汇表大小**之间的权衡。序列长度是描述数据所需的离散 token 数量，词汇表大小是单个 token 可以取值的数量。

对于语言，token 有两个明显的选择：字符和单词。使用字符级 token 时，输入数据具有更长的序列长度，每个 token 属于较小的词汇表但传达的含义很少。使用单词级 token 时，输入数据具有较短的序列长度，每个 token 包含大量语义但词汇表极大。大多数语言模型 [25, 26, 24, 21, 27, 22] 使用字节对编码（byte-pair encoding，BPE）或等效方法作为字符级和单词级分词的折中。

类似地，对于视频，我们希望减少输入的序列长度，同时可能使词汇表更大，但 token 要比原始像素更具语义意义。我们通过**离散图像自编码器** [28] 来实现。在这个第一阶段，我们希望实现两个目标：

1. **压缩信息**：将原始像素信息压缩，使序列建模问题可处理。图像包含大量冗余和噪声信息，我们希望减少描述输入数据所需的序列长度。
2. **引导压缩朝向有意义的表征**：如语义信息，而非高频信号。这样世界模型的输入空间更易于组合学习，且不会被显著减慢学习过程的高频信号所主导。

#### 空间压缩

我们通过在高度和宽度两个方向上将每张输入图像下采样 $D = 16$ 倍来减少输入数据的序列长度。每张尺寸为 $H \times W$ 的图像 $x_t$ 用 $n = \frac{H}{D} \times \frac{W}{D}$ 个 token 描述，词汇表大小为 $K$。

#### DINO 蒸馏

受 [29] 启发，我们通过回归预训练 DINO 模型 [30] 的潜在特征来引导压缩朝向有意义的表征。DINO 是一个已知包含语义信息的自监督图像模型。

离散自编码器是一个全卷积的 2D U-Net [31]。编码器 $E_\theta$ 使用从可学习嵌入表 [28] 的最近邻查找来量化图像特征，得到图像 token $\mathbf{z}_t = E_\theta(x_t)$。需要注意的是，解码器仅用于训练图像自编码器——只有离散编码器 $E_\theta$ 是最终 GAIA-1 模型的一部分。由于解码器是在单张图像上训练的，解码视频时缺乏时间一致性，因此我们还训练了一个视频解码器（见第 2.4 节）。

#### 图像自编码器的训练损失

1. **图像重建损失**：由 $L_1$、$L_2$、感知损失 $L_{perceptual}$ [32] 和 GAN 损失 $L_{GAN}$ [33] 的加权和组成。
2. **量化损失**：使用 [28] 中的嵌入损失（embedding loss）和承诺损失（commitment loss）来更新嵌入向量。我们采用了 [34] 的线性投影和 L2 归一化，因为我们发现这有助于提高词汇表的利用率。
3. **归纳偏置损失**：鼓励量化后的图像特征与预训练 DINO [30] 模型的图像特征匹配，使用余弦相似度损失。将 DINO 的信息蒸馏到学习的 token 中非常重要，因为这使它们能够受益于该模型的归纳偏置。

> **数学原理解读——向量量化（VQ）**：
>
> 向量量化的核心是将连续特征空间映射到有限的离散码本。设编码器输出的连续特征为 $\mathbf{e} \in \mathbb{R}^d$，码本为 $\{\mathbf{c}_1, \mathbf{c}_2, \ldots, \mathbf{c}_K\} \subset \mathbb{R}^d$，量化操作为：
>
> $$
> \mathbf{z}_q = \mathbf{c}_k, \quad k = \arg\min_j \|\mathbf{e} - \mathbf{c}_j\|_2
> $$
>
> 即选择码本中距离编码器输出最近的向量。这是一个不可微操作（argmin 不可微），因此在反向传播时使用**直通估计器**（straight-through estimator），将梯度直接从量化后的表征传递到编码器输出。
>
> **嵌入损失**将码本向量拉向编码器输出：
>
> $$
> L_{embed} = \|\mathbf{e} - sg(\mathbf{z}_q)\|_2^2
> $$
>
> **承诺损失**鼓励编码器输出保持接近码本向量（$sg$ 表示 stop gradient，即停止梯度计算）：
>
> $$
> L_{commit} = \|\mathbf{z}_q - sg(\mathbf{e})\|_2^2
> $$
>
> **比特压缩率**计算：原始图像 $288 \times 512 \times 3 \times 8$ 比特（3 通道 RGB，每通道 8 比特），压缩后 $18 \times 32 \times 13$ 比特（576 个 token，每个 token 从 $K=8192=2^{13}$ 的码本中选取，需要 13 比特编码），压缩比约为 470 倍：
>
> $$
> \frac{288 \times 512 \times 3 \times 8}{18 \times 32 \times 13} \approx 470
> $$

### 2.3 世界模型

如第 2.1 节所述，世界模型的输入为 $(\mathbf{c}_1, \mathbf{z}_1, \mathbf{a}_1, \ldots, \mathbf{c}_T, \mathbf{z}_T, \mathbf{a}_T)$。世界模型是一个自回归 Transformer 网络，对序列输入进行建模。其训练目标是在所有过去 token 的条件下预测序列中的下一个图像 token，使用 Transformer 块的注意力矩阵中的**因果掩码**（causal masking）[35]。

$$
L_{world\_model} = -\sum_{t=1}^{T} \sum_{i=1}^{n} \log p(z_{t,i} \mid \mathbf{z}_{<t},\, z_{t,j<i},\, \mathbf{c}_{\leq t},\, \mathbf{a}_{<t})
$$

**公式 (1)**

> **数学原理详解——世界模型损失函数**：
>
> 这是本文最核心的公式之一。让我们逐项分析：
>
> **1. 整体结构：负对数似然（交叉熵）**
>
> 损失函数是标准的自回归语言模型训练目标——最小化负对数似然。双重求和遍历所有时间步 $t$ 和每个时间步内的所有 token 位置 $i$。
>
> **2. 条件概率的含义**
>
> $p(z_{t,i} \mid \mathbf{z}_{<t},\, z_{t,j<i},\, \mathbf{c}_{\leq t},\, \mathbf{a}_{<t})$ 表示在给定以下条件下，第 $t$ 个时间步第 $i$ 个位置的图像 token 的概率分布：
>
> - $\mathbf{z}_{<t}$：所有之前时间步的图像 token（过去的视觉观察）
> - $z_{t,j<i}$：当前时间步中位置在 $i$ 之前的图像 token（同帧的已生成 token）
> - $\mathbf{c}_{\leq t}$：截至当前时间步的所有文本 token（包括当前步）
> - $\mathbf{a}_{<t}$：所有之前时间步的动作 token
>
> **3. 因果性**
>
> 注意条件中文本用 $\mathbf{c}_{\leq t}$（包含当前时间步），而动作用 $\mathbf{a}_{<t}$（不包含当前步）。这反映了物理因果关系：当前时刻的文本描述（如"前方有行人"）是对当前场景的描述，而动作的效果需要到下一时刻才能观察到。
>
> **4. 自回归分解**
>
> 这个损失函数体现了概率的链式法则（chain rule）。整个视频序列的联合概率被分解为一系列条件概率的乘积：
>
> $$
> p(\mathbf{z}_1, \mathbf{z}_2, \ldots, \mathbf{z}_T) = \prod_{t=1}^{T} \prod_{i=1}^{n} p(z_{t,i} \mid \mathbf{z}_{<t},\, z_{t,j<i},\, \mathbf{c}_{\leq t},\, \mathbf{a}_{<t})
> $$
>
> 最小化负对数似然等价于最大化数据的对数似然，即让模型尽可能准确地预测每一个 token。
>
> **5. 与语言模型的类比**
>
> 在 GPT 等语言模型中，目标是 $-\sum_i \log p(w_i \mid w_{<i})$。GAIA-1 将其扩展到多模态、多时间步的场景：每个"词"变成了图像 token，"上下文"不仅包括之前的图像 token，还包括文本和动作信息。

我们在训练过程中随机 dropout 条件 token，使得世界模型可以进行：(i) 无条件生成，(ii) 动作条件生成，以及 (iii) 文本条件生成。

为了进一步减少世界模型的序列长度，我们将视频从 25Hz 时间降采样到 6.25Hz。这使世界模型能够在不导致序列长度难以处理的情况下对更长时间段进行推理。为了在全帧率下恢复视频预测，我们使用第 2.4 节描述的视频解码器进行时间超分辨率。

### 2.4 视频解码器

沿循图像 [36, 37] 和视频生成 [16, 18] 的最新进展，我们使用**去噪视频扩散模型**（denoising video diffusion model）作为 GAIA-1 的解码器。一种朴素的方法是独立地将每帧 token 解码到像素空间，但这会导致时间上不一致的视频输出。将问题建模为在扩散过程中去噪一系列帧——模型可以在时间维度上访问信息——极大地改善了输出视频的时间一致性。

我们遵循 [38] 使用具有**分解的空间和时间注意力层**的 3D U-Net。训练期间，视频扩散模型以使用预训练图像分词器 $E_\theta$ 离散化输入图像得到的图像 token 为条件。推理时，扩散模型以世界模型预测的图像 token 为条件。

我们训练一个单一模型来联合处理图像和视频生成任务。在视频上训练教会解码器保持时间一致性，而在图像上训练对于单帧的质量至关重要 [16]，因为它教会模型从条件图像 token 中提取信息。训练图像时禁用时间层。

为了训练视频扩散解码器以执行多种推理任务，我们受 [17] 启发，通过掩码某些帧或条件图像 token 来执行多种任务。我们选择训练一个单一的视频扩散模型来处理所有任务，因为已有研究表明多任务训练可以提高单个任务的性能 [17]。这些任务包括：**图像生成**、**视频生成**、**自回归解码**和**视频插帧**。每个任务被等概率采样。例如，对于自回归生成任务，我们提供之前生成的历史帧作为上下文，以及我们想要预测的帧的条件图像 token。我们同时包含前向和后向自回归任务。我们还以概率 $p = 0.15$ 随机掩码每个条件图像 token 作为条件 dropout，因为这有助于模型泛化到不依赖 token 信息的情况并改善时间一致性。

视频解码器在噪声预测目标上训练。更具体地，我们使用 [39] 提出的 **v-参数化**（v-parameterization），因为它避免了不自然的颜色偏移并保持了长期一致性，这与 [16] 的发现类似。在实践中，我们使用 $L_1$ 和 $L_2$ 损失的加权平均。视频解码器损失 $L_{video}$ 为：

$$
L_{video} = \mathbb{E}_{\epsilon, t'} \left[ \|\epsilon_\theta(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m}) - \epsilon\|_2^2 \right]
$$

**公式 (2)**

其中：

- $\epsilon_\theta$ 是去噪视频模型。
- $\epsilon$ 是去噪目标，使用 v-参数化。
- $t' \sim U(0, 1)$ 是采样的离散扩散时间步。
- $\mathbf{x} = (x_1, \ldots, x_{T'})$ 是长度为 $T'$ 的视频序列。
- $\mathbf{x}_{t'} = \alpha_{t'} \mathbf{x} + \sigma_{t'} \epsilon$ 表示加噪后的视频，其中 $\alpha_{t'}$ 和 $\sigma_{t'}$ 是 $t'$ 的函数，定义了噪声调度。
- $\mathbf{z} = (z_1, \ldots, z_{T'}) = E_\theta(\mathbf{x})$ 是条件图像 token 序列。
- $\mathbf{m} = (m_1, \ldots, m_{T'})$ 是由训练任务指定的图像掩码序列（见图 4）。

> **数学原理详解——扩散模型与 v-参数化**：
>
> **扩散模型基础**
>
> 扩散模型包含两个过程：
>
> **前向过程（加噪）**：逐步向数据添加高斯噪声，将数据分布 $q(\mathbf{x}_0)$ 转化为纯噪声分布 $\mathcal{N}(\mathbf{0}, \mathbf{I})$：
>
> $$
> \mathbf{x}_{t'} = \alpha_{t'} \mathbf{x}_0 + \sigma_{t'} \epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})
> $$
>
> 其中 $\alpha_{t'}$ 和 $\sigma_{t'}$ 定义了噪声调度（noise schedule），满足 $\alpha_{t'}^2 + \sigma_{t'}^2 = 1$（通常情况）。当 $t' \to 0$ 时 $\alpha_{t'} \to 1, \sigma_{t'} \to 0$（接近原始数据），当 $t' \to 1$ 时 $\alpha_{t'} \to 0, \sigma_{t'} \to 1$（接近纯噪声）。
>
> **反向过程（去噪）**：学习从噪声中恢复数据。模型 $\epsilon_\theta$ 被训练来预测添加的噪声（或等效的 v 目标）。
>
> **v-参数化**
>
> 标准扩散模型训练预测噪声 $\epsilon$，即 $\epsilon$-参数化。v-参数化定义了一个新的预测目标：
>
> $$
> \mathbf{v} = \alpha_{t'} \epsilon - \sigma_{t'} \mathbf{x}_0
> $$
>
> v-参数化的优势在于：
>
> - 在不同噪声水平下提供更稳定的训练信号
> - 避免颜色偏移问题（这在视频生成中尤为重要）
> - 保持长期时间一致性
>
> 直觉上，$\mathbf{v}$ 可以理解为在加噪过程中数据的"速度"——它描述了从 $\mathbf{x}_0$ 到 $\epsilon$ 的方向。
>
> **条件化机制**
>
> 本文的扩散模型以两种额外信息为条件：
>
> - $\mathbf{z}$：图像 token（来自世界模型的预测），提供场景的语义和结构信息
> - $\mathbf{m}$：掩码序列，指定哪些帧需要生成、哪些帧作为上下文
>
> 这使得同一个扩散模型可以灵活地用于不同任务（图像生成、视频生成、自回归解码、视频插帧），只需改变掩码 $\mathbf{m}$ 的模式。

---

## 3 数据

我们的训练数据集包含 4700 小时的专有驾驶数据，以 25Hz 采集于 2019 年至 2023 年间的英国伦敦，对应约 4.2 亿张独立图像。训练过程中，我们在一组可定制的特征上进行平衡采样以控制数据分布（图 5）。

我们通过以与给定特征的（分桶并预计算的）经验分布成反比的权重对单个数据点进行采样来实现这一点。对于给定样本，我们取所有特征的联合概率来进行平衡，并随机决定是否纳入或丢弃该样本。我们可以通过将采样权重提升到一个指数来控制平衡的强度：指数为 0 将产生经验分布（无平衡），指数为 1 将产生均匀平衡的分布。我们对所有特征使用 0.5 的指数，作为最终平衡效果和因丢弃样本对训练效率影响之间的折中。

**对于分词器**，我们在（纬度、经度、天气类别）上进行平衡，以考虑地理位置和视觉上不同的天气条件，确保分词器能充分表示多样化的场景。

**对于世界模型和视频扩散模型**，我们在（纬度、经度、天气类别、转向行为类别、速度行为类别）上进行平衡，额外考虑速度和转向行为，以确保不同行为的动态特征被世界模型和时间解码器充分捕捉和建模。

我们的验证数据集包含 400 小时的驾驶数据，来自未包含在训练集中的行程。选择用于验证的行程是通过预设地理围栏（geofence）以及随机选择的行程。我们进一步将验证集分为严格地理围栏（仅分析严格位于验证地理围栏内的样本，即训练期间从未见过的道路）和围绕主要数据采集路线的地理围栏（训练期间见过的道路），以监控过拟合和泛化性能。

---

## 4 训练流程

本节描述 GAIA-1 三个可训练组件的优化方式，提供超参数配置、硬件使用和训练时间的详细信息。

### 4.1 图像分词器

图像分词器（0.3B 参数）在分辨率 $H \times W = 288 \times 512$（9:16 比例）的图像上训练。编码器的空间下采样为 $D = 16$，因此每张图像被编码为 $n = 18 \times 32 = 576$ 个离散 token，词汇表大小 $K = 8192$。比特压缩率为：

$$
\frac{288 \times 512 \times 3 \times 8}{18 \times 32 \times 13} \approx 470
$$

离散自编码器使用 AdamW [40] 优化，学习率 $1 \times 10^{-4}$，权重衰减 0.01，beta 系数 (0.5, 0.9)。损失权重为：

| 损失项 | 权重 |
|--------|------|
| $\lambda_{L_1}$ | 0.2 |
| $\lambda_{L_2}$ | 2.0 |
| $\lambda_{L_{perceptual}}$ | 0.1 |
| $\lambda_{L_{GAN}}$ | 1.0 |
| $\lambda_{L_{codebook}}$ | 1.0 |
| $\lambda_{L_{DINO}}$ | 0.1 |

模型训练 200k 步，耗时 4 天，batch size 为 160，分布在 32 块 A100 80GB GPU 上。使用 5k 步线性预热和 10k 步余弦衰减至最终学习率 $1 \times 10^{-5}$。

### 4.2 世界模型

世界模型（6.5B 参数）在大小为 $T = 26$ 的视频序列上以 6.25 Hz 训练，对应 4 秒长的视频。文本编码为每时间步 $m = 32$ 个文本 token，动作为 $l = 2$ 个 token。世界模型的总序列长度为：

$$
T \times (m + n + l) = 26 \times (32 + 576 + 2) = 26 \times 610 = 15860
$$

世界模型使用 AdamW 优化，学习率 $1 \times 10^{-4}$，权重衰减 0.1，beta 系数 (0.9, 0.95)，梯度范数裁剪 1.0。训练样本为无条件、动作条件或文本条件，比例分别为 20%/40%/40%。

模型训练 100k 步，耗时 15 天，2.5k 步线性预热和 97.5k 步余弦衰减，在训练过程中将学习率降低 10 倍。batch size 为 128，分布在 64 块 A100 80GB GPU 上。使用 FlashAttention v2 实现 [41]，在内存利用和推理速度方面提供了显著优势。为优化分布式训练，使用 DeepSpeed ZeRO-2 训练策略 [42] 和激活检查点（activation checkpointing）。

### 4.3 视频解码器

视频解码器（2.6B 参数）在 $T' = 7$ 帧图像序列上训练，分辨率 $H \times W = 288 \times 512$，采样频率为 6.25 Hz、12.5 Hz 或 25 Hz。训练任务（图 4）以等概率采样。使用余弦 $\beta$-噪声调度 [43]。

视频解码器使用 AdamW 优化，学习率 $5 \times 10^{-5}$，权重衰减 0.01，beta 系数 (0.9, 0.99)，梯度范数裁剪 1.0。模型训练 300k 步，耗时 15 天，2.5k 步线性预热和 5k 步余弦衰减至最终学习率 $1 \times 10^{-6}$。使用 $L_1$ 和 $L_2$ 损失的加权平均，权重 $\lambda_{L_1} = 0.1$ 和 $\lambda_{L_2} = 1.0$。batch size 为 64，分布在 32 块 A100 80GB GPU 上。使用衰减率 0.999 的指数移动平均（EMA）。训练策略同样为 DeepSpeed ZeRO-2 加激活检查点。

> **训练规模汇总**：
>
> | 组件 | 参数量 | GPU | 训练步数 | 训练时间 |
> |------|--------|-----|----------|----------|
> | 图像分词器 | 0.3B | 32×A100 | 200k | 4天 |
> | 世界模型 | 6.5B | 64×A100 | 100k | 15天 |
> | 视频解码器 | 2.6B | 32×A100 | 300k | 15天 |
> | **总计** | **约 9.4B** | — | — | **约 34天** |

---

## 5 推理

本节更详细地描述世界模型和视频解码器的推理过程。

### 5.1 世界模型推理

#### 采样策略

世界模型以自回归方式预测下一个图像 token，以之前的文本、图像和动作 token 为条件。给定过去的 token，我们执行 $n$ 次前向步骤来生成一个新的图像帧。在每一步，我们必须从预测的 logits 中采样一个 token 来选择序列中的下一个 token。

经验上我们观察到，基于最大化的采样（即 argmax）会生成陷入重复循环的未来，类似于语言模型 [44]。相反，如果我们简单地从 logits 采样，选择的 token 可能来自概率分布的不可靠尾部，这会将模型推至分布外（out-of-distribution）。

为了同时鼓励多样性和逼真度，我们采用 **top-k 采样**从 top-k 个最可能的选择中采样下一个图像 token。选择的 $k$ 值是构成一个图像帧的 token 数量和预学习码本（词汇表）大小的函数。

我们的世界模型可以用于在给定起始上下文的情况下展开可能的未来，也可以在没有任何起始上下文的情况下从头生成未来。对于长视频生成，如果视频长度超过世界模型的上下文长度，我们采用**滑动窗口**策略。

> **数学原理解读——采样策略的概率分析**：
>
> 在每个生成步骤中，Transformer 输出一个 logits 向量 $\boldsymbol{\ell} \in \mathbb{R}^K$（$K=8192$ 为词汇表大小），通过 softmax 转换为概率分布：
>
> $$
> p(z = k) = \frac{\exp(\ell_k)}{\sum_{j=1}^{K} \exp(\ell_j)}
> $$
>
> **Argmax 采样**：$z^* = \arg\max_k p(z = k)$。这是确定性的，总是选择概率最高的 token。问题在于它会导致退化——连续帧趋于重复相同的模式，因为高概率 token 的组合倾向于形成固定点。
>
> **全分布采样**：$z \sim p(z)$。虽然保持了多样性，但可能从低概率的尾部采样到不合理的 token，一个异常 token 就可能破坏后续所有预测（误差累积）。
>
> **Top-k 采样**：将概率分布截断到 top-k 个最可能的 token，然后在这个截断分布中重新归一化并采样：
>
> $$
> p'(z = k) = \begin{cases} \dfrac{p(z=k)}{\sum_{j \in S_k} p(z=j)}, & k \in S_k \\ 0, & k \notin S_k \end{cases}
> $$
>
> 其中 $S_k$ 是概率最高的 $k$ 个 token 的集合。这在多样性和可靠性之间取得了平衡。论文实验表明 top-k=50 采样产生的 token 具有与真实图像 token 相似的困惑度分布。

#### 文本条件化

视频预测可以通过文本来提示和引导。训练时，我们用来自在线叙述或离线元数据源的文本来条件化视频序列。由于这些文本源并不完美，为了改善生成未来与文本提示之间的对齐，我们在推理时使用**无分类器引导**（classifier-free guidance）[45, 46]。

引导的效果是通过降低可能样本的多样性来增加文本-图像的对齐度。更精确地说，对于每个要预测的下一个 token，我们计算以文本为条件的 logits 以及无条件的 logits。在推理时，我们可以用一个缩放因子放大无条件和文本条件 logits 之间的差异，得到用于采样的最终 logits。

$$
\boldsymbol{\ell}_{final} = (1 + t) \cdot \boldsymbol{\ell}_{conditioned} - t \cdot \boldsymbol{\ell}_{unconditioned}
$$

**公式 (3)**

通过用以另一个文本提示为条件的 logits 替代无条件 logits，我们可以执行**"负面"提示**（negative prompting）[47]。将 logits 推离负面提示并朝向正面提示，鼓励未来的 token 包含"正面"提示特征同时移除"负面"特征。

> **数学原理详解——无分类器引导（CFG）**：
>
> 无分类器引导（Classifier-Free Guidance）是条件生成中的关键技术。其核心思想来源于贝叶斯定理的对数空间推导。
>
> **理论基础**：我们想要采样自 $p(z \mid c)$，其中 $c$ 是文本条件。根据贝叶斯定理：
>
> $$
> \log p(z \mid c) = \log p(c \mid z) + \log p(z) - \log p(c)
> $$
>
> 在 logits 空间中（忽略与 $z$ 无关的常数项）：
>
> $$
> \log p(z \mid c) \propto \log p(c \mid z) + \log p(z)
> $$
>
> 如果我们想"增强"条件信号，可以对似然项进行缩放：
>
> $$
> \log \tilde{p}(z \mid c) \propto (1+t) \log p(z \mid c) - t \log p(z)
> $$
>
> 在 logits 空间中，这正好对应公式 (3)：
>
> $$
> \boldsymbol{\ell}_{final} = (1+t) \cdot \boldsymbol{\ell}_{conditioned} - t \cdot \boldsymbol{\ell}_{unconditioned}
> $$
>
> **直觉理解**：
>
> - 当 $t = 0$ 时：$\boldsymbol{\ell}_{final} = \boldsymbol{\ell}_{conditioned}$，即标准条件生成
> - 当 $t > 0$ 时：放大了条件和无条件之间的差异，使生成更强烈地遵循文本提示
> - 当 $t < 0$ 时：生成会"远离"文本提示
>
> **引导调度**：论文发现对引导缩放因子进行调度非常重要，包括：
>
> - **在 token 维度上调度**：允许一些 token 以高引导采样（强烈遵循提示），另一些以低引导采样（增加多样性）
> - **在帧维度上调度**：控制从早期帧的过渡以及缓解连续帧上引导的累积效应
>
> 典型做法是在 token 上使用线性递减引导，在未来帧上使用余弦衰减（可选初始平台期）。

### 5.2 视频解码器推理

为了解码世界模型生成的 token 序列，我们使用以下视频解码方法：

1. **解码首批帧**：解码前 $T' = 7$ 帧，以对应的 $T'$ 个图像 token 为条件。
2. **自回归解码**：使用 2 个过去重叠帧作为图像上下文和接下来的 $T' - 2$ 个图像 token，自回归解码下一个 $T' - 2$ 帧。
3. **重复**：重复自回归过程直到在 6.25 Hz 下生成 $N$ 帧。
4. **时间上采样 1**：将 $N$ 帧从 6.25 Hz 上采样到 12.5 Hz。
5. **时间上采样 2**：将 $2N - 1$ 帧从 12.5 Hz 上采样到 25.0 Hz。

我们使用 DDIM 采样器 [48]，50 个扩散步骤。在自回归解码过程中，我们看到在将 token 信息内容反映在生成视频中和时间一致性之间存在权衡。为了平衡这两个目标，我们计算两种任务的加权平均 [18]：

$$
\tilde{\epsilon}_\theta(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m}) = w \cdot \epsilon_\theta^\pi(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m}) + (1-w) \cdot \epsilon_\theta(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m})
$$

**公式 (4)**

其中函数 $\epsilon_\theta^\pi(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m})$ 将每帧独立地作为图像去噪，函数 $\epsilon_\theta(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m})$ 将帧序列作为视频联合去噪。在实践中，我们只需开关时间层。我们在每个扩散步骤以概率 $p = 0.25$ 和权重 $w = 0.5$ 随机应用此加权平均。

> **数学原理详解——图像-视频联合去噪**：
>
> 公式 (4) 体现了一个精妙的设计，用于平衡**token 信息保真度**和**时间一致性**：
>
> - $\epsilon_\theta^\pi$（图像模式）：关闭时间注意力层，每帧独立去噪。优势是更忠实地反映每帧 token 的信息，劣势是帧间可能不连贯。
> - $\epsilon_\theta$（视频模式）：开启时间注意力层，帧序列联合去噪。优势是帧间平滑过渡，劣势是可能模糊掉某些帧特有的细节。
>
> 通过权重 $w = 0.5$ 的加权平均（概率 $p = 0.25$ 时应用），在大多数扩散步骤中使用纯视频模式（保证时间一致性），偶尔混入图像模式（锚定到每帧 token 的具体信息）。
>
> 这可以理解为一种**随机正则化**：在去噪轨迹的不同点引入单帧约束，防止视频模式的平滑操作过度抹除帧间差异。

在探索不同的视频解码推理方法时，我们发现从序列末尾开始向后自回归解码视频帧会导致更稳定的物体和更少的地平线闪烁。在整体视频解码方法中，我们因此先解码最后 $T'$ 帧，然后从那里向后自回归解码剩余帧。

---

## 6 缩放规律

GAIA-1 中世界建模任务的公式化与大语言模型（LLM）中常用的方法有共同之处。在两种情况下，任务都简化为预测下一个 token。尽管这种方法在 GAIA-1 中适用于世界建模而非传统的语言任务，但有趣的是，类似于在 LLM 中观察到的**缩放规律** [49, 21, 27] 也适用于 GAIA-1。这表明缩放原则在包括自动驾驶在内的不同 AI 领域中具有广泛的适用性。

为了探索 GAIA-1 的缩放规律，我们使用不到 20 倍计算量训练的模型来预测世界模型的最终性能。我们通过在保留的地理围栏验证集上测量交叉熵来评估这些模型。然后将幂律形式的函数拟合到数据点：

$$
f(x) = c + \left(\frac{x}{a}\right)^b
$$

**缩放规律幂律函数**

> **数学原理详解——缩放规律**：
>
> **幂律的含义**：
>
> 上式中 $x$ 是计算量（FLOPs），$f(x)$ 是验证集交叉熵（越低越好）。参数 $c$ 表示理论下限（即使计算无限大也无法突破的性能极限），$a$ 是缩放常数，$b < 0$ 是缩放指数。
>
> 这意味着性能（损失）随计算量呈幂律关系递减——每增加一个数量级的计算量，性能获得近似固定的改善。这与在大语言模型中观察到的 Kaplan 缩放规律 [49] 完全一致。
>
> **计算量估算**：
>
> 如果我们记 $C$ 为计算量，$N$ 为参数数量（不含嵌入层），则单个 token 前向-反向传播的浮点运算次数为：
>
> $$
> C_{per\_token} = 6N
> $$
>
> 其中因子 6 来自：前向传播约 $2N$ 次运算（每个参数参与一次乘法和一次加法），反向传播约为前向的 2 倍（需要计算参数梯度和激活梯度），总计 $6N$。总计算量为该值乘以训练 token 数量：
>
> $$
> C_{total} = 6N \times D
> $$
>
> 其中 $D$ 为训练 token 总数。
>
> **实验发现**：
>
> 用于拟合幂律的模型范围从 10000 倍到 10 倍更小的模型（参数从 0.65M 到 650M），即比最终 6.5B 模型小得多。使用这些小模型的训练曲线，可以高精度预测 6.5B 模型的最终性能。
>
> **深层意义**：
>
> 缩放规律的存在意味着：
>
> 1. **可预测性**：无需完成全部训练就能预估最终性能
> 2. **资源规划**：可以合理分配计算预算
> 3. **性能上限**：论文的外推表明，通过扩大数据和计算资源，仍有**大幅改进空间**
> 4. **通用性**：世界模型与语言模型共享相同的缩放行为，这验证了将世界建模转化为序列建模的方法论合理性

---

## 7 能力与涌现特性

本节通过一系列定性示例展示 GAIA-1 的能力和涌现特性。GAIA-1 通过以下涌现特性展现了对世界生成规则的理解和总结：

### 7.1 高层结构和场景动态的学习

GAIA-1 生成连贯的场景，物体放置在合理的位置并展现逼真的物体交互，如交通灯、道路规则、让行等。这表明模型不仅仅是记忆统计模式，而是理解了支配世界中物体排列和行为的底层规则。

GAIA-1 可以完全从想象中生成稳定的长视频（分钟级）。为此，模型利用其学习到的隐式世界先验分布来生成完全想象的逼真驾驶场景，包括复杂的道路布局、建筑物、汽车、行人等。

### 7.2 泛化与创造力

GAIA-1 能够基于单个初始提示生成多种不同的未来场景。当给出一段简短的视频作为上下文时，它可以通过重复采样生成众多合理且多样的结果。GAIA-1 准确地建模了响应视频提示的多种潜在未来场景，同时保持与视频中观察到的初始条件的一致性。

世界模型可以推理：

- **(i) 与道路使用者的动态交互**（如让行或不让行）
- **(ii) 多模态自车行为**（如在环形交叉口直行或转弯）
- **(iii) 多模态动态场景**（如可变的交通密度和道路使用者类型）和静态场景（如道路布局、建筑物、植被）

### 7.3 自车行为和驾驶场景的细粒度控制

GAIA-1 可以仅从文本提示生成视频，完全想象场景。例如，可以用文本提示引导模型生成特定天气或光照条件的驾驶场景。

更重要的是，模型展示了对视频中车辆动力学的细粒度控制。通过利用这种控制，我们可以提示模型生成描绘**训练数据边界之外**场景的视频。这表明 GAIA-1 能够将自车动力学与周围环境**解耦**，并有效地泛化到不熟悉的场景。

例如，让 GAIA-1 生成自车向左或向右转向、偏离车道的未来。GAIA-1 在用于训练的专家驾驶数据集中从未见过这些不正确的行为，这表明它可以**外推**到训练数据中未见过的驾驶概念。我们还看到其他智能体对自车控制行为的**逼真反应**。

这种能力意义重大：

- 提供了对行动对环境影响的显式推理能力（**安全性**）
- 允许对动态场景更丰富的理解（**智能**）
- 解锁了基于模型的策略学习（**在世界模型中规划**）
- 启用了闭环探索（**将世界模型视为神经模拟器**）

---

## 8 相关工作

### 视频生成模型

视频生成模型是能够生成逼真视频样本的神经网络，可分为四类：

| 类别 | 代表方法 | 优势 | 局限 |
|------|----------|------|------|
| **VAE 基础** | SVG [54], FitVid [58] | 潜变量推断 | 输出模糊，表示能力有限 |
| **GAN 基础** | MoCoGAN [60], DriveGAN [62] | 生成逼真 | 训练不稳定，多样性不足 |
| **扩散基础** | Imagen Video [16], 潜在扩散 [18] | 逼真、可控、时间一致 | 采样链长，速度慢 |
| **自回归基础** | VideoGPT [74], MAGVIT [80] | 概念简单，精确似然优化 | 生成速度慢 |

### 世界模型

世界模型是一种未来预测模型，学习世界的通用表征以理解其行动的后果 [7, 8]。主要用例包括：

1. **纯表征学习**：世界建模作为预训练任务，以自监督方式学习紧凑的通用表征 [82, 83]，加速后续强化学习的收敛。
2. **规划（前瞻搜索）**：通过想象未来行动的结果来规划，在游戏环境中已证明高效 [9, 84]。
3. **在世界模型中学习策略（神经模拟器）**：解决强化学习算法的样本效率问题 [7, 85, 86, 62, 13, 15, 87]。

最近的工作提议将世界建模转化为单一序列模型，将状态、动作和奖励视为简单的数据流 [10, 19, 14, 88, 12, 89]。这种视角的优势在于世界模型可以受益于应用于大规模无监督训练的高容量序列模型架构的缩放特性 [26]。这正是 GAIA-1 采取的方法。

### 缩放

大语言模型已经展示了扩大模型规模和数据的明确收益 [90, 24, 26, 20, 21, 22, 23]。特别是，[49] 展示了模型/数据大小与损失之间跨多个数量级的可预测关系。[49] 推导了基于 Transformer 的语言模型的幂律，以最优分配模型和数据大小之间的计算预算。这些规律随后被 [27] 通过在改变数据集大小时调整学习率调度来精化。

将大语言模型的缩放原则转移到视觉领域具有提供一致且可预期性能改进的潜力 [92, 93, 43, 16, 94]。在本工作中，通过将世界建模问题转化为无监督序列建模，我们展示了语言模型的类似缩放趋势同样适用于世界模型。

---

## 9 结论与未来工作

GAIA-1 是一个面向自动驾驶的生成式世界模型。世界模型使用向量量化表征将未来预测任务转化为下一个 token 预测任务——这一技术已在大语言模型中成功应用。GAIA-1 展示了获取环境全面理解的能力，通过自监督区分各种概念，如汽车、卡车、公共汽车、行人、骑行者、道路布局、建筑物和交通灯。此外，GAIA-1 利用视频扩散模型的能力生成逼真的驾驶场景，从而作为高级神经模拟器运行。GAIA-1 是一种多模态方法，通过文本和动作指令的组合实现对自车行为和其他场景属性的控制。

虽然我们的方法展示了有望推动自动驾驶边界的成果，但重要的是承认当前的局限性。例如，自回归生成过程虽然非常有效，但尚未达到实时运行。不过值得注意的是，该过程非常适合并行化，允许同时生成多个样本。

GAIA-1 的意义超越了其生成能力。世界模型代表了实现能够理解、预测和适应真实世界复杂性的自主系统的关键一步。此外，通过将世界模型纳入驾驶模型，我们可以使它们更好地理解自身决策并最终泛化到更多真实世界情况。最后，GAIA-1 还可以作为有价值的神经模拟器，允许生成无限数据（包括对抗样本），用于训练和验证自动驾驶系统。

---

## 核心数学公式汇总与深度解读

### 公式总览表

| 编号 | 名称 | 公式 | 作用 |
|------|------|------|------|
| (1) | 世界模型损失 | $L_{wm} = -\sum_{t,i} \log p(z_{t,i} \mid \cdot)$ | 自回归预测下一个图像 token |
| (2) | 视频解码器损失 | $L_{video} = \mathbb{E}[\|\epsilon_\theta(\cdot) - \epsilon\|^2]$ | 扩散模型去噪训练 |
| (3) | 无分类器引导 | $\boldsymbol{\ell}_f = (1+t)\boldsymbol{\ell}_c - t\boldsymbol{\ell}_u$ | 增强文本-视频对齐 |
| (4) | 图像-视频联合去噪 | $\tilde{\epsilon} = w\epsilon^\pi + (1-w)\epsilon$ | 平衡保真度和一致性 |
| — | 缩放规律 | $f(x) = c + (x/a)^b$ | 预测模型缩放性能 |
| — | 计算量估算 | $C = 6N$ | 计算 FLOPs |

### 整体数学框架

GAIA-1 的数学框架可以概括为一个**两阶段生成管道**：

**第一阶段：离散化与序列建模**

将连续的视频、文本、动作信号转化为离散 token 序列，然后用自回归 Transformer 建模这个序列的联合概率分布。核心是概率的链式法则分解：

$$
p(\mathbf{z}_{1:T} \mid \mathbf{c}_{1:T}, \mathbf{a}_{1:T}) = \prod_{t=1}^{T} \prod_{i=1}^{n} p(z_{t,i} \mid \mathbf{z}_{<t},\, z_{t,j<i},\, \mathbf{c}_{\leq t},\, \mathbf{a}_{<t})
$$

**第二阶段：连续化与渲染**

将离散 token 通过条件扩散模型映射回像素空间。扩散过程的核心是**分数匹配**（score matching）：

$$
\nabla_{\mathbf{x}_{t'}} \log p(\mathbf{x}_{t'} \mid \mathbf{z}) \approx -\frac{\epsilon_\theta(\mathbf{x}_{t'},\, t',\, \mathbf{z},\, \mathbf{m})}{\sigma_{t'}}
$$

即模型学习估计对数概率密度的梯度（分数函数），扩散采样沿着这个梯度场从噪声走向数据。

**两阶段的精妙之处**在于：世界模型在低维离散空间中进行"思考"（预测未来会发生什么），而扩散模型在高维连续空间中进行"渲染"（将思考结果转化为逼真图像）。这种分离使得：

1. 世界模型可以专注于**语义级别**的未来预测，不被像素细节困扰
2. 扩散模型可以专注于**高质量渲染**，不需要处理长时序依赖
3. 两个组件可以**独立扩展**，享受各自领域的缩放红利

---

## 参考文献

[1] A. Kendall et al., "Learning to drive in a day," ICRA, 2019.

[2] H. Caesar et al., "nuScenes: A multimodal dataset for autonomous driving," CVPR, 2020.

[3] A. Hu et al., "Probabilistic Future Prediction for Video Scene Understanding," ECCV, 2020.

[4] S. Ettinger et al., "Large Scale Interactive Motion Forecasting for Autonomous Driving: The Waymo Open Motion Dataset," ICCV, 2021.

[5] A. Hu et al., "FIERY: Future Instance Prediction in Bird's-Eye View From Surround Monocular Cameras," ICCV, 2021.

[6] Y. Hu et al., "Planning-oriented autonomous driving," CVPR, 2023.

[7] D. Ha and J. Schmidhuber, "Recurrent world models facilitate policy evolution," NeurIPS, 2018.

[8] Y. LeCun, "A Path Towards Autonomous Machine Intelligence," arXiv, 2022.

[9] J. Schrittwieser et al., "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model," Nature, 2020.

[10] M. Janner et al., "Offline reinforcement learning as one big sequence modeling problem," NeurIPS, 2021.

[11] A. Hu et al., "Model-Based Imitation Learning for Urban Driving," NeurIPS, 2022.

[12] V. Micheli et al., "Transformers are sample-efficient world models," ICLR, 2023.

[13] D. Hafner et al., "Mastering diverse domains through world models," arXiv, 2023.

[14] S. Reed et al., "A generalist agent," TMLR, 2022.

[15] P. Wu et al., "Daydreamer: World models for physical robot learning," CoRL, 2023.

[16] J. Ho et al., "Imagen video: High definition video generation with diffusion models," arXiv, 2022.

[17] W. Harvey et al., "Flexible diffusion modeling of long videos," NeurIPS, 2022.

[18] P. Esser et al., "Structure and content-guided video synthesis with diffusion models," arXiv, 2023.

[19] L. Chen et al., "Decision transformer: Reinforcement learning via sequence modeling," NeurIPS, 2021.

[20] S. Smith et al., "Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B," arXiv, 2022.

[21] A. Chowdhery et al., "PaLM: Scaling language modeling with pathways," arXiv, 2022.

[22] H. Touvron et al., "Llama: Open and efficient foundation language models," arXiv, 2023.

[23] OpenAI, "GPT-4 Technical Report," arXiv, 2023.

[24] C. Raffel et al., "Exploring the limits of transfer learning with a unified text-to-text transformer," JMLR, 2020.

[25] Y. Liu et al., "Roberta: A robustly optimized bert pretraining approach," arXiv, 2019.

[26] T. Brown et al., "Language Models are Few-Shot Learners," NeurIPS, 2020.

[27] J. Hoffmann et al., "An empirical analysis of compute-optimal large language model training," NeurIPS, 2022.

[28] A. van den Oord et al., "Neural discrete representation learning," NeurIPS, 2017.

[29] Z. Peng et al., "BEiT v2: Masked Image Modeling with Vector-Quantized Visual Tokenizers," arXiv, 2022.

[30] M. Caron et al., "Emerging properties in self-supervised vision transformers," ICCV, 2021.

[31] O. Ronneberger et al., "U-Net: Convolutional Networks for Biomedical Image Segmentation," MICCAI, 2015.

[32] J. Johnson et al., "Perceptual losses for real-time style transfer and super-resolution," ECCV, 2016.

[33] P. Esser et al., "Taming transformers for high-resolution image synthesis," CVPR, 2021.

[34] J. Yu et al., "Vector-quantized image modeling with improved VQGAN," ICLR, 2022.

[35] A. Vaswani et al., "Attention is all you need," NeurIPS, 2017.

[36] R. Rombach et al., "High-resolution image synthesis with latent diffusion models," CVPR, 2022.

[37] C. Saharia et al., "Photorealistic text-to-image diffusion models with deep language understanding," NeurIPS, 2022.

[38] J. Ho et al., "Video diffusion models," arXiv, 2022.

[39] T. Salimans and J. Ho, "Progressive distillation for fast sampling of diffusion models," ICLR, 2022.

[40] I. Loshchilov and F. Hutter, "Decoupled Weight Decay Regularization," ICLR, 2019.

[41] T. Dao et al., "FlashAttention: Fast and memory-efficient exact attention with IO-awareness," NeurIPS, 2022.

[42] J. Rasley et al., "DeepSpeed: System Optimizations Enable Training Deep Learning Models with Over 100 Billion Parameters," ACM SIGKDD, 2020.

[43] E. Hoogeboom et al., "simple diffusion: End-to-end diffusion for high resolution images," ICML, 2023.

[44] A. Holtzman et al., "The curious case of neural text degeneration," ICLR, 2020.

[45] J. Ho and T. Salimans, "Classifier-free diffusion guidance," arXiv, 2022.

[46] H. Chang et al., "Muse: Text-to-image generation via masked generative transformers," arXiv, 2023.

[47] "Negative prompt," https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Negative-prompt, 2022.

[48] J. Song et al., "Denoising diffusion implicit models," ICLR, 2021.

[49] J. Kaplan et al., "Scaling laws for neural language models," arXiv, 2020.

[50] D. P. Kingma and M. Welling, "Auto-encoding variational bayes," ICLR, 2014.

[51] I. Goodfellow et al., "Generative adversarial nets," NeurIPS, 2014.

[52] J. Sohl-Dickstein et al., "Deep unsupervised learning using nonequilibrium thermodynamics," ICML, 2015.

[53] A. van den Oord et al., "Conditional image generation with pixelcnn decoders," NeurIPS, 2016.

[54-94] *(其余参考文献同原文)*
