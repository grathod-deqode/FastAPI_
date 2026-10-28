from fastapi import FastAPI 
import time
import asyncio 
app = FastAPI()


@app.get("/sync")
def sync_example():
    print("Task 1 started ")

    time.sleep(5)

    print("Task 2 completed")

    return {
        "message" : "sync task is completed"
    }

@app.get("/async")
async def async_example():
    print("Task 1 started")

    await asyncio.sleep(5)

    print("Task 2 Completed")


    return {
        "message" : "Async task is completed"
    }