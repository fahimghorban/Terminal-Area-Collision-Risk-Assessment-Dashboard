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
    pnmac_type = request.args.get('pnmac_type')

    file_path = os.path.join(DATA_DIR, airport, f'{pnmac_type}.csv')

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()
    entries = df['Total Entries into Risky Box'].tolist()
    durations = df['Total Risky CPA Duration (Seconds)'].tolist()

    return render_template('report.html',
                           airport=airport,
                           pnmac_type=pnmac_type.upper(),
                           dates=dates,
                           entries=entries,
                           durations=durations)

@app.route('/get_table', methods=['GET'])
def get_table():
    airport = request.args.get('airport')
    pnmac_type = request.args.get('pnmac_type')
    date_str = request.args.get('date')

    table_path = os.path.join(DATA_DIR, airport, f'{pnmac_type}_tables', f'{date_str}.csv')

    if not os.path.exists(table_path):
        return jsonify({'columns': [], 'rows': []})

    df = pd.read_csv(table_path)
    return jsonify({
        'columns': df.columns.tolist(),
        'rows': df.to_dict(orient='records')
    })

@app.route('/get_table_page')
def get_table_page():
    airport = request.args.get('airport')
    pnmac_type = request.args.get('pnmac_type')
    date_str = request.args.get('date')

    table_path = os.path.join(DATA_DIR, airport, f'{pnmac_type}_tables', f'{date_str}.csv')
    print(f"[DEBUG] Trying to read: {table_path}")  # ✅ Fixed indentation

    if not os.path.exists(table_path):
        return f"<h3>No data available for {date_str}</h3>", 404

    df = pd.read_csv(table_path)
    return render_template('table_page.html', date=date_str, table=df.to_html(index=False))

if __name__ == "__main__":
    app.run(debug=True)
