### 引言

在学习概率论和统计学的过程中，高斯分布（也称为正态分布）是最基础且重要的概率分布之一。在实际应用中，我们经常需要处理多个高斯分布的联合效应，例如在贝叶斯推断、信号处理等领域。其中一个常见的操作就是计算两个高斯分布函数的乘积。本文将详细推导两个高斯分布函数的乘积，并探讨其结果的性质。

### 高斯分布的定义

首先，回顾一下一元高斯分布的概率密度函数（PDF）的定义。一个均值为  $\mu$ ，方差为  $\sigma^2$  的高斯分布可以表示为：


$$
\mathcal{N}(x | \mu, \sigma^2) = \frac{1}{\sqrt{2 \pi \sigma^2}} \exp \left( -\frac{(x - \mu)^2}{2 \sigma^2} \right)
$$


对于两个高斯分布，假设它们分别为：


$$
p_1(x) = \mathcal{N}(x | \mu_1, \sigma_1^2) = \frac{1}{\sqrt{2 \pi \sigma_1^2}} \exp \left( -\frac{(x - \mu_1)^2}{2 \sigma_1^2} \right)
$$



$$
p_2(x) = \mathcal{N}(x | \mu_2, \sigma_2^2) = \frac{1}{\sqrt{2 \pi \sigma_2^2}} \exp \left( -\frac{(x - \mu_2)^2}{2 \sigma_2^2} \right)
$$


### 两个高斯分布的乘积

我们需要计算这两个高斯分布函数的乘积：


$$
p(x) = p_1(x) \cdot p_2(x)
$$


将两个PDF代入：


$$
p(x) = \frac{1}{\sqrt{2 \pi \sigma_1^2}} \exp \left( -\frac{(x - \mu_1)^2}{2 \sigma_1^2} \right) \cdot \frac{1}{\sqrt{2 \pi \sigma_2^2}} \exp \left( -\frac{(x - \mu_2)^2}{2 \sigma_2^2} \right)
$$


合并常数项和指数项：


$$
p(x) = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( -\frac{(x - \mu_1)^2}{2 \sigma_1^2} - \frac{(x - \mu_2)^2}{2 \sigma_2^2} \right)
$$


### 合并指数项

现在，我们需要合并指数部分：


$$
-\frac{(x - \mu_1)^2}{2 \sigma_1^2} - \frac{(x - \mu_2)^2}{2 \sigma_2^2}
$$


展开平方项：


$$
(x - \mu_1)^2 = x^2 - 2 \mu_1 x + \mu_1^2
$$


$$
(x - \mu_2)^2 = x^2 - 2 \mu_2 x + \mu_2^2
$$


因此，指数部分变为：


$$
-\frac{x^2 - 2 \mu_1 x + \mu_1^2}{2 \sigma_1^2} - \frac{x^2 - 2 \mu_2 x + \mu_2^2}{2 \sigma_2^2}
$$


合并同类项：


$$
- \left( \frac{1}{2 \sigma_1^2} + \frac{1}{2 \sigma_2^2} \right) x^2 + \left( \frac{\mu_1}{\sigma_1^2} + \frac{\mu_2}{\sigma_2^2} \right) x - \left( \frac{\mu_1^2}{2 \sigma_1^2} + \frac{\mu_2^2}{2 \sigma_2^2} \right)
$$


为了简化，令：


$$
\frac{1}{\sigma^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2}
$$



$$
\frac{\mu}{\sigma^2} = \frac{\mu_1}{\sigma_1^2} + \frac{\mu_2}{\sigma_2^2}
$$


这样，指数部分可以表示为：


$$
- \frac{x^2}{2 \sigma^2} + \frac{\mu}{\sigma^2} x - \left( \frac{\mu_1^2}{2 \sigma_1^2} + \frac{\mu_2^2}{2 \sigma_2^2} \right)
$$


### 完成平方

为了将指数部分表示为高斯分布的形式，我们需要完成平方。高斯分布的指数部分通常为：


$$
-\frac{(x - \mu)^2}{2 \sigma^2} = -\frac{x^2}{2 \sigma^2} + \frac{\mu x}{\sigma^2} - \frac{\mu^2}{2 \sigma^2}
$$


比较我们的表达式：


$$
- \frac{x^2}{2 \sigma^2} + \frac{\mu}{\sigma^2} x - \left( \frac{\mu_1^2}{2 \sigma_1^2} + \frac{\mu_2^2}{2 \sigma_2^2} \right)
$$


与高斯分布的指数部分相比，缺少的是  $-\frac{\mu^2}{2 \sigma^2}$ 。因此，我们需要调整：


$$
- \frac{x^2}{2 \sigma^2} + \frac{\mu}{\sigma^2} x - \frac{\mu^2}{2 \sigma^2} + \frac{\mu^2}{2 \sigma^2} - \left( \frac{\mu_1^2}{2 \sigma_1^2} + \frac{\mu_2^2}{2 \sigma_2^2} \right)
$$


