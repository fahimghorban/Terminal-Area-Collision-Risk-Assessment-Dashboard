from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
DATA_DIR = 'data'

@app.route('/')
def index():
    airports = os.listdir(DATA_DIR)
    return render_template('index.html', airports=airports)

@app.route('/report')
def report():
    airport = request.args.get('airport')
    pnmac_type = request.args.get('pnmac_type')  # NEW LINE

    file_path = os.path.join(DATA_DIR, airport, f'{pnmac_type}.csv')  # dynamic file

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()
    entries = df['Total Entries into Risky Box'].tolist()
    durations = df['Total Risky CPA Duration (Seconds)'].tolist()

    return render_template('report.html',
                           airport=airport,
                           pnmac_type=pnmac_type.upper(),  # Pass to HTML
                           dates=dates,
                           entries=entries,
                           durations=durations)

@app.route('/get_table', methods=['GET'])
def get_table():
    airport = request.args.get('airport')
    pnmac_type = request.args.get('pnmac_type')
    date_str = request.args.get('date')  # e.g., "2024-04-16"

    table_path = os.path.join(DATA_DIR, airport, f'{pnmac_type}_tables', f'{date_str}.csv')

    if not os.path.exists(table_path):
        return jsonify({'columns': [], 'rows': []})

    df = pd.read_csv(table_path)
    return jsonify({
        'columns': df.columns.tolist(),
        'rows': df.to_dict(orient='records')
    })

if __name__ == "__main__":
    app.run(debug=True)
