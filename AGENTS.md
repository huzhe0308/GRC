# G.R.C. Agent - AGENTS.md

> Last updated: 2026-08-13 (UI英文化✅ 手动覆盖保护✅ 定期巡检✅ 已发送标识✅)

## 系统概述
Governance, Risk & Compliance 功能分配与评估助手，整合邮件处理、Jira工单评论、PSV表格解析、法规评估分配。

## 三段式工作流

| 阶段 | 模块 | 说明 |
|------|------|------|
| 入口 | 评估分配 | 邮件识别 → PSV解析 → 分配负责人 → 发送评估 |
| 过程 | 评估追踪 | Gap分析 → Summary Comment写入Jira → 关闭Layer3票 |
| 出口 | 综合分析 | 全部评估完成后 → 综合月报 → 反馈团队 |

辅助模块：**法规Wiki**（搜索法规依据，支持关键词+语义搜索）| **联系人管理**（维护评估负责人）

## 核心功能模块

### 1. 评估分配
**场景**: 扫描邮件 → 选择任务 → 解析PSV表格 → 选择收件人 → 发送评估

### 2. 评估追踪（单个评估）
**场景**: 评估分配完成后 → 各市场各领域 Gap 分析 → 完成后写 Summary Comment 到 Jira

**工作流**：
- Jira票更新 → 评估中 → Gap分析完成 → 写 Summary Comment → 关闭Layer3票
- **Cyber/Data**: 在各自子票评估（有子票），无子票=不涉及
- **FuSa/OTA/Immobilizer**: 在Layer3票评估
- **Summary Comment**: 单个评估终点，所有领域评论 Gap 分析完成后写入 Jira，作为该评估的最终结论
- 所有领域的Comments Gap分析足以给出结论后 → 关闭Layer3票

**状态机**: `pending → evaluating → gap_analysis → summary_written → closed`
- `pending`: 初始状态
- `evaluating`: Jira工单正在评估（已更新评论）
- `gap_analysis`: Gap分析完成，足以给出结论
- `summary_written`: Summary Comment 已写入 Jira
- `closed`: Layer3票已关闭

**实现**:
- SQLite: `gap_market_tracking`（market+topic双主键，含gap_summary）+ `gap_layer3_closed`（含gap_summary）
- **票号规则**：Cyber/Data用自己的子票，FuSa/OTA/Immobilizer用Layer3票，OBD用自己的票（部分市场无OBD票）
- topic_comments 每次成功运行后，自动按 Market 标记该市场该领域为 `gap_analysis`（含LLM总结）
- 每个市场显示：Layer3票链接 + 领域Chip（显示状态标签） + 进度条
- **点击Chip**：pending→evaluating→gap_analysis，gap_analysis→重置为pending
- **全部 gap_analysis**（所有领域）→ 显示"写 Summary Comment"按钮
- **Summary Comment 写入后** → 显示"关闭 Layer3 工单"按钮
- **只能关闭 Layer3 票**（子票属于其他团队，不可操作）
- Layer3 已关闭的市场自动显示"已关闭"徽章

### 3. 综合分析（月报汇报）
**场景**: 所有评估的 Summary Comment 都写完后 → 综合月报 → 反馈团队
- 依赖模块2全部完成（每个评估都写了 Summary Comment）
- 汇总所有市场的合规状态 → 生成综合月报 → 发送团队

**分析工具布局**（`POST /api/analysis/<action>`）：
| 入口 | 类型 | 描述 |
|------|------|------|
| 综合市场分析 | Hero 按钮（蓝） | 出口市场 Layer3 合规状态总览 |
| 全部领域评论 | Hero 按钮（紫） | 5大领域 · Jira评论 · 实时数据 |
| OBD | 分领域 | 10条评论 · Kazahstan/Middle East/Turkey |
| FuSa | 分领域 | 59条评论 · 10个市场 |
| Cybersecurity | 分领域 | 64条评论 · Korea/India/Turkey/AUS/NZL |
| OTA | 分领域 | 46条评论 · 6个市场 |
| Immobilizer | 分领域 | 92条评论 · 6个市场 |
| 生成Excel报告 | 导出 | create_excel_final.py |

