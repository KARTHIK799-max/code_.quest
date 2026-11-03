import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "codequest.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        streak INTEGER DEFAULT 1,
        last_active_date TEXT,
        created_at TEXT
    );
    """)

    # Completed Missions & Levels
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed_missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        mission_id TEXT NOT NULL,
        mission_type TEXT NOT NULL,
        stars INTEGER DEFAULT 3,
        xp_earned INTEGER DEFAULT 0,
        completed_at TEXT,
        UNIQUE(user_id, mission_id)
    );
    """)

    # Achievements unlocked
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        badge_id TEXT NOT NULL,
        unlocked_at TEXT,
        UNIQUE(user_id, badge_id)
    );
    """)

    # Default player
    cursor.execute("SELECT id FROM users WHERE id = 'player_one'")
    if not cursor.fetchone():
        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO users (id, username, xp, level, streak, last_active_date, created_at)
        VALUES ('player_one', 'QuestNovice', 120, 2, 3, ?, ?)
        """, (today_str, today_str))
        
        # Initial achievements for starter
        cursor.execute("""
        INSERT OR IGNORE INTO achievements (user_id, badge_id, unlocked_at)
        VALUES ('player_one', 'first_steps', ?)
        """, (today_str,))
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("CodeQuest database initialized at:", DB_PATH)
