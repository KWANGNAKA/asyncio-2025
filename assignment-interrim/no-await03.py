import asyncio, time

async def worker_long():
    print(f"[{time.ctime():}] [Worker_Long] start")
    try:
        await asyncio.sleep(5)  # Simulate a long-running task
        print(f"[{time.ctime():}] [Worker_Long] Done")
    except asyncio.CancelledError:
        print(f"[{time.ctime():}] [Worker_Long] Cancelled")

async def main():
    print(f"{time.ctime()} Starting Main loop....")
    asyncio.create_task(worker_long())  # Fire and forget
    await asyncio.sleep(1)  # Simulate doing other work
    print(f"{time.ctime()} Main loop finished...!")

asyncio.run(main())