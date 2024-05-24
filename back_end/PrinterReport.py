from .Credentials import Credentials
from .DBAccess import DBAccess
import matplotlib.pyplot as plt
import datetime
import queue


class PrinterReport:
    def __init__(self, db_access:DBAccess):
        self.db_access = db_access

    def get_page_count(self, printer_id:int, date:str = "2021-01-01"):
        page_counts:list = self.db_access.get_page_counts_since(printer_id, date)
        return page_counts #returns a list of tuples from the database
    
    #I don't even remember how this works but it does
    def make_data(self, printer_ids:list, date:str = "2021-01-01"):
        data:dict[list[tuple]] = {}
        for printer_id in printer_ids:
            rows = self.get_page_count(printer_id, date)
            for row in rows:
                point = (row[2], row[0], row[1])
                if printer_id in data:
                    data[printer_id].append(point)
                else:
                    data[printer_id] = [point]

        return data
    
    def make_jam_data(self, printer_ids:list):
        data = {}
        for printer_id in printer_ids:
            jams_num = self.db_access.get_jam_count(printer_id)
            data[printer_id] = jams_num
        #sort by highest jam count
        data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
        return data
    
    def make_jams_table(self, data:dict):
        table_data = []
        rank = 1
        for printer in data:
            name = self.db_access.get_printer_name(printer)
            location = self.db_access.get_printer_location(printer)
            table_data.append((rank, name, location, data[printer]))
            rank += 1
        
        return table_data
    



    #This is horrible and convoluted I am terrible at programming
    def sort_by_pg_count(self, data:dict[list[tuple]]):
        pq = queue.PriorityQueue()
        printer_ids = self.db_access.get_express_ids()
        for printer in printer_ids:
            if printer not in data:
                continue
            increase = self.get_increase(data, printer)
            if len(increase) == 0:
                pq.put((0, printer))
                continue
            start_day = data[printer][0][0]
            end_day = data[printer][-1][0]
            num_days = (end_day - start_day).days
            avg = sum(increase)/num_days
            pq.put((avg, printer))

        #make array of printers ordered by average increase
        top_printers = []
        while not pq.empty():
            top_printers.append(pq.get())

        return top_printers
    
    def make_table_data(self, top_printers:list):
        table_data = []
        rank = len(top_printers)
        for printer in top_printers:
            name = self.db_access.get_printer_name(printer[1])
            location = self.db_access.get_printer_location(printer[1])
            table_data.append((rank, name, location, round(printer[0], 1)))
            rank -= 1
        
        #Reverse the list so that the top printer is at the top
        table_data.reverse()

        return table_data



    def get_increase(self, data:dict[list[tuple]], printer_id:int):
        #filter out duplicate dates
        daily_increase = [data[printer_id][i+1][1] - data[printer_id][i][1] for i in range(len(data[printer_id])-1)]
        
        return daily_increase
    
    def get_dates(self, data:dict[list[tuple]], printer_id:int):
        dates = [entry[0] for entry in data[printer_id][1:]]
        return dates
    
    def plot_data(self, data:dict[list[tuple]], printer_ids:list):
        for printer_id in printer_ids:
            printer_name = self.db_access.get_printer_name(printer_id)
            daily_increase = self.get_increase(data, printer_id)
            dates = self.get_dates(data, printer_id)
            location = self.db_access.get_printer_location(printer_id)
            plt.plot(dates, daily_increase, label=location, marker='o')
        
        plt.xlabel('Date')
        plt.ylabel('Pages Printed')
        plt.title('Pages Printed by Day')
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()
    
    def generate_report(self, data:dict[list[tuple]]):
        printers_list = self.sort_by_pg_count(data)
        top_5 = printers_list[-5:]
        bottom_5 = printers_list[:5]

        #get time in mm/dd/yyyy format
        now = datetime.datetime.now()
        date = now.strftime("%m-%d-%Y")
        #create file with todays date as the name
        with open("logs/" + date + ".txt", "w") as file:
            file.write("Top 5 Printers\n")
            for printer in top_5:
                name = self.db_access.get_printer_name(printer[1])
                location = self.db_access.get_printer_location(printer[1])
                file.write(name + " at " + location + " with an average increase of " + str(printer[0]) + " pages per day\n")
            
            file.write("\nBottom 5 Printers\n")
            for printer in bottom_5:
                name = self.db_access.get_printer_name(printer[1])
                location = self.db_access.get_printer_location(printer[1])
                file.write(name + " at " + location + " with an average increase of " + str(printer[0]) + " pages per day\n")

            file.close()

    
    def top_x_printers(self, data:dict[list[tuple]], x:int):
        printers_list = self.sort_by_pg_count(data)
        top_x = printers_list[-x:]
        return top_x
    
    def bottom_x_printers(self, data:dict[list[tuple]], x:int):
        printers_list = self.sort_by_pg_count(data)
        bottom_x = printers_list[:x]
        return bottom_x
        
    





