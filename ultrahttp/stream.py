import typing
import urllib.parse


class DictDataStream:
    def __init__(self, data: dict) -> None:
        self.body = urllib.parse.urlencode(data, doseq=True).encode("utf-8")

    def get_headers(self) -> typing.List[typing.Tuple[bytes, bytes]]:
        content_length = str(len(self.body))
        content_type = b"application/x-www-form-urlencoded"
        return [(b"Content-Length", content_length.encode()), (b"Content-Type", content_type)]

    def __iter__(self) -> typing.Iterator[bytes]:
        yield self.body

    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        yield self.body
