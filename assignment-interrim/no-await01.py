import asyncio, time

async def worker_ok():
    print(f"[{time.ctime():}] [Worker_OK] started")
    await asyncio.sleep(1)  # Simulate non-blocking work
    print(f"[{time.ctime():}] [Worker_OK] Done")

async def main():
    asyncio.create_task(worker_ok())
    await asyncio.sleep(1)

asyncio.run(main())