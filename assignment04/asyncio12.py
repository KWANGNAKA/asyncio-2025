# current task
import asyncio

async def show_current():
    current = asyncio.current_task()
    print("task ปัจจุบัน:", current.get_name())

async def main():
     await show_current()

asyncio.run(main())  