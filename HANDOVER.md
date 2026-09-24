# G.R.C. Agent 项目交接文档

> 交接日期: 2026-09-24  
> 交接人: 胡哲 (huzhe0308)  
> 项目全称: Governance. Regulation. Compliance. Agent

---

## 目录

1. [项目概述](#1-项目概述)
2. [系统架构](#2-系统架构)
3. [代码仓库与部署](#3-代码仓库与部署)
4. [核心代码文件说明](#4-核心代码文件说明)
5. [数据库结构](#5-数据库结构)
6. [Bridge Agent (邮件代理)](#6-bridge-agent-邮件代理)
7. [认证系统](#7-认证系统)
8. [API 接口清单](#8-api-接口清单)
9. [前端文件说明](#9-前端文件说明)
10. [配置文件说明](#10-配置文件说明)
11. [本地开发环境搭建](#11-本地开发环境搭建)
12. [部署流程 (Railway)](#12-部署流程-railway)
13. [Bridge Agent 构建流程](#13-bridge-agent-构建流程)
14. [已知问题与注意事项](#14-已知问题与注意事项)
15. [关键业务逻辑](#15-关键业务逻辑)
16. [常用运维操作](#16-常用运维操作)
17. [交接清单](#17-交接清单)

---

## 1. 项目概述

G.R.C. Agent 是一个汽车出口市场法规合规管理平台，帮助团队完成从评估分配到最终月报的完整工作流。

### 三段式工作流

| 阶段 | 模块 | 说明 |
|------|------|------|
| 入口 | 评估分配 (Assessment Allocation) | 邮件扫描 → PSV解析 → 分配负责人 → 发送评估邮件 |
| 过程 | 评估追踪 (Assessment Tracking) | Gap分析 → Summary Comment写入Jira → 关闭Layer3工单 |
| 出口 | 综合分析 (Analysis) | 全部评估完成 → 生成月报 → 发送团队 |

### 覆盖范围

- **10个出口市场**: Korea, ASEAN RHD, ASEAN LHD, India, Middle East, Kazakhstan, Uzbekistan, Turkey, AUS/NZL
- **6个评估领域**: Cyber Security, Data Security, OTA, OBD, Functional Safety, Immobilizer

### 技术栈

- **后端**: Python 3.11, aiohttp (异步HTTP服务器)
- **前端**: 纯 HTML + CSS + JavaScript (无框架)
- **数据库**: Turso (libSQL, 云端SQLite) — 生产环境; SQLite — 本地开发
- **部署**: Railway (云端) + Bridge Agent (用户本地Windows)
- **外部依赖**: Jira (工单系统), Outlook COM (邮件), VW内部LLM网关 (AI助手)

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    Railway (云服务器)                      │
│                                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │         server_unified.py (aiohttp)          │       │
│  │         端口: 7860 (HTTP + WebSocket)          │       │
│  │                                              │       │
│  │  ┌─────────────┐  ┌────────────────────┐    │       │
│  │  │  HTTP 路由   │  │  WebSocket /ws     │    │       │
│  │  │  (所有API)   │  │  (Bridge连接)      │    │       │
│  │  └──────┬──────┘  └────────┬───────────┘    │       │
│  │         │                    │               │       │
│  │         ▼                    ▼               │       │
│  │  ┌─────────────────────────────────────┐     │       │
│  │  │           app.py (业务逻辑)          │     │       │
│  │  │  - 邮件扫描  - PSV解析  - Jira API  │     │       │
│  │  │  - Gap追踪   - 分析    - AI助手     │     │       │
│  │  └──────────┬──────────────────────────┘     │       │
│  │             │                                │       │
│  │  ┌──────────▼──────────┐  ┌──────────────┐  │       │
│  │  │  auth.py (认证)      │  │ bridge_manager│  │       │
│  │  │  Turso / SQLite     │  │ (HTTP轮询管理) │  │       │
│  │  └─────────────────────┘  └──────┬───────┘  │       │
│  └──────────────────────────────────┼───────────┘       │
│                                     │                   │
│  ┌──────────────────────────────────▼───────────┐       │
│  │           Turso 云数据库                      │       │
│  │  users / sessions / user_settings            │       │
│  │  gap_market_tracking / gap_layer3_closed     │       │
│  │  registered_tickets / assessment_sent        │       │
│  │  gap_inspection_log                          │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
                          │
                    HTTP 轮询 (每2秒)
                          │
┌─────────────────────────▼─────────────────────────────────┐
│              用户本地 Windows 电脑                         │
│                                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │        GRCBridgeAgent.exe (Bridge Agent)      │       │
│  │                                               │       │
│  │  - 轮询 /api/bridge/poll 获取命令             │       │
│  │  - 执行 Outlook COM 操作 (邮件/联系人)        │       │
│  │  - 代理 LLM 请求 (VW内部网关)                  │       │
│  │  - 提交结果到 /api/bridge/result              │       │
│  │  - 开机自启, 单实例运行                        │       │
│  └──────────────────────────────────────────────┘       │
│                                                         │
│  配置目录: %APPDATA%\GRCBridge\                           │
│    - token.txt    (认证Token)                            │
│    - api_url.txt  (服务器地址)                            │
│    - bridge.log   (日志)                                 │
│                                                         │
│  程序目录: %LOCALAPPDATA%\GRCBridge\GRCBridgeAgent.exe    │
└─────────────────────────────────────────────────────────┘
```

### 为什么需要 Bridge Agent?

Railway 云服务器无法访问公司内网资源:
- **Outlook COM**: 只能在安装了 Outlook 的 Windows 机器上运行
- **LLM 网关** (`llm-gateway.dev.cn-vwa.volkswagen-cea.com`): 只能从内网访问

Bridge Agent 运行在用户的办公电脑上,作为云端服务器和内网资源之间的桥梁。

---

## 3. 代码仓库与部署

### Git 仓库

| 远程名称 | URL | 用途 |
|---------|-----|------|
| origin | `https://gitlab.intranet.vwg-cea.cn/ai-scrum/regulation-ai.git` | VW 内部 GitLab (原始仓库) |
| github | `https://github.com/huzhe0308/GRC.git` | GitHub 镜像 (Railway 从此拉取) |

> **注意**: Railway 从 GitHub `main` 分支自动部署。推送到 GitHub main 分支后,Railway 会自动触发重新构建。

### 部署信息

| 项目 | 值 |
|------|-----|
| Railway URL | `https://grc-production-efc4.up.railway.app` |
| 监听端口 | 7860 (Railway 自动映射到 443) |
| 启动命令 | `python demo_app/server_unified.py` |
| 构建方式 | Nixpacks (见 `railway.json`) |
| Dockerfile | 基础镜像 `python:3.11-slim` |

### Railway 环境变量

以下环境变量需要在 Railway 控制台设置:

| 变量名 | 说明 | 示例值 |
|-------|------|--------|
| `TURSO_URL` | Turso 数据库 URL | `libsql://<db-name>-<org>.turso.io` |
| `TURSO_TOKEN` | Turso 认证 Token | (从 Turso 平台获取) |
| `TURSO_HTTP_URL` | Turso HTTP API URL (可选,自动从 TURSO_URL 转换) | `https://<db-name>-<org>.turso.io` |
| `PORT` | 监听端口 (Railway 自动注入) | `7860` |

> **关键**: `RAILWAY_ENVIRONMENT` 和 `RAILWAY_SERVICE_ID` 由 Railway 自动注入,代码中通过这些变量判断是否运行在云端。

### GitHub 推送注意事项

- `config.yaml` 包含 Jira Token,会被 GitHub Secret Scanning 拦截 (HTTP 409)
- `config.yaml` 已在 `.gitignore` 中,但如需更新远程版本,需使用 GitHub REST API 并先移除敏感信息
- `.jira_config`, `contacts.json`, `runtime/`, `build/`, `dist/` 也在 `.gitignore` 中

---

## 4. 核心代码文件说明

### 目录结构

```
regulation-ai/
├── demo_app/
│   ├── app.py              # 主业务逻辑 (4900+ 行) ★ 最核心文件
│   ├── server_unified.py   # aiohttp 异步服务器 (537 行) ★ 入口文件
│   ├── auth.py             # 用户认证系统 (380 行)
│   ├── bridge_manager.py   # Bridge 连接管理 (106 行)
│   ├── ws_server.py        # 旧版 WebSocket 服务器 (已弃用)
│   └── static/
│       ├── index.html      # 主页面 (登录后)
│       ├── login.html      # 登录/注册页面
│       ├── app.js          # 前端逻辑
│       ├── styles.css      # 样式表
│       ├── manual.html     # 用户手册 (HTML版)
│       └── downloads/
│           └── GRCBridgeAgent.exe  # Bridge Agent 可执行文件
├── bridge_agent.py          # Bridge Agent 源码 (852 行) ★ 本地代理
├── GRCBridgeAgent.spec      # PyInstaller 打包配置
├── config.yaml              # 主配置文件 (含 Jira Token, 不入库)
├── config.example.yaml      # 配置模板 (可入库)
├── requirements.txt         # Python 依赖
├── Procfile                 # Railway 启动命令
├── Dockerfile               # Docker 构建文件
├── railway.json             # Railway 配置
├── wiki/                    # 法规知识库 (300+ 文档)
├── scripts/                 # 业务脚本
├── runtime/                 # 运行时数据 (SQLite, 报告等)
└── AGENTS.md                # AI 助手配置文档
```

### app.py — 主业务逻辑

这是最核心的文件,包含所有业务逻辑。以下是关键函数清单:

#### 邮件与 Outlook
| 函数 | 行号 | 说明 |
|------|------|------|
| `fetch_emails()` | 273 | 扫描邮件 (云端走 Bridge, 本地走 Outlook COM) |
| `_try_bridge()` | 585 | 向 Bridge 发送命令的统一入口 |
| `outlook_latest_email()` | — | 获取最新邮件 |
| `outlook_search_emails()` | — | 搜索邮件 |
| `outlook_needs_reply()` | — | 获取待回复邮件 |
| `outlook_yesterday_emails()` | — | 获取昨日邮件 |
| `outlook_find_contact()` | — | 搜索联系人 |
| `outlook_email_detail()` | — | 查看邮件详情 |
| `send_assessment_email()` | — | 发送评估邮件 (通过 Outlook) |

#### LLM / AI 助手
| 函数 | 行号 | 说明 |
|------|------|------|
| `_call_llm_chat()` | 4213 | LLM 调用核心函数 (先走 Bridge 代理, 云端无 Bridge 则报错) |
| `chat_with_llm()` | 4700 | AI 助手对话 (多轮, 含知识库搜索) |
| `_llm_topic_summary()` | 4272 | 领域评论的 LLM 摘要生成 |
| `_llm_market_gap_verdict()` | — | 单市场 Gap 分析结论生成 |
| `_fallback_topic_summary()` | — | LLM 失败时的规则降级摘要 |

#### Jira 集成
| 函数 | 说明 |
|------|------|
| `_load_jira_config()` | 从 config.yaml 或 .jira_config 加载 Jira 认证 |
| `_jira_get()` / `_jira_post()` | Jira REST API 调用封装 |
| `_get_subtask_mapping()` | 获取父工单的子工单映射 (Cyber/Data 子票路由) |
| `_fetch_ticket_info()` | 获取工单详情 |
| `_get_ticket_comment_count()` | 获取工单评论数 |
| `write_summary_comment()` | 写结构化 Summary Comment 到 Jira Layer3 工单 |
| `close_layer3_ticket()` | 关闭 Jira Layer3 工单 |
| `parse_pvs_excel()` | 解析 PSV 表格 (支持标准格式和捷克格式) |

#### Gap 评估追踪
| 函数 | 说明 |
|------|------|
| `_ensure_gap_table()` | 初始化/迁移 SQLite 表结构 |
| `gap_tracking_status()` | 获取所有市场各领域的评估状态 |
| `gap_tracking_set_status()` | 手动设置状态 (带 manual_override 保护) |
| `gap_tracking_reset()` | 重置状态为 pending |
| `_auto_detect_na()` | 自动检测"不涉及"的领域 |
| `_auto_promote_evaluating()` | 自动将 pending 提升为 evaluating |
| `_mark_market_topic_gap_analysis()` | 标记 Gap 分析完成 (含 LLM 总结) |
| `build_topic_comments_report()` | 构建 Jira 评论分析报告 (多线程并发) |

#### 工单注册
| 函数 | 说明 |
|------|------|
| `register_ticket()` | 注册 Jira 工单 (写入 registered_tickets 表) |
| `unregister_ticket()` | 取消注册 |
| `get_registered_tickets()` | 获取已注册工单列表 |

#### 月报与分析
| 函数 | 说明 |
|------|------|
| `run_analysis_action()` | 分析模块入口 (SSE 流式响应) |
| `generate_monthly_report_html()` | 生成法规月报 HTML |
| `send_monthly_report_draft()` | 创建 Outlook 月报草稿邮件 |
| `get_export_markets_data()` | 获取出口市场数据 |

### server_unified.py — 异步服务器入口

Railway 部署的入口文件。使用 aiohttp 在单端口同时处理 HTTP 和 WebSocket。

**关键设计**: 所有阻塞型路由处理函数都通过 `asyncio.to_thread()` 包装,避免阻塞事件循环。每个包装器闭包会设置 `_thread_local.current_user`,因为 `asyncio.to_thread` 在不同线程中执行。

```python
# 典型路由模式 (所有路由都遵循此模式):
_cu = current_user
def _handler():
    _thread_local.current_user = _cu  # 线程间传播用户上下文
    return some_blocking_function(args)
return web.json_response(await asyncio.to_thread(_handler))
```

### auth.py — 认证系统

- **双模式**: 自动检测 `TURSO_URL` 环境变量,有则用 Turso 云数据库,无则用本地 SQLite
- **`_TursoConn` 类**: 模拟 `sqlite3.Connection` 接口,通过 HTTP API 操作 Turso
- **Session Token**: 随机生成,有效期 7 天 (`SESSION_TTL = 86400 * 7`)
- **密码存储**: SHA-256 + 随机 salt
- **用户 LLM 配置**: 每个用户独立存储 `api_key`, `llm_base_url`, `llm_model`

### bridge_manager.py — Bridge 连接管理

管理 Bridge Agent 的 HTTP 轮询连接:
- Bridge 每 2 秒轮询 `/api/bridge/poll` 获取待执行命令
- 服务器通过 `_command_queues[username]` 向 Bridge 推送命令
- Bridge 执行后通过 `/api/bridge/result` 提交结果
- `send_bridge_command_sync()` 同步等待结果 (基于 `threading.Event`)

**连接判定**: Bridge 最后一次 poll 在 30 秒内则视为"已连接"。

### bridge_agent.py — Bridge Agent

运行在用户 Windows 电脑上的本地程序。用 PyInstaller 打包成 exe。

**核心功能**:
- `cmd_scan_emails()`: 关键词+发件人+日期过滤扫描收件箱
- `cmd_read_latest()` / `cmd_search_emails()` / `cmd_needs_reply()` / `cmd_yesterday_emails()`: 邮件读取
- `cmd_find_contact()` / `cmd_send_email()` / `cmd_reply_email()`: 联系人和邮件发送
- `cmd_llm_proxy()`: 代理 LLM 请求到 VW 内部网关

**生命周期管理**:
- `self_install()`: 首次运行时从下载目录复制到 `%LOCALAPPDATA%\GRCBridge\`
- `setup_autostart()`: 创建 Windows 启动项快捷方式
- `is_already_running()`: 通过 Windows Mutex 保证单实例
- `stop_and_replace()`: 更新时自动停止旧版本
- `poll_loop()`: 主循环,含看门狗自动重启和 502 容错

---

## 5. 数据库结构

生产环境使用 Turso (libSQL),本地开发使用 SQLite。表结构相同。

### 表清单

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| `users` | 用户账户 | id, username, display_name, password_hash, salt, api_key, llm_base_url, llm_model |
| `sessions` | 登录会话 | token, user_id, username, created_at, expires_at |
| `user_settings` | 用户自定义设置 | user_id, settings_json (JSON, 含 scan_keywords, scan_lookback_days) |
| `gap_market_tracking` | 评估追踪状态 | market, topic (双主键), status, gap_summary, manual_override, manual_comment_count |
| `gap_layer3_closed` | 已关闭的 Layer3 | market, ticket_key, gap_summary, closed_at |
| `gap_inspection_log` | 巡检日志 | id, source, tickets_checked, changed, details, timestamp (保留最近100条) |
| `assessment_sent` | 已发送评估记录 | ticket_key, parent_key, sent_at, recipients |
| `registered_tickets` | 注册的工单 | ticket_key, registered_by, registered_at |

### gap_market_tracking 状态机

```
pending → evaluating → gap_analysis → summary_written → closed
                                                    ↓
                                               not_applicable (不涉及)
```

- `manual_override = 1`: 用户手动设置的状态,自动逻辑不会覆盖 (除非 Jira 有新评论)
- `manual_comment_count`: 记录设置手动状态时的评论数,用于检测新评论

### 表创建位置

所有表在 `app.py` 的 `_ensure_gap_table()` 函数中创建/迁移,位于 `app.py:3399`。认证表在 `auth.py` 的 `SCHEMA_SQL` 中定义。

---

## 6. Bridge Agent (邮件代理)

### 用户视角

1. 登录系统 → Settings → Download Bridge Agent (exe)
2. 双击 `GRCBridgeAgent.exe`
3. 程序自动安装到 `%LOCALAPPDATA%\GRCBridge\`
4. 提示输入 Token (从 Settings → Show Token 复制)
5. 输入后程序转入后台运行,设置开机自启
6. 网页顶部显示 "Outlook Bridge: Connected"

### 配置文件位置

| 文件 | 路径 | 内容 |
|------|------|------|
| Token | `%APPDATA%\GRCBridge\token.txt` | 认证 Token |
| API URL | `%APPDATA%\GRCBridge\api_url.txt` | 服务器地址 (默认 Railway URL) |
| 日志 | `%APPDATA%\GRCBridge\bridge.log` | 运行日志 |
| 程序 | `%LOCALAPPDATA%\GRCBridge\GRCBridgeAgent.exe` | 稳定位置的可执行文件 |
| 启动项 | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GRCBridgeAgent.lnk` | 开机自启快捷方式 |

### Bridge 命令清单

Bridge Agent 支持以下命令 (通过 HTTP 轮询接收):

| 命令 | 函数 | 说明 |
|------|------|------|
| `scan_emails` | `cmd_scan_emails()` | 关键词+发件人+日期过滤扫描收件箱 |
| `read_latest` | `cmd_read_latest()` | 获取最新邮件 |
| `search_emails` | `cmd_search_emails()` | 搜索邮件 |
| `needs_reply` | `cmd_needs_reply()` | 获取待回复邮件 |
| `yesterday_emails` | `cmd_yesterday_emails()` | 获取昨日邮件 |
| `email_detail` | `cmd_email_detail()` | 查看邮件详情 |
| `find_contact` | `cmd_find_contact()` | 搜索联系人 |
| `send_email` | `cmd_send_email()` | 发送邮件 |
| `reply_email` | `cmd_reply_email()` | 回复邮件 |
| `llm_proxy` | `cmd_llm_proxy()` | 代理 LLM 请求 |
| `ping` | `cmd_ping()` | 连接测试 |

### PyInstaller 打包

```bash
# 在项目根目录执行
pyinstaller GRCBridgeAgent.spec
# 输出: dist/GRCBridgeAgent.exe
# 复制到: demo_app/static/downloads/GRCBridgeAgent.exe
```

Hidden imports (已踩过的坑):
```python
hiddenimports=['win32timezone', 'win32com', 'win32com.client', 
               'pythoncom', 'pywintypes', 'pywin32_system32', 
               'win32com.client.gencache']
```

### Token 注意事项

- Token 文件必须用 `ascii` 编码写入,不能用 `utf-8` (否则 BOM 会导致 `latin-1` 编码错误)
- 读取时用 `utf-8-sig` 编码以兼容可能存在的 BOM
- Token 有效期 7 天,过期后 Bridge Agent 自动停止

---

## 7. 认证系统

### 认证流程

1. 用户登录 → `POST /api/auth/login` → 返回 Bearer Token
2. 前端存储 Token 到 `localStorage`
3. 后续请求携带 `Authorization: Bearer <token>`
4. `server_unified.py` 调用 `verify_token()` 验证
5. 验证通过后设置 `_thread_local.current_user`
6. 静态文件 (`/static/*`) 不需要认证

### Turso vs SQLite

- `auth.py` 检测 `TURSO_URL` 环境变量决定使用哪个后端
- `_TursoConn` 类模拟 `sqlite3.Connection` 接口
- **关键注意**: Turso v2 API 要求所有参数值为字符串类型 (不能传 int/float),`_convert_arg()` 方法处理转换
- `ALTER TABLE` 语句在 Turso 中不支持 `NOT NULL`,需要先加列再更新

### 用户体系

- 目前只有 1 个用户: `admin` (id=2)
- admin 用户使用 config.yaml 中的固定关键词 ("CEADU")
- 非 admin 用户可自定义扫描关键词和回看天数
- 每个用户独立配置 LLM API Key

---

## 8. API 接口清单

### 认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 注册新用户 |
| POST | `/api/auth/login` | 登录,返回 Token |
| POST | `/api/auth/logout` | 登出 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 邮件

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/emails?keywords=X&days=N` | 扫描邮件 (支持用户关键词) |
| GET | `/api/outlook/latest?sender=X` | 最新邮件 |
| GET | `/api/outlook/search?q=X&limit=N` | 搜索邮件 |
| GET | `/api/outlook/needs-reply?date=X` | 待回复邮件 |
| GET | `/api/outlook/yesterday` | 昨日邮件 |
| GET | `/api/outlook/find-contact?name=X` | 搜索联系人 |

### Bridge

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/bridge/status` | Bridge 连接状态 |
| GET | `/api/bridge/poll` | Bridge 轮询获取命令 |
| POST | `/api/bridge/result` | Bridge 提交执行结果 |
| GET | `/download/bridge` | 下载 Bridge Agent exe |

### 评估分配

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/assessments/send` | 发送评估邮件 |
| POST | `/api/parse-pvs` | 解析 PSV 表格 |
| GET | `/api/assessments/sent` | 已发送评估列表 |
| GET | `/api/tickets/registered` | 已注册工单列表 |
| POST | `/api/tickets/register` | 注册工单 |
| POST | `/api/tickets/unregister` | 取消注册 |

### 评估追踪

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/gap-tracking/status` | 所有市场评估状态 |
| POST | `/api/gap-tracking/set-status` | 手动设置状态 |
| POST | `/api/gap-tracking/reset-status` | 重置状态 |
| POST | `/api/gap-tracking/write-summary` | 写 Summary Comment 到 Jira |
| POST | `/api/gap-tracking/close-jira` | 关闭 Jira Layer3 工单 |

### 分析模块

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/analysis/{action}` | 运行分析 (支持 SSE 流式响应) |
| POST | `/api/analysis/topic_comments` | Jira 评论分析 |
| GET | `/api/monthly-report/generate` | 生成月报 HTML |
| POST | `/api/monthly-report/send-draft` | 创建 Outlook 月报草稿 |

### AI 助手

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat` | AI 对话 |
| POST | `/api/chat/send` | AI 对话 (同上) |
| POST | `/api/chat/session` | 创建对话会话 |
| POST | `/api/chat/new-session` | 创建对话会话 |
| POST | `/api/chat/delete` | 删除对话会话 |
| GET | `/api/chat/sessions` | 获取会话列表 |
| GET | `/api/chat/messages?session=X` | 获取会话消息 |

### 设置

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/settings` | 获取用户设置 |
| POST | `/api/settings` | 保存用户设置 |
| POST | `/api/settings/llm` | 保存 LLM 配置 |

### Wiki

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/wiki/search?q=X&limit=N` | 关键词搜索 |
| GET | `/api/wiki/search-semantic?q=X&limit=N` | 语义搜索 |
| GET | `/api/wiki/list` | 文件列表 |
| GET | `/api/wiki/file?path=X` | 读取文件内容 |

### 其他

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/status` | 系统状态快照 |
| GET | `/api/contacts` | 联系人列表 |
| GET | `/api/contacts?topic=X` | 按领域筛选联系人 |
| GET | `/api/export-markets/data` | 出口市场数据 |
| POST | `/api/pvs/sync` | 同步 PSV Wiki |
| POST | `/api/pvs/download` | 从 Jira 下载 PSV 附件 |

---

## 9. 前端文件说明

### 文件清单

| 文件 | 说明 |
|------|------|
| `static/index.html` | 主页面 (登录后), 包含所有功能模块的 HTML 结构 |
| `static/login.html` | 登录/注册页面 |
| `static/app.js` | 所有前端 JavaScript 逻辑 |
| `static/styles.css` | 全部样式 (4000+ 行) |
| `static/manual.html` | 用户手册 (独立页面, 无需登录) |

### 前端关键设计

- **单页应用**: `index.html` 包含所有视图,通过 CSS `display` 切换
- **Token 存储**: `localStorage.getItem("grc_token")`
- **认证检查**: 每次请求携带 `Authorization: Bearer <token>` 头
- **Bridge 状态**: 顶部状态栏轮询 `/api/bridge/status`,显示连接状态
- **SSE 分析流**: 分析模块使用 `fetch() + ReadableStream` 消费 Server-Sent Events
- **版本号**: `app.js?v=14` (HTML 引用时带版本号防缓存)

### CSS 变量

```css
:root {
  --accent: #0f6f86;          /* 主色调: 深青色 */
  --accent-strong: #0b5467;   /* 深色变体 */
  --bg: #eef2f7;              /* 背景: 浅灰蓝 */
  --text: #182233;            /* 正文: 深蓝灰 */
  --danger: #b42318;           /* 危险色: 红色 */
}
```

---

## 10. 配置文件说明

### config.yaml (主配置, 不入库)

```yaml
workflow:
  root_dir: "runtime"
  timezone: "Asia/Shanghai"
  mode: "api"

mail:
  backend: "outlook_com"
  subject_contains: ["CEADU"]   # 扫描关键词 (admin 使用)
  sender_contains: ""
  folder: "inbox"
  lookback_days: 30              # 回看天数
  max_emails: 10
  include_body_chars: 4000
  question_max_chars: 5000

jira:
  url: "https://devstack.vgc.com.cn/jira"
  token: "<JIRA_TOKEN>"          # ← 敏感信息,不入库

llm:
  enabled: true
  provider: "minimax"
  model: "MiniMax"
  api_key: ""
  base_url: "https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1"
  timeout_seconds: 120

wiki:
  root_dir: "wiki"
  search_limit: 8

send:
  backend: "outlook_com"
  dry_run: true
  to: []
  cc: []
  subject_prefix: "[GRC Agent]"
```

### .jira_config (Jira 认证, 不入库)

```json
{
  "url": "https://devstack.vgc.com.cn/jira",
  "token": "<JIRA_TOKEN>",
  "user": "Jingjing Xie"
}
```

### contacts.json (联系人, 不入库)

包含按领域分配的评估负责人信息。API: `/api/contacts` (GET/POST/PUT/DELETE)。

### requirements.txt

```
websockets==17.1
aiohttp>=3.9.0
requests>=2.28.0
pyyaml>=6.0
openpyxl>=3.1.0
```

> Bridge Agent 打包还需要: `pywin32`, `pyinstaller`

---

## 11. 本地开发环境搭建

### 前提条件

- Python 3.11+
- Windows 10/11 (Bridge Agent 和 Outlook COM 需要)
- Outlook 已安装并登录
- 能访问公司内网 (Jira, LLM 网关)

### 步骤

```bash
# 1. 克隆代码
git clone https://gitlab.intranet.vwg-cea.cn/ai-scrum/regulation-ai.git
cd regulation-ai

# 2. 添加 GitHub 远程 (Railway 从此拉取)
git remote add github https://github.com/huzhe0308/GRC.git

# 3. 安装依赖
pip install -r requirements.txt
pip install pywin32  # Bridge Agent 需要

# 4. 配置文件
cp config.example.yaml config.yaml
# 编辑 config.yaml,填入 Jira Token

# 5. 创建 .jira_config (可选,config.yaml 优先)
# 编辑 .jira_config

# 6. 启动本地服务器
python demo_app/server_unified.py
# 或双击 启动服务.bat

# 7. 访问
# http://127.0.0.1:7860
```

### 本地 vs 云端差异

| 行为 | 本地 (无 RAILWAY_ENVIRONMENT) | 云端 (Railway) |
|------|------|------|
| 数据库 | SQLite (`runtime/users.sqlite`) | Turso 云数据库 |
| 邮件扫描 | 直接 Outlook COM | 通过 Bridge Agent |
| LLM 调用 | 直接 urllib → 内部网关 | 通过 Bridge Agent 代理 |
| 静态文件 | 直接读取 | 直接读取 |

代码通过检测 `RAILWAY_ENVIRONMENT` / `RAILWAY_SERVICE_ID` / `DYNO` 环境变量来判断是否运行在云端。

---

## 12. 部署流程 (Railway)

### 自动部署

1. 代码推送到 GitHub `main` 分支
2. Railway 自动检测并触发构建
3. Nixpacks 构建: `pip install -r requirements.txt`
4. 启动: `python demo_app/server_unified.py`
5. 健康检查通过后,新版本上线

### 推送代码到 GitHub

由于 `config.yaml` 包含 Jira Token,无法通过 `git push` 推送。有两种方式:

#### 方式一: 正常 git push (不含 config.yaml)

```bash
# config.yaml 在 .gitignore 中,不会被推送
git add .
git commit -m "your message"
git push github main
```

#### 方式二: GitHub REST API (推送单个文件)

用于推送被 .gitignore 忽略或被 Secret Scanning 拦截的文件:

```python
import base64, json, urllib.request

token = "gho_xxx"  # GitHub PAT
repo = "huzhe0308/GRC"
path = "demo_app/static/index.html"
branch = "main"

# 读取文件内容
with open(path, "rb") as f:
    content_b64 = base64.b64encode(f.read()).decode()

# 获取远程 SHA (如果文件已存在)
# ... GET https://api.github.com/repos/{repo}/contents/{path}?ref={branch}

# 推送
payload = {"message": "update", "content": content_b64, "branch": branch}
# ... PUT https://api.github.com/repos/{repo}/contents/{path}
```

### Railway 环境变量配置

在 Railway 控制台 (https://railway.app) → 项目 → Variables 中设置:

- `TURSO_URL`: Turso 数据库 URL
- `TURSO_TOKEN`: Turso 认证 Token

### 查看日志

Railway 控制台 → 项目 → Deployments → 最新部署 → Logs

---

## 13. Bridge Agent 构建流程

### 前提条件

- Windows 10/11
- Python 3.11
- pywin32, pyinstaller

### 构建步骤

```bash
# 1. 安装依赖
pip install pywin32 pyinstaller

# 2. 构建 exe
cd C:\Users\<username>\regulation-ai
pyinstaller GRCBridgeAgent.spec

# 3. 验证
dist\GRCBridgeAgent.exe --help

# 4. 复制到下载目录
copy dist\GRCBridgeAgent.exe demo_app\static\downloads\GRCBridgeAgent.exe

# 5. 推送到 GitHub (exe 不在 .gitignore 排除外,downloads 目录允许)
# 使用 GitHub REST API 推送
```

### 已踩过的坑 (PyInstaller)

| 问题 | 解决方案 |
|------|---------|
| `win32timezone` ModuleNotFoundError | 加入 hiddenimports |
| `pywintypes` ModuleNotFoundError | 加入 hiddenimports |
| `win32com.client.gencache` ImportError | 加入 hiddenimports |
| Token 文件 BOM 导致 `latin-1` 编码错误 | Token 用 `ascii` 编码写入,读取用 `utf-8-sig` |

---

## 14. 已知问题与注意事项

### 架构层面

1. **LLM 网关仅内网可达**: Railway 云服务器无法直接访问 `llm-gateway.dev.cn-vwa.volkswagen-cea.com`。所有 LLM 请求必须通过 Bridge Agent 代理。如果 Bridge 未连接,AI 功能不可用。

2. **Outlook COM 仅 Windows**: 邮件功能依赖 Windows Outlook COM 接口,只能在安装了 Outlook 的 Windows 机器上通过 Bridge Agent 运行。

3. **config.yaml 不能推送到 GitHub**: 包含 Jira Token,会被 GitHub Secret Scanning 拦截 (HTTP 409)。代码中有硬编码的 fallback 默认值。

4. **单端口限制**: Railway 只暴露一个端口。`server_unified.py` 使用 aiohttp 在同一端口同时处理 HTTP 和 WebSocket。

5. **事件循环阻塞**: 早期版本中阻塞型函数直接在 async handler 中运行,导致 Bridge 轮询请求被阻塞。已通过 `asyncio.to_thread()` 修复,但新增路由时必须遵循此模式。

6. **线程间用户上下文**: `asyncio.to_thread()` 在不同线程中执行,`_thread_local.current_user` 不会自动传播。每个路由包装器必须手动设置。

### 业务层面

1. **Token 7 天过期**: 用户需要定期重新登录获取 Token,并更新 Bridge Agent。

2. **PSV 格式差异**: India (CEADU-3784) 使用捷克格式 (无 "Regulation Focus list" sheet,列索引不同)。`parse_pvs_excel()` 有自动检测逻辑。

3. **Jira 工单号规则**:
   - Cyber/Data Security 使用各自的子工单评估
   - FuSa/OTA/OBD/Immobilizer 使用 Layer3 工单评估
   - 部分市场无独立 OBD 子票 (OBD 评估在 Layer3 工单内)

4. **手动覆盖保护**: 用户手动设置的评估状态不会被自动逻辑覆盖 (除非 Jira 工单有新评论)。`gap_market_tracking.manual_override` 和 `manual_comment_count` 字段实现此逻辑。

5. **月报数据源**: 月报从本地 Excel 文件读取 (`runtime/Export_Markets_Layer3_Comparison.xlsx`),路径在 `app.py` 中硬编码。云端环境需要手动上传 Excel 文件或修改数据源逻辑。

### 依赖与版本

- `websockets==17.1`: 固定版本 (旧版 WebSocket 服务器使用,现已弃用但保留依赖)
- Turso HTTP API v2: 要求所有参数为字符串类型

---

## 15. 关键业务逻辑

### 云端检测

```python
is_cloud = bool(os.environ.get("RAILWAY_ENVIRONMENT") 
                or os.environ.get("RAILWAY_SERVICE_ID") 
                or os.environ.get("DYNO"))
```

在 `fetch_emails()` (app.py:291) 和 `_call_llm_chat()` (app.py:4222) 中使用。

### LLM 调用链

```
chat_with_llm() 
  → _call_llm_chat()
    → _try_bridge("llm_proxy", {...})     # 先尝试 Bridge 代理
    → if cloud and no bridge: return error  # 云端无 Bridge = 报错
    → else: urllib.request.urlopen()      # 直接调用 (本地可用)
```

### 邮件扫描链

```
fetch_emails()
  → if cloud:
    → _try_bridge("scan_emails", {keywords, days_back, limit})  # Bridge 扫描
  → else:
    → find_emails(config)  # 直接 Outlook COM
```

### Gap 追踪状态自动推进

```
gap_tracking_status(auto_detect_na=True)
  → _auto_detect_na()     # 检测 Jira 票已取消的领域 → not_applicable
  → _auto_promote_evaluating()  # 检测有评论的领域 → evaluating
  → (manual_override=1 的领域跳过,除非有新评论)
```

### 市场映射 (代码常量)

| 工单号 | 市场 |
|--------|------|
| CEADU-682, CEADU-2631 | Korea |
| CEADU-2739 | ASEAN RHD |
| CEADU-3005 | ASEAN LHD |
| CEADU-3784 | India |
| CEADU-4514 | Middle East |
| CEADU-4494 | Kazakhstan |
| CEADU-5282, CEADU-7082 | Uzbekistan |
| CEADU-6364 | Turkey |
| CEADU-2711, CEADU-6294, CEADU-6746 | AUS/NZL |

---

## 16. 常用运维操作

### 重启 Bridge Agent

```bash
# 方法1: 任务管理器
# 找到 GRCBridgeAgent.exe → 结束任务 → 双击重新启动

# 方法2: 命令行
taskkill /IM GRCBridgeAgent.exe /F
# 然后双击 %LOCALAPPDATA%\GRCBridge\GRCBridgeAgent.exe
```

### 查看 Bridge 日志

```bash
type %APPDATA%\GRCBridge\bridge.log
```

### 清除 Bridge 配置 (重新输入 Token)

```bash
GRCBridgeAgent.exe --forget
```

### 禁用 Bridge 开机自启

```
Win+R → shell:startup → 删除 GRCBridgeAgent.lnk
```

### 查看数据库内容 (Turso)

通过 Turso 平台 Web 界面查看,或使用 `turso` CLI:

```bash
turso db shell <db-name>
# 然后可以执行 SQL 查询
```

### 推送代码更新

```bash
# 正常代码推送
git add .
git commit -m "your message"
git push github main

# Railway 会自动触发部署
# 查看部署状态: https://railway.app → 项目 → Deployments
```

### 本地测试

```bash
# 启动本地服务器 (使用本地 SQLite,不走 Turso)
python demo_app/server_unified.py

# 访问 http://127.0.0.1:7860
# 邮件和 LLM 功能可直接使用 (不走 Bridge)
```

---

## 17. 交接清单

### 账号与凭证

| 项目 | 说明 | 状态 |
|------|------|------|
| GitHub 账号 | `huzhe0308` — 需要转移仓库所有权或添加协作者 | ☐ 待交接 |
| Railway 项目 | `grc-production-efc4` — 需要转移项目所有权或添加成员 | ☐ 待交接 |
| Turso 数据库 | 需要转移数据库所有权或共享 Token | ☐ 待交接 |
| Jira Token | config.yaml 中的 token — 需要确认是否需要更换 | ☐ 待确认 |

### 代码仓库

| 仓库 | URL | 状态 |
|------|-----|------|
| VW GitLab | `https://gitlab.intranet.vwg-cea.cn/ai-scrum/regulation-ai.git` | ☐ 确认访问权限 |
| GitHub | `https://github.com/huzhe0308/GRC.git` | ☐ 转移或共享 |

### 文档

| 文档 | 位置 | 说明 |
|------|------|------|
| 本交接文档 | `HANDOVER.md` (本项目根目录) | 技术交接 |
| 用户手册 | `USER_MANUAL.md` + `demo_app/static/manual.html` | 终端用户文档 |
| AGENTS.md | `AGENTS.md` | AI 助手配置与功能清单 (详细) |
| 启动教程 | `demo_app/启动教程.md` | 本地启动中文教程 |

### 本地文件 (需确认是否需要转移)

| 文件/目录 | 位置 | 说明 |
|----------|------|------|
| Bridge Agent exe | `%LOCALAPPDATA%\GRCBridge\GRCBridgeAgent.exe` | 当前运行版本 |
| Bridge 配置 | `%APPDATA%\GRCBridge\` | Token, API URL, 日志 |
| Excel 报告数据 | `runtime/` | SQLite 数据库, 报告文件 |
| 法规知识库 | `wiki/` | 300+ 法规文档 (已在 GitHub) |

### 关键联系人

| 角色 | 姓名 | 联系方式 |
|------|------|---------|
| 系统开发者 | 胡哲 (huzhe0308) | (交接人) |
| Jira 用户 | Jingjing Xie | (Jira 配置中的用户) |
| Functional Safety | Sun, Hao (Dr.) | 评估负责人 |
| Cyber/Data Security | Kunze, Kai | 评估负责人 |
| 全领域 (GVEX) | Xie, Jingjin | 评估负责人 |

---

*文档结束。如有疑问请联系交接人。*
