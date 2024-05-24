from flask import Flask, render_template, send_from_directory
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from back_end.main import Main


app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/') 
def index():
    # Call your Python program and get the output
    return render_template('home.html')

@app.route('/pages-week')
def pages_last_week():
    functions = Main()
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    output = functions.get_pages_printed_since(last_week.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day']
    s2 = "selected"

    return render_template('index.html', output=output, column_names=column_names, s2=s2)

@app.route('/pages-day')
def pages_last_day():
    functions = Main()
    last_day = datetime.datetime.now() - datetime.timedelta(days=1)
    output = functions.get_pages_printed_since(last_day.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 
    s1 = "selected"

    return render_template('index.html', output=output, column_names=column_names, s1=s1)

@app.route('/pages-month')
def pages_last_month():
    functions = Main()
    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    output = functions.get_pages_printed_since(last_month.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 
    s3 = "selected"

    return render_template('index.html', output=output, column_names=column_names, s3=s3)

@app.route('/pages-year')
def pages_last_year():
    functions = Main()
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    output = functions.get_pages_printed_since(last_year.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 
    s4 = "selected"
    return render_template('index.html', output=output, column_names=column_names, s4=s4)

@app.route('/printer/<printer_name>')
def printer_detail(printer_name):
    # Find the printer data by name
    functions = Main()
    printer_names = functions.get_printer_names()

    photos = {
        "HP Color LaserJet CP4025":"hp_cp4025.jpg",
        "KM Bizhub C3100P":"c3100p.jpg",
        "HP Color LaserJet CP4525":"hp_cp4525.jpg",
        "KM Bizhub C3350i": "bizhub_c3350i.jpg",
        "KM Bizhub C3351": "bizhub_c335i.jpg",
        "KM Bizhub C458": "kmc458.jpg",
        "HP LaserJet P3005": "hp_p3005.jpg",
        "HP LaserJet P3015": "hp_p3015.jpg",
        "HP LaserJet P4014": "hp_p4014.jpg",
        "HP LaserJet P4015": "hp_p4014.jpg",
        "HP LaserJet 4240": "hp_4240.jpg",
        "HP LaserJet 4250": "hp_4240.jpg",
        "HP Color LaserJet M750": "hp_m750.jpg",
        "HP Color LaserJet M751": "hp_m751.jpg",
        "HP LaserJet P3010 Series": "hp_p3015.jpg",
        "HP LaserJet 2430": "hp_2430.jpg",
    }

    printer = next((p for p in printer_names if p == printer_name), None)
    if printer:
        printer_model = functions.get_printer_model(printer)
        location = functions.get_printer_location(printer)
        if printer_model in photos:
            photo = photos[printer_model]
        return render_template('printer.html', printer=printer, printer_model=printer_model, photo=photo, location=location)
    else:
        return "Printer not found", 404
    
@app.route('/jams')
def jams():
    functions = Main()
    output = functions.get_printer_jams()
    column_names = ['Rank', 'Printer Name', 'Location', 'Jam Count']
    return render_template('index.html', output=output, column_names=column_names)

if __name__ == '__main__':
    app.run(debug=True)
