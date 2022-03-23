from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    
    def __repr__(self):
        return "Task: {} ".format(self.id)
    

@app.route('/', methods=['POST', 'GET'])

def index():
    
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content = task_content)    
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
            
        except:
            return "There was an issue adding your task"
    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # for task in tasks:
            # print("{}, Task Content: {}, Task Date: {}".format(task, task.content, task.date_created))
        return render_template('index.html', tasks = tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    # task_to_delete: Todo.query.get_or_404(id)
    try:
        print("This works")
        db.session.execute("DELETE FROM Todo WHERE id = '{}'".format(id))
        print("This works too")
        db.session.commit()
        print("This works as well")
        return redirect('/')
    except:
        return "There was a problem deleting task from the database"
    

@app.route('/update_helper/<int:id>', methods=['POST', 'GET'])
def update_helper(id):          
    previous_content = Todo.query.get_or_404(id).content    
    return render_template('update.html', previous_content = previous_content, id = id)


@app.route('/update/', methods=['POST', 'GET'])
def update():
    
    
    
        new_content =  request.form['new_content']
        print(new_content)
        id = request.form["id"]
        print(id)
        
        try:
            db.session.execute("UPDATE Todo SET content = '{}' WHERE id = '{}'".format(new_content, int(id)))
            db.session.commit()
            return redirect("/")
        except:
            return "Error Updating Task"
    
       
        



if __name__ == "__main__":
    app.run(debug=True)

