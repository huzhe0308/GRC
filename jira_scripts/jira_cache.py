import json
import os
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class JiraCache:
    CACHE_FILE = "runtime/jira_cache.json"
    
    @classmethod
    def load(cls) -> dict | None:
        cache_path = Path(cls.CACHE_FILE)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return None
    
    @classmethod
    def save(cls, data: dict):
        cache_path = Path(cls.CACHE_FILE)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Jira cache saved to {cls.CACHE_FILE}")
    
    @classmethod
    def get_my_tickets(cls):
        data = cls.load()
        if data:
            issues = data.get('issues', [])
            print(f"=== Cached Jira Tickets ({len(issues)} issues) ===\n")
            for issue in issues[:10]:
                key = issue.get('key', 'N/A')
                fields = issue.get('fields', {})
                summary = fields.get('summary', 'N/A')[:60]
                status = fields.get('status', {}).get('name', 'N/A')
                print(f"[{key}] {status}: {summary}")
            return issues
        print("No cache available. Run with opencode skill first to populate cache.")
        return []

if __name__ == '__main__':
    JiraCache.get_my_tickets()
