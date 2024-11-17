from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Настройки подключения к базе данных
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'appointment_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM appointments')
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', appointments=appointments)

@app.route('/add', methods=['POST'])
def add_appointment():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO appointments (name, date, time) VALUES (%s, %s, %s)',
                   (name, date, time))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
