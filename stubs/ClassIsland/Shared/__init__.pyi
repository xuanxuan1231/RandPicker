import typing
from CommunityToolkit.Mvvm.ComponentModel import ObservableRecipient
from System.Collections.Generic import Dictionary_2
from System import Guid

class AttachableSettingsObject(ObservableRecipient):
    def __init__(self) -> None: ...
    @property
    def AttachedObjects(self) -> Dictionary_2[Guid, typing.Any]: ...
    @AttachedObjects.setter
    def AttachedObjects(self, value: Dictionary_2[Guid, typing.Any]) -> Dictionary_2[Guid, typing.Any]: ...
    @property
    def IsActive(self) -> bool: ...
    @IsActive.setter
    def IsActive(self, value: bool) -> bool: ...
    # Skipped GetAttachedObject due to it being static, abstract and generic.

    GetAttachedObject : GetAttachedObject_MethodGroup
    class GetAttachedObject_MethodGroup:
        def __getitem__(self, t:typing.Type[GetAttachedObject_1_T1]) -> GetAttachedObject_1[GetAttachedObject_1_T1]: ...

        GetAttachedObject_1_T1 = typing.TypeVar('GetAttachedObject_1_T1')
        class GetAttachedObject_1(typing.Generic[GetAttachedObject_1_T1]):
            GetAttachedObject_1_T = AttachableSettingsObject.GetAttachedObject_MethodGroup.GetAttachedObject_1_T1
            @typing.overload
            def __call__(self, id: Guid) -> GetAttachedObject_1_T:...
            @typing.overload
            def __call__(self, id: Guid, defaultValue: GetAttachedObject_1_T) -> GetAttachedObject_1_T:...


    # Skipped WriteAttachedObject due to it being static, abstract and generic.

    WriteAttachedObject : WriteAttachedObject_MethodGroup
    class WriteAttachedObject_MethodGroup:
        def __getitem__(self, t:typing.Type[WriteAttachedObject_1_T1]) -> WriteAttachedObject_1[WriteAttachedObject_1_T1]: ...

        WriteAttachedObject_1_T1 = typing.TypeVar('WriteAttachedObject_1_T1')
        class WriteAttachedObject_1(typing.Generic[WriteAttachedObject_1_T1]):
            WriteAttachedObject_1_T = AttachableSettingsObject.WriteAttachedObject_MethodGroup.WriteAttachedObject_1_T1
            def __call__(self, id: Guid, o: WriteAttachedObject_1_T) -> None:...