**Jira评论API** (`POST /api/analysis/topic_comments`)：
- 直接调用Jira REST API（多线程并发）
- 返回每个市场工单的状态、负责人、最新10条评论 + 评论总数
- 卡片式渲染，评论可点击展开/收起
- MARKETS 常量（10市场，与 comprehensive_analysis.py 一致）作为唯一数据源，TOPIC_CONFIG 由 `_build_topic_config()` 动态生成，覆盖6领域：cyber_security(🔐) / data_security(🔒) / fusa_data(🛡) / ota_data(🔄) / immobilizer_data(🔗) / obd_data(📺)
- 每市场卡片字段: parent=主工单, layer3=Layer3工单, domain=领域子工单（各领域精确映射）
- **LLM摘要层**：每个领域获取评论后调用 MiniMax 生成结构化中文分析（总体判断/各市场状态/风险阻塞/建议行动），失败时降级为规则摘要（`_fallback_topic_summary`）

**报告导出**：
- `layer3_excel` → create_excel_final.py（含4个Sheet）
- **新增**: "Data Consistency Check" sheet，生成Excel时自动从Jira获取工单状态，与报告中状态对比，不一致行标红
- 输出路径: `C:/Users/T1UKLL7/Desktop/Workstation/Analysis/output/Export_Markets_Layer3_Comparison_new.xlsx`

**AI推理过程展示（SSE流）**：
- 分析API支持 `POST /api/analysis/{action}` + body `{ "_stream": true }`
- 返回 `text/event-stream`，每个事件为 `event: progress/data: {status,message,step}` 或 `event: done`
- 前端 `runAnalysis()` 使用 `fetch() + ReadableStream` 消费 SSE
- `thinkingArea` 实时显示步骤（准备/分析中/渲染），完成后自动折叠，显示重试按钮
- 支持 AbortController 取消（取消按钮），重试按钮复用上次 action
- 展开/折叠按钮支持 `aria-expanded`/`aria-controls` 无障碍属性
- 步骤列表动态更新，spinner 动画，完成后变为绿色勾号

**法规月报**：
- 分析模块"报告导出"已替换为"📧 发送法规月报"按钮
- 数据源: `C:\Users\T1UKLL7\Desktop\Workstation\Report\input\Export_Markets_Layer3_Comparison.xlsx`
  - Sheet "Layer 3 Comparison" (行6-15) → Market Overview 表格
  - Sheet "In Progress Details" (行5+) → Critical/Action/Recently Closed 条目
- API:
  - `GET /api/monthly-report/generate` → 读取Excel生成HTML邮件
  - `POST /api/monthly-report/send-draft` → 创建Outlook草稿（非阻塞 Display(False)）
- 收件人默认值: `MONTHLY_REPORT_DEFAULT_TO` (10人) + `MONTHLY_REPORT_DEFAULT_CC` (9人)
- 邮件结构: Hi team → 统计徽章(Critical/Action/Closed/Markets) → Market Overview彩色状态表 → Critical/Action/Closed条目 → 签名
- **Market Overview 表头与Excel一致**: Market | Ticket | Target Countries | Platform | Vehicle Type | SOP Target | Cyber Sec | Data Sec | OTA | OBD | FuSa
- **OBD状态标准**（2026-08核对Jira后）: KZ/UAE OBD工单(CEADU-4864/5081) 6/29已Closed（TMT-E 5/20批准 12MM/10.5MM）→ Excel显示 "Baseload"；Turkey (CEADU-6699) 仍 In Progress
- Outlook COM 草稿预览后自动发送（手动确认）

**服务启停**：
- 启动: `启动服务.bat`（双击）→ 自动杀旧进程 → 后台启动python（隐藏窗口）→ 验证端口 → 开浏览器
- 关闭: `关闭服务.bat`
- 启动脚本: `start_demo.ps1`（PID写入日志 runtime\server_stdout.log / server_stderr.log）
- 服务在后台独立运行，关闭启动窗口不影响服务

