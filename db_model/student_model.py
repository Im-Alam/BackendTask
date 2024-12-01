from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str = Field(..., description="City name where the student lives.")
    country: str = Field(..., description="Country where the student resides.")

class StudentSchema(BaseModel):
    name: str
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    address: Address

class StudentResponse(BaseModel):
    name: str
    age: int
    address: Address

class StudentList(BaseModel):
    name: str
    age: int

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None 
    address: Optional[Address] = None