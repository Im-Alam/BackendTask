from fastapi import HTTPException
from typing import Optional
from db.connect_db import students_collection

from db_model.student_model import StudentSchema


# Utility function to convert ObjectId to string
def student_serializer(student) -> dict:
    return {
        "name": student["name"],
        "age": student["age"],
        "address": student["address"],
    }

async def isValidId(id:str):
    if len(id)==6 and id.isdigit():
        return True
    else:
        return False


async def create_student(student_data: dict) -> dict:
    try:
        result = await students_collection.insert_one(student_data)
        if result.inserted_id:
            return {"id": student_data['id']}
    except Exception as e:
        print(e)
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
    if not isValidId(id):
        raise HTTPException(status_code=400, detail="Invalid student ID, ID is 6 digit-numeric")

    student = await students_collection.find_one({"id": id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_serializer(student)



async def update_student(id: str, student_update: StudentSchema) -> None:
    if not isValidId(id):
        raise HTTPException(status_code=400, detail="Invalid student ID, ID is 6 digit-numeric")

    student = await students_collection.find_one({"id": id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_data = student_update.dict(exclude_unset=True, exclude_none=True)
    await students_collection.update_one(
        {"id": id}, {"$set": updated_data}
    )



async def delete_student(id: str) -> None:
    if not isValidId(id):
        raise HTTPException(status_code=400, detail="Invalid student ID, ID is 6 digit-numeric")

    student = await students_collection.find_one({"id": id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await students_collection.delete_one({"id": id})


if __name__ == "__main__":
    data = {
            "id":"123456",
            "name": "John Doe",
            "age": 25,
            "address": {
                "city": "New York",
                "country": "USA"
                }
            }
    
    create_student(data)