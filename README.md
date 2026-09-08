# AI Agent Workflow Platform

基于工作流画布的 AI Agent 开发平台，通过可视化编排减少 AI 幻觉，实现可控、可追溯的智能工作流。

## 技术栈

### 前端
- **React** - 前端框架
- **React Flow** - 可视化工作流画布
- **TypeScript** - 类型安全
- **TailwindCSS** - 样式框架

### 后端
- **Python 3.10+** - 开发语言
- **FastAPI** - 高性能异步 API 框架
- **LangGraph** - Agent 工作流编排框架
- **SQLAlchemy** - ORM 框架
- **Pydantic** - 数据验证

### 数据库与存储
- **MySQL** - 关系型数据库（用户、工作流定义、执行记录）
- **Redis** - 缓存层（会话、执行状态、热点数据）
- **OSS** - 对象存储（图片、文件等资源）

### 部署与运维
- **Docker** - 容器化部署
- **Nginx** - 反向代理
- **Celery** - 异步任务队列（可选）

## 项目架构

```
myAgent/
├── frontend/                    # React 前端应用
│   ├── public/                  # 静态资源
│   ├── src/
│   │   ├── assets/              # 图片、样式等资源
│   │   ├── components/          # React 组件
│   │   │   ├── canvas/          # 画布相关组件
│   │   │   ├── nodes/           # 自定义节点组件
│   │   │   └── panels/          # 配置面板组件
│   │   ├── pages/               # 页面组件
│   │   ├── services/            # API 服务
│   │   ├── store/               # 状态管理
│   │   ├── types/               # TypeScript 类型定义
│   │   ├── App.jsx              # 根组件
│   │   └── main.jsx             # 入口文件
│   ├── index.html               # HTML 模板
│   ├── vite.config.js           # Vite 配置
│   ├── package.json             # 依赖配置
│   └── eslint.config.js         # ESLint 配置
│
├── backend/                     # FastAPI 后端应用
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # 应用入口
│   │   ├── api/                 # API 路由层
│   │   │   ├── __init__.py
│   │   │   ├── router.py        # 路由汇总
│   │   │   ├── workflows.py     # 工作流 CRUD
│   │   │   ├── executions.py    # 执行记录
│   │   │   └── auth.py          # 用户认证
│   │   ├── core/                # 核心配置
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # 环境变量配置
│   │   │   └── database.py      # 数据库连接
│   │   ├── engine/              # LangGraph 工作流引擎
│   │   │   ├── __init__.py
│   │   │   ├── graph.py         # 工作流图定义
│   │   │   ├── executor.py      # 执行器
│   │   │   └── nodes/           # 节点处理器
│   │   │       └── __init__.py
│   │   ├── models/              # SQLAlchemy 数据模型
│   │   │   └── __init__.py
│   │   ├── schemas/             # Pydantic 数据验证
│   │   │   └── __init__.py
│   │   ├── services/            # 业务逻辑层
│   │   │   └── __init__.py
│   │   └── utils/               # 工具函数
│   │       └── __init__.py
│   ├── requirements.txt         # Python 依赖
│   ├── .env.example             # 环境变量模板
│   └── .gitignore
│
└── README.md                    # 项目文档
```

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                  React 前端                      │
│  ┌─────────────┐    ┌──────────────────────┐    │
│  │ React Flow  │    │  工作流编辑器/执行器  │    │
│  │   (画布)    │    │  结果展示/监控面板    │    │
│  └──────┬──────┘    └──────────┬───────────┘    │
└─────────┼─────────────────────┼────────────────┘
          │ HTTP/WebSocket      │
          ↓                     ↓
┌─────────────────────────────────────────────────┐
│              FastAPI 后端                        │
│  ┌──────────────┐    ┌─────────────────────┐    │
│  │  API 路由层   │    │  工作流管理 API      │    │
│  │  用户/权限    │    │  执行/监控/日志      │    │
│  └──────┬───────┘    └──────────┬──────────┘    │
│         │                       │                │
│         ↓                       ↓                │
│  ┌─────────────────────────────────────────┐    │
│  │         LangGraph 执行引擎               │    │
│  │  节点1 → 节点2 → 条件分支 → 节点3 → 输出  │    │
│  └─────────────────────────────────────────┘    │
└────────────┬──────────────────────┬─────────────┘
             │                      │
    ┌────────┼────────┐    ┌────────┼────────┐
    ↓        ↓        ↓    ↓        ↓        ↓
  MySQL   Redis    OSS   向量DB  外部API  消息队列
  (持久化) (缓存)  (文件) (RAG)  (工具)  (异步)
```

## 核心功能

### 工作流节点类型
- **LLM 节点** - 调用大语言模型
- **工具节点** - 执行外部工具/API
- **条件节点** - 分支逻辑判断
- **人工审核节点** - 关键步骤人工确认
- **知识库节点** - RAG 检索增强生成
- **代码节点** - 执行自定义 Python 代码

### 减少幻觉的设计
1. **分步验证** - 每个节点输出可校验
2. **结构化输出** - JSON Schema 强制格式
3. **人工审核** - 关键节点插入人工确认
4. **知识库检索** - RAG 替代纯生成
5. **重试机制** - 失败自动重试或降级
6. **确定性逻辑** - 非 AI 部分用传统代码

## 快速开始

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 开发计划

- [ ] Phase 1: 基础框架搭建
- [ ] Phase 2: 工作流引擎集成
- [ ] Phase 3: 画布编辑器开发
- [ ] Phase 4: 执行与监控系统
- [ ] Phase 5: 高级功能完善

## 许可证

MIT