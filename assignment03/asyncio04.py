#Event loop
import asyncio

async def green():
    print("Hello")
    await asyncio.sleep(1)
    print("Word")

asyncio.run(green()) #สร้างและ run event loop
#
# loop = asyncio.new_evnet_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(greet())
# loop.close()
