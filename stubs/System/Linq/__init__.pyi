import typing, abc
from System.Collections.Generic import IEnumerable_1

class IGrouping_GenericClasses(abc.ABCMeta):
    Generic_IGrouping_GenericClasses_IGrouping_2_TKey = typing.TypeVar('Generic_IGrouping_GenericClasses_IGrouping_2_TKey')
    Generic_IGrouping_GenericClasses_IGrouping_2_TElement = typing.TypeVar('Generic_IGrouping_GenericClasses_IGrouping_2_TElement')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_IGrouping_GenericClasses_IGrouping_2_TKey], typing.Type[Generic_IGrouping_GenericClasses_IGrouping_2_TElement]]) -> typing.Type[IGrouping_2[Generic_IGrouping_GenericClasses_IGrouping_2_TKey, Generic_IGrouping_GenericClasses_IGrouping_2_TElement]]: ...

IGrouping : IGrouping_GenericClasses

IGrouping_2_TKey = typing.TypeVar('IGrouping_2_TKey', covariant=True)
IGrouping_2_TElement = typing.TypeVar('IGrouping_2_TElement', covariant=True)
class IGrouping_2(typing.Generic[IGrouping_2_TKey, IGrouping_2_TElement], IEnumerable_1[IGrouping_2_TElement], typing.Protocol):
    @property
    def Key(self) -> IGrouping_2_TKey: ...


class ILookup_GenericClasses(abc.ABCMeta):
    Generic_ILookup_GenericClasses_ILookup_2_TKey = typing.TypeVar('Generic_ILookup_GenericClasses_ILookup_2_TKey')
    Generic_ILookup_GenericClasses_ILookup_2_TElement = typing.TypeVar('Generic_ILookup_GenericClasses_ILookup_2_TElement')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ILookup_GenericClasses_ILookup_2_TKey], typing.Type[Generic_ILookup_GenericClasses_ILookup_2_TElement]]) -> typing.Type[ILookup_2[Generic_ILookup_GenericClasses_ILookup_2_TKey, Generic_ILookup_GenericClasses_ILookup_2_TElement]]: ...

ILookup : ILookup_GenericClasses

ILookup_2_TKey = typing.TypeVar('ILookup_2_TKey')
ILookup_2_TElement = typing.TypeVar('ILookup_2_TElement')
class ILookup_2(typing.Generic[ILookup_2_TKey, ILookup_2_TElement], IEnumerable_1[IGrouping_2[ILookup_2_TKey, ILookup_2_TElement]], typing.Protocol):
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> IEnumerable_1[ILookup_2_TElement]: ...
    @abc.abstractmethod
    def Contains(self, key: ILookup_2_TKey) -> bool: ...

