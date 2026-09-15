const MARKETS = [
  { name: "South Korea", ticket: "CEADU-682", layer3: "CEADU-2634", cyber: "CEADU-2623", data: "CEADU-2631", ota: "CEADU-2634", obd: null, fusa: "CEADU-2634" },
  { name: "ASEAN RHD", ticket: "CEADU-2739", layer3: "CEADU-3137", cyber: "CEADU-3137", data: "CEADU-5602", ota: "CEADU-3137", obd: null, fusa: "CEADU-3137" },
  { name: "ASEAN LHD", ticket: "CEADU-3005", layer3: "CEADU-3281", cyber: "CEADU-3281", data: "CEADU-3281", ota: "CEADU-3281", obd: null, fusa: "CEADU-3281" },
  { name: "India", ticket: "CEADU-3784", layer3: "CEADU-3974", cyber: "CEADU-3971", data: "CEADU-3974", ota: "CEADU-3974", obd: null, fusa: "CEADU-3974" },
  { name: "Middle East", ticket: "CEADU-4514", layer3: "CEADU-5081", cyber: "CEADU-5081", data: "CEADU-5751", ota: "CEADU-5081", obd: "CEADU-5081", fusa: "CEADU-5081" },
  { name: "Kazakhstan", ticket: "CEADU-4494", layer3: "CEADU-4864", cyber: "CEADU-4864", data: "CEADU-4870", ota: "CEADU-4864", obd: "CEADU-4864", fusa: "CEADU-4864" },
  { name: "Uzbekistan", ticket: "CEADU-5282", layer3: "CEADU-6502", cyber: "CEADU-6509", data: "CEADU-6508", ota: "CEADU-6502", obd: "CEADU-6502", fusa: "CEADU-6502" },
  { name: "Turkey", ticket: "CEADU-6364", layer3: "CEADU-6699", cyber: "CEADU-6706", data: "CEADU-6705", ota: "CEADU-6699", obd: "CEADU-6699", fusa: "CEADU-6699" },
  { name: "AUS/NZL (CMP21)", ticket: "CEADU-2711", layer3: "CEADU-3128", cyber: "CEADU-3128", data: "CEADU-5601", ota: "CEADU-3128", obd: null, fusa: "CEADU-3128" },
  { name: "AUS/NZL (CSP31)", ticket: "CEADU-6746", layer3: "CEADU-6749", cyber: "CEADU-6749", data: "CEADU-6757", ota: "CEADU-6749", obd: "CEADU-6749", fusa: "CEADU-6749" },
];

const TOPIC_CONFIG = {
  cyber_security: { label: "Cyber Security", icon: "🔐" },
  data_security: { label: "Data Security", icon: "🔒" },
  fusa_data: { label: "Functional Safety", icon: "🛡️" },
  ota_data: { label: "OTA and SW Update", icon: "🔄" },
  immobilizer_data: { label: "Immobilizer", icon: "🔗" },
  obd_data: { label: "OBD", icon: "📡" },
};

const CONTACTS = [
  { id: "c001", name: "Kunze, Kai", email: "kai.kunze@volkswagen-tech.com", topics: ["cyber_security", "data_security", "immobilizer_data"], role: "Cyber/Data Security Expert", active: true },
  { id: "c002", name: "Sun, Hao (Dr.)", email: "hao.sun@volkswagen-tech.com", topics: ["fusa_data"], role: "Functional Safety Expert", active: true },
  { id: "c003", name: "Xie, Jingjin", email: "jingjin.xie@volkswagen-tech.com", topics: ["cyber_security", "data_security", "fusa_data", "ota_data", "immobilizer_data", "obd_data"], role: "GVEX Coordinator", active: true },
];

function gapTrackingStatus() {
  const markets_out = [];
  for (const m of MARKETS) {
    const topics = [];
    for (const [topicKey, cfg] of Object.entries(TOPIC_CONFIG)) {
      const ticket = m[topicKey === "cyber_security" ? "cyber" : topicKey === "data_security" ? "data" : topicKey === "fusa_data" ? "fusa" : topicKey === "ota_data" ? "ota" : topicKey === "obd_data" ? "obd" : "layer3"];
      if (!ticket) continue;
      topics.push({
        topic: topicKey,
        label: cfg.label,
        icon: cfg.icon,
        ticket: ticket,
        status: "pending",
        comments_total: 0,
        gap_summary: "",
        updated_at: "",
        manual_override: 0,
      });
    }
    markets_out.push({
      market: m.name,
      parent_ticket: m.ticket,
      layer3_ticket: m.layer3,
      layer3_url: `https://devstack.vgc.com.cn/jira/browse/${m.layer3}`,
      layer3_closed: false,
      can_close: false,
      topics: topics,
    });
  }
  return {
    markets: markets_out,
    reminders: [],
    last_inspection: { checked: 0, changed: 0, time: "", source: "" },
  };
}

function exportMarketsData() {
  const market_mapping = {
    "Korea": ["CEADU-682", "CEADU-2631"],
    "ASEAN RHD": ["CEADU-2739", "CEADU-5602"],
    "ASEAN LHD": ["CEADU-3005"],
    "India": ["CEADU-3784", "CEADU-3974", "CEADU-3978"],
    "Middle East": ["CEADU-4514", "CEADU-5751", "CEADU-5081", "CEADU-5085"],
    "Kazakhstan": ["CEADU-4494", "CEADU-4870", "CEADU-4864", "CEADU-4868"],
    "Uzbekistan": ["CEADU-5282", "CEADU-6508", "CEADU-6502", "CEADU-6509"],
    "Turkey": ["CEADU-6364", "CEADU-6705", "CEADU-6699", "CEADU-6706"],
    "AUS/NZL CMP21": ["CEADU-2711", "CEADU-5601", "CEADU-3128", "CEADU-3132"],
    "AUS/NZL CSP31": ["CEADU-6746", "CEADU-6757", "CEADU-6749"],
  };
  const markets = [];
  for (const [name, keys] of Object.entries(market_mapping)) {
    markets.push({
      name,
      tickets: keys.map(k => ({ key: k, summary: "", status: "To Do", domain: "All", comments: [] })),
    });
  }
  return { markets };
}

