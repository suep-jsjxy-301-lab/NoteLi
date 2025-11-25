# NoteLi后端

## 项目概述
NoteLi 是一个基于 FastAPI 的后端项目，集成了 AI Agent 功能（使用 LangGraph/LangChain）。项目遵循清晰的分层架构，将业务逻辑、数据访问、接口定义等分离。

## 项目结构图
```
NoteLi-backend/
├── app/                          # FastAPI 应用主包
│   ├── main.py                   # 应用入口，create_app() 所在
│   ├── core/                     # 全局基础设施（与业务无关）
│   │   ├── config.py             # Pydantic Settings，统一读取 config.toml / env
│   │   ├── lifespan.py           # 应用生命周期：on_startup / on_shutdown
│   │   ├── logging.py            # 日志格式化 & 处理器注册
│   │   └── security.py           # JWT、密码哈希、CORS 等安全中间件
│   ├── api/                      # 接口层（按版本隔离）
│   │   └── v1/                   # v1 版本路由总入口
│   │       ├── __init__.py       # 汇总并注册所有 v1 router
│   │       ├── auth.py           # 登录/注册/刷新令牌
│   │       └── chat.py           # 对话相关接口（流式 SSE / WebSocket）
│   ├── agents/                   # AI Agent 层（LangGraph / LangChain）
│   │   ├── __init__.py           # Agent 模块初始化
│   │   ├── base.py               # Agent 基础类定义
│   │   ├── router.py             # Agent 相关路由
│   │   └── tools/                # 可复用工具节点
│   │       ├── __init__.py       # Tools 模块初始化
│   │       └── time.py           # 示例：时间查询 tool
│   ├── models/                   # Pydantic 模型（请求/响应/内部 DTO）
│   │   ├── __init__.py           # Models 模块初始化
│   │   └── response.py           # 统一响应格式 ApiResponse[T]
│   ├── repositories/             # 数据访问层（SQLAlchemy / Beanie）
│   │   └── __init__.py           # Repositories 模块初始化
│   ├── services/                 # 业务逻辑层（可跨多个 repository）
│   │   └── __init__.py           # Services 模块初始化
│   └── utils/                    # 纯工具函数（与框架无关）
│       └── __init__.py           # Utils 模块初始化
├── config.toml                   # 运行时配置（数据库、LLM、第三方密钥）
├── logs/                         # 运行日志
│   └── app.log
├── tests/                        # 单元 & 集成测试
│   └── __init__.py               # Tests 模块初始化
├── .env                          # 环境变量文件
├── .python-version               # Python 版本指定
├── comparison_analysis.md        # 比较分析文档
├── pyproject.toml                # 项目元数据 & 依赖（uv/pip 两用）
├── uv.lock                       # uv 依赖锁定文件
└── README.md                     # 项目说明文档
```

## 各模块详细说明

### 1. app/main.py
- 应用入口文件
- 创建 FastAPI 实例
- 注册 API 路由
- 包含根路径路由

### 2. app/core/ - 核心基础设施
- **config.py**: 使用 Pydantic Settings 管理配置，统一从 config.toml 或环境变量读取
- **lifespan.py**: 定义应用生命周期事件，如启动和关闭时的操作
- **logging.py**: 日志格式化和处理器注册
- **security.py**: 安全相关功能，如 JWT 认证、密码哈希、CORS 配置

### 3. app/api/ - API 接口层
- 按版本隔离接口（当前为 v1）
- **v1/auth.py**: 认证相关接口（登录/注册/刷新令牌）
- **v1/chat.py**: 聊天对话相关接口（支持流式 SSE / WebSocket）
- **v1/__init__.py**: 汇总并注册所有 v1 版本的路由

### 4. app/agents/ - AI Agent 层
- 基于 LangGraph/LangChain 实现的 AI Agent 功能
- **base.py**: Agent 基础类定义
- **router.py**: Agent 相关路由
- **tools/**: 可复用的工具节点
  - **time.py**: 示例工具，时间查询功能

### 5. app/models/ - 数据模型层
- 使用 Pydantic 定义的模型
- 包括请求模型、响应模型和内部 DTO
- **response.py**: 定义统一响应格式 ApiResponse[T]

### 6. app/repositories/ - 数据访问层
- 负责与数据库交互
- 使用 SQLAlchemy 或 Beanie 进行数据访问
- 抽象数据操作，为上层服务提供数据接口

### 7. app/services/ - 业务逻辑层
- 实现核心业务逻辑
- 可跨多个 repository 进行数据操作
- 处理复杂的业务规则和流程

### 8. app/utils/ - 工具函数层
- 纯工具函数，与框架无关
- 提供通用的辅助功能

## 技术栈
- **FastAPI**: Web 框架
- **LangChain/LangGraph**: AI Agent 框架
- **Pydantic**: 数据验证和设置管理
- **Loguru**: 日志处理
- **Python-dotenv**: 环境变量管理

## 依赖管理
- 使用 `pyproject.toml` 管理项目依赖
- 使用 `uv.lock` 锁定依赖版本
- 支持 uv 和 pip 两种包管理器