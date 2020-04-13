import typing
import urllib.parse

from ultrahttp.stream import DictDataStream


class Request:
    def __init__(
        self,
        port: int,
        data_iterator: typing.Optional[typing.AsyncGenerator],
        path: bytes,
        headers: typing.List[typing.Tuple[bytes, bytes]],
        scheme: bytes,
        netloc: bytes,
    ):
        self.port = port
        self.data_iterator = data_iterator
        self.path = path
        self.headers = headers
        self.scheme = scheme
        self.netloc = netloc


def _prepare_request(
    parsed_url: urllib.parse.ParseResult,
    params: typing.Dict[str, typing.Any],
    data: typing.Optional[typing.Dict[str, typing.Any]],
    headers: typing.Optional[typing.Dict[str, str]],
) -> Request:
    if not parsed_url.scheme:
        raise RuntimeError("invalid scheme")

    port = 80
    if parsed_url.scheme == "https":
        port = 443

    _headers = [(b"host", parsed_url.netloc.encode())]

    if headers is not None:
        for key, value in headers.items():
            _headers.append((key.encode(), value.encode()))

    path = parsed_url.path.encode() or b"/"
    if params is not None:
        path += b"?" + urllib.parse.urlencode(params, doseq=True).encode()

    data_iterator = None
    if data is not None:
        data_stream = DictDataStream(data)
        _headers.extend(data_stream.get_headers())
        data_iterator = DictDataStream(data).__aiter__()

    return Request(
        port=port,
        data_iterator=data_iterator,
        path=path,
        headers=_headers,
        scheme=parsed_url.scheme.encode(),
        netloc=parsed_url.netloc.encode(),
    )