**渲染样式**: 月报模板风格（市场表格+彩色状态徽章+卡片布局）

### 4. 合规追踪
- 出口市场Layer3合规状态
- Jira评论分析
- 生成合规报告

### 5. 需求管理
- 生成的评估需求管理
- 发送审核

### 6. 法规Wiki
**场景**: 评估时查询法规依据，分析时核对条款

**搜索功能**：
- **关键词搜索**（默认）：基于 BM25 算法，支持原始法规全文检索（从 raw/papers 目录），返回相关性排序结果
- **语义搜索**（点击 🔮 按钮）：先用关键词召回约 30 个候选，再用 LLM 对每个结果语义打分（0-4分），按语义相关性重排，LLM 理解查询意图后返回真正最相关的内容
- 支持筛选按文件名、标题、更新时间排序
- 结果卡片显示：法规编号、标题、匹配片段预览、文件路径

**知识库结构** (`_archive_llm_wiki/`):
| 目录 | 内容 |
|------|------|
| `raw/` | 原始法规文档（30+ 篇，含 ISO/UN/Guest Country 标准） |
| `entities/` | 法规实体卡片 |
| `concepts/` | 概念定义 |
| `comparisons/` | 法规对比 |
| `queries/` | 常见问题 |
| `pvs/` | PSV 表格文件 |

**API 端点**:
- `GET /api/wiki/search?q=<query>&limit=<n>` — 关键词搜索
- `GET /api/wiki/search-semantic?q=<query>&limit=<n>` — 语义搜索

**LLM 配置**: MiniMax (`https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1`)

### 7. 联系人管理
- 维护评估负责人
- 按Topic分配职责
- 发送评估时选择收件人

### 8. AI助手 (悬浮窗)
**场景**: 右下角浮动助手，任何页面随时提问
- 🤖 右下角悬浮按钮，点击展开
- 💬 基于LLM的对话式AI助手
- 📧 **邮件集成**（NB Outlook技能）：查看邮件、搜索、发邮件
- 📚 知识库搜索（Wiki + 记忆）
- ⚡ 邮件快捷按钮：最新邮件、搜索邮件、待回复邮件
- 📝 上下文感知（多轮对话）
- 🔍 知识库增强（自动关联Wiki条目）

### 9. 自动巡检
**场景**: 定时任务处理邮件和Jira工单
- 邮件巡检（按配置频率自动检查新邮件）
- Jira工单监控（新工单提醒）
- 自动生成报告并发送

## Jira配置
- **URL**: https://devstack.vgc.com.cn/jira
- **Token**: Bearer认证
- **配置文件优先级**: `app.py同级/.jira_config` > `skills/Jira-access/.jira_config`
- **用户**: Jingjing Xie

## LLM配置
- **Model**: MiniMax
- **Base URL**: https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1

## Web UI (http://127.0.0.1:7860)
- 左侧导航: 今日待办 → 评估分配 → 评估追踪 → 分析模块 → 合规追踪 → 需求管理 → 法规Wiki
- 右下角: 🤖 AI助手悬浮窗 (所有页面可用)
- 分析工具: Hero双列布局 + 5列分领域网格

## PSV文件目录
- **路径**: `C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\pvs`
- **解析逻辑**:
  1. 从Jira下载所有PSV附件，选择**最高版本**（Vx.0格式，取数值最大）
  2. 查找本地包含parent_key的文件（选最高版本）
  3. 查找本地包含市场名的文件（选最高版本）
  4. fallback数据

### PSV 文件格式识别（app.py `parse_pvs_excel`）
**捷克格式检测规则**（自动识别，无需手动干预）：
1. 无 "Regulation Focus list" sheet
2. 任一 sheet 名称含 `souhrn` 或 `szp` → 判定为捷克格式
3. 或任一 sheet 前3行文本中含 "english theme" + "themengebiet" → 判定为捷克格式

