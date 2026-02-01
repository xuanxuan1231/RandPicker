import typing, abc

class Console(abc.ABC):
    @staticmethod
    def Write(s: str) -> None: ...
    # Skipped WriteLine due to it being static, abstract and generic.

    WriteLine : WriteLine_MethodGroup
    class WriteLine_MethodGroup:
        @typing.overload
        def __call__(self) -> None:...
        @typing.overload
        def __call__(self, s: str) -> None:...


