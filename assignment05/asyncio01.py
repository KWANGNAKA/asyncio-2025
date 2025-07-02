# example of waiting for all tasks to complete
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
    #done,pending = awit asycio.wait(task,return_when=asyncio.ALL_COMPLETED)
    done,pending = await asyncio.wait(tasks)
    print('All done')

#strat the asyncio program
asyncio.run(main())