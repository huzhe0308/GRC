# Session State — GRC Agent

> Last updated: 2026-08-13 08:30 UTC

## 当前进度摘要

### 已完成（2026-08-13 Session 2）
1. **Dashboard 重命名** — "Today's Tasks" → "Dashboard"（index.html 导航 + viewTitle）
2. **已发送评估标识** — Assessment Allocation 模块 Scan Emails 支持 "✓ Processed" 标签
   - 后端：`assessment_sent` 表 + `send_assessment_email()` 记录 + `GET /api/assessments/sent`
   - 前端：扫描时并行获取，列表浅绿背景 + 绿色徽章，详情页显示提示
   - 发送按钮不禁用（支持同一ticket按topics多次发送）
   - 前端容错：接口失败不影响扫描

### 已完成（2026-08-13 Session 1）
1. **UI 全英文化** — `index.html` 0 中文残留，`app.js` 仅剩 4 处状态检测正则（功能性保留）
2. **手动覆盖保护 A1/A2/A3** — 全链路验证通过。手动设置后自动巡检不覆盖；Jira 新增评论时允许自动更新
3. **定期巡检完成** — 巡检日志表 + API + 前端显示上次扫描时间
4. **评估分配→追踪打通** — 发送评估邮件成功后自动创建 gap_market_tracking `pending` 条目
5. **到期提醒机制** — `can_close=true` + Layer3 未关闭 → 前端黄色提醒横幅
6. **手动标记可视化** — 🔒 图标 + hover tooltip
7. **自动写 Summary** — Summary Comment 自动写入 Jira + 独立API
8. **导出 Excel manual_override 列** — "Data Consistency Check" sheet 新增第9列

## 活跃数据（重启后保留）
- SQLite: `runtime/state.sqlite`
- 巡检日志: `runtime/jira_gap_snapshot.json`, `runtime/jira_gap_updates.json`
- 巡检记录表: `gap_inspection_log`（最新: 2026-08-13 06:11:40, manual, 22 tickets, 0 changed）
- Gap Tracking: 10 市场，8 可关闭，0 已关闭
- 已发送评估: `assessment_sent` 表

## 待办事项

### A. 高优先级 P1
- [x] 评估分配→追踪打通 ✅
- [x] 到期提醒机制 ✅
- [x] 手动标记可视化 ✅
- [ ] **评估分配结果同步回扫描列表**：发送成功后 UI 更新已发送标签（✅ 已实现：doSendAssessment 后 add to processedKeys + re-render）
- [ ] **Cyber/Data 子票手动创建追踪条目**：当前仅依赖 topic_comments 回填，部分市场无子票时缺条目

### B. 中优先级 P2
- [x] 自动写 Summary ✅

### C. 低优先级 P3
- [x] 导出 Excel manual_override 列 ✅

## 文件修改记录（2026-08-13 Session 2）

### `demo_app/app.py`
- 新增 `assessment_sent` 表创建（`gap_inspection_log` 表后）
- `send_assessment_email()` 成功后记录 ticket 到 `assessment_sent` 表，返回 `already_sent`
- 新增 `get_assessments_sent()` 函数（`ASSESSMENT_MARKET_MAPPING` 后）
- 新增 `GET /api/assessments/sent` 端点（`/api/emails` 后）

### `demo_app/static/app.js`
- `assessmentState` 新增 `processedKeys: new Set()`
- `scanEmailsForTasks()` 扫描时独立获取 `/api/assessments/sent`（容错）
- `renderTaskList()` 渲染任务列表时：processed key 显示浅绿背景 + "✓ Processed" 徽章
- `renderTaskDetail()` 详情页 Basic Info 显示已发送提示（不影响发送按钮）
- `doSendAssessment()` 发送成功后立即 add to processedKeys + re-render

### `demo_app/static/index.html`
- 导航 "Today's Tasks" → "Dashboard"
- viewTitle "Today's Tasks" → "Dashboard"

### `demo_app/static/styles.css`
- 新增 `.task-item.task-item-processed`（浅绿背景 + 边框）
- 新增 `.task-actions`（flex布局）
- 新增 `.task-processed-badge`（绿色徽章，与 `.chip-gap` 风格一致）
- 新增 `.task-item-processed .task-key`（深绿字）

## 技术备注
- 服务端口：7860
- 启动：`启动服务.bat` 或 `python demo_app/app.py`
- 重启后端需重新启动服务（静态文件热更新）
- API 测试：`Invoke-RestMethod http://127.0.0.1:7860/api/assessments/sent`
