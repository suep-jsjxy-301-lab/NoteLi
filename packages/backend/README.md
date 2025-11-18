# NoteLi后端

## 项目结构

```
.
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
│   │   └── tools/                # 可复用工具节点
│   │       └── time.py           # 示例：时间查询 tool
│   ├── models/                   # Pydantic 模型（请求/响应/内部 DTO）
│   │   └── response.py           # 统一响应格式 ApiResponse[T]
│   ├── repositories/             # 数据访问层（SQLAlchemy / Beanie）
│   ├── services/                 # 业务逻辑层（可跨多个 repository）
│   └── utils/                    # 纯工具函数（与框架无关）
├── config.toml                   # 运行时配置（数据库、LLM、第三方密钥）
├── logs/                         # 运行日志
│   └── app.log
├── tests/                        # 单元 & 集成测试
├── pyproject.toml                # 项目元数据 & 依赖（uv/pip 两用）
```