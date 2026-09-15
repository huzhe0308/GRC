const state = {
  emails: [],
  reports: [],
  wikiFiles: [],
  wikiTree: null,
  wikiTreeOpen: new Set(["concepts", "entities", "comparisons", "queries"]),
  wikiSearchHits: [],
  selectedEmail: null,
  selectedReport: null,
  selectedWikiPath: "",
  selectedWikiItem: null,
  jiraTickets: [],
  selectedJiraTicket: null,
  automation: null,
  analysisHistory: [],
  currentAnalysis: "",
};

const $ = (id) => document.getElementById(id);

function getToken() {
  try { return localStorage.getItem("grc_token") || null; } catch (e) { return null; }
}

function authHeaders(extra) {
  const headers = Object.assign({ "Content-Type": "application/json" }, extra || {});
  const token = getToken();
  if (token) headers["Authorization"] = "Bearer " + token;
  return headers;
}

(function checkAuth() {
  const token = getToken();
  if (!token) { window.location.href = "/login"; }
})();

async function api(path, options = {}) {
  try {
    const response = await fetch(path, {
      headers: authHeaders(options.headers),
      ...options,
    });
    if (response.status === 401) {
      localStorage.removeItem("grc_token");
      window.location.href = "/login";
      return {};
    }
    const data = await response.json();
    if (!response.ok || data.error) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }
    return data;
  } catch (err) {
    if (err.message && err.message.includes("Failed to fetch")) {
      console.error("Network error:", err);
    }
    throw err;
  }
}

function escapeHtml(text = "") {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatBytes(size) {
  const value = Number(size || 0);
  if (!value) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  let index = 0;
  let current = value;
  while (current >= 1024 && index < units.length - 1) {
    current /= 1024;
    index += 1;
  }
  return `${current.toFixed(current >= 10 || index === 0 ? 0 : 1)} ${units[index]}`;
}

function formatPathParts(path = "") {
  return String(path)
    .split("/")
    .filter(Boolean)
    .join(" / ");
}

function toast(message, isError = false) {
  const node = $("toast");
  node.textContent = message;
  node.classList.toggle("error", isError);
  node.classList.add("show");
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => node.classList.remove("show"), 3200);
}

function switchView(name) {
  document.querySelectorAll(".view").forEach((view) => {
    view.classList.toggle("active", view.id === name);
  });
  document.querySelectorAll(".nav").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === name);
  });

const labels = {
    dashboard: "Dashboard",
    assessment: "Assessment",
    analysis: "Analysis",
    wiki: "Wiki",
    gapTracking: "Gap Tracking",
  };
  $("viewTitle").textContent = labels[name] || name;

  // Load data for specific views
  if (name === "assessment") {
    loadContactsList();
  }
  if (name === "gapTracking") {
    loadGapTracking();
  }
  // Provide context hint to assistant
  if (assistantState) {
    // Assistant is floating, no need to preload here
  }
}

