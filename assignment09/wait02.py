#example of waiting for all task to complete
from random import random
import asyncio

#coroutine to execute in a new task
async def task_coro(arg):
    #generate a random value between 0 and 1
    value = random()
    #block for a moment
    await asyncio.sleep(value)
    #report the a value
    print(f">task {arg} done with {value}")
    return arg, value

async def main():
    #create many tasks
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    #wait for all tasks to complete
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    #report results
    for task in done:
        if task.done():
            print(f"Done: {task.result()}")
    for task in pending:
        if task.done():
            print(f"Pending: {task.result()}")
        else:
            print(f"Pending: {task.get_name()} - {task.done()}")

#run the main coroutine
asyncio.run(main())