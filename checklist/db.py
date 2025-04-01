import sqlite3

def get_db():
    conn = sqlite3.connect("sqlite_db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserSelections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            ModuleItemID TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()

# Initialize the database
if __name__ == "__main__":
    init_db()
