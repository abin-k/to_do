from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, database, models

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
models.Base.metadata.create_all(bind=database.engine) 


#sign up and login

@app.post("/signup/")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, username)
    if existing_user:
        return {"message": "Username already exists"}
    else:
        return crud.create_user(db=db, username=username, password=password)

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username, password)
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
           
#to_do table

@app.post("/todos/")
def create_todo(title: str, description: str, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, title=title, description=description)

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.get("/todos/")
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_todos(db=db, skip=skip, limit=limit)

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, description: str, db: Session = Depends(get_db)):
    return crud.update_todo(db=db, todo_id=todo_id, title=title, description=description)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db=db, todo_id=todo_id)



