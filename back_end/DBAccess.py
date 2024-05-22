import mariadb

class DBAccess:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
    
    def connect(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database 
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")  

    
    def get_location_id(self, complete_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM glpi_locations WHERE completename = '" + complete_name + "'")
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Error: Location not found for: " + complete_name)
            return None
        elif len(rows) > 1:
            print("Error: Multiple locations found for: " + complete_name)
            return None
        else:
            return rows[0][0]
    
    def get_page_counts(self, printer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT total_pages, color_pages, date FROM glpi_printerlogs WHERE printers_id = " + str(printer_id) + " ORDER BY date ASC")
        rows = cursor.fetchall()
        return rows
    
    def get_page_counts_since(self, printer_id, date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT total_pages, color_pages, date FROM glpi_printerlogs WHERE printers_id = " + str(printer_id) + " AND date >= '" + date + "' ORDER BY date ASC")
        rows = cursor.fetchall()
        return rows
    
    def get_page_counts_between(self, printer_id, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT total_pages, color_pages, date FROM glpi_printerlogs WHERE printers_id = " + str(printer_id) + " AND date >= '" + start_date + "' AND date <= '" + end_date + "' ORDER BY date ASC")
        rows = cursor.fetchall()
        return rows

    def get_printer_name(self, printer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM glpi_printers WHERE id = " + str(printer_id))
        rows = cursor.fetchall()
        return rows[0][0]
    
    def get_express_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM glpi_printers WHERE entities_id = 1 AND states_id NOT IN (14, 5, 9, 7, 16, 4, 18)")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    
    def get_location_name(self, printer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT completename FROM glpi_locations WHERE id = (SELECT locations_id FROM glpi_printers WHERE id = " + str(printer_id) + ")")
        rows = cursor.fetchall()
        return rows[0][0] 
    
    def get_printer_model(self, printer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM glpi_printermodels WHERE id = (SELECT printermodels_id FROM glpi_printers WHERE id = " + str(printer_id) + ")")
        rows = cursor.fetchall()
        return rows[0][0]
    

