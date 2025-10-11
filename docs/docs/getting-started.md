# 快速入门指南

本指南将帮助你从零开始运行 Spider Spidroin curation(SpiderSc) 项目的**第一步：基于 Miniprot 的初步注释**。

**重要**: 本流程产生的是**初步注释结果**，需要人工审核和修正后，才能进入后续的精细化分析流程。

## 环境设置

### 1. 安装依赖

```bash
make requirements
```

这会安装所有必要的依赖：Python 3.10、MMseqs2、Miniprot 等。

### 2. 激活环境

```bash
pixi shell
```

## 准备数据

### 3. 数据文件准备

需要准备两类数据文件：

**Spidroin 蛋白序列数据库**

```
data/external/spider-silkome-database.v1.prot.fixed.fasta
```

**蜘蛛基因组序列**
```
data/raw/spider_genome/
├── Trichonephila_clavata.fa.gz
└── Araneus_ventricosus.fa.gz
```

详细的数据格式要求请参见 [数据格式文档](data-formats.md)。

## 运行流程

### 4. 执行初步注释

```bash
make miniprot_mapping
```

这个命令会自动执行：
1. MMseqs2 序列聚类
2. Miniprot 基因组索引
3. Miniprot 序列比对
4. 基因边界预测
5. 结果整合

**预计运行时间**: 每个基因组约 2-3 分钟（取决于基因组大小）

### 5. 查看结果

结果保存在：
```
data/processed/01.miniprot_mapping/
├── {species}.gff    # GFF3 格式注释文件
└── {species}.csv    # CSV 格式统计表格
```

**⚠️ 重要**: 这些是**初步预测**，需要人工审核和修正。

## 自定义参数

### 6. 调整参数

```bash
python spider_silkome_module/miniprot_mapping.py \
    --positive-threshold 0.80 \
    --min-length 2000 \
    --max-length 80000 \
    --extension-length 15000
```

**关键参数**:
- `--positive-threshold`: 比对质量阈值（默认 0.75）
- `--min-length`: 最小基因长度（默认 1000 bp）
- `--max-length`: 最大基因长度（默认 100000 bp）
- `--extension-length`: 延伸长度（默认 10000 bp）

参数详细说明请参见 [技术细节文档](technical-details.md)。

### 7. 指定数据路径

```bash
python spider_silkome_module/miniprot_mapping.py \
    --genome-path /path/to/genomes \
    --spidroin-fasta /path/to/spidroin.fasta
```

## 结果解读

### 8. 输出文件说明

**GFF 文件**:
```
Chr1    miniprot    gene    12345    67890    .    +    .    ID=gene1;spidroin_type=MaSp1
```

**CSV 文件**:
```csv
chr,strand,start,end,n_start,n_end,spidroin_type,length
Chr1,+,12345,67890,2,2,MaSp1,55545
```

**质量指标**:
- `n_start/n_end`: 支持证据数量（≥2 较好）
- `length`: 基因长度（通常 1-50 kb）

详细格式说明请参见 [数据格式文档](data-formats.md)。

### 9. 常见 Spidroin 类型

- **MaSp1/MaSp2**: 主要壶状腺丝蛋白
- **MiSp**: 次要壶状腺丝蛋白
- **Flag/PFlag**: 鞭毛状丝蛋白
- **AcSp**: 葡萄状腺丝蛋白
- **PySp**: 梨状腺丝蛋白
- **AgSp**: 聚合腺丝蛋白

更多类型请参见 [数据格式文档](data-formats.md)。

## 故障排除

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| MMseqs2 环境未找到 | pixi 配置问题 | 检查 `pixi info` |
| 基因组文件错误 | 格式不正确 | 确保是 `.fa.gz` 格式 |
| 没有预测到基因 | 阈值过高 | 降低 `--positive-threshold` |
| 预测基因过多 | 阈值过低 | 提高 `--positive-threshold` |

更多技术细节请参见 [技术细节文档](technical-details.md)。

## 下一步

### 10. 人工修正（必需）

使用基因组浏览器（IGV、JBrowse 等）或 VScode 审核和修正 GFF 文件：
1. 检查基因边界合理性
2. 合并/分割错误预测
3. 删除假阳性
4. 标注可信度

保存为 `{species}.curated.gff`

### 11. 后续流程（待实现）

- **第二步**: 整合转录组和基因组注释
- **第三步**: 多源数据汇总
- **第四步**: k-mer 特征扫描

详见 [完整工作流程文档](workflow.md)。

## 更多资源

- [完整工作流程](workflow.md) - 详细流程说明
- [技术细节](technical-details.md) - 算法和参数
- [数据格式](data-formats.md) - 文件格式说明
- [项目主页](index.md) - 项目概览

