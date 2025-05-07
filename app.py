from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

# Wczytanie danych z pliku
df = pd.read_csv('history.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts', methods=['POST'])
def charts():
    date_range = json.loads(request.form['date_range'])
    start_date = date_range['start_date']
    end_date = date_range['end_date']

    
    filtered_data = df.copy()
    filtered_data['date_time'] = pd.to_datetime(filtered_data['date_time'])
    filtered_data = filtered_data[(filtered_data['date_time'] >= start_date) & (filtered_data['date_time'] <= end_date)]

    chart_data = {
        'date_time': filtered_data['date_time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        'EURbuy': filtered_data['EURbuy'].tolist(),
        'EURsell': filtered_data['EURsell'].tolist(),
        'USDbuy': filtered_data['USDbuy'].tolist(),
        'USDsell': filtered_data['USDsell'].tolist(),
    }

    print(chart_data)  

    return json.dumps(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
