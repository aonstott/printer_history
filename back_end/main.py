from .PrinterReport import PrinterReport
from .Credentials import Credentials
from .DBAccess import DBAccess
from .Plotter import Plotter
import matplotlib.pyplot as plt
import datetime

class Main:
    def __init__(self):
        credentials = Credentials()
        self.db_access = DBAccess(credentials.username, credentials.password, credentials.host, credentials.port, credentials.database)
        self.db_access.connect()
        self.printer_report = PrinterReport(self.db_access)
        self.plotter = Plotter(self.printer_report, self.db_access)
        self.printer_ids = self.db_access.get_express_ids()
    
    def get_sorted_printers(self):
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        self.data = self.printer_report.make_data(self.printer_ids, last_week.strftime("%Y-%m-%d"))
        self.sorted_printers = self.printer_report.sort_by_pg_count(self.data)
        return self.printer_report.make_table_data(self.sorted_printers)
    
    def get_pages_printed_since(self, date:str):
        self.data = self.printer_report.make_data(self.printer_ids, date)
        self.sorted_printers = self.printer_report.sort_by_pg_count(self.data)
        return self.printer_report.make_table_data(self.sorted_printers)
        
