from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, StrictInt

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

class task_create(BaseModel):
    title: str
    owner: str
    priority: StrictInt = Field(default=2, ge=1, le=3)

@app.get("/tasks")
def get_tasks(priority: Optional[int] = Query(default=None, ge=1, le=3)):
    if priority is None:
        return tasks
    return [task for task in tasks if task["priority"] == priority]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: task_create):
    global counter
    new_task = {
        "id": counter,
        "title": task.title,
        "owner": task.owner,
        "priority": task.priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
