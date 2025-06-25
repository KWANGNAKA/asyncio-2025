# Check if a Task is Done
import asyncio

async def simmple_pask():
    await asyncio.sleep(1)
    return "เสร็จแล้ว!"
async def main():
    task = asyncio.create_task(simmple_pask())
    print("ก่อน await:", task.done())
    await task
    print("หลัง await:", task.done()) #เสร็จแล้ว

asyncio.run(main())
