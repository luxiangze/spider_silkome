# 技术细节

本文档描述 Spidroin 注释流程的技术实现细节、算法原理和参数说明。

## 基因边界确定逻辑

### 链方向与结构域的关系

根据链方向和结构域类型，基因边界的确定遵循以下规则：

| 结构域类型 | 链方向 | 记录位置 | 原因 |
|---------|--------|---------|------|
| CTD (C端) | + | end | C端在基因末端，end 是蛋白质的最后一个坐标 |
| CTD (C端) | - | start | C端在基因起始（坐标较小），start 是蛋白质的最后一个坐标 |
| NTD (N端) | + | start | N端在基因起始，start 是蛋白质的第一个坐标 |
| NTD (N端) | - | end | N端在基因末端（坐标较大），end 是蛋白质的第一个坐标 |

### 算法说明

**正链基因 (+)**:
- 基因从 5' → 3' 方向转录
- N 端在基因起始位置（较小坐标）
- C 端在基因终止位置（较大坐标）

**负链基因 (-)**:
- 基因从 3' → 5' 方向转录（相对于参考基因组）
- N 端在基因终止位置（较大坐标）
- C 端在基因起始位置（较小坐标）

### 代码实现

参见 `spider_silkome_module/processing.py` 中的 `extract_positions_from_gff()` 函数。

---

## 质量控制

### 比对质量过滤

**Positive 分数阈值**
- 默认值：0.75
- 范围：0.0 - 1.0
- 说明：Miniprot 比对的 Positive 分数，表示比对的相似度
- 建议：
  - 严格模式：≥ 0.85
  - 标准模式：≥ 0.75
  - 宽松模式：≥ 0.70

**Identity 分数**
- 说明：序列一致性百分比
- 用途：辅助评估比对质量
- 通常 Positive > Identity

### 基因长度过滤

**最小长度阈值**
- 默认值：1000 bp
- 说明：过滤过短的基因预测
- 依据：Spidroin 基因通常较长（通常 > 1 kb）

**最大长度阈值**
- 默认值：100000 bp (100 kb)
- 说明：过滤异常长的基因预测
- 依据：避免错误的基因融合

**延伸长度**
- 默认值：10000 bp (10 kb)
- 说明：当只检测到 N 端或 C 端时，向另一端延伸的长度
- 依据：根据 Spidroin 基因的平均长度估算

### N/C 端配对验证

**配对规则**
- 完整基因应同时具有 N 端和 C 端比对信号
- 两端应在同一染色体/scaffold 上
- 两端应在同一链方向上
- 两端距离应在合理范围内
- 两端中间不能有其他比对信号

**不完整基因处理**
- 只有 N 端：向 C 端方向延伸
- 只有 C 端：向 N 端方向延伸
- 延伸长度由 `--extension-length` 参数控制

---

## MMseqs2 聚类参数

### 序列相似度阈值 (--min-seq-id)
- 默认值：0.9
- 范围：0.0 - 1.0
- 说明：两条序列被认为相似的最小序列一致性
- 影响：值越高，聚类越严格，保留的代表序列越多

### 覆盖度阈值 (-c)
- 默认值：0.8
- 范围：0.0 - 1.0
- 说明：比对覆盖查询序列的最小比例
- 影响：确保比对覆盖足够长的序列区域

### 覆盖度模式 (--cov-mode)
- 默认值：1
- 选项：
  - 0: 双向覆盖（两条序列都需满足覆盖度）
  - 1: 目标序列覆盖度
  - 2: 查询序列覆盖度
- 说明：控制如何计算覆盖度

---

## Miniprot 比对参数

### 线程数 (-t)
- 默认值：70
- 说明：并行比对使用的 CPU 线程数
- 建议：根据服务器配置调整

### 输出格式 (--gff)
- 说明：输出 GFF3 格式的比对结果
- 包含：基因结构、比对分数、序列信息

### 索引选项 (-d)
- 说明：创建或使用基因组索引文件
- 优势：加速重复比对

### 比对选项 (-I)
- 说明：输出详细的比对信息
- 用途：包含 Identity 和 Positive 分数

---

## 数据结构

### GFFData 类
```python
@dataclass
class GFFData:
    seqid: str          # 染色体/scaffold ID
    source: str         # 来源（miniprot）
    type: str           # 特征类型（mRNA）
    start: int          # 起始位置（1-based）
    end: int            # 终止位置（1-based，inclusive）
    score: float        # 比对分数
    strand: str         # 链方向（+/-）
    frame: str          # 相位（.）
    attributes: Attributes  # 属性对象
```

### Attributes 类
```python
@dataclass
class Attributes:
    ID: str             # 比对记录 ID
    Rank: int           # 比对排名
    Identity: float     # 序列一致性
    Positive: float     # 相似度分数
    Target: List[str]   # 目标序列种类以及有效比对区域
```

### Position 类
```python
@dataclass
class Position:
    chr: str                    # 染色体 ID
    strand: str                 # 链方向
    start: Dict[int, int]       # 起始位置及支持数
    end: Dict[int, int]         # 终止位置及支持数
```

---

## 性能优化

### 内存使用
- MMseqs2 聚类：内存需求取决于序列数量
- Miniprot 比对：索引文件会占用内存
- 建议：至少 16 GB RAM

### 计算时间
- MMseqs2 聚类：取决于序列数量和相似度
- Miniprot 索引：每个基因组约  0.5-1 分钟
- Miniprot 比对：每个基因组约 1-3 分钟

### 并行化
- 当前实现：串行处理每个基因组
- 改进空间：可以并行处理多个基因组
- 建议：使用 GNU Parallel 或 Snakemake

---

## 常见问题

### Q: 为什么有些基因只有 N 端或 C 端？

**可能原因**：
1. 基因不完整（基因组组装问题）
2. 比对质量不足（序列分歧大）
3. 结构域缺失（真实的不完整基因）

**解决方案**：
- 降低 `--positive-threshold`
- 检查基因组质量
- 使用 k-mer 扫描补充

### Q: 如何处理假阳性预测？

**识别方法**：
1. 检查比对质量分数
2. 查看基因长度是否合理
3. 检查是否有转录组支持

**处理方式**：
- 人工审核时删除
- 提高 `--positive-threshold`
- 调整 `--min-length`

### Q: 预测的基因边界不准确怎么办？

**原因**：
- Miniprot 基于蛋白比对，不能精确定位外显子边界
- N/C 端结构域可能不完整

**解决方案**：
- 人工修正（必需步骤）
- 整合转录组数据
- K-mer 扫描补充

---

## 参考资源

### 软件文档
- [MMseqs2](https://github.com/soedinglab/MMseqs2)
- [Miniprot](https://github.com/lh3/miniprot)

### 项目文档
- [工作流程](workflow.md)
- [快速入门](getting-started.md)
- [数据格式](data-formats.md)
