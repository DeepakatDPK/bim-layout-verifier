"""SQLite Vector Store for Fast Markup Lookups."""
import sqlite3
import os
from typing import List, Optional, Dict
from dataclasses import dataclass

@dataclass
class StoredMarkup:
    id: str
    markup_type: str
    text: str
    position_x: float
    position_y: float
    size_x: float
    size_y: float
    color_r: int
    color_g: int
    color_b: int
    confidence: float
    source_file: str

class VectorStore:
    """SQLite-backed vector store for efficient markup queries."""
    
    def __init__(self, db_path: str = "markup_store.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS markups (
                id TEXT PRIMARY KEY,
                markup_type TEXT NOT NULL,
                text TEXT,
                position_x REAL NOT NULL,
                position_y REAL NOT NULL,
                size_x REAL NOT NULL,
                size_y REAL NOT NULL,
                color_r INTEGER NOT NULL,
                color_g INTEGER NOT NULL,
                color_b INTEGER NOT NULL,
                confidence REAL DEFAULT 1.0,
                source_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_position ON markups(position_x, position_y)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_markup_type ON markups(markup_type)")
        
        conn.commit()
        conn.close()
    
    def store(self, markup_item):
        """Store a single markup item."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO markups 
            (id, markup_type, text, position_x, position_y, 
             size_x, size_y, color_r, color_g, color_b, 
             confidence, source_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            markup_item.id,
            str(markup_item.markup_type),
            markup_item.text,
            markup_item.position[0],
            markup_item.position[1],
            markup_item.size[0],
            markup_item.size[1],
            markup_item.color[0],
            markup_item.color[1],
            markup_item.color[2],
            markup_item.confidence,
            markup_item.source_file
        ))
        
        conn.commit()
        conn.close()
    
    def query_by_position(self, x: float, y: float, tolerance: float = 20.0) -> List[Dict]:
        """Find markups within position tolerance."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM markups 
            WHERE position_x BETWEEN ? AND ?
              AND position_y BETWEEN ? AND ?
        """, (x - tolerance, x + tolerance, y - tolerance, y + tolerance))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": row[0],
            "markup_type": row[1],
            "text": row[2],
            "position": (row[3], row[4]),
            "size": (row[5], row[6]),
            "color": (row[7], row[8], row[9]),
            "confidence": row[10],
            "source_file": row[11]
        } for row in rows]
    
    def count(self) -> int:
        """Total markup count."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM markups")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def clear(self):
        """Clear all data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM markups")
        conn.commit()
        conn.close()
