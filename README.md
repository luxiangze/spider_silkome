# Spider Spidroin Curation (SpiderSc)

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

蜘蛛丝蛋白（Spidroin）基因鉴定和注释的生物信息学流程。

## 快速开始

```bash
make requirements    # 安装依赖
pixi shell          # 激活环境
make miniprot_mapping  # 运行 Miniprot Mapping 流程
```

📖 **详细文档**: [docs/docs/index.md](https://github.com/luxiangze/spider_silkome/blob/main/docs/docs/index.md)

## 主要功能

- ✅ Miniprot 蛋白-基因组比对
- ✅ 基因边界自动预测
- ✅ 按 Spidroin 类型分类
- 🔄 人工修正（进行中）
- ⏳ 转录组/基因组注释整合（待实现）
- ⏳ k-mer 特征扫描（待实现）

## 文档

- [项目主页](https://github.com/luxiangze/spider_silkome/blob/main/docs/docs/index.md) - 项目概览
- [快速入门](https://github.com/luxiangze/spider_silkome/blob/main/docs/docs/getting-started.md) - 安装和使用
- [完整工作流程](https://github.com/luxiangze/spider_silkome/blob/main/docs/docs/workflow.md) - 详细流程
- [技术细节](https://github.com/luxiangze/spider_silkome/blob/main/docs/docs/technical-details.md) - 算法和参数
- [数据格式](https://github.com/luxiangze/spider_silkome/blob/main/docs/docs/data-formats.md) - 文件格式

## 项目结构

```
spider_silkome/
├── data/                       # 数据目录
│   ├── external/               # Spidroin 蛋白序列数据库
│   ├── raw/                    # 蜘蛛基因组序列
│   ├── interim/                # 中间处理结果
│   └── processed/              # 最终输出（GFF/CSV）
│
├── spider_silkome_module/      # 源代码
│   ├── miniprot_mapping.py     # 主流程脚本
│   ├── processing.py           # 数据处理
│   └── export.py               # 结果导出
│
├── docs/docs/                  # 详细文档
├── notebooks/                  # Jupyter notebooks
└── Makefile                    # 命令入口
```

## 许可证与引用

- **许可证**: 详见 [LICENSE](LICENSE) 文件
- **维护者**: 郭永康
- **模板**: 基于 [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/)

如需引用本项目，请使用：
```
Spider Spidroin Curation (SpiderSc)
https://github.com/luxiangze/spider_silkome
```

