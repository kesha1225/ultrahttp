import asyncio
import typing

from ultrahttp.response import Response


class RequestPool:
    def __init__(self):
        self._requests = []
        self.responses = []

    async def get_result(self) -> typing.List[Response]:
        responses = await asyncio.gather(*self._requests)
        return responses

    def add_request(self, task: typing.Awaitable):
        self._requests.append(task)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.responses = await self.get_result()
