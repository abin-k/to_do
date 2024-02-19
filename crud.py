from sqlalchemy.orm import Session
from models import ToDoItem, User


#sign up and login

def create_user(db: Session, username: str, password: str):
    db_user = User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user

#to_do table

def create_todo(db: Session, title: str, description: str):
    db_todo = ToDoItem(title=title, description=description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int):    
    return db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ToDoItem).offset(skip).limit(limit).all()

def update_todo(db: Session, todo_id: int, title: str, description: str):
    todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    todo.title = title
    todo.description = description
    db.commit()
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    db.delete(todo)
    db.commit()




