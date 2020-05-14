import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jule@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ToDoList(db.Model): # define ToDo list model
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('ToDo', cascade='all,delete,delete-orphan', backref='list', lazy=True) # define relationship

class ToDo(db.Model):  # define ToDo model
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<ToDo {self.id}: {self.description}>'

@app.route('/lists', methods=['POST']) # route handler for CREATING ToDo lists
def create_todolist():
    error = False
    body={}
    try:  # try to commit changes to database
        new_name = request.form.get('name','')
        new = ToDoList(name=new_name) 
        db.session.add(new) 
        db.session.commit()  # add new ToDo list to database
        body['id'] = new.id
        body['name'] = new.name # save attributes of new ToDo list to dict (closing session will expire object)
    except: # if commit unsucessfull, rollback
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: # either way, close session
        db.session.close()
    
    if error:
        abort (400)
    else:
        return redirect(url_for('get_list_todos', list_id=body['id'])) # redirect to page showing new list

@app.route('/lists/<list_id>', methods=['DELETE']) # route handler for DELETING ToDo lists
def delete_todolist(list_id):
    error = False
    try:
        todolist = ToDoList.query.get(list_id)
        db.session.delete(todolist)
        db.session.commit() # delete ToDo list from database
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort (400)
    else:
        return jsonify({'success': True}) # return json notifying successful deletion -> necessary for method DELETE

@app.route('/todos', methods=['POST']) # route handler for CREATING ToDos
def create_todo():
    error = False
    body = {}  
    try:  # try to commit changes to database
        new_data = request.get_json()
        new = ToDo(description=new_data['description'], list_id=new_data['list_id'], completed=False) 
        db.session.add(new) 
        db.session.commit() # add new ToDo to database
        body['id'] = new.id
        body['completed'] = new.completed
        body['description'] = new.description
        body['list_id'] = new.list_id # save attributes of new ToDo to dict (closing session will expire object)
    except: # if commit unsucessfull, rollback
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally: # either way, close session
        db.session.close()
    
    if error:
        abort (400)
    else:
        return jsonify(body) # return json of attributes of new ToDo

@app.route('/todos/<todo_id>', methods=['DELETE']) # route handler for DELETING ToDos
def delete_todo(todo_id):
    error = False
    try:
        todo = ToDo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit() # delete ToDo from database
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort (400)
    else:
        return jsonify({'success': True}) # return json notifying successful deletion -> necessary for method DELETE
        
@app.route('/todos/<todo_id>/set-completed', methods=['POST']) # route handler for UPDATING ToDos
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = ToDo.query.get(todo_id)
        todo.completed = completed
        db.session.commit() # update ToDo (completed attribute) in database
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort (400)
    else:
        return jsonify({'success': True})
       

@app.route('/lists/<list_id>') # route handler for showing list with list_id
def get_list_todos(list_id):  
    if ToDoList.query.get(list_id) is None:
        return redirect(url_for('index'))
    else:
        return render_template('index.html',
            lists=ToDoList.query.order_by('id').all(),  # show all ToDo lists ordered by id (-> order of creation) and
            active_list=ToDoList.query.get(list_id),
            todos=ToDo.query.filter_by(list_id=list_id).order_by('id').all())  # all ToDos corresponding to list_id ordered by id (-> order of creation)        

@app.route('/')  # route handler for home page
def index():
    firstId = ToDoList.query.order_by('id').first().id
    return redirect(url_for('get_list_todos', list_id=firstId)) # redirect to page showing first list (order of creation)
