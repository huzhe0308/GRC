# G.R.C. Agent - 项目状态

> Last updated: 2026-08-12 (wiki统一集成到 employee agent\_archive_llm_wiki)

## 更新记录
| Date | Action |
|------|--------|
| 2026-08-12 | ✅ 综合市场分析Market Overview表头升级为11列，与Excel一致（Market\|Ticket\|Target Countries\|Platform\|Vehicle Type\|SOP Target\|Cyber Sec\|Data Sec\|OTA\|OBD\|FuSa）；前端表头识别更新为英文检测；OBD Details表同步更新 |
| 2026-08-12 | ✅ Market Overview状态全面更新（Jira评论分析2026-08-12）：[OK]/[WIP]/[N/A]/[OPEN] 标签替代emoji，HIGH/MID/LOW风险分级，Action Items/Critical Items按评论重写，SSE输出剥离ANSI码，app.js statusBadge支持新标签；关键修正：Turkey OBD EU7排放无gap但(EU)2018/858待评估、CSP31 OTA无SUMS→[N/A]、India OTA RxSWIN非强制→[OK] |
| 2026-08-12 | ✅ Critical Items前端解析升级：extractActionItems支持emoji+纯文本双格式；critItems关键词扩充OTA/OBD/scope/market名；每项附CEADU编号便于Jira跳转 |
| 2026-08-12 | ✅ comprehensive_analysis.py内容调整：删除"第三部分 OBD适配详细分析"整块表格（Kazakhstan/UAE/Turkey/CSP31的法规/工时/时间线/TMT状态表格及备注说明全部移除）；OTA部分新增R156 Layer3评估结论（若软件更新涉及RXSWIN功能则RXSWIN本身须同步更新）；章节重新编号：行动项=三、风险评估=四 |
| 2026-08-12 | ✅ topic_comments准确性全面提升：MARKETS常量统一数据源（与comprehensive_analysis.py一致，10市场含cyber/data/ota/obd/fusa子工单）；TOPIC_CONFIG动态生成（新增Data Security领域，共6领域）；评论取最近10条+显示总数；每领域LLM摘要（MiniMax，失败降级规则摘要）；前端FuSa/OTA/Immobilizer按钮修复为runTopicComments |
| 2026-08-12 | ✅ topic_comments实测验证（2026-08-12）：全6领域406条评论，LLM摘要全部生成（cyber 1277字/data 1678字/fusa 1642字/ota 1730字/immobilizer 1684字/obd 593字）；OTA/OBD与Jira工单实况对照验证（Market Overview N/A与topic_comments工单实况并行正确），服务运行正常 |
| 2026-08-12 | ✅ UI模块重命名：导航"报告管理"→"需求管理"（index.html导航按钮、app.js视图标签/页面提示/AI助手建议语、模块内容"报告审阅"→"需求审阅"，"报告列表"→"需求列表"） |
| 2026-08-12 | ✅ Hero文案更新："评估分配 → 分析验证 → 报告生成" → "评估分配 → 合规分析 → 月报发送"（与三步工作流业务逻辑匹配） |
| 2026-08-12 | ✅ 分析模块 thinking 折叠：thinking body 内容默认折叠，1秒后自动展开，可手动折叠/展开 |
| 2026-08-12 | ✅ topic_comments数据源修复：FuSa/OTA/Immobilizer/Cyber/Data全部改为Layer3工单（含Data Security独立子票数据）；Immobilizer从mk_entries("cyber")错误改为mk_entries("layer3") |
| 2026-08-12 | ✅ Wiki知识库统一整合：aaf-llm-wiki (52,436文件/1.5GB) 整合至 employee agent\_archive_llm_wiki，PSV文件同步迁移；删除 00-Vmodel |

## 项目概述
Governance, Risk & Compliance 功能分配与评估助手，整合邮件处理、Jira工单评论、PSV表格解析、法规评估分配。

## 启动方式
- **启动**: `C:\Users\T1UKLL7\Desktop\Workstation\employee agent\启动服务.bat`
- **关闭**: `C:\Users\T1UKLL7\Desktop\Workstation\employee agent\关闭服务.bat`
- **访问**: http://127.0.0.1:7860

## 核心功能

### 1. 评估分配
**业务流程**: 收到邮件 → 识别sub-task → 解析PVS → 匹配Layer3 → 选择收件人 → 发送评估
- 扫描Outlook邮件（CEADU关键字）
- 从Jira下载PSV附件（选最高版本）
- PSV表格解析：标准格式 + 捷克格式（India）自动识别
- Layer3 10个领域关键词匹配
- 评估邮件英文版 + HTML格式 + JIRA工单可点击

### 2. 分析模块
- 综合市场分析 / 全部领域评论（Hero双列按钮）
- 分领域评论：OBD/FuSa/Cybersecurity/OTA/Immobilizer（从Jira实时拉取）
- AI推理过程展示（SSE流式：thinkingArea，支持取消/重试）
- 📧 法规月报：从Excel生成HTML邮件，创建Outlook草稿预览

### 3. 合规追踪 & 报告
- 出口市场Layer3合规状态（10市场）
- Market Overview 彩色状态表（与 Excel 一致）
- 法规月报邮件（Critical/Action/Closed分类）

### 4. AI助手 (悬浮窗)
- 右下角全局浮动助手
- 邮件集成（NB Outlook技能）
- 知识库检索（Wiki + 记忆）
- 多轮对话上下文

### 5. 法规Wiki
- 本地法规知识库：`C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki`

## 关键数据

### Layer3 Topics
Cyber Security, Data Security, OTA, OBD, Functional Safety + Diagnostics/Network/Immobilizer/Cryptography/Geolocation

### OBD状态标准（2026-08核对Jira）
| 工单 | 市场 | 状态 | 说明 |
|------|------|------|------|
| CEADU-4864 | Kazakhstan | Closed | TMT-E 5/20批准，12MM/8mo |
| CEADU-5081 | Middle East UAE | Closed | TMT-E 5/20批准，10.5MM/7mo |
| CEADU-6699 | Turkey | In Progress | EU7相关，Open |

### 法规月报收件人
- TO (10人): Kai Kunze, Yi Yu, Dawei Chen, Alvaro Hekler, Shuo He, Yumin Ren, Hao Sun, Wei Zhu, Zhaolong Wang, Zhenxing Wang
- CC (9人): Xiaochen Sun, Wenbo Ma, Xin Cheng, Li Wang, Yiwen Cai, Chengge Wang, Zhishuo Zhang, Richard Ling, Jinfeng Cheng

## 技术栈
- Python 3.14 + Flask (HTTP API)
- Jira REST API (Bearer认证)
- Outlook COM (Windows本地)
- MiniMax LLM (llm-gateway)

## 详细文档
见 `AGENTS.md`（完整功能清单、历史记录、技术细节）
