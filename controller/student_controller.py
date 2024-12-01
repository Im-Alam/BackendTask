from fastapi import HTTPException, Query, Path
from typing import Optional
from bson import ObjectId
from db.connect_db import client

from db_model.student_model import StudentSchema

students_db = client["students_db"]
students_collection = students_db["students"]

# global id_tracker = 

# Utility function to convert ObjectId to string
def student_serializer(student) -> dict:
    return {
        "name": student["name"],
        "age": student["age"],
        "address": student["address"],
    }



async def create_student(student_data: dict) -> dict:
    try:
        result = await students_collection.insert_one(student_data)
        return {"inserted_id": result.inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in inserting operation")



async def list_students(country: Optional[str], age: Optional[int]) -> dict:
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students_cursor = students_collection.find(query)
    students = await students_cursor.to_list(length=100)

    return {"data": [{"name":student["name"], "age":student["age"]} for student in students]}



async def fetch_student_by_id(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_serializer(student)



async def update_student(id: str, student_update: StudentSchema) -> None:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_data = student_update.dict(exclude_unset=True, exclude_none=True)
    await students_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": updated_data}
    )



async def delete_student(id: str) -> None:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await students_collection.delete_one({"_id": ObjectId(id)})


if __name__ == "__main__":
    data = {
            "name": "John Doe",
            "age": 25,
            "address": {
                "city": "New York",
                "country": "USA"
                }
            }
    
    create_student(data)