import sqlite3
from .DBAccess import DBAccess
from .Credentials import Credentials
import datetime

class JamDB:
    def __init__(self, db_access:DBAccess):
        self.conn = sqlite3.connect('jam.db')
        cursor = self.conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS jams (
                    printer_id INTEGER,
                    jam_count INTEGER,
                    date DATE
                        )''')
        self.db_access = db_access
        db_access.connect()
        self.connect


        
    def connect(self):
        self.conn = sqlite3.connect('jam.db')
        self.cursor = self.conn.cursor() 


    def add_jam(self, printer_id, jam_count, date):
        conn = sqlite3.connect('jam.db') 
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jams (printer_id, jam_count, date) VALUES (?, ?, ?)", (printer_id, jam_count, date))
        conn.commit()
        conn.close()
    
    def get_jam_count_on_day(self, printer_id, date):
        cursor = self.conn.cursor() 
        cursor.execute("SELECT jam_count FROM jams WHERE printer_id = ? AND date = ?", (printer_id, date))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][0]
  
    def fill_initial_data(self):
        printer_ids = self.db_access.get_jam_printer_ids()
        todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
        for printer_id in printer_ids:
            if self.get_jam_count_on_day(printer_id, todays_date) == None:
                jam_count = self.db_access.get_jam_count(printer_id)
                self.add_jam(printer_id, jam_count, todays_date)
 

    def get_jams_for_printer(self, printer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT jam_count, date FROM jams WHERE printer_id = ?", (printer_id,))
        rows = cursor.fetchall()
        return rows

jam_db = JamDB(DBAccess(Credentials().username, Credentials().password, Credentials().host, Credentials().port, Credentials().database))
jam_db.fill_initial_data()