即：


$$
-\frac{(x - \mu)^2}{2 \sigma^2} + \left[ \frac{\mu^2}{2 \sigma^2} - \left( \frac{\mu_1^2}{2 \sigma_1^2} + \frac{\mu_2^2}{2 \sigma_2^2} \right) \right]
$$


因此，整个乘积可以表示为：


$$
p(x) = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( -\frac{(x - \mu)^2}{2 \sigma^2} + \left[ \frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} \right] \right)
$$


### 归一化常数

为了使  $p(x)$  成为一个合法的概率密度函数，我们需要确保其积分等于1。观察上式，可以将其重写为：


$$
p(x) = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( \frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} \right) \cdot \exp \left( -\frac{(x - \mu)^2}{2 \sigma^2} \right)
$$


注意到  $\exp \left( -\frac{(x - \mu)^2}{2 \sigma^2} \right)$  是一个高斯分布的核心部分，其积分应为  $\sqrt{2 \pi \sigma^2}$ 。因此，整个乘积的归一化常数为：


$$
\int p(x) dx = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( \frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} \right) \cdot \sqrt{2 \pi \sigma^2} = 1
$$


因此，乘积  $p(x)$  可以表示为：


$$
p(x) = \frac{1}{\sqrt{2 \pi \sigma^2}} \exp \left( -\frac{(x - \mu)^2}{2 \sigma^2} \right) \cdot \frac{\sqrt{2 \pi \sigma^2}}{2 \pi \sigma_1 \sigma_2} \exp \left( \frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} \right)
$$


然而，更简洁的表达是认识到  $p(x)$  本身是一个未归一化的高斯分布，其归一化常数可以通过前面的关系得到。实际上，两个高斯分布的乘积是一个新的高斯分布（可能未归一化），其参数如下：

### 乘积高斯分布的参数

从之前的定义：


$$
\frac{1}{\sigma^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2}
$$



$$
\frac{\mu}{\sigma^2} = \frac{\mu_1}{\sigma_1^2} + \frac{\mu_2}{\sigma_2^2}
$$


因此，新的均值  $\mu$  和方差  $\sigma^2$  为：


$$
\sigma^2 = \frac{\sigma_1^2 \sigma_2^2}{\sigma_1^2 + \sigma_2^2}
$$



$$
\mu = \frac{\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2}{\sigma_1^2 + \sigma_2^2}
$$


### 归一化因子的计算

为了找到乘积的归一化常数，我们需要计算：


$$
S = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( \frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} \right)
$$


计算  $\frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2}$ :

首先， $\mu^2$ :


$$
\mu^2 = \left( \frac{\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2}{\sigma_1^2 + \sigma_2^2} \right)^2 = \frac{(\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2)^2}{(\sigma_1^2 + \sigma_2^2)^2}
$$


 $\sigma^2 = \frac{\sigma_1^2 \sigma_2^2}{\sigma_1^2 + \sigma_2^2}$ , 所以：


$$
\frac{\mu^2}{2 \sigma^2} = \frac{(\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2)^2}{2 \sigma_1^2 \sigma_2^2 (\sigma_1^2 + \sigma_2^2)}
$$


计算整个表达式：


$$
\frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} = \frac{(\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2)^2 - \mu_1^2 \sigma_2^2 (\sigma_1^2 + \sigma_2^2) - \mu_2^2 \sigma_1^2 (\sigma_1^2 + \sigma_2^2)}{2 \sigma_1^2 \sigma_2^2 (\sigma_1^2 + \sigma_2^2)}
$$


展开分子：


$$
(\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2)^2 = \mu_1^2 \sigma_2^4 + 2 \mu_1 \mu_2 \sigma_1^2 \sigma_2^2 + \mu_2^2 \sigma_1^4
$$



$$
\mu_1^2 \sigma_2^2 (\sigma_1^2 + \sigma_2^2) = \mu_1^2 \sigma_1^2 \sigma_2^2 + \mu_1^2 \sigma_2^4
$$



$$
\mu_2^2 \sigma_1^2 (\sigma_1^2 + \sigma_2^2) = \mu_2^2 \sigma_1^4 + \mu_2^2 \sigma_1^2 \sigma_2^2
$$


合并：


$$
\mu_1^2 \sigma_2^4 + 2 \mu_1 \mu_2 \sigma_1^2 \sigma_2^2 + \mu_2^2 \sigma_1^4 - \mu_1^2 \sigma_1^2 \sigma_2^2 - \mu_1^2 \sigma_2^4 - \mu_2^2 \sigma_1^4 - \mu_2^2 \sigma_1^2 \sigma_2^2
$$


消去相同项：


$$
2 \mu_1 \mu_2 \sigma_1^2 \sigma_2^2 - \mu_1^2 \sigma_1^2 \sigma_2^2 - \mu_2^2 \sigma_1^2 \sigma_2^2 = -\sigma_1^2 \sigma_2^2 (\mu_1^2 - 2 \mu_1 \mu_2 + \mu_2^2) = -\sigma_1^2 \sigma_2^2 (\mu_1 - \mu_2)^2
$$


