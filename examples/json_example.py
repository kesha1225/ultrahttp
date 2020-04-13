import asyncio

from ultrahttp import HttpCore

http = HttpCore()


async def main():
    resp = await http.post("https://httpbin.org/post", data={"key": "value2323"}, params={"1": "2"})

    print(await resp.json())


asyncio.get_event_loop().run_until_complete(main())
