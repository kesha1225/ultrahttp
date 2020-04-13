import typing

Params = typing.NewType("Params", typing.Dict[str, typing.Any])
JSONEncoder = typing.Callable[[typing.Any], str]
JSONDecoder = typing.Callable[[str], typing.Any]

