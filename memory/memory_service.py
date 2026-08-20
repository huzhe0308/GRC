import sqlite3
import json
import hashlib
import difflib
from pathlib import Path
from typing import Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def init_memory_db(db_path: Path) -> sqlite3.Connection:
    """初始化Memory数据库"""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            session_id TEXT,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT NOT NULL,
            wiki_hits TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_hash TEXT UNIQUE NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source_wiki_pages TEXT,
            confidence TEXT,
            usage_count INTEGER DEFAULT 0,
            last_used_at TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entity_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            related_entity TEXT NOT NULL,
            source_report TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            UNIQUE(entity_name, relation_type, related_entity)
        )
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_memory_run_id ON conversation_memory(run_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_memory_session ON conversation_memory(session_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_hash ON knowledge_cards(question_hash)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_entity_name ON entity_relations(entity_name)
    """)
    
    conn.commit()
    return conn


class WorkflowMemory:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = init_memory_db(self.db_path)
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _hash_question(self, question: str) -> str:
        return hashlib.sha256(question.encode('utf-8')).hexdigest()[:16]
    
    def store_turn(self, run_id: str, role: str, content: str,
                   wiki_hits: list[str] = None, session_id: str = None) -> int:
        cursor = self.conn.execute("""
            INSERT INTO conversation_memory 
            (run_id, session_id, role, content, wiki_hits)
            VALUES (?, ?, ?, ?, ?)
        """, (
            run_id,
            session_id or self.current_session_id,
            role,
            content,
            json.dumps(wiki_hits or [], ensure_ascii=False) if wiki_hits else None
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def store_question_answer(self, run_id: str, question: str, answer: str,
                              wiki_pages: list[str] = None,
                              confidence: str = None) -> int:
        q_hash = self._hash_question(question)
        
        existing = self.conn.execute(
            "SELECT id FROM knowledge_cards WHERE question_hash = ?",
            (q_hash,)
        ).fetchone()
        
        if existing:
            self.conn.execute("""
                UPDATE knowledge_cards 
                SET answer = ?, source_wiki_pages = ?, confidence = ?,
                    usage_count = usage_count + 1,
                    last_used_at = datetime('now', 'localtime')
                WHERE question_hash = ?
            """, (answer, json.dumps(wiki_pages or [], ensure_ascii=False),
                  confidence, q_hash))
        else:
            self.conn.execute("""
                INSERT INTO knowledge_cards 
                (question_hash, question, answer, source_wiki_pages, confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (q_hash, question, answer,
                  json.dumps(wiki_pages or [], ensure_ascii=False), confidence))
        
        self.store_turn(run_id, "user", question, wiki_pages)
        self.store_turn(run_id, "assistant", answer, wiki_pages)
        self.conn.commit()
        return existing[0] if existing else self.conn.execute(
            "SELECT last_insert_rowid()").fetchone()[0]
    
    def get_recent_context(self, run_id: str = None, limit: int = 10) -> list[dict]:
        query = """
            SELECT run_id, role, content, wiki_hits, created_at
            FROM conversation_memory
        """
        params = []
        if run_id:
            query += " WHERE run_id = ?"
            params.append(run_id)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        
        rows = self.conn.execute(query, params).fetchall()
        return [
            {
                "run_id": r[0],
                "role": r[1],
                "content": r[2],
                "wiki_hits": json.loads(r[3]) if r[3] else [],
                "created_at": r[4]
            }
            for r in reversed(rows)
        ]
    
    def find_similar_question(self, question: str, threshold: float = 0.6) -> dict | None:
        cards = self.conn.execute("""
            SELECT question, answer, source_wiki_pages, usage_count, confidence
            FROM knowledge_cards
        """).fetchall()
        
        best_match = None
        best_score = threshold
        
        q_lower = question.lower()
        for card in cards:
            score = difflib.SequenceMatcher(
                None, q_lower, card[0].lower()
            ).ratio()
            if score > best_score:
                best_score = score
                best_match = {
                    "question": card[0],
                    "answer": card[1],
                    "wiki_pages": json.loads(card[2]) if card[2] else [],
                    "usage_count": card[3],
                    "confidence": card[4],
                    "similarity": score
                }
        
        return best_match
    
    def store_entity_relation(self, entity: str, relation_type: str,
                               related: str, source_report: str = None) -> int:
        try:
            cursor = self.conn.execute("""
                INSERT OR IGNORE INTO entity_relations
                (entity_name, relation_type, related_entity, source_report)
                VALUES (?, ?, ?, ?)
            """, (entity, relation_type, related, source_report))
            self.conn.commit()
            return cursor.lastrowid
        except Exception:
            return 0
    
    def get_entity_context(self, entities: list[str], limit: int = 5) -> list[dict]:
        if not entities:
            return []
        
        placeholders = ','.join('?' * len(entities))
        rows = self.conn.execute(f"""
            SELECT entity_name, relation_type, related_entity, source_report, created_at
            FROM entity_relations
            WHERE entity_name IN ({placeholders}) OR related_entity IN ({placeholders})
            ORDER BY created_at DESC
            LIMIT ?
        """, entities + entities + [limit]).fetchall()
        
        return [
            {
                "entity": r[0],
                "relation": r[1],
                "related": r[2],
                "source": r[3],
                "created_at": r[4]
            }
            for r in rows
        ]
    
    def build_context_prompt(self, question: str = None, run_id: str = None,
                             max_history: int = 5) -> str:
        parts = []
        
        similar = self.find_similar_question(question) if question else None
        if similar:
            parts.append(f"## Similar Past Answer (Similarity: {similar['similarity']:.0%})\n"
                        f"Q: {similar['question']}\nA: {similar['answer']}")
        
        history = self.get_recent_context(run_id, limit=max_history)
        if history:
            history_text = "\n".join([
                f"[{h['role']}]: {h['content'][:200]}..."
                for h in history if h['content']
            ])
            parts.append(f"## Recent Conversation History\n{history_text}")
        
        return "\n\n".join(parts) if parts else ""
    
    def get_stats(self) -> dict:
        stats = {
            "total_memory_turns": self.conn.execute(
                "SELECT COUNT(*) FROM conversation_memory").fetchone()[0],
            "total_knowledge_cards": self.conn.execute(
                "SELECT COUNT(*) FROM knowledge_cards").fetchone()[0],
            "total_entity_relations": self.conn.execute(
                "SELECT COUNT(*) FROM entity_relations").fetchone()[0],
            "top_used_cards": self.conn.execute("""
                SELECT question, usage_count FROM knowledge_cards
                ORDER BY usage_count DESC LIMIT 5
            """).fetchall()
        }
        return stats
    
    def clear_old_entries(self, days: int = 30) -> int:
        cursor = self.conn.execute("""
            DELETE FROM conversation_memory
            WHERE created_at < datetime('now', '-{} days', 'localtime')
        """.format(days))
        self.conn.commit()
        return cursor.rowcount
    
    def close(self):
        self.conn.close()
