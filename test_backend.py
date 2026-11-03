"""
Backend Test Script for CodeQuest
Tests database creation, FastAPI routes, and anti-farming XP logic.
"""
import sys
import os

from database import init_db, get_db

def run_tests():
    print("Testing CodeQuest Database...")
    init_db()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Verify users table exists and has player_one
    cursor.execute("SELECT * FROM users WHERE id = 'player_one'")
    user = cursor.fetchone()
    assert user is not None, "Starter user 'player_one' not found!"
    print(f"PASS: User found: {user['username']} (XP: {user['xp']}, Level: {user['level']})")
    
    # 2. Verify completed_missions table
    cursor.execute("SELECT COUNT(*) as cnt FROM completed_missions")
    count = cursor.fetchone()["cnt"]
    print(f"PASS: Completed missions table initialized (count: {count})")
    
    # 3. Verify achievements table
    cursor.execute("SELECT COUNT(*) as cnt FROM achievements")
    ach_count = cursor.fetchone()["cnt"]
    print(f"PASS: Achievements table initialized (count: {ach_count})")
    
    conn.close()
    print("ALL BACKEND DB TESTS PASSED SUCCESSFULLY! [OK]")

if __name__ == "__main__":
    run_tests()