function renderMarkdown(markdown = "") {
  const source = String(markdown || "");
  if (!source.trim()) {
    return '<p class="empty-copy">No content yet.</p>';
  }

  const blocks = source.replace(/\r/g, "").split(/\n{2,}/);
  const rendered = blocks
    .map((block) => {
      const trimmed = block.trim();
      if (!trimmed) return "";
      if (trimmed.startsWith("```")) {
        const inner = trimmed.replace(/^```[a-zA-Z0-9_-]*\n?/, "").replace(/```$/, "");
        return `<pre><code>${escapeHtml(inner)}</code></pre>`;
      }
      if (/^#{1,3}\s+/.test(trimmed)) {
        const level = trimmed.match(/^#{1,3}/)[0].length;
        const text = trimmed.replace(/^#{1,3}\s+/, "");
        return `<h${level}>${inlineMarkdown(text)}</h${level}>`;
      }
      if (/^[-*]\s+/.test(trimmed)) {
        const items = trimmed
          .split(/\n/)
          .map((line) => line.replace(/^[-*]\s+/, "").trim())
          .filter(Boolean)
          .map((item) => `<li>${inlineMarkdown(item)}</li>`)
          .join("");
        return `<ul>${items}</ul>`;
      }
      return `<p>${inlineMarkdown(trimmed).replace(/\n/g, "<br>")}</p>`;
    })
    .filter(Boolean)
    .join("");
  return rendered;
}

function inlineMarkdown(text) {
  let value = escapeHtml(String(text || ""));
  value = value.replace(/`([^`]+)`/g, "<code>$1</code>");
  value = value.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  value = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
  return value;
}

function setLoading(button, loading, label) {
  if (!button) return;
  if (loading) {
    if (!button.dataset.restoreLabel) {
      button.dataset.restoreLabel = button.textContent;
    }
    button.textContent = label || "Processing";
    button.disabled = true;
  } else {
    button.textContent = button.dataset.restoreLabel || button.textContent;
    button.disabled = false;
  }
}

function summarizeCounts(counts = {}) {
  return Object.entries(counts)
    .map(([name, count]) => `${name}: ${count}`)
    .join(" · ");
}

function countTreeFiles(node) {
  if (!node) return 0;
  if (node.kind === "file") return 1;
  return (node.children || []).reduce((sum, child) => sum + countTreeFiles(child), 0);
}

function buildTree(files) {
  const root = { kind: "folder", name: "llm_wiki", path: "", children: [] };
  const folderMap = new Map([["", root]]);

  const sortedFiles = [...files].sort((a, b) => String(a.path || "").localeCompare(String(b.path || ""), "zh-Hans-CN"));
  for (const file of sortedFiles) {
    const parts = String(file.path || "").split("/").filter(Boolean);
    let currentPath = "";
    let parent = root;
    for (let index = 0; index < parts.length; index += 1) {
      const part = parts[index];
      currentPath = currentPath ? `${currentPath}/${part}` : part;
      const isLeaf = index === parts.length - 1;
      if (isLeaf) {
        parent.children.push({
          kind: "file",
          name: part,
          path: file.path,
          layer: file.layer || "",
          size: Number(file.size || 0),
        });
      } else {
        if (!folderMap.has(currentPath)) {
          const folder = { kind: "folder", name: part, path: currentPath, children: [] };
          folderMap.set(currentPath, folder);
          parent.children.push(folder);
        }
        parent = folderMap.get(currentPath);
      }
    }
  }

  const sortNodes = (node) => {
    if (node.kind === "folder") {
      node.children.sort((a, b) => {
        if (a.kind !== b.kind) return a.kind === "folder" ? -1 : 1;
        return String(a.name).localeCompare(String(b.name), "zh-Hans-CN");
      });
      node.children.forEach(sortNodes);
    }
  };
  sortNodes(root);
  return root;
}

function folderPaths(node, acc = []) {
  if (!node || node.kind !== "folder") return acc;
  if (node.path) acc.push(node.path);
  node.children.forEach((child) => folderPaths(child, acc));
  return acc;
}

function openAncestors(path) {
  const parts = String(path || "").split("/").filter(Boolean);
  let current = "";
  for (let index = 0; index < Math.max(parts.length - 1, 0); index += 1) {
    current = current ? `${current}/${parts[index]}` : parts[index];
    state.wikiTreeOpen.add(current);
  }
}

function expandAllFolders() {
  folderPaths(state.wikiTree).forEach((path) => state.wikiTreeOpen.add(path));
  renderWikiTree();
}

function collapseAllFolders() {
  state.wikiTreeOpen = new Set(["concepts", "entities", "comparisons", "queries"]);
  renderWikiTree();
}

function renderWikiTree() {
  const node = $("wikiTree");
  if (!state.wikiTree) {
    node.innerHTML = '<div class="tree-empty">Wiki not loaded yet.</div>';
    return;
  }

  node.innerHTML = renderTreeChildren(state.wikiTree.children, 0);

  node.querySelectorAll("[data-toggle-folder]").forEach((button) => {
    button.addEventListener("click", () => {
      const path = button.dataset.toggleFolder;
      if (state.wikiTreeOpen.has(path)) {
        state.wikiTreeOpen.delete(path);
      } else {
        state.wikiTreeOpen.add(path);
      }
      renderWikiTree();
    });
  });

  node.querySelectorAll("[data-open-file]").forEach((button) => {
    button.addEventListener("click", () => {
      const path = button.dataset.openFile;
      const item = state.wikiFiles.find((file) => file.path === path);
      openWikiFile(item || { path, name: path.split("/").pop() || path });
    });
  });
}

function renderTreeChildren(children, depth) {
  if (!children || !children.length) {
    return '<div class="tree-empty">No pages in this directory.</div>';
  }

  return children
    .map((child) => {
      if (child.kind === "folder") {
        const isOpen = state.wikiTreeOpen.has(child.path);
        const count = countTreeFiles(child);
        return `
          <div class="tree-folder depth-${depth}">
            <button class="tree-row folder ${isOpen ? "open" : ""}" data-toggle-folder="${escapeHtml(child.path)}" aria-expanded="${isOpen ? "true" : "false"}">
              <span class="tree-caret">${isOpen ? "▾" : "▸"}</span>
              <span class="tree-name">${escapeHtml(child.name)}</span>
              <span class="tree-count">${count}</span>
            </button>
            <div class="tree-children ${isOpen ? "open" : ""}">
              ${renderTreeChildren(child.children, depth + 1)}
            </div>
          </div>
        `;
      }

      const active = state.selectedWikiPath === child.path ? "active" : "";
      return `
        <button class="tree-row file ${active}" data-open-file="${escapeHtml(child.path)}">
          <span class="tree-dot"></span>
          <span class="tree-name">${escapeHtml(child.name)}</span>
          <span class="tree-meta">${escapeHtml(child.layer || "file")}</span>
        </button>
      `;
    })
    .join("");
}

function renderWikiSearchSummary(query, hits, isSemantic = false) {
  const summary = $("wikiSearchSummary");
  if (!query.trim()) {
    summary.innerHTML = "";
    return;
  }

  const modeLabel = isSemantic ? '<span class="pill semantic-pill">🔮 Semantic Search</span>' : '<span class="pill">Keyword Search</span>';
  summary.innerHTML = `
    <div class="search-summary">
      <span class="pill">Query: ${escapeHtml(query)}</span>
      ${modeLabel}
      <span class="pill">${hits.length} hits</span>
    </div>
  `;
}

function renderWikiSearchResults(hits) {
  const node = $("wikiSearchResults");
  if (!hits.length) {
    node.innerHTML = "";
    return;
  }

  node.innerHTML = hits
    .map((hit, index) => {
      const path = hit.path || hit.rel_path || "";
      const title = hit.title || path;
      const snippets = (hit.matches || [])
        .slice(0, 2)
        .map((match) => {
          const text = match.text || match[1] || "";
          const line = match.line || match[0] || "";
          return `<div class="hit-snippet">L${escapeHtml(line)} · ${escapeHtml(text)}</div>`;
        })
        .join("");
      return `
        <article class="hit-card" data-hit-index="${index}">
          <div class="hit-head">
            <h4>${escapeHtml(title)}</h4>
            <span class="hit-score">${escapeHtml(hit.score || "")}</span>
          </div>
          <div class="hit-path">${escapeHtml(path)}</div>
          <div class="hit-snippets">${snippets || '<div class="hit-snippet">No snippet available</div>'}</div>
        </article>
      `;
    })
    .join("");

  node.querySelectorAll("[data-hit-index]").forEach((button) => {
    button.addEventListener("click", () => {
      node.querySelectorAll(".hit-card").forEach((card) => card.classList.remove("active"));
      button.classList.add("active");
      const hit = hits[Number(button.dataset.hitIndex)];
      const path = hit.path || hit.rel_path;
      if (path) {
        const item = state.wikiFiles.find((file) => file.path === path);
        openWikiFile(
          item || {
            path,
            name: path.split("/").pop() || path,
            layer: hit.layer || "",
            size: 0,
          },
          { preserveSearch: true }
        );
      }
    });
  });
}

function renderWikiSelection(item, text) {
  $("wikiDocTitle").textContent = item?.name || item?.title || "Wiki Preview";
  $("wikiBreadcrumb").textContent = item?.path ? formatPathParts(item.path) : "Select a file to view content";
  $("wikiMeta").innerHTML = [
    item?.layer ? `<span class="pill">${escapeHtml(item.layer)}</span>` : "",
    item?.size ? `<span class="pill">${escapeHtml(formatBytes(item.size))}</span>` : "",
    item?.path ? `<span class="pill">${escapeHtml(item.path.split("/").length)} levels</span>` : "",
  ]
    .filter(Boolean)
    .join("");
  $("wikiPreview").innerHTML = renderMarkdown(text || "");
  $("wikiPreview").classList.toggle("empty", !String(text || "").trim());
}

async function openWikiFile(item, options = {}) {
  const target = typeof item === "string" ? { path: item } : item || {};
  if (!target.path) return;

  state.selectedWikiPath = target.path;
  state.selectedWikiItem = target;
  openAncestors(target.path);
  renderWikiTree();

  try {
    const data = await api(`/api/wiki/file?path=${encodeURIComponent(target.path)}`);
    const text = data.text || "";
    const titleMatch = text.match(/^#\s+(.+)$/m);
    const displayItem = {
      ...target,
      name: titleMatch ? titleMatch[1].trim() : target.name || target.path.split("/").pop() || target.path,
    };
    state.selectedWikiItem = displayItem;
    renderWikiSelection(displayItem, text);
    if (!options.preserveSearch) {
      $("wikiSearchInput").value = $("wikiSearchInput").value.trim();
    }
    $("wikiSearchResults").querySelectorAll(".hit-card").forEach((card) => card.classList.remove("active"));
  } catch (err) {
    toast(`Cannot open Wiki page：${err.message}`, true);
  }
}

async function loadStatus() {
  try {
    const data = await api("/api/status");
    if ($("modelName")) $("modelName").textContent = data.model || "-";
    if ($("mailKeyword")) {
      const kw = data.mail_keyword;
      $("mailKeyword").textContent = Array.isArray(kw) ? kw.join(", ") : (kw || "-");
    }
    if ($("reportCount")) $("reportCount").textContent = data.reports || 0;
    const counts = data.wiki_counts || {};
    if ($("wikiCount")) $("wikiCount").textContent = Object.values(counts).reduce((sum, value) => sum + Number(value || 0), 0);
    if ($("wikiLayerSummary")) $("wikiLayerSummary").textContent = summarizeCounts(counts);
    renderRuns(data.runs || []);
    renderAutomation(data.automation || {});
  } catch (err) {
    console.error("loadStatus error:", err);
  }
}

function renderRuns(runs) {
  const node = $("recentRuns");
  if (!runs.length) {
    node.innerHTML = '<div class="empty-block">No run history yet.</div>';
    return;
  }

  node.innerHTML = runs
    .map(
      (run) => `
        <article class="list-card">
          <div class="list-card-head">
            <h4>${escapeHtml(run.run_id || "unknown")}</h4>
            <span class="pill">${escapeHtml(run.status || "")}</span>
          </div>
          <p>${escapeHtml(run.started_at || "")}</p>
          <div class="meta-line">${escapeHtml(run.report_path || "")}</div>
        </article>
      `
    )
    .join("");
}

async function loadEmails() {
  const button = $("loadEmails");
  setLoading(button, true, "Reading");
  try {
    const data = await api("/api/emails");
    state.emails = data.emails || [];
    const emailCountEl = $("emailCount");
    const emailListEl = $("emailList");
    const emailBodyEl = $("emailBody");
    if (emailCountEl) emailCountEl.textContent = state.emails.length;
    if (emailListEl) {
      emailListEl.innerHTML = state.emails.length
        ? state.emails
            .map(
              (email, index) => `
              <article class="list-card email-card" data-email-index="${index}">
                <div class="list-card-head">
                  <h4>${escapeHtml(email.subject || "(no subject)")}</h4>
                  <span class="pill">Email</span>
                </div>
                <p>${escapeHtml(email.body_preview || "no body preview")}</p>
                <div class="meta-line">
                  ${escapeHtml(email.sender || "")}
                  · ${escapeHtml(email.received || "")}
                  · Attachments ${Array.isArray(email.attachments) ? email.attachments.length : 0}
                </div>
              </article>
            `
            )
            .join("")
        : '<div class="empty-block">No matching emails.</div>';

      document.querySelectorAll("[data-email-index]").forEach((node) => {
        node.addEventListener("click", () => {
          document.querySelectorAll("[data-email-index]").forEach((item) => item.classList.remove("active"));
          node.classList.add("active");
          state.selectedEmail = state.emails[Number(node.dataset.emailIndex)];
          if (emailBodyEl) {
            emailBodyEl.textContent = state.selectedEmail.body || "No body.";
            emailBodyEl.classList.remove("empty");
          }
        });
      });
    }
    if (state.emails.length && !state.selectedEmail) {
      const first = document.querySelector("[data-email-index]");
      if (first) first.click();
    }
    toast(`Loaded ${state.emails.length} related emails`);
  } catch (err) {
    toast(`Failed to read emails: ${err.message}`, true);
  } finally {
    setLoading(button, false);
  }
}

async function loadWiki() {
  const data = await api("/api/wiki/list");
  state.wikiFiles = data.files || [];
  state.wikiTree = buildTree(state.wikiFiles);
  $("wikiItemCount").textContent = state.wikiFiles.length;
  $("wikiLayerSummary").textContent = summarizeCounts(data.counts || {});
  renderWikiTree();
  renderWikiSearchSummary($("wikiSearchInput").value.trim(), state.wikiSearchHits);
  renderWikiSearchResults(state.wikiSearchHits);

  if (!state.selectedWikiPath && state.wikiFiles.length) {
    const initial = state.wikiFiles.find((file) => !String(file.path || "").startsWith("raw/")) || state.wikiFiles[0];
    await openWikiFile(initial);
  }
}

async function searchWiki() {
  const query = $("wikiSearchInput").value.trim();
  if (!query) {
    state.wikiSearchHits = [];
    renderWikiSearchSummary("", []);
    renderWikiSearchResults([]);
    renderWikiTree();
    return;
  }

  const button = $("wikiSearchBtn");
  setLoading(button, true, "Searching");
  try {
    const data = await api(`/api/wiki/search?q=${encodeURIComponent(query)}&limit=12`);
    state.wikiSearchHits = data.hits || [];
    renderWikiSearchSummary(query, state.wikiSearchHits);
    renderWikiSearchResults(state.wikiSearchHits);
    toast(`Found ${state.wikiSearchHits.length} Wiki results`);
  } catch (err) {
    toast(`Search failed: ${err.message}`, true);
  } finally {
    setLoading(button, false);
  }
}

async function searchWikiSemantic() {
  const query = $("wikiSearchInput").value.trim();
  if (!query) {
    toast("Please enter a search query first", true);
    return;
  }

  const button = $("wikiSearchSemanticBtn");
  setLoading(button, true, "Semantic analysis running");
  try {
    const data = await api(`/api/wiki/search-semantic?q=${encodeURIComponent(query)}&limit=12`);
    state.wikiSearchHits = data.hits || [];
    renderWikiSearchSummary(query, state.wikiSearchHits, true);
    renderWikiSearchResults(state.wikiSearchHits);
    if (data.error) {
      toast(`Semantic search fallback: ${data.error}`, true);
    } else {
      toast(`Semantic search complete，Found ${state.wikiSearchHits.length} most relevant results`);
    }
  } catch (err) {
    toast(`Semantic search failed：${err.message}`, true);
  } finally {
    setLoading(button, false);
  }
}

function renderAutomation(auto) {
  state.automation = auto;
  $("automationState").textContent = auto.enabled ? "On" : "Off";
  $("intervalMinutes").value = auto.interval_minutes || $("intervalMinutes").value || 15;
  $("autoSend").checked = Boolean(auto.auto_send);
  $("forceRun").checked = Boolean(auto.force);
  const lines = [
    `Status: ${auto.last_status || "idle"}`,
    `Last run: ${auto.last_run_at || "-"}`,
    `Next run: ${auto.next_run_at || "-"}`,
    "",
    auto.last_output || "No auto-monitor log yet.",
  ];
  $("automationLog").textContent = lines.join("\n");
}

async function updateAutomation(action) {
  const data = await api("/api/automation", {
    method: "POST",
    body: JSON.stringify({
      action,
      email_interval: $("emailInterval").value,
      email_auto_send: $("emailAutoSend").checked,
      email_force: $("emailForceRun").checked,
      jira_interval: $("jiraInterval").value,
      jira_alert_new: $("jiraAlertNew").checked,
      jira_force: $("jiraForceRun").checked,
    }),
  });
  renderAutomation(data);
  toast(action === "start" ? "Auto-monitor started" : "Auto-monitor stopped");
}

function bindEvents() {
  document.querySelectorAll(".nav").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view));
  });
  document.querySelectorAll("[data-open-view]").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.openView));
  });
  $("refreshAll").addEventListener("click", refreshAll);
  $("quickAction").addEventListener("click", () => handleQuickAction("readEmails"));
  $("loadEmails")?.addEventListener("click", loadEmails);

  $("loadWiki").addEventListener("click", loadWiki);
  $("wikiSearchBtn").addEventListener("click", searchWiki);
  $("wikiSearchSemanticBtn")?.addEventListener("click", searchWikiSemantic);
  $("wikiSearchInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter") searchWiki();
  });
  $("expandAll").addEventListener("click", expandAllFolders);
  $("collapseAll").addEventListener("click", collapseAllFolders);
  $("startAutomation").addEventListener("click", () => updateAutomation("start"));
  $("stopAutomation").addEventListener("click", () => updateAutomation("stop"));
  $("loadJira").addEventListener("click", loadJira);
  $("jiraSearchBtn").addEventListener("click", searchJira);
  $("jiraSearchInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter") searchJira();
  });
  $("opencodeRefresh").addEventListener("click", opencodeRefreshJira);

  $("refreshGapTracking").addEventListener("click", () => {
    toast("Refreshing tracking status......");
    loadGapTracking();
  });
  $("triggerGapCheck")?.addEventListener("click", async () => {
    toast("Checking Jira comment updates......");
    try {
      const r = await api("/api/gap-tracking/trigger-check", { method: "POST" });
      if (r.ok) {
        toast(`Check complete: ${r.changed || 0} tickets updated`);
        if (r.changed > 0) {
          showGapUpdateBanner(r.changes);
        }
        loadGapTracking();
      } else {
        toast("Check failed: " + (r.error || ""), true);
      }
    } catch (e) {
      toast("Check failed: " + e.message, true);
    }
  });
  $("gapMonitorCheck")?.addEventListener("change", async function () {
    try {
      const action = this.checked ? "start" : "stop";
      await api("/api/gap-tracking/monitor", { method: "POST", body: JSON.stringify({ action, interval: 1800 }) });
      toast(this.checked ? "Auto-monitor enabled (every 30 min)" : "Auto-monitor off");
      if (this.checked) {
        startGapMonitorPoll();
      } else {
        stopGapMonitorPoll();
      }
    } catch (e) {
      toast("Settings failed: " + e.message, true);
      this.checked = !this.checked;
    }
  });
  $("gapUpdateDismiss")?.addEventListener("click", async () => {
    $("gapUpdateBanner").classList.add("hidden");
    await api("/api/gap-tracking/mark-read", { method: "POST" });
  });
  $("gapUpdateViewBtn")?.addEventListener("click", () => {
    $("gapUpdateBanner").classList.add("hidden");
    loadGapTracking();
    showGapUpdatesPanel();
  });
  
  // Quick action buttons
  document.querySelectorAll(".action-btn[data-action]").forEach(btn => {
    btn.addEventListener("click", () => handleQuickAction(btn.dataset.action));
  });
  
  // Dashboard refresh
  $("dashboardRefreshMarkets")?.addEventListener("click", loadDashboardModules);
  
  // Assessment module
  $("scanEmails")?.addEventListener("click", scanEmailsForTasks);
  $("clearTasks")?.addEventListener("click", clearTasks);
  $("viewParentTicket")?.addEventListener("click", viewParentTicket);
  $("parsePVS")?.addEventListener("click", () => {
    // Get the first PVS attachment filename
    const parent = assessmentState.parentTicket;
    if (!parent) {
      toast("Please view the Parent ticket first", true);
      return;
    }
    const attachments = parent.attachments || [];
    const pvsFile = attachments.find(a => 
      a.filename?.toLowerCase().includes('pvs') || 
      a.filename?.toLowerCase().includes('psv')
    );
    if (pvsFile && pvsFile.filename) {
      parsePVSFile(pvsFile.filename);
    } else {
      toast("No PVS/PSV file found", true);
    }
  });
  $("sendAssessment")?.addEventListener("click", sendAssessmentEmail);
  
  // Analysis module
  $("verifyMarketOverview")?.addEventListener("click", verifyMarketOverview);
  $("verifyOBDData")?.addEventListener("click", verifyOBDData);
  $("verifyCyberSecurity")?.addEventListener("click", verifyCyberSecurity);
  $("verifyFuSa")?.addEventListener("click", verifyFuSa);
  $("verifyOTA")?.addEventListener("click", verifyOTA);
  $("verifyImmobilizer")?.addEventListener("click", verifyImmobilizer);
  $("verifyAllTopics")?.addEventListener("click", verifyAllTopics);
  $("generateLayer3Excel")?.addEventListener("click", generateLayer3Excel);
  $("sendMonthlyReport")?.addEventListener("click", sendMonthlyReport);
  $("exportAnalysis")?.addEventListener("click", exportAnalysisResult);
  $("copyAnalysis")?.addEventListener("click", copyAnalysisResult);
$("toggleAnalysisView")?.addEventListener("click", toggleAnalysisView);

  let _lastAnalysisAction = null;

  $("cancelAnalysis")?.addEventListener("click", () => {
    if (_analysisAbort) {
      _analysisAbort.abort();
      _analysisAbort = null;
    }
  });

  $("retryAnalysis")?.addEventListener("click", () => {
    const action = _lastAnalysisAction || "market_overview";
    runAnalysis(action);
  });

  $("toggleThinking")?.addEventListener("click", (e) => {
    e.stopPropagation();
    const body = $("thinkingBody");
    setThinkingExpanded(!body.classList.contains("expanded"));
  });

  $("thinkingArea")?.querySelector(".thinking-header")?.addEventListener("click", () => {
    const btn = $("toggleThinking");
    btn?.click();
  });
  
  // Contacts management - use event delegation
  document.addEventListener("click", (e) => {
    if (e.target.closest("#addContact")) {
      e.preventDefault();
      showContactDialog();
    }
    if (e.target.closest("#refreshContacts")) {
      e.preventDefault();
      loadContactsList();
    }
  });
}

// ===== Analysis Module =====

let _analysisAbort = null;

const THINKING_STEPS = {
  prepare: "Preparing environment",
  analyzing: "Running analysis",
  rendering: "Rendering results",
};

function showThinking(expand = true) {
  const area = $("thinkingArea");
  const body = $("thinkingBody");
  area.hidden = false;
  area.className = "thinking-area";
  $("thinkingStatus").textContent = "Thinking...";
  $("cancelAnalysis").hidden = false;
  $("retryAnalysis").hidden = true;
  $("thinkingSteps").innerHTML = "";
  area.querySelectorAll(".thinking-final-state").forEach((el) => el.remove());
  setThinkingExpanded(false);
  area.setAttribute("aria-expanded", "true");
  if (expand) {
    setTimeout(() => setThinkingExpanded(true), 1000);
  }
}

function setThinkingExpanded(expanded) {
  const body = $("thinkingBody");
  const toggle = $("toggleThinking");
  if (!body) return;
  body.classList.toggle("expanded", expanded);
  body.setAttribute("aria-hidden", String(!expanded));
  if (toggle) {
    toggle.setAttribute("aria-expanded", String(expanded));
    toggle.textContent = expanded ? "▲" : "▼";
  }
}

function appendThinkingStep(label, type = "active") {
  const ul = $("thinkingSteps");
  const li = document.createElement("li");
  li.className = type;
  li.textContent = label;
  ul.appendChild(li);
  const all = ul.querySelectorAll("li");
  all.forEach((el, i) => el.classList.remove("active"));
  li.classList.add("active");
}

function setThinkingState(state, message) {
  const area = $("thinkingArea");
  const statusEl = $("analysisStatus");
  const cancelBtn = $("cancelAnalysis");
  const retryBtn = $("retryAnalysis");
  area.className = "thinking-area " + state;
  $("thinkingStatus").textContent = message;
  statusEl.textContent = message;
  if (state === "success") {
    $("thinkingSteps").innerHTML += `<li class="done">✅ Analysis complete</li>`;
    setThinkingExpanded(true);
    cancelBtn.hidden = true;
    retryBtn.hidden = false;
    area.setAttribute("aria-expanded", "true");
    setFinalState("✅ Analysis complete");
  } else if (state === "error") {
    $("thinkingSteps").innerHTML += `<li class="failed">❌ ${escapeHtml(message)}</li>`;
    cancelBtn.hidden = true;
    retryBtn.hidden = false;
    setFinalState("❌ " + message);
  } else if (state === "cancelled") {
    $("thinkingSteps").innerHTML += `<li class="failed">⏹ Cancelled</li>`;
    cancelBtn.hidden = true;
    retryBtn.hidden = false;
    setFinalState("⏹ Cancelled, click to retry");
  }
}

function setFinalState(text) {
  const area = $("thinkingArea");
  area.querySelectorAll(".thinking-final-state").forEach((el) => el.remove());
  area.insertAdjacentHTML("beforeend", `<div class="thinking-final-state">${escapeHtml(text)}</div>`);
}

async function runAnalysis(action) {
  const outputEl = $("analysisResult");
  const statusEl = $("analysisStatus");
  const exportBtn = $("exportAnalysis");
  const copyBtn = $("copyAnalysis");
  const cancelBtn = $("cancelAnalysis");
  const retryBtn = $("retryAnalysis");

  outputEl.classList.remove("empty");
  outputEl.className = "analysis-result empty";
  outputEl.innerHTML = '<div class="analysis-placeholder">Analysis results will appear here...</div>';
  statusEl.textContent = "Running " + actionName(action) + "...";
  exportBtn.disabled = true;
  copyBtn.disabled = true;
  retryBtn.hidden = true;
  showThinking(true);
  appendThinkingStep("Preparing environment...", "active");
  _lastAnalysisAction = action;

  const ctrl = new AbortController();
  _analysisAbort = ctrl;

  try {
    const resp = await fetch(`/api/analysis/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ _stream: true }),
      signal: ctrl.signal,
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ error: `HTTP ${resp.status}` }));
      throw new Error(err.error || `HTTP ${resp.status}`);
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const raw of lines) {
        if (!raw.startsWith("event:")) continue;
        const evType = raw.slice(6).trim();
        const dataLine = lines[lines.indexOf(raw) + 1];
        if (!dataLine || !dataLine.startsWith("data:")) continue;
        const data = JSON.parse(dataLine.slice(5).trim());

        if (evType === "progress") {
          if (data.status === "step") {
            const label = THINKING_STEPS[data.step] || data.message;
            appendThinkingStep(label);
            $("thinkingStatus").textContent = label;
          }
        } else if (evType === "done") {
          const text = data.output || JSON.stringify(data, null, 2);
          outputEl.textContent = text;
          outputEl.classList.remove("empty");
          state.currentAnalysis = text;
          exportBtn.disabled = false;
          copyBtn.disabled = false;
          setThinkingState("success", "Analysis complete");
          toast("Analysis complete");
        }
      }
    }

    _analysisAbort = null;
  } catch (err) {
    if (err.name === "AbortError") {
      setThinkingState("cancelled", "Cancelled by user");
    } else {
      setThinkingState("error", err.message || "Analysis failed");
      outputEl.innerHTML = `<div class="analysis-placeholder" style="color:#b42318">Analysis failed: ${escapeHtml(err.message)}</div>`;
      statusEl.textContent = "Analysis failed";
      toast("Analysis failed: " + err.message, true);
    }
    _analysisAbort = null;
  }
}