**捷克格式列映射** (R1=标题行, R2=表头, R3起=数据):
| 字段 | 列索引 | 说明 |
|------|:---:|------|
| Topic | 0 | "English theme" |
| DocID | 2 | "Regularie" (如 AIS-189) |
| DocName | 4 | "Titel" |
| Mandatory | 11 | "Alle Fahrzeuge" 有日期=mandatory，空=if fitted |

**Layer3 关键词**（app.py `LAYER3_KEYWORDS`）：
- **Data Security** 包含: `data security`, `data privacy`, `privacy`, `personal data`, `gdpr`, `data protect`
- PSV 中大量条目 Topic 为 `xxx data privacy`（如 s.korea/australia/new zealand/malaysia/vietnam/indonesia/thailand/philippines/singapore）→ 归入 Data Security

**已知捷克格式**: India (CEADU-3784)
**已知标准格式**: Turkey, Korea, Uzbekistan, Australia/NZ, Middle East 等（含 "Regulation Focus list" sheet）

## 市场映射
| 工单 | 市场 |
|------|------|
| CEADU-682 | Korea |
| CEADU-2631 | Korea |
| CEADU-2739 | ASEAN RHD |
| CEADU-3005 | ASEAN LHD |
| CEADU-3784 | India |
| CEADU-4514 | Middle East |
| CEADU-4494 | Kazakhstan |
| CEADU-5282 | Uzbekistan |
| CEADU-6364 | Turkey |
| CEADU-2711 | AUS/NZL |
| CEADU-6294 | AUS/NZL |
| CEADU-6746 | AUS/NZL |
| CEADU-7082 | Uzbekistan |
| CEADU-7085 | (同CEADU-7082) |

## Layer3 Topics (10个领域)
- Cyber Security, Data Security, OTA, OBD, Functional Safety
- Diagnostics, Network, Immobilizer-theft, Cryptography, Geolocation Data

## 联系人配置
- **文件**: `C:\Users\T1UKLL7\Desktop\Workstation\employee agent\contacts.json`
- **API**: `/api/contacts` (GET/POST/PUT/DELETE)
- **负责人**:
  - Sun, Hao (Dr.) - Functional Safety
  - Xie, Jingjin - 全领域(GVEX)
  - Kunze, Kai - Cyber Security, Data Security, Immobilizer-theft

## 目录结构
```
GRC Agent/  (原 employee agent/)
├── demo_app/
│   ├── app.py         # 后端API (7860端口) + topic_comments API
│   └── static/
│       ├── index.html # Hero双列布局 + 分领域网格
│       ├── app.js     # runTopicComments() + 卡片渲染器
│       └── styles.css # hero-btn / topic-card 样式
├── scripts/           # 业务脚本
├── contacts.json      # 联系人配置
├── .jira_config       # Jira认证配置
├── config.yaml        # 主配置
├── memory/            # 记忆服务 (SQLite)
│   └── memory_service.py
└── runtime/           # 运行时数据
    ├── reports/       # 生成的报告
    ├── chat_memory.json
    ├── chat_sessions.json
    ├── memory.sqlite
    └── state.sqlite
```

## Memory 服务
SQLite 数据库（`runtime/memory.sqlite`），3张表：
| 表 | 用途 |
|----|------|
| `conversation_memory` | 对话历史（run_id/session_id/role/content/wiki_hits） |
| `knowledge_cards` | 问答卡片（去重hash + 相似度匹配） |
| `entity_relations` | 实体关系图（实体/关系类型/关联实体） |

核心方法：`store_question_answer()`、`find_similar_question()`、`build_context_prompt()`

