# example of starting many tasks and getting access to all tasks
import time
import asyncio

# coroutine for a task
async def dowload_image(name, delay):
    print(f"{time.ctime()} {name} กำลังโหลด...")
    await asyncio.sleep(delay)
    print(f"{time.ctime()} {name} โฟลดเสร็จแล้ว!")

# define a main coroutine
async def main():
    # report a message
    print(f"{time.ctime()} main coroutine started")
    # start mant tasks
    # started_tasks = [asyncio.create_task(dowload_image(i, i)) for i in range(3)]

    # โหลดแบบย้อนกลับโดยใช้ reversed
    started_tasks = [asyncio.create_task(dowload_image(i, delay)) for i, delay in zip(reversed(range(3)), range(3))]

    # allow some of the tasks time to start
    await asyncio.sleep(0.1)
    for task in started_tasks:
        await task

        
# start the asyncio program
asyncio.run(main())