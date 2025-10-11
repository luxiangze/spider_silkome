# 数据格式说明

本文档描述 Spider Silkome 项目中使用的各种数据文件格式。

## 输入数据格式

### Spidroin 蛋白序列 (FASTA)

**文件位置**: `data/external/spider-silkome-database.v1.prot.fixed.fasta`

**说明**: 这是经过人工修正过的文件，例如：

`>5|2132|Oecobiidae|Oecobius|sp. (OTU0418)|MiSp|MiSp|CTD`修改成：

`>5|2132|Oecobiidae|Oecobius|sp-OTU0418|MiSp|MiSp|CTD`

`>46|5944|Tetragnathidae|Metellina|merianae|Ampullate_spidroin|Ampullate spidroin|CTD`修改成：

`>46|5944|Tetragnathidae|Metellina|merianae|Ampullate_spidroin|Ampullate_spidroin|CTD`

**原始文件来源**: 从 [Spider Silkome](https://spider-silkome.org/)  数据库中下载。

**格式要求**:
```
>index|ID|Family|Genus|Species|Spidroin_type|Spidroin_type|CTD/NTD
SEQUENCE
```

**示例**:
```
>1|7047|Oecobiidae|Oecobius|navus|MiSp|MiSp|CTD
AGASSAAIARAGNALTTQSSTSRISYNVNSLVGPGGSFNLAALPAIMSNQVQSISASSPE
>2|7047|Oecobiidae|Oecobius|navus|MiSp|MiSp|CTD
GSGGGKLGGAGRGFYGASGAFGGLGAGLGGLGVGAGSSGGGSGGGGGGGGGAGDGGSAGV
```

**关键信息**:
- index: 序列在数据库中的索引
- ID: 序列的唯一标识符
- Family: 科
- Genus: 属
- Species: 种
- Spidroin 类型（MaSp1, MaSp2, AcSp 等）
- 结构域类型（CTD 或 NTD）

### 基因组序列 (FASTA.GZ)

**文件位置**: `data/raw/spider_genome/*.fa.gz`

**格式要求**:
- 压缩的 FASTA 格式（gzip）
- 文件命名：`{Species_name}.fa.gz`

**示例**:
```
>Chr1
ATCGATCGATCG...
>Chr2
GCTAGCTAGCTA...
```

---

## 中间数据格式

### MMseqs2 代表序列 (FASTA)

**文件位置**: `data/interim/mmseqs/*_rep_seq.fasta`

**说明**: 聚类后的代表性序列，格式与输入 FASTA 相同

### Miniprot 索引 (.mpi)

**文件位置**: `data/interim/genome_mpi/*.mpi`

**说明**: Miniprot 的二进制索引文件，用于加速比对

### Miniprot 原始比对结果 (GFF)

**文件位置**: `data/interim/miniprot/{species}_all/{species}.gff`

**格式**: GFF3

**示例**:
```
##gff-version 3
Chr1	miniprot	mRNA	12345	12567	89.5	+	.	ID=MP000001;Rank=1;Identity=0.892;Positive=0.915;Target=sp|P19837|MaSp1|Nephila_clavipes|CTD 1 223 +
```

**字段说明**:
1. seqid: 染色体/scaffold ID
2. source: miniprot
3. type: mRNA
4. start: 起始位置（1-based）
5. end: 终止位置（1-based, inclusive）
6. score: 比对分数
7. strand: 链方向（+/-）
8. frame: 相位（通常为 .）
9. attributes: 分号分隔的属性

**Attributes 字段**:
- `ID`: 比对记录的唯一标识符
- `Rank`: 该查询序列的比对排名
- `Identity`: 序列一致性百分比
- `Positive`: 相似度分数百分比
- `Target`: 查询序列信息（ID 起始 终止 方向）

### 按类型分类的 GFF

**文件位置**: `data/interim/miniprot/{species}_all/{species}.mRNA.{spidroin_type}.gff`

**说明**: 从 mRNA GFF 中提取特定 Spidroin 类型的记录

### 位置信息表格 (CSV)

**文件位置**: `data/interim/miniprot/{species}_all/{species}.mRNA.{spidroin_type}.csv`

**格式**: CSV

**示例**:
```csv
chr,strand,start_positions,end_positions,n_start,n_end
Chr1,+,"{12345: 2, 12350: 1}","{67890: 2, 67895: 1}",2,2
Chr2,-,"{23456: 3}","{78901: 3}",1,1
```

**字段说明**:
- `chr`: 染色体 ID
- `strand`: 链方向
- `start_positions`: 起始位置字典（位置: 支持数）
- `end_positions`: 终止位置字典（位置: 支持数）
- `n_start`: 不同起始位置的数量
- `n_end`: 不同终止位置的数量

### 合并的基因预测 (GFF)

**文件位置**: `data/interim/miniprot/{species}_all/{species}.mRNA.{spidroin_type}.combined.gff`

**说明**: 根据 N/C 端位置组合生成的基因预测

---

## 输出数据格式

### 初步注释 GFF

**文件位置**: `data/processed/01.miniprot_mapping/{species}.gff`

**格式**: GFF3

**示例**:
```
##gff-version 3
Chr1	miniprot	gene	12345	67890	.	+	.	ID=gene_001;spidroin_type=MaSp1;n_start=2;n_end=2;length=55545
Chr1	miniprot	gene	78901	123456	.	-	.	ID=gene_002;spidroin_type=MaSp2;n_start=3;n_end=3;length=44555
```

**Attributes 字段**:
- `ID`: 基因唯一标识符
- `spidroin_type`: Spidroin 类型
- `n_start`: 支持起始位置的证据数
- `n_end`: 支持终止位置的证据数
- `length`: 基因长度（bp）

### 初步注释 CSV

**文件位置**: `data/processed/01.miniprot_mapping/{species}.csv`

**格式**: CSV

**示例**:
```csv
chr,strand,start_position,start_count,end_position,end_count,length,score,valid,reason
Chr1,+,12345,67890,2,2,MaSp1,55545,5,valid,
Chr1,-,78901,123456,3,3,MaSp2,44555,8,valid,
```

**字段说明**:
- `chr`: 染色体 ID
- `strand`: 链方向（+/-）
- `start_position`: 基因起始位置
- `end_position`: 基因终止位置
- `start_count`: 支持起始位置的 N/C 端数量
- `end_count`: 支持终止位置的 N/C 端数量
- `spidroin_type`: Spidroin 类型
- `length`: 基因长度（bp）
- `score`: 比对分数
- `valid`: 是否有效
- `reason`: 无效原因

---

## 数据流向图

```
输入数据
├── spider-silkome-database.v1.prot.fixed.fasta (FASTA)
└── {species}.fa.gz (FASTA.GZ)
    ↓
MMseqs2 聚类
    ↓
├── *_rep_seq.fasta (FASTA)
└── *_rep_seq_manually.fasta (FASTA, 手动筛选)
    ↓
Miniprot 索引
    ↓
└── {species}.mpi (Binary)
    ↓
Miniprot 比对
    ↓
└── {species}.gff (GFF3)
    ↓
提取 mRNA
    ↓
└── {species}.mRNA.gff (GFF3)
    ↓
按类型分类
    ↓
└── {species}.mRNA.{type}.gff (GFF3)
    ↓
位置提取
    ↓
├── {species}.mRNA.{type}.csv (CSV)
└── {species}.mRNA.{type}.combined.gff (GFF3)
    ↓
合并所有类型
    ↓
├── {species}.gff (GFF3) - 初步注释
└── {species}.csv (CSV) - 统计信息
```

---

## 文件命名规范

### 物种名称
- 格式：`Genus_species`
- 示例：`Trichonephila_clavata`, `Araneus_ventricosus`
- 注意：使用下划线分隔，首字母大写

### Spidroin 类型
常见类型：
- `MaSp1`, `MaSp2`, `MaSp3`, `MaSp3B`, `MaSp2B`: 主要壶状腺丝蛋白
- `MiSp`: 次要壶状腺丝蛋白
- `Flag`, `PFlag`: 鞭毛状丝蛋白
- `AcSp`: 葡萄状腺丝蛋白
- `TuSp`: 管状腺丝蛋白
- `PySp`: 梨状腺丝蛋白
- `AgSp1`, `AgSp2`: 聚合腺丝蛋白
- `CySp`: 柱状腺丝蛋白
- `CrSp`: 冠状腺丝蛋白
- `Spidroin`: 未分类的丝蛋白
- `Putative_spidroin`: 推定的丝蛋白
- `Ampullate_spidroin`: 壶状腺丝蛋白（未细分）

---

## 坐标系统

### GFF3 坐标
- **1-based**: 第一个碱基的位置是 1
- **Inclusive**: start 和 end 都包含在特征内
- **示例**: `start=100, end=200` 表示从第 100 个碱基到第 200 个碱基（共 101 个碱基）

### BED 坐标（如果使用）
- **0-based**: 第一个碱基的位置是 0
- **Half-open**: start 包含，end 不包含
- **示例**: `start=99, end=200` 表示从第 100 个碱基到第 200 个碱基（共 101 个碱基）

### 转换公式
```
GFF to BED: start_bed = start_gff - 1, end_bed = end_gff
BED to GFF: start_gff = start_bed + 1, end_gff = end_bed
```

---

## 质量控制指标

### 比对质量
- **Identity**: 序列一致性，范围 0.0-1.0
- **Positive**: 相似度分数，范围 0.0-1.0
- **通常**: Positive ≥ Identity

### 基因预测质量
- **n_start**: 支持起始位置的证据数，≥2 较好
- **n_end**: 支持终止位置的证据数，≥2 较好
- **length**: 基因长度，通常 1-50 kb

---

## 参考文档

- [工作流程](workflow.md)
- [技术细节](technical-details.md)
- [快速入门](getting-started.md)
