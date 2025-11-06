import sqlite3, os, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = BASE / "hotel_reservas.db"

def connect():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS room_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT UNIQUE NOT NULL,
        room_type_id INTEGER NOT NULL,
        FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        total_price REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
    );
    """)

    cur.execute("INSERT OR IGNORE INTO room_types (id, code, name, price) VALUES (1,'simple','Simple', 80.0)")
    cur.execute("INSERT OR IGNORE INTO room_types (id, code, name, price) VALUES (2,'doble','Doble', 120.0)")
    cur.execute("INSERT OR IGNORE INTO room_types (id, code, name, price) VALUES (3,'suite','Suite', 220.0)")

    for i in range(101, 111):
        cur.execute("INSERT OR IGNORE INTO rooms (room_number, room_type_id) VALUES (?,?)",
                    (f"{i}", 1 if i < 105 else (2 if i < 108 else 3)))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB inicializada en:", DB_PATH)
