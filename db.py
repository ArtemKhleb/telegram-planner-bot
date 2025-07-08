import sqlite3
from datetime import datetime

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    datetime TEXT,
    completed INTEGER DEFAULT 0
)''')
conn.commit()

def add_task(text):
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (text,))
    conn.commit()
    return text

def get_tasks():
    cursor.execute("SELECT id, description, completed FROM tasks WHERE completed = 0")
    rows = cursor.fetchall()
    if not rows:
        return "✅ Нет активных задач."
    return "\n".join([f"{r[0]}. {r[1]}" for r in rows])

def complete_task(task_id):
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    return f"✅ Задача {task_id} завершена."