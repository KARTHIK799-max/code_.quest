import math
from datetime import datetime, date
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_db, init_db

app = FastAPI(
    title="CodeQuest API",
    description="Backend API for CodeQuest - Gamified Coding Education Platform",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database schema on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Pydantic Request Models
class ProgressUpdate(BaseModel):
    user_id: str = "player_one"
    mission_id: str
    mission_type: str = "game"  # 'game' | 'quiz' | 'lesson'
    xp_to_award: int = 100
    stars: int = 3
    badges_to_unlock: Optional[List[str]] = []

class ResetRequest(BaseModel):
    user_id: str = "player_one"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CodeQuest Backend",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/user/profile")
def get_user_profile(user_id: str = "player_one"):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    cursor.execute("SELECT mission_id, mission_type, stars, completed_at FROM completed_missions WHERE user_id = ?", (user_id,))
    missions = [dict(m) for m in cursor.fetchall()]

    cursor.execute("SELECT badge_id, unlocked_at FROM achievements WHERE user_id = ?", (user_id,))
    achievements = [dict(a) for a in cursor.fetchall()]
    
    conn.close()
    
    return {
        "id": user["id"],
        "username": user["username"],
        "xp": user["xp"],
        "level": user["level"],
        "streak": user["streak"],
        "last_active_date": user["last_active_date"],
        "completed_missions": missions,
        "achievements": achievements
    }

@app.post("/api/user/progress")
def record_progress(data: ProgressUpdate):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE id = ?", (data.user_id,))
    user = cursor.fetchone()
    if not user:
        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO users (id, username, xp, level, streak, last_active_date, created_at) VALUES (?, 'Learner', 0, 1, 1, ?, ?)",
                       (data.user_id, today_str, today_str))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (data.user_id,))
        user = cursor.fetchone()

    # Check if mission was already completed
    cursor.execute("SELECT id FROM completed_missions WHERE user_id = ? AND mission_id = ?", (data.user_id, data.mission_id))
    already_completed = cursor.fetchone() is not None
    
    xp_earned = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if not already_completed:
        xp_earned = data.xp_to_award
        cursor.execute("""
        INSERT INTO completed_missions (user_id, mission_id, mission_type, stars, xp_earned, completed_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (data.user_id, data.mission_id, data.mission_type, data.stars, xp_earned, today_str))
    else:
        # Update stars if player did better
        cursor.execute("""
        UPDATE completed_missions SET stars = MAX(stars, ?) WHERE user_id = ? AND mission_id = ?
        """, (data.stars, data.user_id, data.mission_id))

    # Calculate new XP and level
    new_xp = user["xp"] + xp_earned
    # Level formula: level = floor(sqrt(xp / 50)) + 1
    new_level = max(1, math.floor(math.sqrt(new_xp / 50)) + 1)
    
    # Calculate streak: if last active is yesterday, streak += 1. If today, same. If older, reset to 1.
    last_active = user["last_active_date"]
    new_streak = user["streak"]
    if last_active and last_active != today_str:
        try:
            last_date = datetime.strptime(last_active, "%Y-%m-%d").date()
            today_date = date.today()
            diff_days = (today_date - last_date).days
            if diff_days == 1:
                new_streak += 1
            elif diff_days > 1:
                new_streak = 1
        except Exception:
            pass

    cursor.execute("""
    UPDATE users SET xp = ?, level = ?, streak = ?, last_active_date = ? WHERE id = ?
    """, (new_xp, new_level, new_streak, today_str, data.user_id))

    # Record any new achievements
    unlocked_badges = []
    if data.badges_to_unlock:
        for badge in data.badges_to_unlock:
            cursor.execute("INSERT OR IGNORE INTO achievements (user_id, badge_id, unlocked_at) VALUES (?, ?, ?)",
                           (data.user_id, badge, today_str))
            unlocked_badges.append(badge)

    conn.commit()
    conn.close()

    return {
        "success": True,
        "already_completed": already_completed,
        "xp_earned": xp_earned,
        "total_xp": new_xp,
        "level": new_level,
        "streak": new_streak,
        "unlocked_badges": unlocked_badges
    }

@app.post("/api/user/reset")
def reset_progress(req: ResetRequest):
    conn = get_db()
    cursor = conn.cursor()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("DELETE FROM completed_missions WHERE user_id = ?", (req.user_id,))
    cursor.execute("DELETE FROM achievements WHERE user_id = ?", (req.user_id,))
    cursor.execute("UPDATE users SET xp = 0, level = 1, streak = 1, last_active_date = ? WHERE id = ?", (today_str, req.user_id))
    
    conn.commit()
    conn.close()
    return {"success": True, "message": "Progress reset successfully"}

@app.get("/api/leaderboard")
def get_leaderboard(user_id: str = "player_one"):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, xp, level, streak FROM users WHERE id = ?", (user_id,))
    curr_user = cursor.fetchone()
    conn.close()
    
    user_xp = curr_user["xp"] if curr_user else 150
    user_lvl = curr_user["level"] if curr_user else 2
    user_streak = curr_user["streak"] if curr_user else 3

    # Seeded community learners + active user
    learners = [
        {"rank": 1, "username": "Ada_Lovelace", "xp": 4250, "level": 10, "streak": 28, "badge": "Algorithm Pioneer", "is_user": False},
        {"rank": 2, "username": "Alan_Turing", "xp": 3890, "level": 9, "streak": 21, "badge": "Turing Complete", "is_user": False},
        {"rank": 3, "username": "Grace_Hopper", "xp": 3420, "level": 9, "streak": 19, "badge": "Compiler Queen", "is_user": False},
        {"rank": 4, "username": "Linus_Kernel", "xp": 2980, "level": 8, "streak": 14, "badge": "Open Source Hero", "is_user": False},
        {"rank": 5, "username": "Karthik_CSE", "xp": user_xp, "level": user_lvl, "streak": user_streak, "badge": "Rising Star", "is_user": True},
        {"rank": 6, "username": "CodeSamurai", "xp": 1150, "level": 5, "streak": 7, "badge": "Loop Master", "is_user": False},
        {"rank": 7, "username": "ByteWizard", "xp": 940, "level": 4, "streak": 5, "badge": "Bug Hunter", "is_user": False},
        {"rank": 8, "username": "PixelPioneer", "xp": 720, "level": 3, "streak": 4, "badge": "Explorer", "is_user": False},
    ]

    # Re-sort dynamically by XP
    learners.sort(key=lambda x: x["xp"], reverse=True)
    for idx, item in enumerate(learners):
        item["rank"] = idx + 1

    return {"leaderboard": learners}
