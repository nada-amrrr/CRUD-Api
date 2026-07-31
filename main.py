from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Task(BaseModel):
    title: str

class Updated_Task(BaseModel):
    title: Optional[str]
    done: Optional[bool]

tasks = [
    {"id": 1, "title":"docker course", "done":True},
    {"id": 2, "title":"kubernetes course", "done":True},
    {"id": 3, "title":"GitLab course", "done":False}
]

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def display_tasks():
    return tasks

from fastapi import HTTPException

@app.get("/tasks/{id}")
async def display_task(id:int):
    for task in tasks:
        if(id==task["id"]):
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.post("/tasks",status_code=201)
async def create_task(task_title:Task):
    if (task_title.title.strip() ==""):
        raise HTTPException(status_code=400, detail=f"No given title")    
    id = 0
    for task in tasks:
        if task["id"]>id:
            id=task["id"]
    task = {
        "id":id+1, "title":task_title.title, "done":False
    }
    tasks.append(task) 
    return task 

@app.put("/tasks/{id}")
async def update_task(id: int, new_task: Updated_Task):
    the_task = None
    found=False
    for task in tasks:
        if task["id"]==id:
            the_task=task
            found=True
    if found == False:
        raise HTTPException(status_code=404, detail="Unknown Id")
    if the_task==None:
         return {"Task doesn't exist"}
    if new_task.title != None:
        if new_task.title.strip() == "":
            raise HTTPException(status_code=400, detail=f"No given title")
        the_task["title"]=new_task.title
    if new_task.done != None:
            the_task["done"]=new_task.done
    return the_task


@app.delete("/tasks/{id}",status_code=204)
async def delete_task(id: int):
    found = False
    for task in tasks:
        if task["id"]==id:
            tasks.remove(task)
            found=True
            return
    if found == False:
        raise HTTPException(status_code=404, detail="Unknown Id")

