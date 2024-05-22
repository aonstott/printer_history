import matplotlib.pyplot as plt
import datetime
from .PrinterReport import PrinterReport
from .DBAccess import DBAccess

class Plotter:
    def __init__(self, printer_report:PrinterReport, db_access:DBAccess):
        self.printer_report = printer_report
        self.db_access = db_access


    def plot_data(self, data:dict[list[tuple]], printer_ids:list):
        for printer_id in printer_ids:
            daily_increase = self.printer_report.get_increase(data, printer_id)
            dates = self.printer_report.get_dates(data, printer_id)
            location = self.db_access.get_location_name(printer_id)
            plt.plot(dates, daily_increase, label=location, marker='o')
        
        plt.xlabel('Date')
        plt.ylabel('Pages Printed')
        plt.title('Pages Printed by Day')
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()