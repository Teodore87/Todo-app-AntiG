# app.py - Main Flask application for the Todo list
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Todo
import os

# Initialize Flask app and configure SQLite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app context
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()
    # Ensure at least one list exists
    from models import TodoList
    if not TodoList.query.first():
        default_list = TodoList(name="General")
        db.session.add(default_list)
        db.session.commit()

# Home route redirected to default list or specific list
@app.route('/')
@app.route('/list/<int:list_id>')
def index(list_id=None):
    from models import TodoList
    
    # Get all lists for the sidebar
    all_lists = TodoList.query.all()
    
    # If no list_id provided, use the first available list
    if list_id is None:
        if all_lists:
            return redirect(url_for('index', list_id=all_lists[0].id))
        else:
            # This case should be handled by the db_create_all block above
            return "No lists available", 404
            
    current_list = TodoList.query.get_or_404(list_id)
    
    # Filter logic: all, active, completed
    filter_type = request.args.get('filter', 'all')
    
    query = Todo.query.filter_by(list_id=list_id).order_by(Todo.position.asc())
    
    if filter_type == 'active':
        todos = query.filter_by(completed=False).all()
    elif filter_type == 'completed':
        todos = query.filter_by(completed=True).all()
    else:
        todos = query.all()
        
    return render_template('index.html', 
                         todos=todos, 
                         lists=all_lists, 
                         current_list=current_list, 
                         current_filter=filter_type)

# Route to add a new todo
@app.route('/add/<int:list_id>', methods=['POST'])
def add_todo(list_id):
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        # Get the highest position in this list to append to the end
        max_pos = db.session.query(db.func.max(Todo.position)).filter_by(list_id=list_id).scalar() or 0
        new_todo = Todo(title=title, description=description, list_id=list_id, position=max_pos + 1)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index', list_id=list_id))

# Route to delete a todo by ID
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    list_id = todo.list_id
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index', list_id=list_id))

# Route to toggle the completion status of a todo
@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index', list_id=todo.list_id, filter=request.args.get('filter', 'all')))

# Route to edit the title and description of an existing todo
@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    if new_title:
        todo.title = new_title
        todo.description = new_description
        db.session.commit()
    return redirect(url_for('index', list_id=todo.list_id))

# Route to reorder todos by moving them up or down
@app.route('/move/<int:todo_id>/<direction>')
def move_todo(todo_id, direction):
    todo = Todo.query.get_or_404(todo_id)
    todos = Todo.query.filter_by(list_id=todo.list_id).order_by(Todo.position.asc()).all()
    idx = todos.index(todo)
    
    if direction == 'up' and idx > 0:
        other = todos[idx-1]
        todo.position, other.position = other.position, todo.position
    elif direction == 'down' and idx < len(todos) - 1:
        other = todos[idx+1]
        todo.position, other.position = other.position, todo.position
        
    db.session.commit()
    return redirect(url_for('index', list_id=todo.list_id))

# --- List Management Routes ---

@app.route('/list/add', methods=['POST'])
def add_list():
    name = request.form.get('name')
    if name:
        from models import TodoList
        new_list = TodoList(name=name)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('index', list_id=new_list.id))
    return redirect(url_for('index'))

@app.route('/list/delete/<int:list_id>', methods=['POST'])
def delete_list(list_id):
    from models import TodoList
    todo_list = TodoList.query.get_or_404(list_id)
    
    # Don't delete if it's the only list
    if TodoList.query.count() > 1:
        db.session.delete(todo_list)
        db.session.commit()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
