from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import uvicorn
import os

from database import SessionLocal, engine
from models import Student, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("student_form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    new_student = Student(name=name, age=age, email=email)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    students = db.query(Student).all()

    return templates.TemplateResponse(
        "student_data.html",
        {
            "request": request,
            "students": students,
            "message": f"Student '{name}' added successfully!"
        }
    )

    // this

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)