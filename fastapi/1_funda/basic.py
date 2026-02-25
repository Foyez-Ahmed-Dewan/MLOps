from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#----
app = FastAPI()

@app.get("/")
async def hello_msg():
    return {"message": "Hello, how are you?"}

#-----
class Fruit(BaseModel):
    id : int
    name: str
    owner: str
    
fruits: List[Fruit] = []
#----

@app.post("/request")
async def user_to_server(sample: Fruit):
    fruits.append(sample)
    return {"message": "successful"}

#---

@app.get("/fruits", response_model=List[Fruit])
async def server_to_user():
    # for f in fruits:
    #     print(f"fruit id: {f.id}, fruit name: {f.name}")
    return fruits

#---
@app.put("/replace/{fruit_id}")
async def update_info(fruit_id: int, updated_data: Fruit):
    for idx, fruit in enumerate(fruits):
        if (fruit.id == fruit_id):
            fruits[idx] = updated_data
            return {"message": "successful edit"}
    return {"message": "No match"} 

#---
@app.delete("/delete/{fruit_id}")
async def delete_item(fruit_id: int):
    for idx, fruit in enumerate(fruits):
        if (fruit.id == fruit_id):
            fruits.pop(idx)
            return {"message": "successful deletion"}
    return {"message" : "not found"}
            