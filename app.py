from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy #importing SQLAlchemy
from datetime import datetime #importing datetime module

app = Flask(__name__)  #creating a Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  #configuring the database URI
db = SQLAlchemy(app)  #creating a SQLAlchemy instance

class Todo(db.Model): #defining a model for the Todo table
    id = db.Column(db.Integer, primary_key=True)  #defining the id column as an integer primary key
    content = db.Column(db.String(200), nullable=False)  #defining the content
    date_created = db.Column(db.DateTime, default=lambda: datetime.utcnow())  #defining the date_created column with a default value of the current timestamp

    def __repr__(self):  #defining a string representation for the Todo model
        return '<Task %r>' % self.id  #returning a string representation of the task with its id


@app.route('/', methods=['GET', 'POST'])  #creating a route for the home page
def index():
    if request.method == 'POST': #checking if the request method is POST
        task_content = request.form['content']  #getting the content from the form
        new_task = Todo(content=task_content)  #creating a new task with the content

        try:  #trying to add the new task to the database
            db.session.add(new_task)  #adding the new task to the session
            db.session.commit()  #committing the changes to the database
            return redirect('/')  #redirecting to the home page
        except:
            return 'Error adding task to database'     

    else:  #if the request method is not POST
        tasks = Todo.query.order_by(Todo.date_created).all()  #querying all tasks from the database and ordering them by date_created
        return render_template('index.html', tasks=tasks)  #returning a rendered template


#CREATING A ROUTE FOR DELETING A TASK
@app.route('/delete/<int:id>')  
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  #getting the task to delete by id or returning a 404 error if not found
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting task'


#CREATING A ROUTE FOR UPDATING A TASK
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)  #getting the task to update by id or returning a 404 error if not found   

    if request.method == 'POST':
        task.content = request.form['content']  #updating the content of the task with the new content from the form
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating task' 
    else:
        return render_template('update.html', task=task)  #rendering the update template with the task to update


if __name__ == '__main__':  #checking if the script is run directly
    app.run(debug=True)  #running the app in debug mode

     