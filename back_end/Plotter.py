import matplotlib.pyplot as plt
import datetime
from .PrinterReport import PrinterReport
from .DBAccess import DBAccess
from .jam_db import JamDB
from .Credentials import Credentials
import io
import base64
import numpy as np


class Plotter:
    def __init__(self):
        credentials = Credentials()
        self.db_access = DBAccess(credentials.username, credentials.password, credentials.host, credentials.port, credentials.database)
        self.jam_db = JamDB(self.db_access)
        self.printer_report = PrinterReport(self.db_access)


    def plot_data(self, data:dict[list[tuple]], printer_ids:list):
        for printer_id in printer_ids:
            daily_increase = self.printer_report.get_increase(data, printer_id)
            dates = self.printer_report.get_dates(data, printer_id)
            location = self.db_access.get_printer_location(printer_id)
            plt.plot(dates, daily_increase, label=location, marker='o')
        
        plt.xlabel('Date')
        plt.ylabel('Pages Printed')
        plt.title('Pages Printed by Day')
        plt.xticks(rotation=20)
        plt.legend()
        plt.show()

    def plot_jams(self, printer_id:int):
        jam_data = self.jam_db.get_jams_for_printer(printer_id)
        jam_count = [entry[0] for entry in jam_data]
        dates = [entry[1] for entry in jam_data]
        #sort by date
        jam_count = [x for _,x in sorted(zip(dates, jam_count))]
        dates = sorted(dates)
        plt.plot(dates, jam_count, label="Jams", marker='o')
        plt.xlabel('Date')
        plt.ylabel('Jams')
        plt.title('Jams by Day')
        plt.xticks(rotation=20)
        plt.legend()
        y_ticks = np.arange(np.floor(np.min(jam_count)), np.ceil(np.max(jam_count))+1)
        plt.yticks(y_ticks)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return base64.b64encode(buffer.read()).decode('utf-8')
        


####TESTING#####



