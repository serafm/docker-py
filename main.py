import json
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException, Response

app = FastAPI()


@dataclass
class Student:
    id: int
    name: str
    age: int
    semester: int

students: 'dict[int, Student]' = {}

with open("students.json", encoding="utf8") as file:
    students_raw = json.load(file)
    for student_raw in students_raw:
        student = Student(**student_raw)
        students[student.id] = student


@app.get("/")
def read_root() -> Response:
    return Response("The server is running. Welcome!")


@app.get("/students/{student_id}", response_model=Student)
def read_item(student_id: int) -> Student:
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]
