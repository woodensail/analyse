__author__ = 'sail'
import sqlite3

db_filename = r'resource/chat.db'


def get_id( name=None):
    conn = sqlite3.connect(db_filename)
    result = conn.execute('SELECT usrid FROM chatdb WHERE name=? ORDER BY date DESC,time DESC LIMIT 1 ', (name,))
    return result.fetchone()[0]