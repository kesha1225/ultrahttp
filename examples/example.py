import asyncio

from ultrahttp import HttpCore, Params


http = HttpCore()


async def main():
    resp = await http.get(
        "https://www.youtube.com/watch",
        params=Params({"v": "Kr2DTn43EoE"}),
        headers={"hello": "world"},
    )

    print(resp.headers)
    print(resp.reason)
    print(resp.status_code)
    print(resp.http_version)
    print(await resp.text())


asyncio.get_event_loop().run_until_complete(main())
