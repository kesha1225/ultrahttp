import urllib.parse
import typing

import httpcore
import typing_extensions
from httpcore import AsyncByteStream

from .response import Response
from .request import Request, _prepare_request


class HttpCore:
    def __init__(self, http2: bool = False):
        self.connection_pool = httpcore.AsyncConnectionPool(http2=http2)

    async def _request(
        self,
        url: str,
        method: bytes,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        data: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> Response:
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
                body=None,
                http_version=http_version,
                status_code=status_code,
                reason=reason,
                headers=response_headers,
                stream=stream,
            )

    async def request(
        self,
        url: str,
        method: str,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        data: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> Response:
        if method.upper().encode() not in [b"GET", b"POST", b"PUT", b"DELETE"]:
            raise RuntimeError("invalid method")

        return await self._request(
            url, method.upper().encode(), params=params, headers=headers, data=data
        )

    async def get(
        self,
        url: str,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
    ) -> Response:
        return await self.request(url, "GET", params=params, headers=headers)

    async def post(
        self,
        url: str,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        data: typing.Optional[typing.Dict[str, typing.Any]] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
    ) -> Response:
        return await self.request(
            url, "POST", params=params, data=data, headers=headers
        )
