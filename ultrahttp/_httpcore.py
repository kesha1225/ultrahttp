import urllib.parse
import typing

import httpcore
import typing_extensions
from httpcore import AsyncByteStream

from ._types import Params
from .response import Response, _read_response_body
from .request import Request, _prepare_request


class HttpCore:
    def __init__(self, http2: bool = False):
        self.connection_pool = httpcore.AsyncConnectionPool(http2=http2)

    async def _request(
        self,
        url: str,
        method: typing_extensions.Literal[b"GET", b"POST", b"PUT", b"DELETE"],
        params: typing.Optional[Params] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        data: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        parsed_url = urllib.parse.urlparse(url)
        request: Request = _prepare_request(
            parsed_url=parsed_url, params=params, data=data, headers=headers
        )

        async with self.connection_pool as http:

            raw_response = await http.request(
                method,
                (request.scheme, request.netloc, request.port, request.path,),
                request.headers,
                stream=AsyncByteStream(iterator=request.data_iterator),
            )

            http_version, status_code, reason, response_headers, stream = raw_response

            return Response(
                b"".join(await _read_response_body(stream)),
                http_version,
                status_code,
                reason,
                response_headers,
            )

    async def get(
        self,
        url: str,
        params: typing.Optional[Params] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
    ):
        return await self._request(url, b"GET", params=params, headers=headers)

    async def post(
        self,
        url: str,
        params: typing.Optional[Params] = None,
        data: typing.Optional[typing.Dict[str, typing.Any]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
    ):
        return await self._request(
            url, b"POST", params=params, data=data, headers=headers
        )
