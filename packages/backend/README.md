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
│   │   ├── errors.py             # 全局异常定义
│   │   ├── lifespan.py           # 应用生命周期：on_startup / on_shutdown
│   │   ├── logger.py             # 日志格式化 & 处理器注册
│   │   ├── redis.py              # Redis 连接管理
│   │   ├── security.py           # JWT、密码哈希、CORS 等安全中间件
│   │   └── tortoise.py           # Tortoise ORM 配置
│   ├── middleware/               # 中间件层
│   │   ├── __init__.py           # 中间件模块初始化
│   │   ├── always_200.py         # 始终返回200状态码中间件（调试用）
│   │   └── timer.py              # 请求计时中间件
│   ├── models/                   # 数据库模型层（Pydantic + Tortoise ORM）
│   │   ├── __init__.py           # Models 模块初始化
│   │   ├── models.py             # 基础模型定义
│   │   └── user.py               # 用户相关模型
│   ├── schemas/                  # 序列化模型层（Pydantic 模型）
│   │   ├── __init__.py           # Schemas 模块初始化
│   │   ├── response.py           # 统一响应格式 ApiResponse[T]
│   │   ├── token.py              # 令牌相关模型
│   │   └── user.py               # 用户相关请求/响应模型
│   ├── api/                      # 接口层（按版本隔离）
│   │   └── v1/                   # v1 版本路由总入口
│   │       ├── __init__.py       # 汇总并注册所有 v1 router
│   │       ├── auth.py           # 登录/注册/刷新令牌
│   │       ├── chat.py           # 对话相关接口（流式 SSE / WebSocket）
│   │       └── user.py           # 用户相关接口
│   ├── agents/                   # AI Agent 层（LangGraph / LangChain）
│   │   ├── __init__.py           # Agent 模块初始化
│   │   ├── base.py               # Agent 基础类定义
│   │   ├── router.py             # Agent 相关路由
│   │   └── tools/                # 可复用工具节点
│   │       ├── __init__.py       # Tools 模块初始化
│   │       └── time.py           # 示例：时间查询 tool
│   ├── repositories/             # 数据访问层（Tortoise ORM）
│   │   └── __init__.py           # Repositories 模块初始化
│   │   └── user.py               # 用户数据访问操作
│   ├── services/                 # 业务逻辑层（可跨多个 repository）
│   │   └── __init__.py           # Services 模块初始化
│   │   └── user.py               # 用户相关业务逻辑
│   └── utils/                    # 纯工具函数（与框架无关）
│       ├── __init__.py           # Utils 模块初始化
│       ├── exception.py          # 异常处理工具
│       └── response.py           # 响应处理工具
├── config.toml                   # 运行时配置（数据库、LLM、第三方密钥）
├── database/                     # 数据库文件
│   └── db.sqlite3                # SQLite 数据库文件
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
- **errors.py**: 定义全局异常类型
- **lifespan.py**: 定义应用生命周期事件，如启动和关闭时的操作
- **logger.py**: 日志格式化和处理器注册
- **redis.py**: Redis 连接管理
- **security.py**: 安全相关功能，如 JWT 认证、密码哈希、CORS 配置
- **tortoise.py**: Tortoise ORM 配置

### 3. app/middleware/ - 中间件层
- **always_200.py**: 调试用中间件，始终返回200状态码
- **timer.py**: 请求计时中间件，记录请求处理时间

### 4. app/models/ - 数据库模型层
- 使用 Tortoise ORM 定义的数据库模型
- **models.py**: 基础模型定义
- **user.py**: 用户相关的数据库模型

### 5. app/schemas/ - 序列化模型层
- 使用 Pydantic 定义的序列化模型
- 包括请求模型、响应模型等
- **response.py**: 定义统一响应格式 ApiResponse[T]
- **token.py**: 令牌相关的请求/响应模型
- **user.py**: 用户相关的请求/响应模型

### 6. app/api/ - API 接口层
- 按版本隔离接口（当前为 v1）
- **v1/auth.py**: 认证相关接口（登录/注册/刷新令牌）
- **v1/chat.py**: 聊天对话相关接口（支持流式 SSE / WebSocket）
- **v1/user.py**: 用户相关接口
- **v1/__init__.py**: 汇总并注册所有 v1 版本的路由

### 7. app/agents/ - AI Agent 层
- 基于 LangGraph/LangChain 实现的 AI Agent 功能
- **base.py**: Agent 基础类定义
- **router.py**: Agent 相关路由
- **tools/**: 可复用的工具节点
 - **time.py**: 示例工具，时间查询功能

### 8. app/repositories/ - 数据访问层
- 负责与数据库交互
- 使用 Tortoise ORM 进行数据访问
- 抽象数据操作，为上层服务提供数据接口
- **user.py**: 用户数据访问操作

### 9. app/services/ - 业务逻辑层
- 实现核心业务逻辑
- 可跨多个 repository 进行数据操作
- 处理复杂的业务规则和流程
- **user.py**: 用户相关业务逻辑

### 10. app/utils/ - 工具函数层
- 纯工具函数，与框架无关
- 提供通用的辅助功能
- **exception.py**: 异常处理工具
- **response.py**: 响应处理工具

## 技术栈
- **FastAPI**: Web 框架
- **LangChain/LangGraph**: AI Agent 框架
- **Tortoise ORM**: 异步 ORM
- **Pydantic**: 数据验证和设置管理
- **Redis**: 缓存和会话存储
- **Loguru**: 日志处理
- **Python-dotenv**: 环境变量管理

## 依赖管理
- 使用 `pyproject.toml` 管理项目依赖
- 使用 `uv.lock` 锁定依赖版本
