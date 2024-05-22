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
    functions = Main()
    output = functions.get_sorted_printers()  # Replace this with your Python function that generates output
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day']

    return render_template('index.html', output=output, column_names=column_names)

@app.route('/pages-week')
def pages_last_week():
    functions = Main()
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    output = functions.get_pages_printed_since(last_week.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 

    return render_template('index.html', output=output, column_names=column_names)

@app.route('/pages-day')
def pages_last_day():
    functions = Main()
    last_day = datetime.datetime.now() - datetime.timedelta(days=1)
    output = functions.get_pages_printed_since(last_day.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 

    return render_template('index.html', output=output, column_names=column_names)

@app.route('/pages-month')
def pages_last_month():
    functions = Main()
    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    output = functions.get_pages_printed_since(last_month.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 

    return render_template('index.html', output=output, column_names=column_names)

@app.route('/pages-year')
def pages_last_year():
    functions = Main()
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    output = functions.get_pages_printed_since(last_year.strftime("%Y-%m-%d"))
    column_names = ['Rank', 'Printer Name', 'Location', 'Pages Per Day'] 

    return render_template('index.html', output=output, column_names=column_names)

if __name__ == '__main__':
    app.run(debug=True)
