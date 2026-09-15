export default function handler(req, res) {
  res.status(503).json({ error: "Backend not available in demo mode" });
}
