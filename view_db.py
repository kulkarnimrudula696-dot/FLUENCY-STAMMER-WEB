"""
FLUENCY Database Viewer Script
Run this script anytime to inspect the SQLite database tables and data:
python view_db.py
"""

import sqlite3
import os
import json

db_path = os.path.join("instance", "database.db")
if not os.path.exists(db_path):
    db_path = "database.db"

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}. Please run app.py first to initialize.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print(f"       FLUENCY DATABASE INSPECTOR ({db_path})")
print("=" * 70)

# 1. Show Users
print("\n--- 1. USERS TABLE (`users`) ---")
cursor.execute("SELECT id, name, email, actual_age, practice_age, selected_mascot, preferred_language, created_at FROM users")
users = cursor.fetchall()
if users:
    print(f"{'ID':<4} | {'Name':<18} | {'Email':<24} | {'Age':<4} | {'Prac Age':<8} | {'Mascot':<10} | {'Language':<10}")
    print("-" * 90)
    for u in users:
        print(f"{u[0]:<4} | {u[1]:<18} | {u[2]:<24} | {u[3]:<4} | {u[4]:<8} | {u[5]:<10} | {u[6]:<10}")
else:
    print("No users found.")

# 2. Show Practice Sessions
print("\n--- 2. PRACTICE SESSIONS TABLE (`practice_sessions`) ---")
cursor.execute("SELECT id, user_id, mode, title, duration_seconds, wpm, pauses_count, clarity_score, created_at FROM practice_sessions ORDER BY id DESC LIMIT 10")
sessions = cursor.fetchall()
if sessions:
    print(f"{'ID':<4} | {'User':<5} | {'Mode':<12} | {'Title':<28} | {'Dur(s)':<6} | {'WPM':<6} | {'Pauses':<8} | {'Clarity':<8} | {'Date':<16}")
    print("-" * 110)
    for s in sessions:
        print(f"{s[0]:<4} | {s[1]:<5} | {s[2]:<12} | {s[3][:26]:<28} | {s[4]:<6} | {s[5]:<6} | {s[6]:<8} | {s[7]:<8} | {str(s[8])[:16]:<16}")
else:
    print("No practice sessions found.")

# 3. Show Bug Reports
print("\n--- 3. BUG REPORTS TABLE (`bug_reports`) ---")
cursor.execute("SELECT id, user_id, title, page_occurred, severity, status, created_at FROM bug_reports")
bugs = cursor.fetchall()
if bugs:
    print(f"{'Ticket':<8} | {'User':<5} | {'Title':<26} | {'Page':<16} | {'Severity':<10} | {'Status':<10}")
    print("-" * 85)
    for b in bugs:
        print(f"FL-{b[0]:04d}  | {str(b[1]):<5} | {b[2][:24]:<26} | {b[3]:<16} | {b[4]:<10} | {b[5]:<10}")
else:
    print("No bug reports logged.")

print("\n" + "=" * 70)
conn.close()
