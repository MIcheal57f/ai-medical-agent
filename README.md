医疗智能问答系统（Medical AI Assistant）
项目介绍

本项目是一个基于 RAG（检索增强生成） 的医疗智能问答系统，结合多种检索优化技术，实现了一个接近真实应用场景的 AI 医疗助手。
系统支持多轮对话、医疗安全判断、智能检索与回答生成，能够在一定程度上模拟医疗咨询流程。

---


##  核心功能
-  **RAG 检索增强生成**
  基于 FAISS 的向量检索（语义搜索）、基于 BM25 的关键词检索（精准匹配）、混合检索（向量 + 关键词融合）、基于 LLM 的重排序（Rerank）提升结果相关性
-  **多轮对话能力**
  支持会话历史记录（Session Memory）、基于上下文的问题改写（Query Rewrite）、利用历史信息优化检索效果
-  **医疗安全机制**
  医疗意图识别（过滤非医疗问题）、紧急症状分级（高/中/低风险）、非医疗问题拒答、症状分析与建议生成、回答附带免责声明（保证安全性）
-  **知识库系统**
  支持 TXT / PDF 文件加载、自动文本切分（Chunking）、本地向量数据库持久化存储
-  工程化设计
  分层架构（core / services / storage / tools）、日志系统（控制台 + 文件日志）、检索与生成流程解耦（Pipeline 化设计）

---

##  技术栈
- 大模型（LLM）：DeepSeek-V3（OpenAI 兼容 API，硅基流动提供）
- 嵌入模型：BAAI/bge-large-zh-v1.5
- 向量数据库：FAISS
- 框架：LangChain
- 前端：Streamlit
- 检索技术：Hybrid Search（FAISS + BM25）
- 文本处理：jieba 中文分词

##  项目结构

```
ai_agent/
│
├── app.py                 # 前端界面（Streamlit）
├── llm.py                 # LLM调用封装
├── prompt.py              # Prompt模板
├── requirements.txt       # 依赖管理
│
├── core/                  # 核心逻辑层
│   ├── __init__.py
│   ├── rag.py             # RAG主流程
│   ├── rerank.py          # 重排序模块
│   ├── rewrite.py         # 查询改写
│   └── logger.py          # 日志系统
│
├── services/              # 服务层
│   ├── __init__.py
│   ├── agent.py           # 智能代理
│   └── medical_service.py # 医疗服务逻辑
│
├── knowledge/             # 数据处理层
│   ├── __init__.py
│   ├── loader.py          # 文档加载
│   └── splitter.py        # 文本切分
│
├── storage/               # 存储层
│   ├── __init__.py
│   ├── embedding.py       # 向量构建
│   └── faiss_index/       # 向量索引（本地生成，不上传）
│
├── tools/                 # 工具模块
│   ├── emergency_tool.py  # 紧急情况判断
│   └── symptom_tool.py    # 症状分析
│
├── data/                  # 知识库
│   └── medical.txt
│
├── logs/                  # 日志文件（不上传）
└── .gitignore             # Git忽略规则
```


运行方式
  pip install -r requirements.txt
  streamlit run app.py

项目亮点
  实现 混合检索，大幅提升召回准确率
  加入 LLM 重排序（Rerank） 优化回答质量
  使用 Query Rewrite 增强多轮对话效果
  构建 医疗安全机制，具备真实应用价值
  工程化架构清晰，易于扩展与维护

本项目仅提供医疗信息参考，不替代专业医生诊断。如有身体不适，请及时就医。
后续优化方向
  引入 Agent 智能决策能力
  扩展专业医疗知识库
  增加 RAG 效果评测指标
