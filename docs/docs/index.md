# Spider Spidroin curation

Spider Spidroin curation(SpiderSc) 是一个用于蜘蛛丝蛋白（Spidroin）基因鉴定和分析的生物信息学流程。该项目通过整合蛋白序列比对、基因组映射、转录组数据和基因组注释等多种方法，实现对蜘蛛基因组中丝蛋白基因的系统性鉴定和精细注释。

## 快速开始

```bash
# 1. 安装依赖
make requirements

# 2. 激活环境
pixi shell

# 3. 运行 Miniprot 初步注释
make miniprot_mapping
```

详细步骤请参见 [快速入门指南](getting-started.md)。

## 项目概览

### 当前实现：第一步 Miniprot 初步注释

本项目当前实现了完整 Spidroin 注释流程的**第一步**：

- ✅ MMseqs2 序列聚类去冗余
- ✅ Miniprot 蛋白-基因组比对
- ✅ 基因边界自动预测
- ✅ 按 Spidroin 类型分类
- ✅ 生成初步 GFF 注释文件

**输出位置**: `data/processed/01.miniprot_mapping/`

**重要**: 输出结果是初步预测，需要人工审核和修正。

### 完整流程路线图

```
第一步: Miniprot 初步注释 ✓ (已实现)
    ↓
人工修正 GFF 文件 (进行中)
    ↓
第二步: 整合转录组和基因组注释 (待实现)
    ↓
第三步: 多源数据汇总 (待实现)
    ↓
第四步: k-mer 特征扫描 (待实现)
```

详见 [完整工作流程](workflow.md)。

## 主要命令

```bash
# 运行初步注释流程
make miniprot_mapping

# 使用自定义参数
python spider_silkome_module/miniprot_mapping.py \
    --positive-threshold 0.75 \
    --min-length 1000

# 代码格式化和检查
make format
make lint
```

更多命令请参见 [快速入门指南](getting-started.md)。

## 文档导航

### 核心文档
- **[快速入门指南](getting-started.md)** - 从零开始运行流程
- **[完整工作流程](workflow.md)** - 详细的流程说明和后续步骤
- **[技术细节](technical-details.md)** - 算法原理和参数说明
- **[数据格式](data-formats.md)** - 输入输出文件格式

### 关键概念

**Spidroin 类型**:
- MaSp1/MaSp2: 主要壶状腺丝蛋白
- MiSp: 次要壶状腺丝蛋白
- Flag/PFlag: 鞭毛状丝蛋白
- AcSp: 葡萄状腺丝蛋白
- 更多类型见 [数据格式文档](data-formats.md)

**基因边界确定**:
- 基于 N 端和 C 端结构域的比对位置
- 考虑链方向（+/-）的影响
- 详见 [技术细节文档](technical-details.md)

## 项目结构

```
spider_silkome/
├── data/
│   ├── external/          # Spidroin 蛋白序列数据库
│   ├── raw/              # 基因组序列
│   ├── interim/          # 中间处理结果
│   └── processed/        # 最终输出结果
├── spider_silkome_module/
│   ├── spidroin_curation.py  # 主流程脚本
│   ├── processing.py         # 数据处理函数
│   └── export.py             # 结果导出函数
├── notebooks/            # Jupyter notebooks
├── docs/                 # 文档
└── Makefile             # 命令入口
```

## 贡献与支持

- 报告问题：[GitHub Issues](https://github.com/your-repo/issues)
- 文档反馈：欢迎提交 PR
- 联系方式：见项目 README

## 许可证

详见 LICENSE 文件。
