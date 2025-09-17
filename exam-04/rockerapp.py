# file: rocketapp.py
from fastapi import FastAPI, HTTPException
import asyncio
import random

app = FastAPI(title="Asynchronous Rocket Launcher")

# เก็บ task ที่ยิงไปแล้ว (optional)
rockets = set()

async def launch_rocket(student_id: str, eta: float):
    print(f"Rocket {student_id} launched! ETA: {eta:.2f} seconds")
    await asyncio.sleep(eta)
    print(f"Rocket {student_id} reached destination after {eta:.2f} seconds")

@app.get("/fire/{student_id}")
async def fire_rocket(student_id: str):
    if not (len(student_id) == 10 and student_id.isdigit()):
        raise HTTPException(status_code=400, detail="student_id must be 10 digits")

    eta = random.uniform(1.0, 2.0)


    # ยิงเป็น background task
    task = asyncio.create_task(launch_rocket(student_id, eta))
    rockets.add(task)
    # ทำความสะอาด set เมื่อ task เสร็จ
    task.add_done_callback(lambda t: rockets.discard(t))

    # รอเวลาเท่ากับ eta เพื่อสะท้อนเวลาถึงจริง
    await asyncio.sleep(eta)

    return {"message": f"Rocket {student_id} fired!", "time_to_target": round(eta, 2)}
