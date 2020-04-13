import typing
import json

from httpcore import AsyncByteStream

from ._types import JSONDecoder


class Response:
    def __init__(
        self,
        body: typing.Optional[bytes],
        http_version: bytes,
        status_code: int,
        reason: bytes,
        headers: typing.List[typing.Tuple[bytes, bytes]],
        stream: AsyncByteStream
    ):
        self.body: typing.Optional[bytes] = body
        self._http_version = http_version
        self.status_code = status_code
        self._reason = reason
        self._headers = headers
        self._stream = stream

    @property
    def http_version(self) -> str:
        self._http_version = (
            self._http_version.decode()
            if isinstance(self._http_version, bytes)
            else self._http_version
        )
        return self._http_version

    @property
    def reason(self) -> str:
        self._reason = (
            self._reason.decode() if isinstance(self._reason, bytes) else self._reason
        )
        return self._reason

    @property
    def headers(self) -> typing.Dict[str, str]:
        self._headers = (
            {k.decode(): v.decode() for k, v in dict(self._headers).items()}
            if isinstance(self._headers, list)
            else self._headers
        )
        return self._headers

    async def content(self) -> bytes:
        if self.body is None:
            self.body = await _read_response_body(self._stream)
        return self.body

    async def text(self, encoding: str = "utf-8") -> str:
        return (await self.content()).decode(encoding)

    async def json(self, json_decoder: JSONDecoder = json.loads) -> typing.Dict[str, str]:
        return json_decoder(await self.text())

    def __str__(self):
        return f"<Response [{self.status_code}]>"


async def _read_response_body(stream: AsyncByteStream) -> bytes:
    try:
        body = []
        async for chunk in stream:
            body.append(chunk)
    finally:
        await stream.aclose()
    return b"".join(body)