function actionName(action) {
  const names = {
    deep_jira: "Deep Jira Analysis",
    market_overview: "Market Overview",
    obd_data: "OBD Verification",
    cyber_security: "Cyber Security Verification",
    layer3_excel: "Generate Layer3 Excel Report",
    fusa_data: "FuSa Verification",
    ota_data: "OTA and SW Update Verification",
    immobilizer_data: "Immobilizer Verification",
  };
  return names[action] || action;
}

function verifyMarketOverview() {
  runAnalysis("market_overview");
}

function verifyOBDData() {
  runTopicComments("obd_data");
}

function verifyCyberSecurity() {
  runTopicComments("cyber_security");
}

function verifyFuSa() {
  runTopicComments("fusa_data");
}

function verifyOTA() {
  runTopicComments("ota_data");
}

function verifyImmobilizer() {
  runTopicComments("immobilizer_data");
}

function verifyAllTopics() {
  runTopicComments("all");
}

function generateLayer3Excel() {
  runAnalysis("layer3_excel");
}

// ===== Topic Comments Module =====
async function runTopicComments(topic) {
  const outputEl = $("analysisResult");
  const statusEl = $("analysisStatus");
  const exportBtn = $("exportAnalysis");
  const copyBtn = $("copyAnalysis");
  showThinking(true);
  outputEl.classList.remove("empty");
  outputEl.innerHTML = '<div class="analysis-placeholder">Loading ' + (topic === "all" ? "all domains" : topic) + " data...</div>";
  statusEl.textContent = "Fetching Jira comments...";
  exportBtn.disabled = true;
  copyBtn.disabled = true;
  const topicLabel = topic === "all" ? "All topics" : topic;
  appendThinkingStep(`Fetching ${topicLabel} comment data...`);
  try {
    const data = await api(`/api/analysis/topic_comments`, {
      method: "POST",
      body: JSON.stringify({ topic: topic === "all" ? "" : topic }),
    });
    appendThinkingStep(`Fetched ${Object.keys(data.topics || {}).length} topics`);
    const html = renderTopicCommentsHTML(data);
    displayTopicCommentsResult(html, data);
  } catch (err) {
    setThinkingState("error", err.message);
    outputEl.innerHTML = '<div class="analysis-placeholder" style="color:#b42318">Error: ' + escapeHtml(err.message) + '</div>';
    statusEl.textContent = "Load failed";
    toast("Load failed: " + err.message, true);
  }
}

function displayTopicCommentsResult(html, data) {
  const container = $("analysisResult");
  const exportBtn = $("exportAnalysis");
  const copyBtn = $("copyAnalysis");
  const toggleBtn = $("toggleAnalysisView");
  container.classList.remove("empty");
  container.innerHTML = html;
  const rawText = JSON.stringify(data, null, 2);
  state.currentAnalysis = rawText;
  exportBtn.disabled = false;
  copyBtn.disabled = false;
  if (toggleBtn) toggleBtn.disabled = false;
  $("analysisStatus").textContent = "Analysis complete";
  setThinkingState("success", "Comments loaded");
  toast("Loaded");
  loadGapTracking();
}

