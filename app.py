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

# Home route with filtering logic
@app.route('/')
def index():
    # Filter logic: all, active, completed
    filter_type = request.args.get('filter', 'all')
    
    query = Todo.query.order_by(Todo.position.asc())
    
    if filter_type == 'active':
        todos = query.filter_by(completed=False).all()
    elif filter_type == 'completed':
        todos = query.filter_by(completed=True).all()
    else:
        todos = query.all()
        
    return render_template('index.html', todos=todos, current_filter=filter_type)

# Route to add a new todo
@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    if title:
        # Get the highest position to append to the end
        max_pos = db.session.query(db.func.max(Todo.position)).scalar() or 0
        new_todo = Todo(title=title, position=max_pos + 1)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

# Route to delete a todo by ID
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Route to toggle the completion status of a todo
@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index', filter=request.args.get('filter', 'all')))

# Route to edit the title of an existing todo
@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    new_title = request.form.get('title')
    if new_title:
        todo.title = new_title
        db.session.commit()
    return redirect(url_for('index'))

# Route to reorder todos by moving them up or down
@app.route('/move/<int:todo_id>/<direction>')
def move_todo(todo_id, direction):
    todo = Todo.query.get_or_404(todo_id)
    todos = Todo.query.order_by(Todo.position.asc()).all()
    idx = todos.index(todo)
    
    if direction == 'up' and idx > 0:
        other = todos[idx-1]
        todo.position, other.position = other.position, todo.position
    elif direction == 'down' and idx < len(todos) - 1:
        other = todos[idx+1]
        todo.position, other.position = other.position, todo.position
        
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
