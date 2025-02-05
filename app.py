from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_migrate import Migrate


app = Flask(__name__)  # referencing the file "app.py"
# 3 slashes -> relative path , 4 slashes -> absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):  # set shakl el database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc))
    isCompleted = db.Column(db.Boolean, default=False)

    def __rep__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])  # route to the home page
def index():
    if request.method == 'POST':
        # get the content(task) from the form
        task_content = request.form['content']
        new_task = Todo(content=task_content)   # create a new task
        try:
            db.session.add(new_task)  # add to database
            db.session.commit()  # commit the changes
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')  # route to delete a task
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Couldn\'t delete the task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form.get(
            'content', task_to_update.content)
        task_to_update.isCompleted = 'isCompleted' in request.form
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Couldn\'t update the task'
    else:
        task = Todo.query.get_or_404(id)
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)  # set debug = true to show errors in the web page
