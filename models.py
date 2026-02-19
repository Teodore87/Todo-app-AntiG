# models.py - Database models for the Todo application
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

class Todo(db.Model):
    """
    Todo model representing a single task.
    id: Unique identifier for the todo
    title: The text description of the task
    completed: Boolean status of the task
    position: Integer used for ordering (Move Up/Down)
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)

    # String representation for debugging
    def __repr__(self):
        return f'<Todo {self.title}>'
