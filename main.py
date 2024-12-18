from fastapi import FastAPI, Depends, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional


from db_model.student_model import StudentSchema, StudentResponse, StudentUpdate
from controller.student_controller import (
    create_student,
    list_students,
    fetch_student_by_id,
    update_student,
    delete_student,
)
from nanoid import generate

app = FastAPI(version="1.0.0", title="Backend intern hiring task")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', summary="Home page")
async def dashboard():
    return "Backend intern task home page."


@app.post("/students", response_model=dict, status_code=201, summary="Create student")
async def create_student_api(student: StudentSchema):
    # print(type(student))
    student_data = {
        "id": generate(alphabet = '123456789', size=6),
        "name": student.name,
        "age": student.age,
        "address": student.address.model_dump(),
    }
    result = await create_student(student_data)

    return result


@app.get("/students", response_model=dict, summary="List students")
async def list_students_api(
    country: Optional[str] = Query(None),
    age: Optional[int] = Query(None),
):
    return await list_students(country, age)


@app.get("/students/{id}", response_model=StudentResponse)
async def fetch_student_api(id: str = Path(...)):
    return await fetch_student_by_id(id)


@app.patch("/students/{id}", status_code=204)
async def update_student_api(
    id: str = Path(...), student_update: StudentUpdate = Depends()):
    await update_student(id, student_update)
    return {}


@app.delete("/students/{id}", status_code=200)
async def delete_student_api(id: str = Path(...)):
    await delete_student(id)
    return {}
