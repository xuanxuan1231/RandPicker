import typing
from System import IServiceProvider

class Ioc(IServiceProvider):
    def __init__(self) -> None: ...
    @classmethod
    @property
    def Default(cls) -> Ioc: ...
    def ConfigureServices(self, serviceProvider: IServiceProvider) -> None: ...
    # Skipped GetRequiredService due to it being static, abstract and generic.

    GetRequiredService : GetRequiredService_MethodGroup
    class GetRequiredService_MethodGroup:
        def __getitem__(self, t:typing.Type[GetRequiredService_1_T1]) -> GetRequiredService_1[GetRequiredService_1_T1]: ...

        GetRequiredService_1_T1 = typing.TypeVar('GetRequiredService_1_T1')
        class GetRequiredService_1(typing.Generic[GetRequiredService_1_T1]):
            GetRequiredService_1_T = Ioc.GetRequiredService_MethodGroup.GetRequiredService_1_T1
            def __call__(self) -> GetRequiredService_1_T:...


    # Skipped GetService due to it being static, abstract and generic.

    GetService : GetService_MethodGroup
    class GetService_MethodGroup:
        def __getitem__(self, t:typing.Type[GetService_1_T1]) -> GetService_1[GetService_1_T1]: ...

        GetService_1_T1 = typing.TypeVar('GetService_1_T1')
        class GetService_1(typing.Generic[GetService_1_T1]):
            GetService_1_T = Ioc.GetService_MethodGroup.GetService_1_T1
            def __call__(self) -> GetService_1_T:...

        def __call__(self, serviceType: typing.Type[typing.Any]) -> typing.Any:...


