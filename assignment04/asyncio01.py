# example of getting the current task from the main coroutine
import asyncio

#define a mne coroutine
async def main():
    #report a message
    print('main coroutine started')
    #get the current task
    Task = asyncio.current_task()
    #report its deteils
    print(Task)
    
#start the coroutine program
asyncio.run(main())