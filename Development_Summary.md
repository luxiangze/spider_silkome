# Spider Spidroin curation(SpiderSc)  开发总结

> 本文档主要用于记录 SpiderSc 项目中 Miniprot Mapping 模块的修改过程，以及后续的模块化工作。

## 概述

本次工作将 `notebooks/Miniprot_mapping.ipynb` 中的分析流程模块化，创建了标准的命令行入口和完整的文档。

**重要说明**: 本模块实现的是完整 Spidroin 注释流程的**第一步：基于 Miniprot 的初步注释**。产生的结果需要人工审核修正后，才能进入后续的精细化分析流程（整合转录组数据、基因组注释、k-mer 扫描等）。

## 完成的工作

### 1. 创建模块化脚本

**文件**: `spider_silkome_module/miniprot_mapping.py`

将 notebook 中的代码重构为可重用的函数模块：

- `cluster_spidroin_sequences()`: MMseqs2 序列聚类
- `index_genome()`: Miniprot 基因组索引
- `align_to_genome()`: Miniprot 序列比对
- `extract_mrna_gff()`: 提取 mRNA 记录
- `split_by_spidroin_type()`: 按类型分割 GFF
- `parse_gff_file()`: 解析 GFF 文件
- `process_spidroin_type()`: 处理单个 spidroin 类型
- `combine_all_spidroins()`: 合并所有类型的预测结果
- `run_spidroin_curation_pipeline()`: 完整流程的主函数

**特点**:
- 完整的类型注解
- 详细的文档字符串
- 命令行参数支持
- 日志输出
- 错误处理

### 2. 更新 Makefile

**文件**: `Makefile`

添加了两个新的命令：

```makefile
# 运行完整的 spidroin 鉴定流程
make miniprot_mapping

# 使用自定义参数运行
make miniprot_mapping_custom # 需要提前在 Makefile 中设置参数
```

### 3. 更新项目文档

#### 3.1 工作流程说明 (`docs/docs/index.md`)

添加了以下内容：
- 项目描述
- 完整的工作流程概述（5个步骤）
- 数据流向图
- 命令使用说明
- 技术细节（基因边界确定逻辑）
- 质量控制说明

#### 3.2 快速入门指南 (`docs/docs/getting-started.md`)

创建了详细的使用指南，包括：
- 环境设置步骤
- 数据准备说明
- 完整的流程执行步骤
- 结果文件格式说明
- 参数调整指南
- 结果解读方法
- 故障排除建议

## 使用方法

### 基本使用

```bash
# 1. 安装依赖
make requirements

# 2. 激活环境
pixi shell

# 3. 运行 Miniprot Mapping
make miniprot_mapping
```

### 自定义参数

```bash
python spider_silkome_module/miniprot_mapping.py \
    --positive-threshold 0.75 \
    --min-length 1000 \
    --max-length 100000 \
    --extension-length 10000
```

### 指定数据路径

```bash
python spider_silkome_module/miniprot_mapping.py \
    --genome-path /path/to/genomes \
    --spidroin-fasta /path/to/spidroin.fasta
```

## 输出结果

初步注释结果保存在 `data/processed/01.miniprot_mapping/` 目录：

```
data/processed/01.miniprot_mapping/
├── {species}.gff    # GFF3 格式的初步注释（需人工修正）
└── {species}.csv    # CSV 格式的统计信息
```

**⚠️ 重要**: 这些是基于 Miniprot 比对的自动化初步预测，需要人工审核和修正。

## 完整流程概览

```
第一步: Miniprot 初步注释 (本模块实现) ✓
    ↓
人工修正 GFF 文件 (手动操作)
    ↓
    ├─→ 第二步A: 整合三代 DRS 转录组数据 (待实现)
    └─→ 第二步B: 整合高质量基因组注释信息 (待实现)
         ↓
    第三步: 汇总多源数据 (待实现)
         ↓
    第四步: k-mer 特征提取 + 全基因组扫描 (待实现)
```

