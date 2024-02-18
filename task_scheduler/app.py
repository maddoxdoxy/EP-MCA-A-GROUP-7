from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
tasks = []

@app.route('/schedule', methods=['POST'])
def schedule_task():
    task = request.form["task"]
    reminder = request.form['reminder']
    reminder_datetime = datetime.strptime(reminder, '%Y-%m-%dT%H:%M')
    tasks.append({'task': task, 'reminder': reminder_datetime})
    return redirect(url_for('index'))

@app.route('/')
def index():
    datetime_now = datetime.now()
    return render_template('index.html', datetime_now=datetime_now)

@app.route('/tasks')
def view_tasks():
    return render_template('tasks.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)