## 已完成功能
- [x] 评估分配模块（邮件→PSV→联系人→发送）
- [x] 邮件扫描识别（包含CEADU即显示）
- [x] Parent工单跳转
- [x] PSV表格解析 + Layer3法规匹配（10个领域）
- [x] 联系人管理模块 + 按Topic分配
- [x] 从Jira自动下载PSV附件
- [x] AI助手悬浮窗（右下角全局可用）
- [x] 对话功能（多轮对话、上下文记忆）
- [x] 知识库增强搜索（自动关联Wiki）
- [x] 邮件集成（NB Outlook技能）
- [x] 分析模块：月报风格渲染（市场表格+彩色状态徽章+卡片）
- [x] Agent重命名：Employee → G.R.C.
- [x] 移除独立"数据一致性检查"按钮 → 集成至Layer3 Excel（Data Consistency Check sheet）
- [x] 分领域验证 → 分领域评论分析（重构）
- [x] 新增 topic_comments API（直接Jira REST，多线程）
- [x] 分析工具UI：Hero双列按钮 + 5列自适应网格
- [x] 移除"最近分析记录"（不保存历史）
- [x] 评估邮件英文版 + HTML格式 + JIRA工单可点击链接
- [x] 评估邮件主题改为 Parent ticket + 市场/平台后缀（如 CEADU-6364 (MQB Export/Turkey)）
- [x] Cyber Security / Data Security 动态Sub-task路由（从Jira获取子工单映射）
- [x] PSV捷克格式自动识别解析（India CEADU-3784：无 Regulation Focus list，列索引偏移）
- [x] 法规月报功能（分析模块"报告导出"→"发送法规月报"，自动从Excel读取数据生成HTML邮件，创建Outlook草稿预览后发送）
- [x] AI推理过程展示（分析模块SSE流式响应，thinkingArea显示分析步骤，支持展开/折叠、取消、重试；状态：加载中/进行中/成功/失败/已取消）
- [x] PSV Layer3 关键词补充：Immobilizer-theft（"immobilizer"/"vehicle alarm"）
- [x] 移除Outlook COM检测横幅（index.html/JS/CSS/app.py中相关代码全部清理）
- [x] OBD状态修正：Excel KZ/UAE OBD列 Required → Baseload（Jira工单6/29已Closed，TMT-E 5/20批准）
- [x] 月报邮件Market Overview表头升级：与Excel一致，含Platform/Vehicle Type列
- [x] 综合市场分析Market Overview表头升级：11列与Excel完全一致（Market|Ticket|Target Countries|Platform|Vehicle Type|SOP Target|Cyber Sec|Data Sec|OTA|OBD|FuSa），前端识别条件更新为英文表头检测
- [x] 综合市场分析Market Overview状态全面更新（2026-08-12 Jira评论分析）：描述性状态标签（Baseload/In Progress/Completed/Covered/Required/N/A）替代emoji，风险分级HIGH/MID/LOW，Action Items/Critical Items 依据工单最新评论重写；SSE输出剥离ANSI码；app.js statusBadge支持新描述性标签；关键修正：Turkey OBD EU7排放无gap已确认但(EU)2018/858 OBD信息访问权待评估、CSP31 OTA无SUMS→N/A、India OTA RxSWIN非强制→Baseload
- [x] Critical Items前端解析升级：extractActionItems支持emoji(🔴🔶⚪)+纯文本双格式识别；critItems关键词扩充OTA/OBD/scope/market名；P1/P2/P3每项均附CEADU编号便于Jira跳转
- [x] comprehensive_analysis.py内容调整：删除"第三部分 OBD适配详细分析"整块表格；OTA新增R156法规Layer3评估结论（RXSWIN软件更新时须同步更新）；章节重新编号：行动项=三、风险评估=四
- [x] topic_comments准确性全面提升（2026-08-12）：(1)MARKETS常量作为唯一数据源（10市场，与comprehensive_analysis.py一致），TOPIC_CONFIG动态生成（6领域：Cyber/Data/FuSa/OTA/Immobilizer/OBD，各领域ticket精确映射）；(2)评论获取5条→10条，卡片显示"▼ N comments (of M total)"；(3)LLM摘要层：每个领域自动调用MiniMax生成结构化中文分析（总体判断/各市场状态/风险阻塞/建议行动），失败时降级为规则摘要；(4)修复FuSa/OTA/Immobilizer按钮调用runTopicComments（之前错误调用runAnalysis）；(5)数据源全部改为Layer3工单（FuSa/OTA/Immobilizer/Cyber/Data均无独立子票，评论在Layer3工单内），Immobilizer修复为mk_entries("layer3")
- [x] topic_comments运行逻辑修复（2026-08-12）：runTopicComments()添加showThinking()调用（之前从未显示thinking区导致无法折叠）；统一setThinkingExpanded()/setFinalState()状态管理；thinking区默认折叠1秒后展开
- [x] topic_comments上线验证（2026-08-12实测）：全6领域406条评论，LLM摘要全部生成成功；OTA/OBD工单与Jira实况交叉验证；服务运行正常
- [x] UI模块重命名（2026-08-12）：导航"报告管理"→"需求管理"，模块内容同步更新（报告审阅→需求审阅，报告列表→需求列表，相关提示文案）
- [x] Hero文案更新（2026-08-12）：主页描述从"评估分配 → 分析验证 → 报告生成"更新为"评估分配 → 合规分析 → 月报发送"（反映真实三步工作流）
- [x] 分析模块 thinking 折叠（2026-08-12）：thinking body 内容默认折叠，1秒后自动展开，用户可手动折叠/展开分析步骤 |
- [x] 评估追踪模块（2026-08-12）：新增"评估追踪"导航页 + `gap_tracking` SQLite表 + API（`GET/POST /api/gap-tracking/status`、`/api/gap-tracking/set-status`、`/api/gap-tracking/close-jira`）；topic_comments 每次成功运行后自动将对应Market-Topic标记为 gap_analysis（含LLM总结）；全部领域 gap_analysis 后 → 显示"写 Summary Comment"按钮 → 写入 Jira 后 → 显示"关闭 Layer3"按钮；支持手动推进/重置状态 |
- [x] 评估追踪状态流程（2026-08-12）：状态机 `pending→evaluating→gap_analysis→summary_written→closed`；gap_analysis=Gap分析完成可写结论；summary_written=Summary Comment 已写入 Jira（单个评估终点）；closed=Layer3票已关闭；topic_comments自动标记为 gap_analysis（含LLM总结）
- [x] 评估追踪状态来源修复（2026-08-12）：cyber/data 评论来源从 Layer3 票修正为各自的 Cyber/Data 子票（如 South Korea CEADU-2623）；LLM 逐市场分析评论内容判定状态（Jira票关闭→gap_analysis，取消→not_applicable，无评论→pending，有评论但无结论→evaluating）；取消的子票显示"不涉及"chip，不计入can_close阻塞 |
- [x] Uzbekistan/CSP31 OBD票号修正（2026-08-12）：Uzbekistan OBD `CEADU-5282(parent)→CEADU-6502(layer3)`；AUS/NZL CSP31 OBD `CEADU-6746(parent)→CEADU-6749(layer3)`。无专用OBD子票的市场OBD评估在Layer3票内（OBD评论实际在Layer3，如Uzbekistan CEADU-6502含UN-R 83.06 OBD评估9条评论） |
- [ ] 评估追踪手动覆盖保护（进行中-2026-08-13）：用户手动改过状态的 market+topic，自动逻辑不再覆盖（除非该 Jira 票新增评论）。机制：`gap_market_tracking` 新增 `manual_override`(INT) + `manual_comment_count`(INT) 列；`_mark_market_topic_pending` 改为 UPSERT 保留行而非 DELETE（保留 manual_override 标记）；新增 `_get_ticket_comment_count()` 辅助函数。剩余待改：`gap_tracking_set_status/reset` 记录标记、`_auto_detect_na`/`_auto_promote_evaluating`/`gap_tracking_status`/`build_topic_comments_report` 跳过 manual_override=1 且无新评论的行 |
- [x] 评估追踪手动覆盖保护完成（2026-08-13）：A1/A2/A3 全部验证通过。全链路：手动设置→自动巡检不覆盖；新增评论→允许自动更新。`_auto_detect_na` UPDATE 前复查 manual_override；`_auto_promote_evaluating` 已有保护；`gap_tracking_status` 缺失条目时读 manual_override；`build_topic_comments_report` 跳过 manual_override=1 且无新评论 |
- [x] UI 语言统一（2026-08-13）：index.html 100% 英文化（0 中文残留），app.js 仅剩 4 处状态检测正则（低/中/高/不涉及）+ 1 处 JS 兜底值，属功能性保留。导航按钮、按钮、Dialog、Toast 全部英文 |
- [x] 定期巡检完成（2026-08-13）：(1) 新增 `gap_inspection_log` 表（保留100条）；(2) `_log_inspection()` / `get_last_inspection()` 记录每次巡检（自动循环+手动Check Now）；(3) `GET /api/gap-tracking/inspection` 新端点；(4) `gap-tracking/status` 返回 `last_inspection`；(5) 前端统计栏显示 "🔍 Last scan: <时间> (<来源>)"；(6) `_auto_detect_na` UPDATE 加 `manual_override=0` 保护条件。实测：手动触发 checked=22, changed=0，日志正常写入 |
- [x] Dashboard 重命名（2026-08-13）：导航按钮与页面标题 "Today's Tasks" → "Dashboard"
- [x] 已发送评估标识（2026-08-13）：评估分配模块 Scan Emails 支持标记已发送。机制：(1) 新增 `assessment_sent` 表（ticket主键+parent_key+sent_at+recipients）；(2) `send_assessment_email()` 成功后自动记录并返回 `already_sent` 标志；(3) 新增 `GET /api/assessments/sent` 端点 + `get_assessments_sent()`；(4) 前端 `assessmentState.processedKeys` 扫描时并行获取已发送列表，任务列表显示绿色 "✓ Processed" 徽章 + 浅绿背景（`.task-item-processed`/`.task-processed-badge`），详情页 Basic Info 显示已发送提示；(5) 发送按钮不禁用（同一ticket按topics可多次发送，仅提示不拦截）；(6) 前端容错：接口失败不影响扫描 |

