from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ['*'],
)

@app.post("/students")
async def create_student():
    return {"Hello": "World"}


@app.get("/students")
async def list_student_with_condition():
    return {"Hello": "World"}


@app.get("/students/{id}")
async def get_student_by_id():
    return {"Hello": "World"}


@app.patch("/students/{id}")
async def update_student(id):
    return {"Hello": "World"}


@app.delete("/students/{id}")
async def delete_student(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)