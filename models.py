# models.py - Database models for the Todo application
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

class TodoList(db.Model):
    """
    TodoList model representing a collection of tasks.
    id: Unique identifier for the list
    name: Name of the list
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Relationship to tasks
    todos = db.relationship('Todo', backref='todo_list', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<TodoList {self.name}>'

class Todo(db.Model):
    """
    Todo model representing a single task.
    id: Unique identifier for the todo
    title: The text description of the task
    description: Extra information about the task
    completed: Boolean status of the task
    position: Integer used for ordering (Move Up/Down)
    list_id: Foreign key to associate with a TodoList
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'), nullable=False)

    # String representation for debugging
    def __repr__(self):
        return f'<Todo {self.title}>'
