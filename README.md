# NoteLi

基于 AI Agent 的笔记管理与协作平台（市创项目）

## 技术栈
- **编程语言**：Python 3.11  
- **依赖管理**：uv（高性能 Python 包管理工具）  
- **后端框架**：FastAPI（现代、高性能的异步 Web 框架）  
- **AI 框架**：LangChain 1.0（用于构建基于大模型的智能应用）  
- **ORM 工具**：SQLModel（基于 SQLAlchemy 与 Pydantic 的现代化 ORM）  
- **数据库（按需选用）**：
  - PostgreSQL（关系型数据库，适用于结构化数据）
  - Redis（高性能内存数据库，用于缓存与会话管理）
  - MongoDB（文档型数据库，适用于非结构化或半结构化数据）

## 团队纪律
1. 禁止任何人直接 push 到 `dev`/`main`，必须 MR + CI 绿灯。  
2. 禁止 `git pull` 默认合并，统一 `pull.rebase=true`。  
3. 禁止 `git commit --no-verify` 跳过钩子，Pre-commit 必须跑单测、lint。  
4. 每天上班第一件事：先 `git fetch -p` 看一眼有没有新分支，再开始写代码。  
5. 功能分支生命周期 ≤ 3 天，太长就拆。

--------------------------------------------------
## 日常开发循环（每人每天重复）
--------------------------------------------------
0. 从最新 dev 开出功能分支，命名格式：`feature/名字-一句话`  
```bash
git fetch -p
git checkout dev
git pull
git checkout -b feature/123-login-cache
```

1. 写代码，commit 粒度保持"能一句话说明白"  
```bash
git add .
git commit -m "feat: 登录接口增加 Redis 缓存 15min"
```

2. 推送之前，先拉最新远程 dev（rebase 模式）  
```bash
git fetch -p
git rebase origin/dev        # 有冲突就当场解决，别拖
```

3. 把功能分支推到自己远程仓库  
```bash
git push -u origin feature/123-login-cache
```

4. 在 Web 端发 Merge Request（PR）  
- 评审通过 → Squash merge → 自动删除远程功能分支  
- 评审拒绝 → 本地继续改，再 force-push（因为 rebase 过）  
```bash
git add .
git commit --amend --no-edit
git push --force-with-lease
```

--------------------------------------------------
## 冲突爆发时（三句口诀）
--------------------------------------------------
1. 先备份：  
   `git branch backup/123`  
2. 再拉最新：  
   `git fetch && git rebase origin/dev`  
3. 解决完继续：  
   `git rebase --continue && git push --force-with-lease`

--------------------------------------------------
## 紧急热修复（hotfix）
--------------------------------------------------
1. 从线上标签开 hotfix 分支  
```bash
git fetch --tags
git checkout -b hotfix/2.3.1 v2.3.0
```

2. 修完打标签，CI 自动部署  
```bash
git commit -m "fix: 修复越权漏洞"
git tag v2.3.1
git push origin v2.3.1
```

3. 把 hotfix 合并回 dev 和 main，保持"修复在最老分支，向上合并"  
```bash
git checkout dev && git merge hotfix/2.3.1
git checkout main && git merge hotfix/2.3.1
git push origin dev main --follow-tags
```

--------------------------------------------------
## 协作节奏示意图
--------------------------------------------------
```
main   ●────●────●─●  (仅放稳定标签)
        \    \      \
dev      ●────●──────●────●────●   (日常集成)
          \    \      \    \
feature    ●────●      ●    ●     (短分支，用完即删)
```

