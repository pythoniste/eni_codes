import sqlite3

if __name__ == "__main__":
    from server import DB_NAME

    conn = sqlite3.connect(DB_NAME)

    c = conn.cursor()

    c.execute("CREATE TABLE sessions (peer text, start text, end text, nb int)")

    conn.commit()

    conn.close()