因此：


$$
\frac{\mu^2}{2 \sigma^2} - \frac{\mu_1^2}{2 \sigma_1^2} - \frac{\mu_2^2}{2 \sigma_2^2} = \frac{ -\sigma_1^2 \sigma_2^2 (\mu_1 - \mu_2)^2 }{2 \sigma_1^2 \sigma_2^2 (\sigma_1^2 + \sigma_2^2)} = -\frac{(\mu_1 - \mu_2)^2}{2 (\sigma_1^2 + \sigma_2^2)}
$$


因此，归一化因子  $S$  为：


$$
S = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( -\frac{(\mu_1 - \mu_2)^2}{2 (\sigma_1^2 + \sigma_2^2)} \right)
$$


而乘积  $p(x)$  可以表示为：


$$
p(x) = S \cdot \mathcal{N}(x | \mu, \sigma^2)
$$


因此，两个高斯分布的乘积是一个缩放的高斯分布：


$$
p_1(x) p_2(x) = \frac{1}{2 \pi \sigma_1 \sigma_2} \exp \left( -\frac{(\mu_1 - \mu_2)^2}{2 (\sigma_1^2 + \sigma_2^2)} \right) \cdot \mathcal{N}(x | \mu, \sigma^2)
$$


### 最终表达式

更简洁的表达是：

两个高斯分布  $\mathcal{N}(x | \mu_1, \sigma_1^2)$  和  $\mathcal{N}(x | \mu_2, \sigma_2^2)$  的乘积为：


$$
\mathcal{N}(x | \mu_1, \sigma_1^2) \cdot \mathcal{N}(x | \mu_2, \sigma_2^2) = Z_{12} \cdot \mathcal{N}(x | \mu, \sigma^2)
$$


其中：


$$
\frac{1}{\sigma^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2}
$$



$$
\mu = \frac{\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2}{\sigma_1^2 + \sigma_2^2}
$$



$$
Z_{12} = \frac{1}{\sqrt{2 \pi (\sigma_1^2 + \sigma_2^2)}} \exp \left( -\frac{(\mu_1 - \mu_2)^2}{2 (\sigma_1^2 + \sigma_2^2)} \right)
$$


### 验证

为了验证我们的结果，可以检查当  $\mu_1 = \mu_2$  和  $\sigma_1 = \sigma_2$  时：

-  $\sigma^2 = \frac{\sigma_1^4}{2 \sigma_1^2} = \frac{\sigma_1^2}{2}$
-  $\mu = \frac{\mu_1 \sigma_1^2 + \mu_1 \sigma_1^2}{2 \sigma_1^2} = \mu_1$
-  $Z_{12} = \frac{1}{\sqrt{2 \pi \cdot 2 \sigma_1^2}} = \frac{1}{2 \sqrt{\pi} \sigma_1}$

乘积：


$$
\mathcal{N}(x | \mu_1, \sigma_1^2)^2 = \frac{1}{2 \sqrt{\pi} \sigma_1} \cdot \mathcal{N}(x | \mu_1, \frac{\sigma_1^2}{2})
$$


这与直觉一致，因为两个相同的高斯分布相乘会得到一个更“尖锐”的高斯分布（方差减小），并有一个缩放因子。

### 结论

综上所述，两个高斯分布函数的乘积可以表示为：


$$
\mathcal{N}(x | \mu_1, \sigma_1^2) \cdot \mathcal{N}(x | \mu_2, \sigma_2^2) = Z_{12} \cdot \mathcal{N}(x | \mu, \sigma^2)
$$


其中：

- 新的方差  $\sigma^2$  满足：


$$
  \frac{1}{\sigma^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2} \quad \Rightarrow \quad \sigma^2 = \frac{\sigma_1^2 \sigma_2^2}{\sigma_1^2 + \sigma_2^2}
  $$


- 新的均值  $\mu$  为：


$$
  \mu = \frac{\mu_1 \sigma_2^2 + \mu_2 \sigma_1^2}{\sigma_1^2 + \sigma_2^2}
  $$


- 缩放因子  $Z_{12}$  为：


$$
  Z_{12} = \frac{1}{\sqrt{2 \pi (\sigma_1^2 + \sigma_2^2)}} \exp \left( -\frac{(\mu_1 - \mu_2)^2}{2 (\sigma_1^2 + \sigma_2^2)} \right)
  $$


这个结果表明，两个高斯分布的乘积仍然是一个高斯分布的形式（乘以一个常数），其精度（方差的倒数）是两个原始高斯分布精度的和，均值是两个原始均值的加权平均，权重与各自的方差成反比。缩放因子  $Z_{12}$  反映了两个原始高斯分布之间的“重叠”程度，当两个分布的中心越接近且方差越大时， $Z_{12}$  越大。
