"""
Web application for visualizing currency exchange rates based on data from a CSV file.
Allows generating EUR and USD rate charts for a selected date range.
Author: Adrian Lesniak

Menu options:
- Select a date range and generate charts
- Add a new record to the history
- Export filtered data to CSV/Excel
- Filter and sort data by various criteria
- All operations are logged, and errors are saved to a log file

"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
import pandas as pd
import json
import logging
import os
from datetime import datetime
import io
import tempfile
import shutil

# Logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'  # Wymagane do sesji Flask

CSV_FILE = 'history.csv'

def load_data():
    """Loads data from the CSV file and returns a DataFrame."""
    try:
        df = pd.read_csv(CSV_FILE)
        df['date_time'] = pd.to_datetime(df['date_time'])
        return df
    except Exception as e:
        logging.error(f'Error loading data: {e}')
        return pd.DataFrame()

def save_data(new_row):
    """Saves a new record to the CSV file."""
    try:
        df = load_data()
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        logging.info('Added new record to history.')
        return True
    except Exception as e:
        logging.error(f'Error saving data: {e}')
        return False

def filter_and_sort_data(df, filters=None, sort_by=None, sort_order='asc'):
    """Filters and sorts data based on provided criteria."""
    try:
        filtered_df = df.copy()
        
        if filters:
            # Date range filter
            if 'start_date' in filters and filters['start_date']:
                start_dt = pd.to_datetime(filters['start_date'])
                filtered_df = filtered_df[filtered_df['date_time'] >= start_dt]
            
            if 'end_date' in filters and filters['end_date']:
                end_dt = pd.to_datetime(filters['end_date'])
                filtered_df = filtered_df[filtered_df['date_time'] <= end_dt]
            
            # Currency filters
            if 'currency' in filters and filters['currency']:
                currency = filters['currency'].upper()
                if currency == 'EUR':
                    filtered_df = filtered_df[['date_time', 'EURbuy', 'EURsell']]
                elif currency == 'USD':
                    filtered_df = filtered_df[['date_time', 'USDbuy', 'USDsell']]
            
            # Value range filters
            if 'min_value' in filters and filters['min_value']:
                min_val = float(filters['min_value'])
                for col in ['EURbuy', 'EURsell', 'USDbuy', 'USDsell']:
                    if col in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df[col] >= min_val]
            
            if 'max_value' in filters and filters['max_value']:
                max_val = float(filters['max_value'])
                for col in ['EURbuy', 'EURsell', 'USDbuy', 'USDsell']:
                    if col in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df[col] <= max_val]
        
        # Sorting
        if sort_by and sort_by in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))
        
        return filtered_df
    except Exception as e:
        logging.error(f'Error in filter_and_sort_data: {e}')
        return df

@app.route('/')
def index():
    """Main page with menu and instructions."""
    return render_template('index.html')

@app.route('/charts', methods=['POST'])
def charts():
    """Returns chart data for the selected date range."""
    try:
        data = json.loads(request.form['date_range'])
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Additional filters
        filters = {
            'start_date': start_date,
            'end_date': end_date,
            'currency': data.get('currency'),
            'min_value': data.get('min_value'),
            'max_value': data.get('max_value')
        }
        
        sort_by = data.get('sort_by')
        sort_order = data.get('sort_order', 'asc')

        df = load_data()
        if df.empty:
            return jsonify({'error': 'No data available!'}), 500

        # Apply filters and sorting
        filtered_data = filter_and_sort_data(df, filters, sort_by, sort_order)

        if filtered_data.empty:
            return jsonify({'error': 'No data matches the selected criteria!'}), 400

        # Prepare chart data
        if not filtered_data.empty:
            date_time_series = pd.Series(filtered_data['date_time'])
            date_time_series = pd.to_datetime(date_time_series, errors='coerce')
            date_time_list = date_time_series.dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
        else:
            date_time_list = []
            
        chart_data = {
            'date_time': date_time_list,
            'EURbuy': filtered_data['EURbuy'].tolist() if not filtered_data.empty else [],
            'EURsell': filtered_data['EURsell'].tolist() if not filtered_data.empty else [],
            'USDbuy': filtered_data['USDbuy'].tolist() if not filtered_data.empty else [],
            'USDsell': filtered_data['USDsell'].tolist() if not filtered_data.empty else [],
        }
        logging.info(f'Generated chart data for range: {start_date} - {end_date}')
        return jsonify(chart_data)
    except Exception as e:
        logging.error(f'Error in charts: {e}')
        return jsonify({'error': 'An error occurred while generating charts.'}), 500

@app.route('/export', methods=['POST'])
def export_data():
    """Exports filtered data to CSV or Excel format."""
    try:
        data = request.get_json()
        export_format = data.get('format', 'csv').lower()
        filters = data.get('filters', {})
        sort_by = data.get('sort_by')
        sort_order = data.get('sort_order', 'asc')

        df = load_data()
        if df.empty:
            return jsonify({'error': 'No data available!'}), 500

        # Apply filters and sorting
        filtered_data = filter_and_sort_data(df, filters, sort_by, sort_order)

        if filtered_data.empty:
            return jsonify({'error': 'No data matches the selected criteria!'}), 400

        # Create export file
        if export_format == 'excel':
            # Export to Excel using temporary file
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
                with pd.ExcelWriter(tmp_file.name, engine='openpyxl') as writer:
                    filtered_data.to_excel(writer, sheet_name='Currency_Data', index=False)
            
            filename = f'currency_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            # Export to CSV
            output = io.StringIO()
            filtered_data.to_csv(output, index=False)
            output.seek(0)
            
            filename = f'currency_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                as_attachment=True,
                download_name=filename,
                mimetype='text/csv'
            )
            
    except Exception as e:
        logging.error(f'Error in export_data: {e}')
        return jsonify({'error': 'An error occurred while exporting data.'}), 500

@app.route('/filter', methods=['POST'])
def filter_data():
    """Returns filtered data for display in table format."""
    try:
        data = request.get_json()
        filters = data.get('filters', {})
        sort_by = data.get('sort_by')
        sort_order = data.get('sort_order', 'asc')
        page = data.get('page', 1)
        per_page = data.get('per_page', 50)

        df = load_data()
        if df.empty:
            return jsonify({'error': 'No data available!'}), 500

        # Apply filters and sorting
        filtered_data = filter_and_sort_data(df, filters, sort_by, sort_order)

        if filtered_data.empty:
            return jsonify({'error': 'No data matches the selected criteria!'}), 400

        # Pagination
        total_records = len(filtered_data)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_data = filtered_data.iloc[start_idx:end_idx]

        # Convert to list of dictionaries for JSON response
        records = []
        for _, row in paginated_data.iterrows():
            record = {
                'date_time': row['date_time'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['date_time']) else '',
                'EURbuy': float(row['EURbuy']) if pd.notna(row['EURbuy']) else 0,
                'EURsell': float(row['EURsell']) if pd.notna(row['EURsell']) else 0,
                'USDbuy': float(row['USDbuy']) if pd.notna(row['USDbuy']) else 0,
                'USDsell': float(row['USDsell']) if pd.notna(row['USDsell']) else 0
            }
            records.append(record)

        response_data = {
            'records': records,
            'total_records': total_records,
            'current_page': page,
            'per_page': per_page,
            'total_pages': (total_records + per_page - 1) // per_page
        }

        logging.info(f'Filtered data returned: {len(records)} records')
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f'Error in filter_data: {e}')
        return jsonify({'error': 'An error occurred while filtering data.'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple admin login form and logic."""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        # Prosty login: admin/admin123
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return jsonify({'success': 'Logged in!'}), 200
        else:
            return jsonify({'error': 'Invalid credentials!'}), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_record():
    """Adds a new record to the history based on form data. Only for logged-in admin."""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized! Please log in as admin.'}), 401
    try:
        data = request.get_json()
        # Field validation
        required_fields = ['date_time', 'EURbuy', 'EURsell', 'USDbuy', 'USDsell']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields!'}), 400
        # Date conversion
        try:
            data['date_time'] = pd.to_datetime(data['date_time'])
        except Exception:
            return jsonify({'error': 'Invalid date format!'}), 400
        # Save to file
        data['date_time'] = data['date_time'].strftime('%Y-%m-%d %H:%M:%S')
        if save_data(data):
            return jsonify({'success': 'Record added!'}), 200
        else:
            return jsonify({'error': 'Save error!'}), 500
    except Exception as e:
        logging.error(f'Error in add_record: {e}')
        return jsonify({'error': 'An error occurred while adding the record.'}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Returns the last N added records (change history)."""
    try:
        N = int(request.args.get('n', 10))
        df = load_data()
        if df.empty:
            return jsonify({'error': 'No data available!'}), 500
        last_records = df.sort_values(by='date_time', ascending=False).head(N)
        records = last_records.to_dict(orient='records')
        return jsonify({'history': records}), 200
    except Exception as e:
        logging.error(f'Error in get_history: {e}')
        return jsonify({'error': 'An error occurred while fetching history.'}), 500

@app.route('/api/rates', methods=['GET'])
def api_rates():
    """Public REST API: returns filtered rates as JSON (with pagination and sorting)."""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        currency = request.args.get('currency')
        min_value = request.args.get('min_value')
        max_value = request.args.get('max_value')
        sort_by = request.args.get('sort_by')
        sort_order = request.args.get('sort_order', 'asc')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        filters = {
            'start_date': start_date,
            'end_date': end_date,
            'currency': currency,
            'min_value': min_value,
            'max_value': max_value
        }
        df = load_data()
        if df.empty:
            return jsonify({'error': 'No data available!'}), 500
        filtered_data = filter_and_sort_data(df, filters, sort_by, sort_order)
        total_records = len(filtered_data)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_data = filtered_data.iloc[start_idx:end_idx]
        records = paginated_data.to_dict(orient='records')
        return jsonify({
            'records': records,
            'total_records': total_records,
            'current_page': page,
            'per_page': per_page,
            'total_pages': (total_records + per_page - 1) // per_page
        }), 200
    except Exception as e:
        logging.error(f'Error in api_rates: {e}')
        return jsonify({'error': 'An error occurred while fetching rates.'}), 500

# --- Data versioning/undo ---
BACKUP_FILE = 'history_backup.csv'

def backup_data():
    try:
        shutil.copyfile(CSV_FILE, BACKUP_FILE)
        logging.info('Backup created.')
    except Exception as e:
        logging.error(f'Error creating backup: {e}')

def restore_backup():
    try:
        if os.path.exists(BACKUP_FILE):
            shutil.copyfile(BACKUP_FILE, CSV_FILE)
            logging.info('Backup restored.')
            return True
        return False
    except Exception as e:
        logging.error(f'Error restoring backup: {e}')
        return False

@app.route('/undo', methods=['POST'])
def undo_last_change():
    """Restores the last backup of the data file (undo last change)."""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized! Please log in as admin.'}), 401
    try:
        if restore_backup():
            return jsonify({'success': 'Last change undone (backup restored).'}), 200
        else:
            return jsonify({'error': 'No backup available!'}), 400
    except Exception as e:
        logging.error(f'Error in undo_last_change: {e}')
        return jsonify({'error': 'An error occurred while restoring backup.'}), 500

# --- Backup before every add ---
@app.before_request
def backup_before_add():
    if request.endpoint == 'add_record' and request.method == 'POST':
        backup_data()

if __name__ == '__main__':
    app.run(debug=True)
