import sqlite3
class JamDB:
    def __init__(self):
        conn = sqlite3.connect('jam.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS jams (
                    id INTEGER PRIMARY KEY,
                    jam_count INTEGER,
                    date DATE
                        )''')


    def add_jam(self, printer_id, jam_count, date):
        conn = sqlite3.connect('jam.db') 
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jams (printer_id, jam_count, date) VALUES (?, ?, ?)", (printer_id, jam_count, date))
        conn.commit()
        conn.close()
  