function getRoutes(path, method, query, body) {
  if (path === "/api/status") {
    return {
      model: "MiniMax",
      api_key_set: false,
      send_dry_run: true,
      send_to: [],
      mail_backend: "",
      mail_keyword: ["CEADU"],
      reports: 0,
      wiki_counts: { raw: 0, entities: 0, concepts: 0, comparisons: 0, queries: 0 },
      runs: [],
      automation: { enabled: false, running: false, last_status: "idle" },
    };
  }
  if (path === "/api/emails") return { emails: [] };
  if (path === "/api/assessments/sent") return { sent: [] };
  if (path === "/api/reports") return { reports: [] };
  if (path === "/api/wiki/list") return { files: [], counts: { raw: 0, entities: 0, concepts: 0, comparisons: 0, queries: 0 } };
  if (path === "/api/wiki/search") return { results: [] };
  if (path === "/api/wiki/search-semantic") return { results: [] };
  if (path === "/api/wiki/file") return { path: "", text: "Wiki content not available in cloud demo mode." };
  if (path === "/api/automation") return { enabled: false, running: false, last_status: "idle" };
  if (path === "/api/jira/tickets") return { tickets: [] };
  if (path === "/api/jira/search") return { tickets: [] };
  if (path === "/api/jira/refresh") return { ok: true, message: "Jira refresh not available in cloud mode" };
  if (path === "/api/export-markets/data") return exportMarketsData();
  if (path === "/api/export-markets/ticket-detail") return { key: query.key || "", error: "Not available in cloud mode" };
  if (path === "/api/gap-tracking/status") return gapTrackingStatus();
  if (path === "/api/gap-tracking/updates") return { updates: [] };
  if (path === "/api/gap-tracking/monitor-status") return { running: false, enabled: false, interval_sec: 1800, last_check: "", next_check: "" };
  if (path === "/api/gap-tracking/inspection") return { checked: 0, changed: 0, time: "", source: "", monitor: { running: false, enabled: false } };
  if (path === "/api/contacts") return { contacts: CONTACTS };
  if (path === "/api/contacts/by-topic") return { contacts: CONTACTS, topic: query.topic || "" };
  if (path === "/api/chat/sessions") return { sessions: [] };
  if (path === "/api/chat/messages") return { messages: [] };
  if (path === "/api/chat/search") return { results: [] };
  if (path === "/api/chat/new-session" && method === "POST") return { session_id: "demo-" + Date.now() };
  if (path === "/api/chat/send" && method === "POST") return { reply: "AI assistant is not available in cloud demo mode. Please use the local version for full functionality." };
  if (path === "/api/monthly-report/generate") return { html: "<p>Monthly report generation requires local backend.</p>" };
  if (path === "/api/assessment/parse-pvs") return { regulations: [], message: "PSV parsing requires local backend." };
  if (path === "/api/run" && method === "POST") return { ok: false, error: "Agent execution requires local backend." };
  if (path === "/api/outlook/latest") return { emails: [] };
  if (path === "/api/outlook/search") return { emails: [] };
  if (path === "/api/outlook/needs-reply") return { emails: [] };
  if (path === "/api/outlook/yesterday") return { emails: [] };
  return null;
}

function postRoutes(path, body) {
  if (path === "/api/contacts") {
    if (body.action === "add") return { ok: true, contact: { id: "c" + (CONTACTS.length + 1), ...body } };
    if (body.action === "update") return { ok: true };
    if (body.action === "delete") return { ok: true };
  }
  if (path === "/api/gap-tracking/set-status") return { ok: true };
  if (path === "/api/gap-tracking/reset") return { ok: true };
  if (path === "/api/gap-tracking/complete") return { ok: true };
  if (path === "/api/gap-tracking/close-layer3") return { ok: true, message: "Close Layer3 requires local backend" };
  if (path === "/api/gap-tracking/write-summary") return { ok: true, message: "Write summary requires local backend" };
  if (path === "/api/gap-tracking/trigger-check") return { ok: true, checked: 0, changed: 0 };
  if (path === "/api/gap-tracking/mark-read") return { ok: true };
  if (path === "/api/gap-tracking/monitor") return { ok: true, running: false };
  if (path === "/api/assessment/send") return { ok: false, error: "Assessment email sending requires local backend." };
  if (path === "/api/monthly-report/send-draft") return { ok: false, error: "Email sending requires local Outlook." };
  if (path === "/api/export-markets/generate-report") return { ok: false, error: "Report generation requires local backend." };
  if (path.startsWith("/api/analysis/")) return { ok: false, error: "Analysis requires local backend." };
  return null;
}

export default function handler(req, res) {
  const url = new URL(req.url, "http://localhost");
  const path = url.pathname;
  const query = Object.fromEntries(url.searchParams);
  const method = req.method;

  res.setHeader("Content-Type", "application/json");

  let body = {};
  if (method === "POST") {
    try {
      body = typeof req.body === "string" ? JSON.parse(req.body) : (req.body || {});
    } catch (e) {
      body = {};
    }
  }

  const data = method === "GET" ? getRoutes(path, method, query, body) : postRoutes(path, body);
  if (data !== null) {
    res.status(200).json(data);
  } else {
    res.status(404).json({ error: "Not found: " + path });
  }
}
