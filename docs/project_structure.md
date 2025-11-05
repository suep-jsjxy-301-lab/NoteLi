# NoteLi 项目目录结构

## 项目概览

NoteLi 是一个多包项目，包含前端和后端两个主要部分，采用现代化的微服务架构设计。

## 目录结构

```
NoteLi/
├── .gitignore                 # Git 忽略配置文件
├── docker-compose.yml         # Docker Compose 配置文件
├── LICENSE                    # 项目许可证
├── README.md                  # 项目主介绍文件
├── docs/                      # 项目文档目录
│   └── project_structure.md   # 项目目录结构文档 (当前文件)
├── packages/                  # 包管理目录
│   ├── backend/               # 后端服务包
│   │   ├── .python-version    # Python 版本指定
│   │   ├── langgraph.json     # LangGraph 配置文件
│   │   ├── main.py            # 后端主入口文件
│   │   ├── pyproject.toml     # Python 项目配置文件
│   │   ├── README.md          # 后端服务说明文档
│   │   ├── uv.lock            # Python 依赖锁定文件
│   │   ├── app/               # 后端应用源码目录
│   │   │   ├── agents/        # 智能代理模块
│   │   │   │   └── agent.py   # 代理实现文件
│   │   │   ├── api/           # API 接口定义
│   │   │   ├── core/          # 核心功能模块
│   │   │   ├── models/        # 数据模型定义
│   │   │   ├── repo/          # 数据仓库层
│   │   │   └── services/      # 业务服务层
│   │   └── tests/             # 后端测试文件
│   └── frontend/              # 前端应用包 (目录结构未详列)
└── scripts/                   # 项目脚本目录
```

## 各目录说明

### 根目录文件
- `.gitignore`: 定义 Git 版本控制系统忽略的文件和目录
- `docker-compose.yml`: Docker 容器编排配置文件
- `LICENSE`: 项目许可证信息
- `README.md`: 项目说明文档，包含项目介绍、安装和使用方法

### docs/
项目文档目录，包含项目相关的说明文档。

### packages/
多包项目结构的包管理目录，包含前后端两个独立的服务包。

#### packages/backend/
后端服务包，采用 Python 开发，集成了 LangGraph 框架。

- `.python-version`: 指定项目使用的 Python 版本
- `langgraph.json`: LangGraph 框架的配置文件
- `main.py`: 应用程序的主入口文件
- `pyproject.toml`: Python 项目的配置文件，包含依赖管理、构建配置等
- `README.md`: 后端服务的详细说明文档
- `uv.lock`: Python 依赖锁定文件，确保依赖版本一致
- `app/`: 后端应用的主要源代码目录
 - `agents/`: 包含智能代理相关的实现，如 `agent.py`
  - `api/`: API 接口定义和实现
  - `core/`: 核心功能模块
  - `models/`: 数据模型定义
  - `repo/`: 数据仓库/数据访问层
  - `services/`: 业务逻辑服务层
- `tests/`: 后端测试代码

#### packages/frontend/
前端应用包，包含用户界面相关的代码(具体结构未在当前视图中显示)。

### scripts/
项目脚本目录，包含构建、部署、开发等辅助脚本。