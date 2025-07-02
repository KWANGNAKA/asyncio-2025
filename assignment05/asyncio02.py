# example of waiting for the first task to complete
from random import random
import asyncio

#corutine to execute in a new task
async def task_coro(arg):
    #generate a random valu between 0 and 1
    Value = random()
    #block for a moment
    await asyncio.sleep(Value)
    #report the value
    print(f'>task {arg} done with {Value}')

#main corouting
async def main():
    #create many tasks
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    #wait for all tasks to complete
    done,pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    #report result
    print('Done')
    #get the first task to commplete
    first = done.pop()
    print(first)

#strat the asyncio program
asyncio.run(main())