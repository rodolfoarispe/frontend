from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# los 3/ indican ubicacion relativa. usar 4 para absoluta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class myApp():
    APP_TITLE = 'Prueba'
    APP_SUB_TITLE = 'this is a test we made with Bulma'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Task %r' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', myapp=myApp(), tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
    else:
        return render_template('update.html', myapp=myApp(), task=task)

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Error updating'


if __name__ == "__main__":
    app.run(debug=True)
