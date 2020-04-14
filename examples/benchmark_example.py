import asyncio
import time

import aiohttp

import ultrahttp


async def aiohttp_test():
    session = aiohttp.ClientSession()
    for _ in range(30):
        async with session.get("https://www.google.com/") as r:
            resp = await r.text()
            print(resp)


async def ultrahttp_test():
    http = ultrahttp.HttpCore()

    async with ultrahttp.RequestPool() as pool:
        for _ in range(30):
            pool.add_request(http.get("https://www.google.com/"))

    for res in pool.responses:
        resp = await res.text()
        print(resp)


s = time.time()
asyncio.get_event_loop().run_until_complete(ultrahttp_test())
print(time.time() - s)
# 2.1875200271606445 aiohttp
# 0.8386387825012207 ultrahttp
