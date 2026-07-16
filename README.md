# 影律通（Cinemalaw AI）

> 影视行业合同与版权合规智能审查系统

## 项目简介

影律通是基于 RAG（检索增强生成）技术架构的影视行业智能审查系统，通过构建影视行业法律法规知识库，实现合同条款的高精度审查、智能问答和全文溯源。

### 核心特性

- **影视垂直领域专精**：针对影视合同特殊性深度定制
- **零幻觉架构**：Prompt隔离区 + 对抗测试 + RAGAS评估三重防线
- **全文溯源高亮**：每条审查意见均可追溯至原文条款
- **混合检索**：向量检索（BGE-M3）+ BM25检索（ES）→ RRF融合 → Reranker精排
- **层级切片**：按法律层级结构（编-章-节-条-款）智能切片

## 系统架构

```
用户查询 → 混合检索（BGE-M3 + BM25）→ RRF融合 → Reranker精排 → Top-5
    → Prompt隔离区（System Prompt + Context + Query）
    → LLM生成（Claude 3.5 / DeepSeek）
    → 结构化输出 + 溯源高亮
```

## 快速开始

### 环境要求

- Python 3.10+
- Elasticsearch 8.x（BM25检索）
- Milvus 2.4+（向量检索）
- GPU（可选，用于LayoutLM/BGE模型推理）

### 安装

```bash
# 克隆项目
git clone <repo_url>
cd cinemalaw-ai

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入实际配置
```

### 开发模式运行

```bash
# 初始化ES索引
python scripts/init_es_index.py

# 初始化Milvus集合
python scripts/init_milvus_collection.py

# 灌入示例数据（Mock模式）
python scripts/ingest_sample_data.py

# 启动API服务
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
pytest tests/ -v

# 运行评估
python scripts/run_evaluation.py
```

### Docker部署

```bash
# 启动全部服务（ES + Milvus + App）
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

### API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
cinemalaw-ai/
├── config/          # 配置管理
├── src/
│   ├── ingestion/   # 数据灌入管道（文档解析→切片→标注→入库）
│   ├── retrieval/   # 混合检索引擎（向量+BM25→RRF→Rerank）
│   ├── generation/  # RAG生成（Prompt模板→LLM调用→引用溯源）
│   ├── evaluation/  # RAGAS评估
│   ├── models/      # 数据模型定义
│   └── utils/       # 工具函数
├── api/             # FastAPI接口层
├── scripts/         # 工具脚本
└── tests/           # 测试用例
```

## 核心技术点

| 模块 | 技术 | 说明 |
|------|------|------|
| 文档解析 | LayoutLM v3 | 版面分析，支持表格/印章识别 |
| 层级切片 | 正则匹配 | 按编-章-节-条-款层级切片 |
| 向量检索 | BGE-M3 + Milvus | 1024维向量，cosine相似度 |
| BM25检索 | Elasticsearch + IK | 中文分词，BM25全文检索 |
| 融合排序 | RRF | 1/(60+R_bm25) + 1/(60+R_vec) |
| 精排 | BGE-Reranker-Large | Cross-Encoder，阈值0.35 |
| LLM | Claude 3.5 / DeepSeek | Prompt隔离区，零幻觉设计 |
| 评估 | RAGAS | Faithfulness/Relevance/Recall |

## 开发指南

- 开发模式下所有外部服务（LayoutLM、BGE、ES、Milvus）均使用Mock实现
- 通过 `.env` 配置切换 Mock/Production 模式
- 所有代码均有类型注解和docstring
- 核心算法（层级切片、RRF融合）有详细注释和单元测试

## 版本

- v1.0.0 - 初始版本
