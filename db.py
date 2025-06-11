import sqlite3

def init_db():
    conn = sqlite3.connect("appointments.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_time_available(date, time):
    conn = sqlite3.connect("appointments.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointments WHERE date=? AND time=?", (date, time))
    result = cur.fetchone()
    conn.close()
    return result is None

def save_appointment(name, date, time):
    conn = sqlite3.connect("appointments.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()
