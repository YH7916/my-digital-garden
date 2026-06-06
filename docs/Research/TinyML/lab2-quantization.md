---
title: Lab2 Quantization 笔记
tags: [tinyml, quantization, pytorch]
updated: 2026-05-04
publish: true
blog_dest: Research/TinyML/lab2-quantization.md
---

# Lab2: Quantization（量化）

> 把模型的浮点数权重和激活值压缩成整数，让模型更小、推理更快。核心问题：怎么映射、误差怎么控制、推理怎么全程用整数。

---

## 一、为什么要量化

神经网络默认用 32-bit 浮点数（fp32）存储权重。量化把它压缩成 8-bit 或更少的整数：

- 模型体积缩小 4x（32bit → 8bit）
- 整数运算比浮点运算快，省电
- 代价是精度略有损失

---

## 二、两种量化方式

| | K-Means 量化 | Linear 量化 |
|--|--|--|
| 原理 | 把权重聚成 $2^n$ 个簇，同簇共享一个值 | 把浮点范围均匀映射到整数范围 |
| 质心分布 | 根据数据分布自由放置，密集在数据多的地方 | 均匀分布，间距固定 |
| 精度 | 更高（适应数据分布） | 略低 |
| 硬件支持 | 差（推理需要查表） | 好（全程整数运算，硬件直接支持） |
| 实现复杂度 | 高（需存 codebook） | 低（只需 scale 和 zero_point） |

---

## 三、K-Means 量化

### 核心思想

用 K-Means 聚类把权重分成 $2^n$ 个簇，每个簇用一个质心值代替所有权重。

就像把 256 种颜色的图片压缩成只用 16 种颜色——每个像素找最近的颜色替代。

### Codebook

量化结果存成 codebook，包含两部分：

- `centroids`：$2^n$ 个质心值（浮点数）
- `labels`：每个权重属于哪个簇（整数索引）

推理时还原：
```python
quantized_weight = codebook.centroids[codebook.labels]
```
`centroids[labels]` 是 fancy indexing：labels 是整数数组，直接当下标用，取出对应质心值。

### K-Means 算法步骤

1. 随机初始化 $2^n$ 个质心
2. 每个权重找最近的质心，打上标签
3. 每个簇的新质心 = 该簇所有权重的均值
4. 重复 2-3 直到收敛

### Q3：更新质心

```python
codebook.centroids[k] = fp32_tensor[codebook.labels == k].mean()
```

`codebook.labels == k` 返回布尔数组，用来筛选属于第 k 簇的权重，再取均值。

### n-bit 量化能表示多少种值

n-bit → $2^n$ 个簇 → $2^n$ 种颜色

- 2-bit → 4 种
- 4-bit → 16 种
- 8-bit → 256 种

---

## 四、Linear 量化

### 核心公式

$$r = S(q - Z)$$

- $r$：浮点数（真实值）
- $q$：整数（量化后存储的值）
- $S$：scale（缩放因子）—— 一个整数单位代表多大的浮点值
- $Z$：zero point（零点）—— 浮点 0 对应哪个整数

### Scale 和 Zero Point 怎么算

把浮点范围 $[r_{min}, r_{max}]$ 映射到整数范围 $[q_{min}, q_{max}]$：

$$S = \frac{r_{max} - r_{min}}{q_{max} - q_{min}}$$

$$Z = \text{round}\left(q_{min} - \frac{r_{min}}{S}\right)$$

8-bit 整数范围：$q_{min} = -128$，$q_{max} = 127$

### 量化过程（Q4）

从浮点 $r$ 得到整数 $q$：

$$q = \text{round}\left(\frac{r}{S}\right) + Z$$

代码：
```python
scaled_tensor = fp_tensor / scale        # 除以 scale
rounded_tensor = scaled_tensor.round()   # 四舍五入
shifted_tensor = rounded_tensor + zero_point  # 加零点
```

### 权重量化的特殊处理

权重分布几乎关于 0 对称，所以令 $Z_{weight} = 0$，简化为：

$$S = \frac{r_{max}}{q_{max}}$$

其中 $r_{max}$ 取权重绝对值的最大值。

### Per-channel 量化

卷积权重是 4D 张量 `(out_channels, in_channels, kH, kW)`。

每个输出通道用独立的 scale，效果比全局共用一个 scale 好。

---

## 五、整数推理（Quantized Inference）

### 为什么要整数推理

量化的目标不只是压缩存储，还要让**推理过程全程用整数运算**，不用浮点数，这样才能真正加速。

### 数学推导

浮点推理：$r_{out} = r_{in} \times r_{weight} + r_{bias}$

代入 $r = S(q-Z)$，令 $Z_{weight}=0$，$Z_{bias}=0$，$S_{bias} = S_{in} \cdot S_{weight}$，化简得：

$$q_{out} = \left(q_{in} \times q_{weight} + Q_{bias}\right) \times \frac{S_{in} \cdot S_{weight}}{S_{out}} + Z_{out}$$

其中 $Q_{bias} = q_{bias} - Z_{in} \times q_{weight}$（推理前预计算，省掉运行时减法）

### 三步实现（Q7/Q8）

```python
# Step 1: 整数矩阵乘法（已给出）
output = linear(q_input, q_weight) + Q_bias

# Step 2: 乘缩放系数，换算到输出整数域
output = output.float() * (input_scale * weight_scale / output_scale)

# Step 3: 加输出零点
output = output + output_zero_point
```

Step 2 中 `weight_scale` 需要 reshape：
- 全连接层：`.view(1, -1)`，因为 output 形状是 `[batch, oc]`
- 卷积层：`.view(1, -1, 1, 1)`，因为 output 形状是 `[batch, oc, h, w]`

### Bias 的 scale（Q6）

bias 要和 $q_{in} \times q_{weight}$ 直接相加，两者必须用同一个 scale（单位相同才能加），所以：

$$S_{bias} = S_{in} \cdot S_{weight}$$

### 为什么量化模型没有 ReLU（Q9.2）

量化时用 ReLU **之后**的激活值范围来计算 `output_scale` 和 `output_zero_point`。ReLU 之后没有负数，这个非负范围已经编码进量化参数里了，推理时自然输出非负值，不需要再单独做 ReLU。

### 输入预处理（Q9.1）

原始输入是浮点数，范围 (0, 1)，需要转成 int8 (-128, 127)：

$$S = \frac{1-0}{127-(-128)} = \frac{1}{255}, \quad Z = -128$$

$$q = r \times 255 - 128$$

```python
(x * 255 - 128).clamp(-128, 127).to(torch.int8)
```

---

## 六、BN Fusion（BatchNorm 融合）

量化前先把 BatchNorm 层融合进前面的卷积层。

BatchNorm 做的是对输出做线性变换（缩放+平移），可以直接合并到卷积的权重和偏置里，减少推理时的额外乘法。融合后精度不变。

---

## 七、PyTorch 常用操作速查

| 操作 | 含义 |
|--|--|
| `tensor.view(1, -1)` | 改变形状，-1 表示自动计算该维度大小 |
| `tensor.float()` | 转成浮点类型 |
| `tensor.to(torch.int8)` | 转成 8-bit 整数类型 |
| `tensor.clamp(a, b)` | 截断，超出 [a,b] 的值强制拉回边界 |
| `tensor.round()` | 四舍五入 |
| `tensor[bool_array]` | 布尔索引，筛选为 True 的元素 |
| `centroids[labels]` | Fancy indexing，用整数数组当下标取值 |