function escapeHtml(text) {
  if (!text) return "";
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function topicStatusBadge(text) {
  const t = (text || "").trim();
  if (/done|closed|completed|closed/i.test(t)) {
    return '<span class="mr-badge mr-completed">' + escapeHtml(t) + '</span>';
  }
  if (/in progress|open/i.test(t)) {
    return '<span class="mr-badge mr-inprogress">' + escapeHtml(t) + '</span>';
  }
  if (/error/i.test(t)) {
    return '<span class="mr-badge mr-required">ERROR</span>';
  }
  return '<span class="mr-badge mr-na">' + escapeHtml(t) + '</span>';
}

function renderTopicCommentsHTML(data) {
  if (!data || !data.ok || !data.topics) {
    return '<div class="topic-error">Data loading failed: ' + escapeHtml(JSON.stringify(data)) + '</div>';
  }
  const topics = data.topics;
  let html = '';
  html += '<div class="topic-container">';

  const allMarkets = [];
  for (const t in topics) {
    allMarkets.push(...topics[t].markets);
  }
  const totalComments = allMarkets.reduce((s, m) => s + (m.comment_count || 0), 0);
  const totalTickets = allMarkets.length;

  html += '<div class="topic-summary-bar">';
  html += '<span class="topic-stat"><b>' + totalTickets + '</b> tickets</span>';
  html += '<span class="topic-stat"><b>' + totalComments + '</b> comments</span>';
  html += '<span class="topic-stat"><b>' + Object.keys(topics).length + '</b> domains</span>';
  html += '</div>';

  const topicOrder = ["cyber_security", "data_security", "fusa_data", "ota_data", "immobilizer_data", "obd_data"];
  const orderedTopics = topicOrder.filter(t => topics[t]).concat(Object.keys(topics).filter(t => !topicOrder.includes(t)));

  for (const topicKey of orderedTopics) {
    const topicData = topics[topicKey];
    const icon = topicData.icon || "";
    const label = topicData.label || topicKey;
    html += '<div class="topic-section">';
    html += '<div class="topic-section-header">' + escapeHtml(icon) + ' ' + escapeHtml(label) + '</div>';
    if (topicData.summary) {
      html += '<div class="topic-ai-summary">';
      html += topicData.summary.split("\n").map(l => '<div>' + escapeHtml(l) + '</div>').join('');
      html += '</div>';
    }
    html += '<div class="topic-markets-grid">';

    const markets = topicData.markets || [];
    if (markets.length === 0) {
      html += '<div class="topic-no-data">No related tickets for this domain</div>';
    }
    for (const m of markets) {
      html += '<div class="topic-card">';
      html += '<div class="topic-card-header">';
      html += '<span class="topic-market-name">' + escapeHtml(m.market) + '</span>';
      html += '<span class="topic-ticket-key">' + escapeHtml(m.domain || m.parent) + (m.layer3 ? ' / ' + escapeHtml(m.layer3) : '') + '<span class="topic-ticket-parent"> (' + escapeHtml(m.parent) + ')</span></span>';
      html += '</div>';
      html += '<div class="topic-card-meta">';
      html += topicStatusBadge(m.status);
      if (m.assignee) html += '<span class="topic-assignee">' + escapeHtml(m.assignee) + '</span>';
      if (m.updated) html += '<span class="topic-date">' + escapeHtml(m.updated) + '</span>';
      html += '</div>';

      const comments = m.comments || [];
      const totalComments = m.comment_count || 0;
      if (comments.length > 0) {
        html += '<div class="topic-comments-header">';
        html += '<span class="topic-comment-toggle" onclick="toggleTopicComments(this)">&#9660; ' + comments.length + ' comments';
        if (totalComments > comments.length) {
          html += ' <span class="topic-comment-total">(of ' + totalComments + ' total)</span>';
        }
        html += '</span>';
        html += '</div>';
        html += '<div class="topic-comment-list" style="display:none">';
        for (const c of comments) {
          html += '<div class="topic-comment">';
          html += '<div class="topic-comment-meta">';
          html += '<b>' + escapeHtml(c.author) + '</b>';
          html += '<span class="topic-comment-date">' + escapeHtml(c.created) + '</span>';
          html += '</div>';
          html += '<div class="topic-comment-body">' + escapeHtml(c.body) + '</div>';
          html += '</div>';
        }
        html += '</div>';
      } else {
        html += '<div class="topic-no-comments">No comments' + (totalComments > 0 ? ' (' + totalComments + ' total)' : '') + '</div>';
      }
      html += '</div>';
    }
    html += '</div></div>';
  }
  html += '</div>';
  return html;
}

window.toggleTopicComments = function(btn) {
  const list = btn.closest(".topic-card").querySelector(".topic-comment-list");
  if (!list) return;
  const isOpen = list.style.display !== "none";
  list.style.display = isOpen ? "none" : "block";
  btn.innerHTML = (isOpen ? "&#9658;" : "&#9660;") + " " + btn.textContent.replace(/^[▲▼]\s*/, "");
};

function verifyFuSa() {
  runTopicComments("fusa_data");
}

function verifyOTA() {
  runTopicComments("ota_data");
}

function verifyImmobilizer() {
  runTopicComments("immobilizer_data");
}

function verifyDataSecurity() {
  runTopicComments("data_security");
}

// ===== Gap Analysis Tracking =====

async function loadGapTracking() {
  try {
    const data = await api("/api/gap-tracking/status");
    renderGapTracking(data);
    checkGapMonitorStatus();
  } catch (err) {
    const grid = $("gapTrackingGrid");
    if (grid) grid.innerHTML = '<div class="topic-error">Failed to load tracking status: ' + escapeHtml(err.message) + '</div>';
  }
}

let gapMonitorPollInterval = null;
let gapLastUpdateTime = "";

async function checkGapMonitorStatus() {
  try {
    const r = await api("/api/gap-tracking/monitor-status");
    const checkEl = $("gapMonitorCheck");
    if (checkEl) checkEl.checked = r.running;
    if (r.running) {
      startGapMonitorPoll();
      const updates = await api("/api/gap-tracking/updates");
      if (updates.unread_count > 0) {
        showGapUpdateBanner(updates.recent.filter(u => !u.read).slice(0, 5));
      }
    }
  } catch (e) {}
}

async function startGapMonitorPoll() {
  if (gapMonitorPollInterval) return;
  gapMonitorPollInterval = setInterval(async () => {
    if (!document.getElementById("gapTracking")?.classList.contains("active")) return;
    try {
      const updates = await api("/api/gap-tracking/updates?since=" + encodeURIComponent(gapLastUpdateTime));
      gapLastUpdateTime = updates.last_update || gapLastUpdateTime;
      if (updates.unread_count > 0) {
        showGapUpdateBanner(updates.recent.filter(u => !u.read).slice(0, 5));
      }
    } catch (e) {}
  }, 60000);
}

function stopGapMonitorPoll() {
  if (gapMonitorPollInterval) {
    clearInterval(gapMonitorPollInterval);
    gapMonitorPollInterval = null;
  }
}

function showGapUpdateBanner(changes) {
  const banner = $("gapUpdateBanner");
  const text = $("gapUpdateBannerText");
  if (!banner || !text) return;
  const count = changes.length;
  const markets = [...new Set(changes.map(c => c.market))];
  text.textContent = `Detected ${count} tickets have comment updates: ${markets.join("、")}`;
  banner.classList.remove("hidden");
}

function showGapUpdatesPanel() {
  api("/api/gap-tracking/updates").then(d => {
    if (!d.recent || d.recent.length === 0) {
      toast("No updates yet");
      return;
    }
    const html = '<div class="gap-updates-list">' + d.recent.slice(0, 20).map(u => {
      const icon = u.type === "comment_added" ? "💬" : "✂️";
      return `<div class="gap-update-item ${u.read ? 'read' : 'unread'}">
        <span class="gap-update-icon">${icon}</span>
        <span class="gap-update-market">${escapeHtml(u.market)}</span>
        <span class="gap-update-topic">${escapeHtml(u.topic)}</span>
        <span class="gap-update-details">${escapeHtml(u.details || u.type)}</span>
        <span class="gap-update-time">${escapeHtml(u.time)}</span>
      </div>`;
    }).join("") + "</div>";
    const modal = createModal("Jira Comment Updates", html + '<button onclick="this.closest(\'.modal-overlay\').remove()" class="btn primary">Close</button>', "600px");
    document.body.appendChild(modal);
  });
}

function createModal(title, content, width) {
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1000;display:flex;align-items:center;justify-content:center;";
  const box = document.createElement("div");
  box.style.cssText = `background:#fff;border-radius:10px;padding:20px;max-width:90vw;width:${width||"500px"};max-height:80vh;overflow:auto;box-shadow:0 4px 20px rgba(0,0,0,0.15);`;
  box.innerHTML = `<h3 style="margin:0 0 15px;font-size:16px;border-bottom:1px solid #eee;padding-bottom:10px;">${escapeHtml(title)}</h3><div>${content}</div>`;
  overlay.appendChild(box);
  overlay.addEventListener("click", e => { if (e.target === overlay) overlay.remove(); });
  return overlay;
}

const STATUS_LABELS = {
  "pending": "Pending",
  "evaluating": "Evaluating",
  "gap_analysis": "Gap Analysis",
  "completed": "Completed",
  "not_applicable": "N/A",
  "closed": "Closed"
};

const STATUS_FLOW = ["pending", "evaluating", "gap_analysis"];

function getNextStatus(current) {
  const idx = STATUS_FLOW.indexOf(current);
  if (idx === -1 || current === "gap_analysis") return "pending";
  return STATUS_FLOW[idx + 1] || "pending";
}

function makeGapChip(topic, market) {
  const icon = topic.icon || "";
  const label = topic.label || topic.topic || "";
  const ticket = topic.ticket || "";
  const status = topic.status || "pending";
  const updated = topic.updated_at || "";
  const gapSummary = topic.gap_summary || "";
  const manualOverride = topic.manual_override ? 1 : 0;
  const statusLabel = STATUS_LABELS[status] || status;
  const titleStr = (status === "gap_analysis" ? "Right-click: reset\n" : "Right-click: advance status\n") + "Left-click: open Jira ticket " + (updated ? " | updated " + updated : "") + (manualOverride ? "\n🔒 Manually set - auto logic will NOT override without new Jira comments" : "");
  const ticketHtml = ticket
    ? '<span class="gap-chip-ticket">' + escapeHtml(ticket) + "</span>"
    : '<span class="gap-chip-ticket gap-chip-na">N/A</span>';
  const summaryHint = gapSummary ? `<span class="gap-chip-summary">${escapeHtml(gapSummary.substring(0, 30))}</span>` : "";
  const lockHtml = manualOverride ? '<span class="gap-chip-lock" title="Manually set - auto logic will not override without new Jira comments">🔒</span>' : "";
  return '<div class="gap-chip gap-chip-' + status + (manualOverride ? " gap-chip-manual" : "") + '" data-market="' + escapeHtmlAttr(market) + '" data-topic="' + escapeHtmlAttr(topic.topic || "") + '" data-label="' + escapeHtmlAttr(label) + '" data-status="' + escapeHtmlAttr(status) + '" data-ticket="' + escapeHtmlAttr(ticket) + '" title="' + escapeHtmlAttr(titleStr) + '">' +
    '<span class="gap-chip-icon">' + escapeHtml(icon) + "</span>" +
    '<span class="gap-chip-label">' + escapeHtml(label) + "</span>" +
    (status !== "not_applicable" ? '<span class="gap-chip-status">' + escapeHtml(statusLabel) + "</span>" : "") +
    lockHtml +
    ticketHtml +
    summaryHint +
    "</div>";
}

function escapeHtmlAttr(value) {
  return String(value || "").replace(/"/g, "&quot;");
}

function renderGapTracking(data) {
  const grid = $("gapTrackingGrid");
  const summaryEl = $("gapTrackingSummary");
  if (!grid) return;
  if (!data || !data.ok) {
    grid.innerHTML = '<div class="gap-error">' + escapeHtml((data && data.error) || "No data") + "</div>";
    return;
  }
  const summary = data.summary || {};
  if (summaryEl) {
    const insp = data.last_inspection;
    const inspHtml = insp ? '<span class="gap-insp-tag">🔍 Last scan: <b>' + escapeHtml(insp.run_at) + '</b> (' + escapeHtml(insp.source) + ')</span>' : '<span class="gap-insp-tag">🔍 No scan yet</span>';
    const reminders = data.reminders || [];
    const actionReminders = reminders.filter(r => r.action_needed);
    const remindHtml = actionReminders.length > 0
      ? '<span class="gap-stat gap-remind-stat">⏰ Reminder: <b>' + actionReminders.length + '</b> market(s) ready to close</span>'
      : "";
    summaryEl.innerHTML =
      '<span class="gap-stat">🌏 Total <b>' + summary.total_markets + '</b> markets</span>' +
      '<span class="gap-stat">✅ Gap analysis done <b>' + summary.all_done + '</b></span>' +
      '<span class="gap-stat gap-ready-stat">🔓 Ready to close Layer3 <b>' + summary.ready_to_close + '</b></span>' +
      '<span class="gap-stat gap-done-stat">📌 Closed <b>' + summary.closed + '</b></span>' +
      remindHtml +
      inspHtml;
  }
  const markets = data.markets || [];
  const remindEl = $("gapReminders");
  if (remindEl) {
    const reminders = data.reminders || [];
    const active = reminders.filter(r => r.action_needed);
    if (active.length > 0) {
      remindEl.innerHTML =
        '<div class="gap-reminders-title">⏰ Close reminders</div>' +
        active.map(r =>
          '<div class="gap-reminder-item">' +
          '<span class="gap-reminder-market"><b>' + escapeHtml(r.market) + '</b></span>' +
          '<span class="gap-reminder-text">' + escapeHtml(r.reminder_text) + '</span>' +
          '<a class="gap-ticket-link" href="' + escapeHtmlAttr(r.layer3_url || "https://devstack.vgc.com.cn/jira/browse/" + encodeURIComponent(r.layer3_ticket || "")) + '" target="_blank" rel="noopener">' + escapeHtml(r.layer3_ticket) + '</a>' +
          '</div>'
        ).join("");
      remindEl.classList.remove("hidden");
    } else {
      remindEl.classList.add("hidden");
    }
  }
  grid.innerHTML = markets.map(m => {
    const total = Math.max((m.total_topics || 1), 1);
    const effectiveDone = (m.gap_analyzed || 0) + (m.na_count || 0);
    const progressPct = Math.round((effectiveDone / total) * 100);
    const allDone = effectiveDone >= (m.total_topics || 0) && (m.total_topics || 0) > 0;
    const chips = (m.topics || []).map(t => makeGapChip(t, m.market)).join("");
    const layer3Url = m.layer3_open_url || "https://devstack.vgc.com.cn/jira/browse/" + encodeURIComponent(m.layer3_ticket || "");
    const layer3Ticket = m.layer3_ticket || "";
    let closeArea = "";
    if (m.layer3_closed) {
      closeArea = '<span class="gap-closed-tag">📌 Closed' + (m.layer3_closed_at ? " " + escapeHtml(m.layer3_closed_at) : "") + "</span>";
    } else if (allDone) {
      closeArea = '<button class="gap-btn gap-btn-close" data-market="' + escapeHtmlAttr(m.market) + '">Close Layer3 Ticket</button>';
    } else {
      closeArea = '<span class="gap-btn-disabled">Waiting for all Gap Analysis</span>';
    }
    return '<div class="gap-card gap-market-card' + (m.layer3_closed ? " gap-layer3-closed" : "") + '">' +
      '<div class="gap-card-head">' +
      '<span class="gap-card-icon">🌏</span>' +
      "<b>" + escapeHtml(m.market) + "</b>" +
      '<span class="gap-layer3-info">Layer3: <a class="gap-ticket-link" href="' + escapeHtmlAttr(layer3Url) + '" target="_blank" rel="noopener">' + escapeHtml(layer3Ticket) + "</a></span>" +
      "</div>" +
      '<div class="gap-progress"><div class="gap-progress-bar" style="width:' + progressPct + '%"></div></div>' +
      '<div class="gap-progress-label">' + effectiveDone + " / " + (m.total_topics || 0) + " domains of Gap Analysis complete</div>" +
      '<div class="gap-topic-chips">' + chips + "</div>" +
      '<div class="gap-actions" data-market="' + escapeHtmlAttr(m.market) + '">' + closeArea + "</div>" +
      "</div>";
  }).join("");
  document.querySelectorAll(".gap-chip").forEach(chip => {
    const market = chip.dataset.market;
    const topic = chip.dataset.topic;
    const label = chip.dataset.label;
    const status = chip.dataset.status || "pending";
    const ticket = chip.dataset.ticket || "";
    if (!market || !topic) return;
    // Left-click: open Jira ticket
    chip.addEventListener("click", function (ev) {
      ev.stopPropagation();
      if (ticket) {
        window.open("https://devstack.vgc.com.cn/jira/browse/" + encodeURIComponent(ticket), "_blank");
      }
    });
    // Right-click: cycle status (pending->evaluating->gap_analysis, gap_analysis->reset to pending)
    chip.addEventListener("contextmenu", function (ev) {
      ev.stopPropagation();
      ev.preventDefault();
      if (status === "gap_analysis") {
        if (confirm("" + market + " / " + label + "」reset to pending?")) {
          gapReset(market, topic);
        }
      } else if (status === "completed") {
        if (confirm("" + market + " / " + label + "」reset to pending?")) {
          gapReset(market, topic);
        }
      } else {
        const next = getNextStatus(status);
        let msg = "" + market + " / " + label + " mark as " + (next === "gap_analysis" ? "Gap analysis done (close comments)" : "Evaluating") + "?";
        if (next === "gap_analysis" && ticket) {
          msg += "\n\nNote: verify comments for " + ticket + " and finish Gap summary";
        }
        if (confirm(msg)) {
          gapSetStatus(market, topic, next);
        }
      }
    });
  });
  document.querySelectorAll(".gap-btn-close[data-market]").forEach(btn => {
    btn.addEventListener("click", function () {
      gapCloseLayer3(btn.dataset.market);
    });
  });
}

async function gapComplete(market, topic) {
  try {
    const data = await api("/api/gap-tracking/complete", { method: "POST", body: JSON.stringify({ market, topic }) });
    toast("Marked as complete: " + market + " / " + topic);
    loadGapTracking();
  } catch (err) {
    toast("Failed to mark: " + err.message, true);
  }
}

async function gapSetStatus(market, topic, status) {
  const labelMap = { "evaluating": "Evaluating", "gap_analysis": "Gap analysis done", "pending": "Pending" };
  const label = labelMap[status] || status;
  try {
    await api("/api/gap-tracking/set-status", { method: "POST", body: JSON.stringify({ market, topic, status }) });
    toast("Updated: " + market + " / " + topic + " → " + label);
    loadGapTracking();
  } catch (err) {
    toast("Update failed: " + err.message, true);
  }
}

async function gapReset(market, topic) {
  if (!confirm("Reset " + market + " / " + topic + " to pending?")) return;
  try {
    await api("/api/gap-tracking/reset", { method: "POST", body: JSON.stringify({ market, topic }) });
    toast("Reset successfully: " + market + " / " + topic);
    loadGapTracking();
  } catch (err) {
    toast("Reset failed: " + err.message, true);
  }
}

async function gapCloseLayer3(market) {
  if (!confirm("Close the Layer3 ticket for " + market + "?\n(Only the Layer3 ticket is closed, Cyber/Data subtickets are untouched)")) return;
  try {
    const result = await api("/api/gap-tracking/close-layer3", { method: "POST", body: JSON.stringify({ market }) });
    if (result.ok) {
      toast("Layer3 ticket closed: " + (result.ticket || ""));
      loadGapTracking();
    } else {
      toast("Close failed: " + (result.error || "Unknown error"), true);
    }
  } catch (err) {
    toast("Close failed: " + err.message, true);
  }
}

// ===== Monthly Report =====

async function sendMonthlyReport() {
  try {
    const data = await api("/api/monthly-report/generate");
    if (data.error) {
      toast("Report generation failed: " + data.error, true);
      return;
    }
    const confirmSend = confirm(
      `Monthly report generated\n\nStatistics: ${data.stats.critical} Critical | ${data.stats.action} Action | ${data.stats.closed} Closed | ${data.stats.markets} Markets\n\nClick"Confirm"Will open mail draft in Outlook for preview. Send manually after confirming.，确认后手动发送。`
    );
    if (!confirmSend) return;
    const sendBtn = $("sendMonthlyReport");
    sendBtn.disabled = true;
    sendBtn.querySelector(".action-text").textContent = "Generating...";
    try {
      const result = await api("/api/monthly-report/send-draft", {
        method: "POST",
        body: JSON.stringify({})
      });
      if (result.ok) {
        toast(`Monthly report draft created: ${result.subject}`);
        showDraftStatus(result);
      } else {
        toast("Draft creation failed: " + result.error, true);
      }
    } finally {
      sendBtn.disabled = false;
      sendBtn.querySelector(".action-text").textContent = "Send Monthly Report";
    }
  } catch (err) {
    toast("Report failed: " + err.message, true);
  }
}

function showDraftStatus(result) {
  const area = $("analysisResult");
  const statusEl = $("analysisStatus");
  statusEl.textContent = `Monthly report draft created | ${new Date().toLocaleTimeString()}`;
  area.classList.remove("empty");
  const toList = (result.to || []).map(escapeHtml).join("<br>");
  const ccList = (result.cc || []).map(escapeHtml).join("<br>");
  area.innerHTML = `<div class="monthly-report-draft">
    <h3>📧 Monthly Report Draft Created</h3>
    <p><strong>Subject: </strong> ${escapeHtml(result.subject)}</p>
    <p><strong>To (${(result.to || []).length}):</strong><br>${toList}</p>
    <p><strong>Cc (${(result.cc || []).length}):</strong><br>${ccList}</p>
    <p class="hint">Outlook window opened，Please preview and send manually.</p>
  </div>`;
}

function generateLayer3Excel() {
  runAnalysis("layer3_excel");
}

// ===== Monthly Report Style Renderer =====

function hasBoxChars(line) {
  return /[\u2500-\u257f]/u.test(line || "");
}

function splitTableRow(line) {
  const cells = [];
  const parts = line.split("\u2502");
  for (const part of parts) {
    const trimmed = part.trim();
    if (trimmed !== "" && !/^[\u2500\u2534\u252c\u251c\u253c\u2518]+$/.test(trimmed)) {
      cells.push(trimmed);
    }
  }
  return cells;
}

function statusBadge(text) {
  const t = (text || "").trim();
  const badgeClassMap = [
    [/^baseload/i, "mr-baseload"],
    [/^in progress/i, "mr-inprogress"],
    [/^completed/i, "mr-completed"],
    [/^covered/i, "mr-covered"],
    [/^required/i, "mr-required"],
    [/^n\/a/i, "mr-na"],
    [/^high/i, "mr-required"],
    [/^mid/i, "mr-inprogress"],
    [/^low/i, "mr-baseload"],
  ];
  for (const [re, cls] of badgeClassMap) {
    if (re.test(t)) return '<span class="mr-badge ' + cls + '">' + escapeHtml(t) + "</span>";
  }
  if (/baseload|done|completed|closed|completed/.test(t) || t === "✅" || t.includes("低")) {
    return '<span class="mr-badge mr-baseload">' + escapeHtml(t || "Baseload") + "</span>";
  }
  if (/in.progress|in progress|progress|open|Pending|Pending/.test(t) || t.includes("🔶") || t.includes("中")) {
    return '<span class="mr-badge mr-inprogress">' + escapeHtml(t) + "</span>";
  }
  if (/covered/i.test(t)) {
    return '<span class="mr-badge mr-covered">' + escapeHtml(t) + "</span>";
  }
  if (/required/i.test(t) || t.includes("🔴") || t.includes("高")) {
    return '<span class="mr-badge mr-required">' + escapeHtml(t) + "</span>";
  }
  if (/partial/i.test(t)) {
    return '<span class="mr-badge mr-partial">' + escapeHtml(t) + "</span>";
  }
  if (/n\.?a|n\/a|N\/A|bev|TBD/i.test(t) || t === "-" || t === "N/A" || t.startsWith("N/A")) {
    return '<span class="mr-badge mr-na">' + escapeHtml(t || "N/A") + "</span>";
  }
  return escapeHtml(t);
}

function renderMarketOverviewTable(text) {
  const lines = text.split("\n");
  let headerIdx = -1;
  for (let i = 0; i < lines.length && i < 80; i++) {
    const t = lines[i].trim();
    if (t.includes("\u2502") && t.includes("Market") && t.includes("Ticket")) {
      headerIdx = i;
      break;
    }
  }
  if (headerIdx < 0) return "";

  const tableLines = [];
  for (let i = headerIdx; i < lines.length; i++) {
    const t = lines[i].trim();
    if (!t) break;
    const c0 = t[0];
    if (c0 === "\u2502") {
      tableLines.push(t);
    } else if (c0 === "\u251c" || c0 === "\u2500") {
      continue;
    } else {
      break;
    }
  }
  if (tableLines.length < 2) return "";

  const headerCells = splitTableRow(tableLines[0]).map(c => escapeHtml(c));
  const statusCols = [];
  for (let j = 0; j < headerCells.length; j++) {
    if (/Cyber|Data|OTA|OBD|FuSa/i.test(headerCells[j])) statusCols.push(j);
  }
  let html = '<table class="mr-table"><thead><tr>';
  for (const cell of headerCells) html += "<th>" + cell + "</th>";
  html += "</tr></thead><tbody>";
  let isAlt = false;
  for (let i = 1; i < tableLines.length; i++) {
    const cells = splitTableRow(tableLines[i]);
    if (cells.length < 2) continue;
    html += "<tr" + (isAlt ? ' style="background:#f8f9fa"' : "") + ">";
    for (let j = 0; j < cells.length; j++) {
      const isStatus = statusCols.includes(j);
      html += "<td>" + (j === 0 ? "<strong>" + escapeHtml(cells[j]) + "</strong>" : isStatus ? statusBadge(cells[j]) : escapeHtml(cells[j])) + "</td>";
    }
    html += "</tr>";
    isAlt = !isAlt;
  }
  html += "</tbody></table>";
  return html;
}

function parseOBDRows(text) {
  const lines = text.split("\n");
  let inTable = false;
  const rows = [];
  for (const line of lines) {
    const t = line.trim();
    const c0 = t[0];
    if (inTable) {
      if (c0 === "\u2502") {
        const cells = splitTableRow(t);
        if (cells.length >= 4) rows.push(cells);
      } else if (c0 === "\u2514" || c0 === "\u251c") {
        break;
      } else if (rows.length > 0) {
        break;
      }
    } else if (c0 === "\u2502" && t.includes("\u6cd5")) {
      inTable = true;
      const cells = splitTableRow(t);
      if (cells.length >= 4) rows.push(cells);
    }
  }
  return rows;
}

function renderOBDRows(rows) {
  if (rows.length === 0) return "";
  let html = '<table class="mr-table" style="margin-top:12px"><thead><tr>';
  for (const cell of rows[0]) html += "<th>" + escapeHtml(cell) + "</th>";
  html += "</tr></thead><tbody>";
  for (let i = 1; i < rows.length; i++) {
    html += "<tr>";
    for (const cell of rows[i]) {
      const badge = /approved/i.test(cell) ? '<span class="mr-badge mr-approved">' + escapeHtml(cell) + "</span>" :
                    /pending/i.test(cell) ? '<span class="mr-badge mr-pending">' + escapeHtml(cell) + "</span>" :
                    /^\d/i.test(cell) ? '<span class="mr-mm">' + escapeHtml(cell) + "</span>" :
                    escapeHtml(cell);
      html += "<td>" + badge + "</td>";
    }
    html += "</tr>";
  }
  html += "</tbody></table>";
  return html;
}

function extractActionItems(text, pLabel) {
  const emoji = "[🔴🟠🟡🟢🔵🟣⚪🔶🔷]";
  const divider = emoji + "\\s*[Pp]" + (pLabel.match(/\d/)[0]) + "\\s*[:：]";
  const nextDivider = emoji + "\\s*[Pp][234]\\s*[:：]";
  const endMarkers = "={5,}|ANALYSIS_COMPLETE";

  const re = new RegExp(divider + "[\\s\\S]*?(?=" + nextDivider + "|" + endMarkers + "|$)", "gi");
  const block = text.match(re);
  if (!block) return [];

  const lines = block[0].split("\n");
  const items = [];
  let foundLabel = false;
  for (const raw of lines) {
    const l = raw.trim();
    if (!l) continue;
    const noBullet = l.replace(/^[🔴🟠🟡🟢🔵🟣⚪🔶🔷•\-★\u2022\u2212\u2605✅🔸🔹]\s*/, "").trim();
    if (!noBullet) continue;
    if (!foundLabel && /^[Pp]\d\s*[:：]/.test(noBullet)) {
      foundLabel = true;
      continue;
    }
    const clean = noBullet.split(/\s*\|\s*/).map(s => s.trim()).filter(s => s.length > 3);
    items.push(...clean);
  }
  return items;
}

function buildItemCard(item) {
  const ticketMatch = item.match(/(CEADU-\d+)/);
  const marketMatch = item.match(/^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*/);
  const ticket = ticketMatch ? ticketMatch[1] : "";
  const market = marketMatch ? marketMatch[0] : "";
  const desc = escapeHtml(item.replace(/(CEADU-\d+)/g, "").trim());
  return '<div class="mr-card">' +
    '<div class="mr-card-header">' +
    (market ? "<strong>" + escapeHtml(market) + "</strong>" : "") +
    (ticket ? '<span class="mr-ticket">' + escapeHtml(ticket) + "</span>" : "") +
    "</div>" +
    '<div class="mr-card-body">' + (desc || escapeHtml(item)) + "</div>" +
    "</div>";
}

function renderMonthlyReport(text) {
  if (!text || !text.trim()) return '<div class="analysis-placeholder">Analysis results will appear here...</div>';

  const lines = text.split("\n");
  let p1Items = [], p2Items = [];
  try { p1Items = extractActionItems(text, "P1"); } catch(e) {}
  try { p2Items = extractActionItems(text, "P2"); } catch(e) {}
  const allItems = [...p1Items, ...p2Items];

  let actionCount = 0, closedCount = 0;
  for (const l of lines) {
    if (/in.progress|\u8fdb\u884c|progress|open|\u5f85\u5b8c\u6210/i.test(l)) actionCount++;
    if (/closed|done|completed|\u5df2\u5b8c\u6210/i.test(l)) closedCount++;
  }
  const critItems = allItems.filter(i => /urgent|critical|\u7d27\u6025|\u9ad8\u98ce\u9669|\u4f18\u5148|cyber|data|ota|obd|scope|immediate|turkey|csp31|uzbek|kz|ae|\u5f85\u5b8c\u6210|\u5f85\u5904\u7406/i.test(i)).slice(0, 5);
  const actionItems = allItems.slice(0, 8);
  const closedItems = allItems.filter(i => /closed|done|completed|\u2705|\u5b8c\u6210|\u901a\u8fc7/i.test(i)).slice(0, 3);

  const mktTable = renderMarketOverviewTable(text);

  const obdStart = lines.findIndex(l => l.includes("\u3010\u4e09\u3001OBD"));
  let obdSection = "";
  if (obdStart >= 0) {
    const obdEnd = lines.findIndex((l, i) => i > obdStart && l.includes("\u3010\u56db\u3001"));
    obdSection = lines.slice(obdStart, obdEnd > 0 ? obdEnd : lines.length).join("\n");
  }
  const obdRows = parseOBDRows(obdSection);

  let html = '<div class="mr-container">';

  html += '<div class="mr-stats">' +
    '<span class="mr-stat mr-stat-critical">&#x1f6a8; <b>' + Math.max(1, Math.min(3, critItems.length || 1)) + "</b> Critical</span>" +
    '<span class="mr-stat mr-stat-action">&#x1f4cc; <b>' + (actionCount || allItems.length) + "</b> Action</span>" +
    '<span class="mr-stat mr-stat-closed">&#x2705; <b>' + (closedCount || closedItems.length) + "</b> Closed</span>" +
    '<span class="mr-stat mr-stat-markets">&#x1f30d; <b>10</b> Markets</span>' +
    "</div>";

  html += '<div class="mr-section"><h2 class="mr-section-title">&#x1f30d; Market Overview</h2>';
  if (mktTable) {
    html += mktTable;
    html += '<div class="mr-legend">' +
      '<span class="mr-badge mr-baseload">Baseload</span>= Compliance achieved | ' +
      '<span class="mr-badge mr-inprogress">In Progress</span>= Work ongoing | ' +
      '<span class="mr-badge mr-completed">Completed</span>= Assessment done | ' +
      '<span class="mr-badge mr-covered">Covered</span>= Covered | ' +
      '<span class="mr-badge mr-required">Required</span>= Certification needed | ' +
      '<span class="mr-badge mr-na">N/A</span>= Not applicable' +
      "</div>";
  } else {
    html += parseGenericText(text);
  }
  html += "</div>";

  if (critItems.length > 0) {
    html += '<h2 class="mr-section-title mr-title-critical">&#x26a0; Critical Items</h2>';
    for (const item of critItems) html += buildItemCard(item);
  }

  if (actionItems.length > 0) {
    html += '<h2 class="mr-section-title mr-title-action">&#x1f4cc; Action Items</h2>';
    for (const item of actionItems) html += buildItemCard(item);
  }

  if (obdRows.length > 0) {
    html += '<h2 class="mr-section-title">&#x1f4e1; OBD Details</h2>';
    html += renderOBDRows(obdRows);
  }

  if (closedItems.length > 0) {
    html += '<h2 class="mr-section-title mr-title-closed">&#x2705; Recently Closed</h2>';
    for (const item of closedItems) html += buildItemCard(item);
  }

  const riskIdx = lines.findIndex(l => l.includes("\u3010\u4e94"));
  if (riskIdx >= 0) {
    const riskSection = lines.slice(riskIdx, lines.length).join("\n");
    const bullets = riskSection.split("\n")
      .filter(l => l.trim() && /^[\u2022\u2212\u2605\U0001f4a1\u26a0]/.test(l.trim()))
      .map(l => l.replace(/^[\u2022\u2212\u2605\U0001f4a1\u26a0]\s*/, "").trim())
      .filter(Boolean);
    if (bullets.length > 0) {
      html += '<h2 class="mr-section-title">&#x1f4a1; Key Insights</h2>' +
        '<div class="mr-insights">' + bullets.map(b => '<div class="mr-insight-item">' + escapeHtml(b) + "</div>").join("") + "</div>";
    }
  }

  html += "</div>";
  return html;
}

function parseGenericText(text) {
  const bullets = text.split("\n").filter(l => /^[\u2022\u2212\u2605]/.test(l.trim()));
  if (bullets.length > 0) return bullets.map(b => '<div class="mr-bullet">' + escapeHtml(b.replace(/^[\u2022\u2212\u2605]\s*/, "")) + "</div>").join("");
  return '<div class="mr-text">' + escapeHtml(text.substring(0, 800)) + "</div>";
}

function renderAnalysisOutput(text) {
  return renderMonthlyReport(text);
}

function renderRawWithFormat(text) {
  return renderMonthlyReport(text);
}
const analysisViewState = {
  renderedHtml: "",
  rawText: "",
  isRaw: false,
};

function displayAnalysisResult(text) {
  const container = $("analysisResult");
  const exportBtn = $("exportAnalysis");
  const copyBtn = $("copyAnalysis");
  const toggleBtn = $("toggleAnalysisView");

  if (!text || !text.trim()) {
    container.innerHTML = '<div class="analysis-placeholder">Analysis results will appear here...</div>';
    container.classList.add("empty");
    state.currentAnalysis = "";
    exportBtn.disabled = true;
    copyBtn.disabled = true;
    if (toggleBtn) toggleBtn.disabled = true;
    return;
  }

  container.classList.remove("empty");
  state.currentAnalysis = text;
  exportBtn.disabled = false;
  copyBtn.disabled = false;
  if (toggleBtn) toggleBtn.disabled = false;

  analysisViewState.rawText = text;
  analysisViewState.renderedHtml = renderAnalysisOutput(text);

  if (analysisViewState.isRaw) {
    container.innerHTML = `<div class="analysis-raw">${escapeHtml(text)}</div>`;
    if (toggleBtn) toggleBtn.textContent = "Render View";
  } else {
    container.innerHTML = analysisViewState.renderedHtml;
    if (toggleBtn) toggleBtn.textContent = "Raw View";
  }
}

function toggleAnalysisView() {
  const container = $("analysisResult");
  analysisViewState.isRaw = !analysisViewState.isRaw;
  const toggleBtn = $("toggleAnalysisView");

  if (analysisViewState.isRaw) {
    container.innerHTML = `<div class="analysis-raw">${escapeHtml(analysisViewState.rawText)}</div>`;
    if (toggleBtn) toggleBtn.textContent = "Render View";
  } else {
    container.innerHTML = analysisViewState.renderedHtml;
    if (toggleBtn) toggleBtn.textContent = "Raw View";
  }
}


  runAnalysis = async function(action) {
  const outputEl = $("analysisResult");
  const statusEl = $("analysisStatus");
  const exportBtn = $("exportAnalysis");
  const copyBtn = $("copyAnalysis");
  outputEl.classList.remove("empty");
  outputEl.innerHTML = '<div class="analysis-placeholder">Analysis running...</div>';
  statusEl.textContent = "Running " + actionName(action) + "...";
  try {
    const data = await api(`/api/analysis/${action}`, { method: "POST" });
    const text = data.output || data.result || JSON.stringify(data, null, 2);
    displayAnalysisResult(text);
    statusEl.textContent = "Analysis complete";
    $("analysisStatus").textContent = "Analysis complete - " + actionName(action);
    toast("Analysis complete");
  } catch (err) {
    outputEl.innerHTML = `<div class="analysis-placeholder" style="color:#b42318">Error: ${escapeHtml(err.message)}</div>`;
    statusEl.textContent = "Analysis failed";
    toast("Analysis failed: " + err.message, true);
  }
};

async function exportAnalysisResult() {
  if (!state.currentAnalysis) {
    toast("Nothing to export", true);
    return;
  }
  // Download as text file
  const filename = `analysis_${new Date().toISOString().slice(0, 10)}.txt`;
  const blob = new Blob([state.currentAnalysis], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
  toast("Analysis results exported");
}

async function copyAnalysisResult() {
  if (!state.currentAnalysis) {
    toast("Nothing to copy", true);
    return;
  }
  try {
    await navigator.clipboard.writeText(state.currentAnalysis);
    toast("Copied to clipboard");
  } catch (err) {
    toast("Copy failed：" + err.message, true);
  }
}

async function opencodeRefreshJira() {
  const button = $("opencodeRefresh");
  button.disabled = true;
  button.textContent = "Refreshing...";
  try {
    const result = await api("/api/jira/refresh");
    if (result.status === "refreshed") {
      toast("Jira tickets refreshed successfully");
      await loadJira();
    } else {
      toast("Please run 'opencode' and use Jira skill to refresh");
    }
  } catch (err) {
    toast("Refresh failed: " + err.message, true);
  } finally {
    button.disabled = false;
    button.textContent = "Refresh via Opencode";
  }
}

async function loadJira() {
  try {
    const data = await api("/api/jira/tickets");
    state.jiraTickets = data.tickets || [];
    $("jiraCount").textContent = state.jiraTickets.length;
    renderJiraList();
  } catch (err) {
    toast("Failed to load Jira tickets：" + err.message, true);
    state.jiraTickets = [];
    renderJiraList();
  }
}

function renderJiraList() {
  const container = $("jiraList");
  if (!state.jiraTickets.length) {
    container.innerHTML = '<p class="empty-copy">No CEADU Layer3 related tickets.</p>';
    return;
  }
  
  // Group tickets by category
  const layer3Direct = state.jiraTickets.filter(t => t.category === "layer3_direct");
  const securitySubtask = state.jiraTickets.filter(t => t.category === "security_subtask");
  const others = state.jiraTickets.filter(t => t.category !== "layer3_direct" && t.category !== "security_subtask");
  
  let html = '';
  
  if (layer3Direct.length) {
    html += '<div class="jira-section"><h4>📋 Your Layer3 Tickets</h4>';
    layer3Direct.forEach(ticket => {
      html += renderJiraItem(ticket);
    });
    html += '</div>';
  }
  
  if (securitySubtask.length) {
    html += '<div class="jira-section"><h4>🔐 Data/Cyber Security Related</h4>';
    securitySubtask.forEach(ticket => {
      html += renderJiraItem(ticket);
    });
    html += '</div>';
  }
  
  if (others.length) {
    html += '<div class="jira-section"><h4>Other Tickets</h4>';
    others.forEach(ticket => {
      html += renderJiraItem(ticket);
    });
    html += '</div>';
  }
  
  container.innerHTML = html;
  container.querySelectorAll(".email-item").forEach(item => {
    item.addEventListener("click", () => {
      const key = item.dataset.key;
      state.selectedJiraTicket = state.jiraTickets.find(t => t.key === key);
      renderJiraList();
      renderJiraDetail();
    });
  });
}

function renderJiraItem(ticket) {
  const categoryClass = ticket.category === "layer3_direct" ? "layer3" : ticket.category === "security_subtask" ? "security" : "";
  return `
    <div class="email-item ${categoryClass} ${state.selectedJiraTicket?.key === ticket.key ? "selected" : ""}" data-key="${escapeHtml(ticket.key)}">
      <div class="email-meta">
        <span class="ticket-key">${escapeHtml(ticket.key)}</span>
        <span class="ticket-status ${escapeHtml(ticket.status?.toLowerCase().replace(" ", "-"))}">${escapeHtml(ticket.status)}</span>
        <span class="ticket-priority">${escapeHtml(ticket.priority || "N/A")}</span>
      </div>
      <p class="ticket-summary">${escapeHtml(ticket.summary || "N/A")}</p>
      <span class="ticket-project">${escapeHtml(ticket.project || "")}</span>
    </div>
  `;
}

function renderJiraDetail() {
  const container = $("jiraDetail");
  if (!state.selectedJiraTicket) {
    container.innerHTML = '<p class="empty-copy">Please select a ticket to view details.</p>';
    return;
  }
  const t = state.selectedJiraTicket;
  container.innerHTML = `
    <h3>${escapeHtml(t.key)}: ${escapeHtml(t.summary)}</h3>
    <div class="ticket-detail">
      <p><strong>Status: </strong> ${escapeHtml(t.status)}</p>
      <p><strong>Priority: </strong> ${escapeHtml(t.priority || "N/A")}</p>
      <p><strong>Project: </strong> ${escapeHtml(t.project)}</p>
      <p><a href="https://devstack.vgc.com.cn/jira/browse/${escapeHtml(t.key)}" target="_blank">Open in Jira</a></p>
    </div>
  `;
  container.classList.remove("empty");
}

async function searchJira() {
  const jql = $("jiraSearchInput").value.trim();
  if (!jql) {
    loadJira();
    return;
  }
  try {
    const data = await api("/api/jira/search?jql=" + encodeURIComponent(jql));
    state.jiraTickets = [];
    $("jiraCount").textContent = "Searching";
    container.innerHTML = '<p class="empty-copy">Search results: ' + escapeHtml(data.result || "N/A") + '</p>';
  } catch (err) {
    toast("Search failed: " + err.message, true);
  }
}

async function refreshAll() {
  // Load sequentially with individual error handling
  try {
    await loadStatus();
  } catch (e) {
    console.log("Status refresh failed:", e.message);
  }

  try {
    await loadWiki();
  } catch (e) {
    console.log("Wiki refresh failed:", e.message);
  }

  loadDashboardModules();

  toast("Refresh complete");
}

// ===== Three-Module Dashboard =====
async function loadDashboardModules() {
  await Promise.allSettled([
    loadModule1Allocation(),
    loadModule2Tracking(),
    loadModule3Analysis()
  ]);
}

// ---- Module 1: Assessment Allocation ----
async function loadModule1Allocation() {
  const container = $("m1Tasks");
  const countEl = $("m1TaskCount");
  try {
    const m1Ctrl = new AbortController();
    const m1Tid = setTimeout(() => m1Ctrl.abort(), 8000);
    const [emailData, jiraData] = await Promise.all([
      api("/api/emails").catch(() => ({ emails: [], error: "n/a" })),
      api("/api/export-markets/data", { signal: m1Ctrl.signal }).catch(() => ({ markets: [] }))
    ]);
    clearTimeout(m1Tid);

    const emails = emailData.emails || [];
    const tasks = [];

    const relevantEmails = emails.filter(e => e.subject && /CEADU|PSV|regulation/i.test(e.subject));
    if (relevantEmails.length > 0) {
      tasks.push({
        icon: "📧",
        title: relevantEmails.length + "  emails contain compliance tasks",
        desc: (relevantEmails[0]?.subject || "Click to view").slice(0, 60),
        onClick: () => switchView("assessment")
      });
    }

    const pending = [];
    for (const m of jiraData.markets || []) {
      for (const t of m.tickets || []) {
        if (t.status === "Open" || t.status === "IN EVALUATION" || t.status === "In Progress") {
          pending.push({ market: m.name, ticket: t });
        }
      }
    }
    if (pending.length > 0) {
      const sample = pending[0];
      tasks.push({
        icon: "🎯",
        title: pending.length + "  tickets being evaluated",
        desc: sample.market + ": " + sample.ticket.key + " (" + sample.ticket.status + ")",
        onClick: () => switchView("assessment")
      });
    }

    countEl.textContent = tasks.length ? tasks.length + "  items pending" : "No new tasks";
    container.innerHTML = tasks.length
      ? tasks.map(t => '<div class="dash-task-item" onclick="switchView(\'assessment\')"><span class="action-icon">' + t.icon + '</span><div class="action-content"><strong>' + t.title + '</strong><p>' + t.desc + '</p></div><span class="action-arrow">→</span></div>').join("")
      : '<div class="empty-block">🎉 No new tasks</div>';
  } catch (err) {
    console.error("Module1 error:", err);
    countEl.textContent = "Failed to load";
  }
}

// ---- Module 2: Gap Tracking ----
async function loadModule2Tracking() {
  const container = $("m2Tasks");
  const countEl = $("m2TaskCount");
  try {
    const data = await api("/api/gap-tracking/status").catch(() => null);

    if (!data || !data.markets) {
      countEl.textContent = "No data";
      container.innerHTML = '<div class="empty-block">Run Gap Tracking first</div>';
      return;
    }

    const markets = data.markets || [];
    let closedCount = 0;
    const items = [];

    for (const m of markets) {
      if (m.layer3_closed) { closedCount++; continue; }
      const topics = (m.topics || []).filter(t => t.status !== "not_applicable");
      const done = topics.filter(t => t.status === "gap_analysis").length;
      const total = topics.length || 1;
      const pct = Math.round(done / total * 100);
      items.push({ m, pct, done, total, canClose: m.can_close });
    }

    countEl.textContent = items.length + " markets evaluating · " + closedCount + " completed";

    if (items.length === 0 && markets.length > 0) {
      container.innerHTML = '<div class="empty-block">All markets Closed</div>';
      return;
    }
    if (items.length === 0) {
      container.innerHTML = '<div class="empty-block">No market data</div>';
      return;
    }

    // Sort: can_close first, then by progress
    items.sort((a, b) => ((b.canClose ? 1 : 0) - (a.canClose ? 1 : 0)) || (b.pct - a.pct));

    container.innerHTML = items.map(({ m, pct, done, total, canClose }) => {
      const naCount = (m.na_count || 0);
      // Determine display state
      const label = canClose ? "Ready for Summary" : "Evaluating";
      const chipCls = canClose ? "gap" : (m.evaluating > 0 ? "eval" : "pending");
      const naHint = naCount > 0 ? (" · " + naCount + " (N/A)") : "";
      const subText = canClose
        ? "✅ All domains completed (click to track)"
        : done + "/" + total + " domains Gap complete" + naHint + "";
      return '<div class="dash-market-item" onclick="switchView(\'gapTracking\')"><div class="dash-market-row"><strong>' + escapeHtml(m.market || "?") + '</strong><span class="chip chip-' + chipCls + '">' + label + (naCount > 0 ? " · " + naCount + "不涉及" : "") + '</span></div><div class="dash-progress"><div class="dash-progress-fill" style="width:' + pct + '%"></div></div><div class="dash-market-sub">' + subText + '</div></div>';
    }).join("");
  } catch (err) {
    console.error("Module2 error:", err);
    countEl.textContent = "Failed to load";
  }
}

// ---- Module 3: Monthly Report ----
async function loadModule3Analysis() {
  const container = $("m3Tasks");
  const countEl = $("m3TaskCount");
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);
    const [mkt, track] = await Promise.all([
      api("/api/export-markets/data", { signal: controller.signal }).catch(() => ({ markets: [] })),
      api("/api/gap-tracking/status").catch(() => null)
    ]);
    clearTimeout(timeoutId);
    const markets = mkt.markets || [];

    let closedMkts = 0;
    let canCloseMkts = 0;
    if (track && track.markets) {
      closedMkts = track.markets.filter(m => m.layer3_closed).length;
      canCloseMkts = track.markets.filter(m => m.can_close && !m.layer3_closed).length;
    }
    const totalTickets = markets.reduce((s, m) => s + (m.ticket_count || 0), 0);
    const closedTickets = markets.reduce((s, m) => s + (m.completed_count || 0), 0);
    const inProgress = markets.reduce((s, m) => s + (m.in_progress_count || 0), 0);

    let html = '<div class="metric-strip">'
      + '<div class="metric-card"><span>Layer3 Closed</span><strong class="status-completed">' + closedMkts + '</strong></div>'
      + '<div class="metric-card"><span>Ready to Close</span><strong style="color:#d97706">' + canCloseMkts + '</strong></div>'
      + '<div class="metric-card"><span>In Progress</span><strong class="status-inprogress">' + inProgress + '</strong></div>'
      + '</div>';

    const allDone = closedMkts === (track?.markets?.length || 10) && (track?.markets?.length || 0) > 0;
    html += '<div class="dash-report-card' + (allDone ? " ready" : (canCloseMkts > 0 ? "" : "")) + '">'
      + '<div class="dash-market-row"><strong>📧 Monthly Report</strong>'
      + '<span class="chip chip-' + (allDone ? "gap" : "eval") + '">' + (allDone ? "✅ Ready to Send" : "Pending") + '</span>'
      + '</div>'
      + '<p class="dash-sub">' + (allDone ? "All tickets closed, monthly report ready" : (canCloseMkts > 0 ? canCloseMkts + " markets can write Summary Comment" : closedMkts + " marketsClosed，" + ((track?.markets?.length || 10) - closedMkts - canCloseMkts) + "In Progress")) + '</p>'
      + '</div>';

    countEl.textContent = (track?.markets?.length || 0) + " markets · " + closedMkts + " Closed · " + canCloseMkts + " Ready to Close";
    container.innerHTML = html || '<div class="empty-block">No data</div>';
  } catch (err) {
    console.error("Module3 error:", err);
    countEl.textContent = "Failed to load";
  }
}

// Quick Actions
function handleQuickAction(action) {
  switch (action) {
    case "readEmails":
      scanEmailsForTasks();
      switchView("assessment");
      break;
    case "checkCompliance":
      loadDashboardModules();
      break;
    case "generateReport":
      switchView("analysis");
      break;
    case "searchWiki":
      switchView("wiki");
      break;
  }
}

// Quick Actions
function handleQuickAction(action) {
  switch (action) {
    case "readEmails":
      scanEmailsForTasks();
      switchView("assessment");
      break;
    case "checkCompliance":
      loadDashboardModules();
      break;
    case "generateReport":
      switchView("analysis");
      break;
    case "searchWiki":
      switchView("wiki");
      break;
  }
}

// Assessment Allocation Module
const assessmentState = {
  tasks: [],
  selectedTask: null,
  parentTicket: null,
  pvsResults: [],
  processedKeys: new Set(),
};

async function scanEmailsForTasks() {
  const button = $("scanEmails");
  button.disabled = true;
  button.textContent = "Scanning...";
  
  try {
    // Fetch emails first (required), then fetch processed keys (optional)
    const data = await api("/api/emails");
    try {
      const sentData = await api("/api/assessments/sent");
      assessmentState.processedKeys = new Set((sentData.sent || []).map(r => r.ticket));
    } catch (e) {
      console.warn("[scanEmailsForTasks] Could not load processed keys:", e);
      assessmentState.processedKeys = new Set();
    }

    const emails = data.emails || [];
    
    if (data.error) {
      toast("Failed to get emails: " + data.error, true);
      assessmentState.tasks = [];
      renderTaskList();
      return;
    }
    
    // Extract Jira subtask references from emails
    const tasks = [];
    const ticketRegex = /CEADU-\d+/gi;
    
    for (const email of emails) {
      const matches = email.subject?.match(ticketRegex) || [];
      const bodyMatches = email.body?.match(ticketRegex) || [];
      const allMatches = [...new Set([...matches, ...bodyMatches])];
      
      for (const ticketKey of allMatches) {
        const upperKey = ticketKey.toUpperCase();
        tasks.push({
          key: upperKey,
          subject: email.subject,
          sender: email.sender,
          received: email.received,
          body: email.body,
          entryid: email.entryid
        });
      }
    }
    
    // Deduplicate by key
    const uniqueTasks = [];
    const seen = new Set();
    for (const t of tasks) {
      if (!seen.has(t.key)) {
        seen.add(t.key);
        uniqueTasks.push(t);
      }
    }
    
    assessmentState.tasks = uniqueTasks;
    $("taskCount").textContent = uniqueTasks.length;
    renderTaskList();
    
    if (uniqueTasks.length > 0) {
      toast(`Found ${uniqueTasks.length} assessment tasks`);
    } else if (emails.length > 0) {
      // If no tasks found but we have emails, show all CEADU emails as potential tasks
      for (const email of emails) {
        const matches = email.subject?.match(ticketRegex) || [];
        for (const ticketKey of matches) {
          const upperKey = ticketKey.toUpperCase();
          if (!seen.has(upperKey)) {
            seen.add(upperKey);
            uniqueTasks.push({
              key: upperKey,
              subject: email.subject,
              sender: email.sender,
              received: email.received,
              body: email.body,
              entryid: email.entryid
            });
          }
        }
      }
      assessmentState.tasks = uniqueTasks;
      $("taskCount").textContent = uniqueTasks.length;
      renderTaskList();
      
      if (uniqueTasks.length > 0) {
        toast(`Found ${uniqueTasks.length}CEADU emails (all shown)`);
      } else {
        toast("No assessment tasks found");
      }
    } else {
      toast("No CEADU-related emails found");
    }
  } catch (err) {
    toast("Scan failed：" + err.message, true);
  } finally {
    button.disabled = false;
    button.textContent = "Scan Emails";
  }
}

function clearTasks() {
  assessmentState.tasks = [];
  assessmentState.selectedTask = null;
  assessmentState.parentTicket = null;
  assessmentState.pvsResults = [];
  $("taskCount").textContent = "0";
  renderTaskList();
  renderTaskDetail();
  renderParentInfo();
  renderPVSResults();
  toast("Task list cleared");
}

function renderTaskList() {
  const container = $("taskList");
  const tasks = assessmentState.tasks;
  
  if (!tasks.length) {
    container.innerHTML = '<div class="empty-block">Click "Scan Emails" to detect tasks</div>';
    return;
  }
  
  container.innerHTML = tasks.map((task, idx) => {
    const processed = assessmentState.processedKeys.has(task.key);
    return `
    <div class="task-item ${assessmentState.selectedTask?.key === task.key ? 'selected' : ''} ${processed ? 'task-item-processed' : ''}" data-idx="${idx}">
      <div class="task-header">
        <span class="task-key">${task.key}</span>
        <span class="task-actions">${processed ? '<span class="task-processed-badge">✓ Processed</span>' : ''}<span class="task-time">${task.received?.substring(0, 10) || ''}</span></span>
      </div>
      <p class="task-subject">${escapeHtml(task.subject?.substring(0, 60) || 'No subject')}</p>
      <p class="task-sender">From: ${escapeHtml(task.sender || 'Unknown')}</p>
    </div>
  `;
  }).join("");
  
  container.querySelectorAll(".task-item").forEach(item => {
    item.addEventListener("click", () => {
      const idx = parseInt(item.dataset.idx);
      assessmentState.selectedTask = tasks[idx];
      assessmentState.parentTicket = null;
      assessmentState.pvsResults = [];
      renderTaskList();
      renderTaskDetail();
    });
  });
}

function renderTaskDetail() {
  const container = $("taskDetail");
  const task = assessmentState.selectedTask;
  
  if (!task) {
    container.innerHTML = '<div class="empty-block">Please select a task from the left</div>';
    $("taskActions").style.display = "none";
    return;
  }
  
  const processed = assessmentState.processedKeys.has(task.key);
  $("taskDetailTitle").textContent = task.key;
  $("taskActions").style.display = "flex";
  $("sendAssessment").disabled = true;
  
  container.innerHTML = `
    <div class="detail-section">
      <h4>Basic Info ${processed ? '<span class="task-processed-badge">✓ Processed - Assessment request already sent</span>' : ''}</h4>
      <div class="detail-row">
        <span class="label">Jira ticket: </span>
        <a href="https://devstack.vgc.com.cn/jira/browse/${task.key}" target="_blank">${task.key}</a>
      </div>
      <div class="detail-row">
        <span class="label">Subject: </span>
        <span>${escapeHtml(task.subject || 'N/A')}</span>
      </div>
      <div class="detail-row">
        <span class="label">From: </span>
        <span>${escapeHtml(task.sender || 'Unknown')}</span>
      </div>
      <div class="detail-row">
        <span class="label">Received: </span>
        <span>${task.received || '未知'}</span>
      </div>
    </div>
    <div class="detail-section">
      <h4>Email Body</h4>
      <pre class="email-preview">${escapeHtml(task.body?.substring(0, 1000) || 'No body')}</pre>
    </div>
  `;
  
  // Enable send if we have PVS results
  if (assessmentState.pvsResults.length > 0) {
    $("sendAssessment").disabled = false;
  }
}

async function viewParentTicket() {
  const task = assessmentState.selectedTask;
  if (!task) {
    toast("Please select a task first", true);
    return;
  }
  
  toast("Getting parent ticket info......");
  
  try {
    // Step 1: Get current task to find parent
    const taskData = await api(`/api/jira/issue?key=${encodeURIComponent(task.key)}`);
    
    if (!taskData.issue) {
      toast("Cannot get ticket info - check Jira connection", true);
      return;
    }
    
    const fields = taskData.issue.fields || {};
    const parent = fields.parent;
    
    if (!parent || !parent.key) {
      toast("This ticket has no parent ticket", true);
      return;
    }
    
    toast(`Found parent: ${parent.key}`);
    
    // Step 2: Get parent ticket attachments
    const parentData = await api(`/api/jira/issue?key=${encodeURIComponent(parent.key)}`);
    
    if (parentData.issue) {
      const parentFields = parentData.issue.fields || {};
      
      assessmentState.parentTicket = {
        key: parent.key,
        summary: parentFields.summary || '',
        parentKey: parent.key,
        attachments: parentFields.attachment || []
      };
      
      renderParentInfo();
      toast(`Parent ticket: ${parent.key}, attachments: ${assessmentState.parentTicket.attachments.length}`);
    } else {
      toast("Cannot get parent ticket details", true);
    }
    
  } catch (err) {
    console.error("viewParentTicket error:", err);
    toast("Failed to get parent：" + err.message, true);
  }
}

function renderParentInfo() {
  const container = $("taskDetail");
  const parent = assessmentState.parentTicket;
  const task = assessmentState.selectedTask;
  
  if (!parent) return;
  
  const attachments = parent.attachments || [];
  const pvsAttachments = attachments.filter(a => 
    a.filename?.toLowerCase().includes('pvs') || 
    a.filename?.toLowerCase().includes('psv')
  );
  
  $("taskDetailTitle").textContent = `${task?.key || ''} → Parent: ${parent.key}`;
  
  container.innerHTML = `
    <div class="detail-section">
      <h4>Parent Ticket Info</h4>
      <div class="detail-row">
        <span class="label">Parent:</span>
        <a href="https://devstack.vgc.com.cn/jira/browse/${parent.key}" target="_blank">${parent.key}</a>
      </div>
      <div class="detail-row">
        <span class="label">Subject: </span>
        <span>${escapeHtml(parent.summary || 'Unknown')}</span>
      </div>
    </div>
    <div class="detail-section">
      <h4>Attachments (${attachments.length})</h4>
      ${attachments.length > 0 ? attachments.map(a => `
        <div class="attachment-item">
          <span class="attachment-name">${escapeHtml(a.filename || 'Unknown')}</span>
          <span class="attachment-size">${(a.size / 1024).toFixed(1)} KB</span>
          ${a.filename?.toLowerCase().includes('pvs') || a.filename?.toLowerCase().includes('psv') ? 
            `<button class="ghost small" onclick="parsePVSFile('${escapeHtml(a.filename)}')">Parse</button>` : ''}
        </div>
      `).join("") : '<div class="empty-block">No attachments</div>'}
    </div>
    ${pvsAttachments.length > 0 ? `
    <div class="detail-section">
      <h4>PVS/PSV Files (${pvsAttachments.length})</h4>
      <p>Click "Parse" to read table</p>
    </div>
    ` : ''}
  `;
}

async function parsePVSFile(filename) {
  const parent = assessmentState.parentTicket;
  if (!parent) {
    toast("Please view the Parent ticket first", true);
    return;
  }
  
  const button = $("parsePVS");
  button.disabled = true;
  button.textContent = "Parsing...";
  
  console.log("parsePVSFile:", { parent: parent.key, filename });
  toast("Parsing PSV file...");
  
  try {
    const apiPath = `/api/assessment/parse-pvs?parent=${encodeURIComponent(parent.key)}&file=${encodeURIComponent(filename)}`;
    
    const response = await fetch(apiPath, {
      method: 'GET',
      headers: { "Content-Type": "application/json" }
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      toast("Parse failed：" + response.status, true);
      return;
    }
    
    const data = await response.json();
    
    if (data.error) {
      toast("Parse failed：" + data.error, true);
      return;
    }
    
    assessmentState.pvsResults = data.results || [];
    renderPVSResults();
    $("sendAssessment").disabled = assessmentState.pvsResults.length === 0;
    
    // Show different hints by source
    let sourceMsg = "";
    if (data.source === "parsed") {
      sourceMsg = `✓ Parsing from local PSV (${data.market})`;
    } else if (data.source === "wiki") {
      sourceMsg = "✓ Reading from Wiki";
    } else {
      sourceMsg = "⚠ Fallback data";
      // If there is hint info
      if (data.message) {
        toast(data.message, true);
      }
    }
    
    if (assessmentState.pvsResults.length > 0) {
      toast(`${sourceMsg}，Found ${assessmentState.pvsResults.length} Layer3 regulations`);
    } else {
      toast("No Layer3 regulations matched - check PSV file");
    }
    
  } catch (err) {
    console.error("parsePVSFile error:", err);
    toast("Parse failed：" + err.message, true);
  } finally {
    button.disabled = false;
    button.textContent = "Parse PSV Table";
  }
}

function renderPVSResults() {
  const container = $("pvsResults");
  const results = assessmentState.pvsResults;
  
  if (!results.length) {
    container.innerHTML = '<div class="empty-block">Parse PSV table to show results</div>';
    return;
  }
  
  container.innerHTML = `
    <div class="pvs-summary">
      <span>Total <strong>${results.length}</strong> Layer3 regulations</span>
    </div>
    <div class="pvs-table-container">
      <table class="pvs-table">
        <thead>
          <tr>
            <th style="width:40px"><input type="checkbox" checked onchange="toggleAllPVS(this.checked)" /></th>
            <th>Document-ID</th>
            <th>Regulation Name</th>
            <th style="width:80px">Mandatory</th>
            <th style="width:100px">Layer3</th>
          </tr>
        </thead>
        <tbody>
          ${results.map((r, idx) => `
            <tr>
              <td><input type="checkbox" class="pvs-checkbox" data-idx="${idx}" checked /></td>
              <td class="doc-id">${escapeHtml(r.documentId || '-')}</td>
              <td class="doc-name">${escapeHtml(r.documentName || '-')}</td>
              <td>${escapeHtml(r.mandatory || '-')}</td>
              <td><span class="layer3-badge">${escapeHtml(r.layer3 || '-')}</span></td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function toggleAllPVS(checked) {
  document.querySelectorAll('.pvs-checkbox').forEach(cb => cb.checked = checked);
}

function selectAllPVS() {
  document.querySelectorAll(".pvs-checkbox").forEach(cb => cb.checked = true);
}

let contactsCache = [];

async function loadContacts() {
  if (contactsCache.length) return contactsCache;
  try {
    const data = await api("/api/contacts");
    contactsCache = data.contacts || [];
  } catch (e) {
    contactsCache = [];
  }
  return contactsCache;
}

function showRecipientDialog(selectedResults) {
  const dialog = document.createElement("div");
  dialog.className = "modal-overlay";
  dialog.innerHTML = `
    <div class="modal-content" style="max-width:500px">
      <h3>Select recipients</h3>
      <div class="recipient-list" style="max-height:300px;overflow-y:auto;margin:16px 0">
        <p style="color:#888;font-size:13px">Check relevant evaluators:</p>
      </div>
      <div style="display:flex;gap:8px;justify-content:flex-end">
        <button id="cancelSend" class="secondary">Cancel</button>
        <button id="confirmSend" class="primary" disabled>Send Assessment (0)</button>
      </div>
    </div>
  `;
  document.body.appendChild(dialog);
  
  const listDiv = dialog.querySelector(".recipient-list");
  const confirmBtn = dialog.querySelector("#confirmSend");
  const cancelBtn = dialog.querySelector("#cancelSend");
  
  loadContacts().then(contacts => {
    contacts.forEach(c => {
      const layer3Topics = c.topics || [];
      const relatedLayer3 = selectedResults.filter(r => layer3Topics.some(t => r.layer3?.includes(t)));
      const isRelated = relatedLayer3.length > 0;
      
      const item = document.createElement("label");
      item.style.cssText = "display:flex;align-items:center;gap:8px;padding:8px;border-radius:4px;cursor:pointer";
      if (isRelated) item.style.background = "#e8f5e9";
      item.innerHTML = `
        <input type="checkbox" class="recipient-cb" value="${c.id}" ${isRelated ? "checked" : ""} />
        <span><strong>${c.name}</strong> (${c.role || "Unknown Role"})</span>
        <span style="color:#666;font-size:12px">- ${c.email}</span>
        <span style="color:#888;font-size:11px">[${layer3Topics.join(", ")}]</span>
      `;
      listDiv.appendChild(item);
    });
    
    // Update count
    const updateCount = () => {
      const checked = dialog.querySelectorAll(".recipient-cb:checked").length;
      confirmBtn.textContent = `Send Assessment (${checked})`;
      confirmBtn.disabled = checked === 0;
    };
    
    dialog.querySelectorAll(".recipient-cb").forEach(cb => {
      cb.addEventListener("change", updateCount);
    });
    updateCount();
  });
  
  cancelBtn.addEventListener("click", () => {
    document.body.removeChild(dialog);
  });
  
  confirmBtn.addEventListener("click", async () => {
    const selectedRecipients = Array.from(dialog.querySelectorAll(".recipient-cb:checked"))
      .map(cb => cb.value);
    
    document.body.removeChild(dialog);
    await doSendAssessment(selectedResults, selectedRecipients);
  });
  
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) document.body.removeChild(dialog);
  });
}