## 第一步流程详细步骤（本模块）

1. **MMseqs2 聚类**: 去除冗余序列
2. **Miniprot 索引**: 建立基因组索引
3. **Miniprot 比对**: 蛋白序列比对到基因组
4. **提取分类**: 提取并按类型分类 mRNA 记录
5. **边界预测**: 根据 N/C 端位置推断基因边界
6. **结果整合**: 合并所有类型生成初步注释

## 与原 Notebook 的对应关系

| Notebook Cell | 模块化函数 |
|--------------|-----------|
| Cell 3 (MMseqs2) | `cluster_spidroin_sequences()` |
| Cell 4 (Miniprot indexing) | `index_genome()` |
| Cell 4 (Miniprot alignment) | `align_to_genome()` |
| Cell 4 (Extract mRNA) | `extract_mrna_gff()` |
| Cell 4 (Split by type) | `split_by_spidroin_type()` |
| Cell 5 (Process each type) | `process_spidroin_type()` |
| Cell 5 (Combine results) | `combine_all_spidroins()` |

## 优势

相比原 notebook，模块化后的优势：

1. **可重用性**: 函数可以在其他脚本中导入使用
2. **可维护性**: 代码结构清晰，易于维护和更新
3. **可测试性**: 每个函数可以独立测试
4. **可配置性**: 支持命令行参数，灵活调整
5. **自动化**: 可以集成到自动化流程中
6. **文档化**: 完整的文档字符串和使用指南
7. **标准化**: 遵循项目的代码规范

## 后续工作

### 当前模块的改进建议

1. **添加单元测试**: 为关键函数编写测试用例
2. **添加进度条**: 使用 tqdm 显示处理进度
3. **并行处理**: 对多个基因组的处理可以并行化
4. **结果可视化**: 添加基因分布的可视化功能
5. **质量报告**: 生成 HTML 格式的质量控制报告

### 后续流程模块（待开发）

1. **人工修正辅助工具**（基因组多的时候可以开发，现在用 VScode 打开 GFF 文件人工修正）
   - 开发交互式审核界面
   - 自动标注可疑预测
   - 版本控制和修正记录

2. **转录组数据整合模块**
   - DRS 数据比对和处理
   - 转录本结构验证
   - 可变剪接识别

3. **基因组注释整合模块**
   - 多种注释结果的交叉验证
   - 证据等级评分系统
   - 冲突解决策略

4. **k-mer 扫描模块**
   - k-mer 特征提取算法
   - 全基因组高效扫描
   - 不完整基因识别

### 核心文档
- **`index.md`** - 项目主页，简洁的概览和导航
- **`getting-started.md`** - 快速入门指南，精简的操作步骤

### 详细文档
- **`workflow.md`** - 完整工作流程说明，包含所有5个步骤
- **`technical-details.md`** - 技术细节，算法原理和参数说明
- **`data-formats.md`** - 数据格式详细说明

### 文档特点
- **模块化**: 每个文档专注于特定主题
- **相互链接**: 通过链接连接相关文档
- **层次清晰**: 从概览到详细，逐步深入
- **易于维护**: 修改某个主题只需更新对应文档

## 相关文件

### 代码模块
- 模块化脚本: `spider_silkome_module/miniprot_mapping.py`
- Makefile 入口: `Makefile`
- 原始 Notebook: `notebooks/Spidroin_curation.ipynb`

### 文档
- 项目主页: `docs/docs/index.md`
- 快速入门: `docs/docs/getting-started.md`
- 完整流程: `docs/docs/workflow.md`
- 技术细节: `docs/docs/technical-details.md`
- 数据格式: `docs/docs/data-formats.md`

---

**创建日期**: 2025-10-11
**最后更新**: 2025-10-11
**版本**: 1.1
**作者**: 郭永康