## 待办事项（2026-08-13 整理，下次会话继续）

### A. 高优先级 P1
- [x] **评估分配→追踪打通**（2026-08-13 完成）：发送评估邮件成功后自动创建 gap_market_tracking `pending` 条目（`_create_tracking_from_assessment` 辅助函数 + `ASSESSMENT_MARKET_MAPPING` 市场映射）；仅对 Layer3 票内评估的领域创建条目（FuSa/OTA/OBD/Immobilizer），Cyber/Data 依赖子票由 topic_comments 回填
- [x] **到期提醒机制**（2026-08-13 完成）：`gap_tracking_status` 新增 `reminders` 字段，`can_close=true` 且 Layer3 未关闭的市场生成提醒（Action needed / 部分领域分析中）；前端新增 `gapReminders` 提醒区域（黄色横幅，显示市场名 + 提醒文案 + Layer3工单链接），summary 栏显示 ⏰ 提醒数量统计
- [x] **手动标记可视化**（2026-08-13 完成）：`gap_tracking_status` 返回的每个 topic 新增 `manual_override` 字段；前端 chip 级 `manual_override=1` 时显示 🔒 图标（橙色左边框标记），hover title 提示"Manually set - auto logic will not override without new Jira comments"

### B. 中优先级 P2
- [x] **自动写 Summary**（2026-08-13 完成）：`_build_market_summary_comment()` 生成结构化合规评估摘要（含各领域评估状态+gap_summary）；`write_summary_comment()` 通过 Jira REST API 写入 Layer3 工单评论；`close_layer3_ticket()` 关闭前自动写 Summary Comment；新增 `POST /api/gap-tracking/write-summary` 独立端点，可手动触发写入；gap_summary 同时写入 `gap_layer3_closed` 表

### C. 低优先级 P3
- [x] **导出 Excel 增加 manual_override 状态列**（2026-08-13 完成）：`create_excel_final.py` 的 "Data Consistency Check" sheet 新增第9列 "Manual Override"；从 `gap_market_tracking` 数据库读取 `manual_override=1` 的记录；显示手动设置过的 market 列表；黄色高亮单元格标记
