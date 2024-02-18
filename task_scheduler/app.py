from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    scheduled_time = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        scheduled_time = request.form['scheduled_time']
        new_task = Task(title=title, description=description, scheduled_time=scheduled_time)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.scheduled_time = request.form['scheduled_time']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', task=task)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)