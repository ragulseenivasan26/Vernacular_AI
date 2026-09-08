import sqlite3
import os
import csv
import io
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vernacular_ai.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database table if it doesn't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                source_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_favorite INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def save_translation(source_lang, target_lang, source_text, translated_text):
    """Saves a new translation entry into SQLite database."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO translations (source_lang, target_lang, source_text, translated_text)
            VALUES (?, ?, ?, ?)
        """, (source_lang, target_lang, source_text, translated_text))
        conn.commit()
        return cursor.lastrowid

def get_history(limit=50):
    """Fetches recent translation history."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, source_lang, target_lang, source_text, translated_text, created_at, is_favorite
            FROM translations
            ORDER BY created_at DESC, id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_all_rows():
    """Returns all rows for export."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, source_lang, target_lang, source_text, translated_text, created_at, is_favorite
            FROM translations
            ORDER BY id ASC
        """)
        return [dict(row) for row in cursor.fetchall()]

def delete_history_item(item_id):
    """Deletes a specific history item by ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM translations WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0

def clear_all_history():
    """Clears all translation history."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM translations")
        conn.commit()
        return True

def toggle_favorite(item_id):
    """Toggles bookmark/favorite status."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE translations
            SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END
            WHERE id = ?
        """, (item_id,))
        conn.commit()
        
        cursor.execute("SELECT is_favorite FROM translations WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return row["is_favorite"] if row else None

def get_db_info():
    """Returns comprehensive database metadata, storage location, and statistics."""
    init_db()
    file_size = 0
    if os.path.exists(DB_PATH):
        file_size = os.path.getsize(DB_PATH)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM translations")
        total_rows = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM translations WHERE is_favorite = 1")
        starred_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT target_lang) FROM translations")
        languages_count = cursor.fetchone()[0]

        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='translations'")
        schema_row = cursor.fetchone()
        schema_sql = schema_row[0] if schema_row else ""

    return {
        "database_file": os.path.abspath(DB_PATH),
        "database_engine": "SQLite 3",
        "file_size_bytes": file_size,
        "file_size_kb": round(file_size / 1024, 2),
        "total_records": total_rows,
        "starred_records": starred_count,
        "distinct_target_languages": languages_count,
        "table_name": "translations",
        "schema_sql": schema_sql
    }

def export_as_csv():
    """Exports all rows as CSV string."""
    rows = get_all_rows()
    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue()

def find_cached_translation(source_text, source_lang="English", target_lang="Tamil"):
    """Finds a previously saved translation from SQLite cache (essential for offline mode)."""
    if not source_text:
        return None
    init_db()
    cleaned = str(source_text).strip()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT translated_text FROM translations
            WHERE LOWER(TRIM(source_text)) = LOWER(?)
              AND (LOWER(target_lang) = LOWER(?) OR target_lang = ?)
            ORDER BY id DESC LIMIT 1
        """, (cleaned, target_lang, target_lang))
        row = cursor.fetchone()
        return row["translated_text"] if row else None

