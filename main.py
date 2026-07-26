from fastapi import FastAPI

app = FastAPI()

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
    
