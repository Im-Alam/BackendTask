from pydantic import BaseModel, Field
from typing import List, Optional

class Student(BaseModel):
    name: str
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    address: Optional[dict] = {
        "city": "",
        "country": ""
    }