async function sendAssessmentEmail() {
  const task = assessmentState.selectedTask;
  const selectedResults = Array.from(document.querySelectorAll(".pvs-checkbox:checked"))
    .map(cb => assessmentState.pvsResults[parseInt(cb.dataset.idx)]);
  
  if (!selectedResults.length) {
    toast("Please select at least one regulation", true);
    return;
  }
  
  await loadContacts();
  showRecipientDialog(selectedResults);
}

async function doSendAssessment(selectedResults, recipients) {
  const task = assessmentState.selectedTask;
  
  const data = {
    taskKey: task.key,
    parentKey: assessmentState.parentTicket?.key,
    regulations: selectedResults,
    recipients: recipients
  };
  
  toast("Sending assessment email...");
  
  try {
    const result = await api("/api/assessment/send", {
      method: "POST",
      body: JSON.stringify(data)
    });
    
    if (result.ok) {
      toast(`Assessment email sent to ${result.recipients?.join(", ") || "success"}`);
      if (task) {
        assessmentState.processedKeys.add(task.key);
        renderTaskList();
        renderTaskDetail();
      }
    } else {
      toast("Send failed: " + (result.error || "Unknown error"), true);
    }
  } catch (err) {
    toast("Send failed: " + err.message, true);
  }
}

// Contacts Management
async function loadContactsList() {
  const container = $("contactsList");
  try {
    const data = await api("/api/contacts");
    const contacts = data.contacts || [];
    
    if (!contacts.length) {
      container.innerHTML = '<div class="empty-block">No contacts - click "Add Contact" to create</div>';
      return;
    }
    
    const rows = contacts.map(c => {
      const topicsHtml = (c.topics || []).map(t => `<span class="layer3-badge">${escapeHtml(t)}</span>`).join(" ");
      return `<tr data-contact-id="${escapeHtml(c.id)}">
        <td><strong>${escapeHtml(c.name)}</strong></td>
        <td>${escapeHtml(c.email)}</td>
        <td>${escapeHtml(c.role || "-")}</td>
        <td>${topicsHtml}</td>
        <td>
          <button class="ghost small btn-edit-contact">Edit</button>
          <button class="ghost small danger btn-delete-contact">Delete</button>
        </td>
      </tr>`;
    }).join("");
    
    container.innerHTML = `<table class="pvs-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Topics</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;
    
    // Event delegation for edit/delete buttons
    container.querySelectorAll(".btn-edit-contact").forEach(btn => {
      btn.addEventListener("click", () => {
        const row = btn.closest("tr");
        const contactId = row.dataset.contactId;
        const contact = contacts.find(c => c.id === contactId);
        if (contact) showContactDialog(contact);
      });
    });
    
    container.querySelectorAll(".btn-delete-contact").forEach(btn => {
      btn.addEventListener("click", () => deleteContact(btn.closest("tr").dataset.contactId));
    });
  } catch (err) {
    container.innerHTML = '<div class="empty-block">Failed to load: ' + err.message + '</div>';
  }
}

function showContactDialog(contact = null) {
  const dialog = document.createElement("div");
  dialog.className = "modal-overlay";
  
  const isEdit = !!contact;
  dialog.innerHTML = `
    <div class="modal-content" style="max-width:450px">
      <h3>${isEdit ? "Edit Contact" : "Add Contact"}</h3>
      <div style="display:flex;flex-direction:column;gap:12px;margin:16px 0">
        <div>
          <label style="display:block;margin-bottom:4px;font-weight:500">Name *</label>
          <input type="text" id="contactName" value="${isEdit ? escapeHtml(contact.name) : ""}" style="width:100%;padding:8px;border:1px solid #ddd;border-radius:4px" />
        </div>
        <div>
          <label style="display:block;margin-bottom:4px;font-weight:500">Email *</label>
          <input type="email" id="contactEmail" value="${isEdit ? escapeHtml(contact.email) : ""}" style="width:100%;padding:8px;border:1px solid #ddd;border-radius:4px" />
        </div>
        <div>
          <label style="display:block;margin-bottom:4px;font-weight:500">Role</label>
          <input type="text" id="contactRole" value="${isEdit ? escapeHtml(contact.role || "") : ""}" placeholder="e.g. Cyber Security Engineer" style="width:100%;padding:8px;border:1px solid #ddd;border-radius:4px" />
        </div>
        <div>
          <label style="display:block;margin-bottom:4px;font-weight:500">Topics (multi-select)</label>
          <div style="display:flex;flex-wrap:wrap;gap:8px">
            ${["Cyber Security", "Data Security", "OTA", "OBD", "Functional Safety", "Diagnostics", "Network", "Immobilizer-theft", "Cryptography", "Geolocation Data"].map(topic => `
              <label style="display:flex;align-items:center;gap:4px;cursor:pointer">
                <input type="checkbox" class="contact-topic" value="${topic}" ${((contact || {}).topics || []).includes(topic) ? "checked" : ""} />
                <span>${topic}</span>
              </label>
            `).join("")}
          </div>
        </div>
      </div>
      <div style="display:flex;gap:8px;justify-content:flex-end">
        <button id="cancelContact" class="secondary">Cancel</button>
        <button id="saveContact" class="primary">${isEdit ? "Save" : "Add"}</button>
      </div>
    </div>
  `;
  document.body.appendChild(dialog);
  
  dialog.querySelector("#cancelContact").addEventListener("click", () => document.body.removeChild(dialog));
  
  const saveBtn = dialog.querySelector("#saveContact");
  if (!saveBtn) {
    console.error("Save button not found in dialog");
    return;
  }
  
  saveBtn.addEventListener("click", async () => {
    console.log("Save button clicked, isEdit:", isEdit);
    const name = dialog.querySelector("#contactName")?.value?.trim() || "";
    const email = dialog.querySelector("#contactEmail")?.value?.trim() || "";
    const role = dialog.querySelector("#contactRole")?.value?.trim() || "";
    const topics = Array.from(dialog.querySelectorAll(".contact-topic:checked")).map(cb => cb.value);
    console.log("Form data:", { name, email, role, topics });
    
    if (!name || !email) {
      toast("Please fill in name and email", true);
      return;
    }
    
    try {
      const body = isEdit 
        ? { action: "update", id: contact.id, name, email, role, topics, active: true }
        : { action: "add", name, email, role, topics };
      console.log("Sending to API:", body);
      
      const result = await api("/api/contacts", { method: "POST", body: JSON.stringify(body) });
      console.log("API result:", result);
      toast(isEdit ? "Contact updated" : "Contact added");
      document.body.removeChild(dialog);
      contactsCache = [];
      loadContactsList();
    } catch (err) {
      console.error("API error:", err);
      toast("Save failed：" + err.message, true);
    }
  });
  
  dialog.addEventListener("click", (e) => {
    if (e.target === dialog) document.body.removeChild(dialog);
  });
}

async function editContact(id) {
  const contacts = await loadContacts();
  const contact = contacts.find(c => c.id === id);
  if (contact) showContactDialog(contact);
}

async function deleteContact(id) {
  if (!confirm("Are you sure you want to delete this contact?")) return;
  try {
    await api("/api/contacts", { method: "POST", body: JSON.stringify({ action: "delete", id }) });
    toast("Contact deleted");
    contactsCache = [];
    loadContactsList();
  } catch (err) {
    toast("Delete failed：" + err.message, true);
  }
}

// ===== Assistant Floating Window =====
const assistantState = {
  messages: [],
  isOpen: false,
  isMinimized: false,
  isLoading: false,
  sessionId: null
};

const QUICK_QUESTIONS = [
  "Korea Cyber Security compliance requirements",
  "India OBD requirements",
  "UN-R156 OTA requirements",
  "Turkey export certification requirements",
  "Which markets have Data Security requirements",
  "Generate export market compliance report"
];

function toggleAssistant() {
  const panel = $("assistantPanel");
  const fab = $("assistantFab");
  
  assistantState.isOpen = !assistantState.isOpen;
  panel.classList.toggle("hidden", !assistantState.isOpen);
  panel.classList.toggle("visible", assistantState.isOpen);
  fab.classList.toggle("has-unread", false);
  
  if (assistantState.isOpen && !assistantState.messages.length) {
    renderAssistantWelcome();
    loadAssistantSessions();
  } else if (assistantState.isOpen) {
    renderAssistantMessages();
  }
}

function minimizeAssistant() {
  assistantState.isOpen = false;
  assistantState.isMinimized = true;
  $("assistantPanel").classList.add("hidden");
  $("assistantPanel").classList.remove("visible");
}

function renderAssistantWelcome() {
  const container = $("assistantMessages");
  container.innerHTML = `
    <div class="assistant-welcome">
      <div class="welcome-icon">🤖</div>
      <h3>Automotive Compliance AI</h3>
      <p>Reg search · Email · Compliance</p>
      <div class="quick-questions">
        ${QUICK_QUESTIONS.map(q => `
          <button class="quick-question-btn" data-question="${escapeHtml(q)}">${escapeHtml(q.length > 16 ? q.substring(0, 16) + "..." : q)}</button>
        `).join("")}
      </div>
      <div class="quick-questions email-chips">
        <button class="quick-question-btn email-action" data-q="latest emails">Latest Emails</button>
        <button class="quick-question-btn email-action" data-q="search CEADU emails">Search CEADU Emails</button>
        <button class="quick-question-btn email-action" data-q="emails needing reply">Needs Reply</button>
        <button class="quick-question-btn email-action" data-q="yesterday's briefing">📅 yesterday's briefing</button>
      </div>
    </div>
  `;
  
  container.querySelectorAll(".quick-question-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      if (btn.dataset.q) {
        $("assistantInput").value = btn.dataset.q;
      } else {
        $("assistantInput").value = btn.dataset.question;
      }
      sendAssistantMessage();
    });
  });
}

function renderAssistantMessages() {
  const container = $("assistantMessages");
  if (!assistantState.messages.length) {
    renderAssistantWelcome();
    return;
  }
  
  container.innerHTML = assistantState.messages.map(msg => `
    <div class="assistant-message ${msg.role}">
      ${msg.content}
      <span class="msg-time">${msg.timestamp || ""}</span>
    </div>
  `).join("");
  
  container.scrollTop = container.scrollHeight;
}

function appendAssistantMessage(role, content) {
  const container = $("assistantMessages");
  const hasWelcome = container.querySelector(".assistant-welcome");
  if (hasWelcome) {
    container.innerHTML = "";
  }
  
  const div = document.createElement("div");
  div.className = `assistant-message ${role}`;
  div.textContent = content;
  const time = document.createElement("span");
  time.className = "msg-time";
  time.textContent = new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
  div.appendChild(time);
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function showAssistantLoading() {
  const container = $("assistantMessages");
  const loading = document.createElement("div");
  loading.className = "assistant-loading";
  loading.id = "assistantLoading";
  loading.textContent = "Thinking";
  container.appendChild(loading);
  container.scrollTop = container.scrollHeight;
}

function removeAssistantLoading() {
  const loading = $("assistantLoading");
  if (loading) loading.remove();
}

async function sendAssistantMessage() {
  const input = $("assistantInput");
  const message = input.value.trim();
  
  if (!message || assistantState.isLoading) return;
  
  assistantState.isLoading = true;
  $("assistantSendBtn").disabled = true;
  $("assistantSendBtn").textContent = "...";
  
  appendAssistantMessage("user", message);
  input.value = "";
  input.style.height = "auto";
  
  showAssistantLoading();
  
  // Create session if needed
  let sessionId = assistantState.sessionId;
  if (!sessionId) {
    try {
      const sessionResult = await api("/api/chat/new-session", { method: "POST", body: JSON.stringify({}) });
      if (sessionResult.ok && sessionResult.session) {
        sessionId = sessionResult.session.id;
        assistantState.sessionId = sessionId;
      }
    } catch (e) { /* ignore session creation errors */ }
  }
  
  // Pre-fetch knowledge context to provide better answers
  let knowledgeContext = "";
  try {
    const kbData = await api(`/api/chat/search?q=${encodeURIComponent(message)}`);
    const hits = kbData.wiki_hits || [];
    if (hits.length > 0) {
      knowledgeContext = "\n\nReference knowledge base: \n" + hits.slice(0, 3)
        .map(h => `- ${h.title || h.path || ""}: ${(h.matches || []).map(m => m.text || m[1] || "").join("; ").substring(0, 200)}`)
        .join("\n");
    }
  } catch (e) { /* knowledge search is best-effort */ }
  
  try {
    const data = await api("/api/chat/send", {
      method: "POST",
      body: JSON.stringify({
        session_id: sessionId,
        message: message + knowledgeContext
      })
    });
    
    removeAssistantLoading();
    
    if (data.ok) {
      assistantState.messages.push({
        role: "assistant",
        content: data.response,
        timestamp: new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })
      });
      appendAssistantMessage("assistant", data.response);
    } else {
      appendAssistantMessage("assistant", "Error: " + (data.error || "Unknown error"));
    }
  } catch (err) {
    removeAssistantLoading();
    appendAssistantMessage("assistant", "Request failed: " + err.message);
  } finally {
    assistantState.isLoading = false;
    $("assistantSendBtn").disabled = false;
    $("assistantSendBtn").textContent = "Send";
  }
}

async function loadAssistantSessions() {
  try {
    const data = await api("/api/chat/sessions");
    if ((data.sessions || []).length > 0) {
      // Show suggestion if there are previous sessions
      const lastSession = data.sessions[0];
      const suggestionEl = $("assistantSuggestion");
      const textEl = $("suggestionText");
      if (suggestionEl && textEl) {
        textEl.textContent = `Continue previous conversation: ${lastSession.title || ""}`;
        suggestionEl.classList.remove("hidden");
        suggestionEl.dataset.sessionId = lastSession.id;
      }
    }
  } catch (e) { /* best-effort */ }
}

function useLastSession() {
  const suggestion = $("assistantSuggestion");
  const sessionId = suggestion?.dataset.sessionId;
  if (!sessionId) return;
  
  useSession(sessionId);
}

async function useSession(sessionId) {
  assistantState.sessionId = sessionId;
  $("assistantSuggestion").classList.add("hidden");
  try {
    const data = await api(`/api/chat/messages?session=${encodeURIComponent(sessionId)}&limit=20`);
    assistantState.messages = (data.messages || []).map(m => ({
      role: m.role,
      content: m.content,
      timestamp: m.timestamp ? m.timestamp.substring(11, 16) : ""
    }));
    renderAssistantMessages();
  } catch (e) {
    /* best-effort */
  }
}

function newAssistantSession() {
  assistantState.sessionId = null;
  assistantState.messages = [];
  $("assistantSuggestion").classList.add("hidden");
  renderAssistantWelcome();
  toast("Started new conversation");
}

// Context-aware: when user switches views, provide current context to assistant
function getCurrentContextHint() {
  const view = document.querySelector(".view.active")?.id || "dashboard";
  const hints = {
    dashboard: "Currently on Dashboard",
    assessment: "Currently on Assessment page",
    analysis: "Currently on Analysis page",
    wiki: "Currently on Wiki page"
  };
  return hints[view] || "";
}

// Auto-suggest based on current view
function showContextSuggestion() {
  const prompt = getCurrentContextHint();
  if (!prompt) return;
  
  const suggestions = {
    dashboard: "What pending tasks do I have today?",
    assessment: "Scan emails for assessment tasks?",
    analysis: "Analyze current market compliance status?",
    wiki: "Check UN-R155 compliance requirements?"
  };
  
  const viewId = $(".view.active.active")?.id;
  const suggestion = suggestions[viewId];
  if (suggestion) {
    // Show suggestion
    const container = $("assistantMessages");
    const hint = document.createElement("div");
    hint.className = "assistant-suggestion";
    hint.id = "contextSuggestion";
    hint.innerHTML = `<span>${escapeHtml(suggestion)}</span><button class="ghost small" onclick="document.getElementById('assistantInput').value='${escapeHtml(suggestion)}';document.getElementById('assistantInput').focus();">Use</button>`;
    container.prepend(hint);
  }
}

// Event listeners
$("assistantFab").addEventListener("click", toggleAssistant);
$("assistantMiniBtn").addEventListener("click", minimizeAssistant);
$("assistantSendBtn").addEventListener("click", sendAssistantMessage);
$("assistantInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendAssistantMessage();
  }
  // Auto-resize
  e.target.style.height = "auto";
  e.target.style.height = Math.min(e.target.scrollHeight, 100) + "px";
});
$("assistantInput").addEventListener("input", (e) => {
  e.target.style.height = "auto";
  e.target.style.height = Math.min(e.target.scrollHeight, 100) + "px";
});
$("suggestionUse").addEventListener("click", useLastSession);

// Init: hide panel on load
document.addEventListener("DOMContentLoaded", () => {
  $("assistantPanel").classList.add("hidden");
  $("assistantPanel").classList.remove("visible");
});

bindEvents();
refreshAll();
setInterval(loadStatus, 15000);

// Logout handler
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      await fetch("/api/auth/logout", { method: "POST", headers: authHeaders() });
    } catch (e) {}
    localStorage.removeItem("grc_token");
    window.location.href = "/login";
  });
}

// Load current user info
fetch("/api/auth/me", { headers: authHeaders() })
  .then(r => r.json())
  .then(data => {
    if (data.ok && data.user) {
      const titleEl = document.querySelector("p.eyebrow");
      if (titleEl) titleEl.textContent = `G.R.C. Agent — ${data.user.display_name || data.user.username}`;
    }
  })
  .catch(() => {});
