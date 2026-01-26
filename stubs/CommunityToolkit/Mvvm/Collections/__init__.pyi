import typing, abc
from System.Collections import IEnumerable
from System.Collections.Specialized import INotifyCollectionChanged
from System.ComponentModel import INotifyPropertyChanged
from System.Collections.Generic import IReadOnlyList_1, IEnumerable_1, IComparer_1
from System.Linq import IGrouping_2, ILookup_2
from System.Collections.ObjectModel import ObservableCollection_1, ReadOnlyObservableCollection_1

class IReadOnlyObservableGroup_GenericClasses(abc.ABCMeta):
    Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_1_TKey = typing.TypeVar('Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_1_TKey')
    @typing.overload
    def __getitem__(self, types : typing.Type[Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_1_TKey]) -> typing.Type[IReadOnlyObservableGroup_1[Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_1_TKey]]: ...
    Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TKey = typing.TypeVar('Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TKey')
    Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TElement = typing.TypeVar('Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TElement')
    @typing.overload
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TKey], typing.Type[Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TElement]]) -> typing.Type[IReadOnlyObservableGroup_2[Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TKey, Generic_IReadOnlyObservableGroup_GenericClasses_IReadOnlyObservableGroup_2_TElement]]: ...

class IReadOnlyObservableGroup(IReadOnlyObservableGroup_0, metaclass =IReadOnlyObservableGroup_GenericClasses): ...

class IReadOnlyObservableGroup_0(IEnumerable, INotifyCollectionChanged, INotifyPropertyChanged, typing.Protocol):
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> typing.Any: ...
    @property
    def Key(self) -> typing.Any: ...


IReadOnlyObservableGroup_1_TKey = typing.TypeVar('IReadOnlyObservableGroup_1_TKey', covariant=True)
class IReadOnlyObservableGroup_1(typing.Generic[IReadOnlyObservableGroup_1_TKey], IReadOnlyObservableGroup_0, typing.Protocol):
    @property
    def Key(self) -> IReadOnlyObservableGroup_1_TKey: ...


IReadOnlyObservableGroup_2_TKey = typing.TypeVar('IReadOnlyObservableGroup_2_TKey', covariant=True)
IReadOnlyObservableGroup_2_TElement = typing.TypeVar('IReadOnlyObservableGroup_2_TElement', covariant=True)
class IReadOnlyObservableGroup_2(typing.Generic[IReadOnlyObservableGroup_2_TKey, IReadOnlyObservableGroup_2_TElement], IReadOnlyList_1[IReadOnlyObservableGroup_2_TElement], IGrouping_2[IReadOnlyObservableGroup_2_TKey, IReadOnlyObservableGroup_2_TElement], IReadOnlyObservableGroup_1[IReadOnlyObservableGroup_2_TKey], typing.Protocol):
    @property
    def Item(self) -> IReadOnlyObservableGroup_2_TElement: ...


class ObservableGroup_GenericClasses(abc.ABCMeta):
    Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TKey = typing.TypeVar('Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TKey')
    Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TElement = typing.TypeVar('Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TElement')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TKey], typing.Type[Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TElement]]) -> typing.Type[ObservableGroup_2[Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TKey, Generic_ObservableGroup_GenericClasses_ObservableGroup_2_TElement]]: ...

ObservableGroup : ObservableGroup_GenericClasses

ObservableGroup_2_TKey = typing.TypeVar('ObservableGroup_2_TKey')
ObservableGroup_2_TElement = typing.TypeVar('ObservableGroup_2_TElement')
class ObservableGroup_2(typing.Generic[ObservableGroup_2_TKey, ObservableGroup_2_TElement], ObservableCollection_1[ObservableGroup_2_TElement], IReadOnlyObservableGroup_2[ObservableGroup_2_TKey, ObservableGroup_2_TElement]):
    @typing.overload
    def __init__(self, grouping: IGrouping_2[ObservableGroup_2_TKey, ObservableGroup_2_TElement]) -> None: ...
    @typing.overload
    def __init__(self, key: ObservableGroup_2_TKey) -> None: ...
    @typing.overload
    def __init__(self, key: ObservableGroup_2_TKey, collection: IEnumerable_1[ObservableGroup_2_TElement]) -> None: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ObservableGroup_2_TElement: ...
    @Item.setter
    def Item(self, value: ObservableGroup_2_TElement) -> ObservableGroup_2_TElement: ...
    @property
    def Key(self) -> ObservableGroup_2_TKey: ...
    @Key.setter
    def Key(self, value: ObservableGroup_2_TKey) -> ObservableGroup_2_TKey: ...


class ObservableGroupedCollection_GenericClasses(abc.ABCMeta):
    Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TKey = typing.TypeVar('Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TKey')
    Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TElement = typing.TypeVar('Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TElement')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TKey], typing.Type[Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TElement]]) -> typing.Type[ObservableGroupedCollection_2[Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TKey, Generic_ObservableGroupedCollection_GenericClasses_ObservableGroupedCollection_2_TElement]]: ...

ObservableGroupedCollection : ObservableGroupedCollection_GenericClasses

ObservableGroupedCollection_2_TKey = typing.TypeVar('ObservableGroupedCollection_2_TKey')
ObservableGroupedCollection_2_TElement = typing.TypeVar('ObservableGroupedCollection_2_TElement')
class ObservableGroupedCollection_2(typing.Generic[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement], ObservableCollection_1[ObservableGroup_2[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement]], ILookup_2[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement]):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, collection: IEnumerable_1[IGrouping_2[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement]]) -> None: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ObservableGroup_2[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement]: ...
    @Item.setter
    def Item(self, value: ObservableGroup_2[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement]) -> ObservableGroup_2[ObservableGroupedCollection_2_TKey, ObservableGroupedCollection_2_TElement]: ...


class ObservableGroupedCollectionExtensions(abc.ABC):
    # Skipped AddGroup due to it being static, abstract and generic.

    AddGroup : AddGroup_MethodGroup
    class AddGroup_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AddGroup_2_T1], typing.Type[AddGroup_2_T2]]) -> AddGroup_2[AddGroup_2_T1, AddGroup_2_T2]: ...

        AddGroup_2_T1 = typing.TypeVar('AddGroup_2_T1')
        AddGroup_2_T2 = typing.TypeVar('AddGroup_2_T2')
        class AddGroup_2(typing.Generic[AddGroup_2_T1, AddGroup_2_T2]):
            AddGroup_2_TKey = ObservableGroupedCollectionExtensions.AddGroup_MethodGroup.AddGroup_2_T1
            AddGroup_2_TElement = ObservableGroupedCollectionExtensions.AddGroup_MethodGroup.AddGroup_2_T2
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[AddGroup_2_TKey, AddGroup_2_TElement], grouping: IGrouping_2[AddGroup_2_TKey, AddGroup_2_TElement]) -> ObservableGroup_2[AddGroup_2_TKey, AddGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[AddGroup_2_TKey, AddGroup_2_TElement], key: AddGroup_2_TKey) -> ObservableGroup_2[AddGroup_2_TKey, AddGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[AddGroup_2_TKey, AddGroup_2_TElement], key: AddGroup_2_TKey, collection: IEnumerable_1[AddGroup_2_TElement]) -> ObservableGroup_2[AddGroup_2_TKey, AddGroup_2_TElement]:...


    # Skipped AddItem due to it being static, abstract and generic.

    AddItem : AddItem_MethodGroup
    class AddItem_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[AddItem_2_T1], typing.Type[AddItem_2_T2]]) -> AddItem_2[AddItem_2_T1, AddItem_2_T2]: ...

        AddItem_2_T1 = typing.TypeVar('AddItem_2_T1')
        AddItem_2_T2 = typing.TypeVar('AddItem_2_T2')
        class AddItem_2(typing.Generic[AddItem_2_T1, AddItem_2_T2]):
            AddItem_2_TKey = ObservableGroupedCollectionExtensions.AddItem_MethodGroup.AddItem_2_T1
            AddItem_2_TElement = ObservableGroupedCollectionExtensions.AddItem_MethodGroup.AddItem_2_T2
            def __call__(self, source: ObservableGroupedCollection_2[AddItem_2_TKey, AddItem_2_TElement], key: AddItem_2_TKey, item: AddItem_2_TElement) -> ObservableGroup_2[AddItem_2_TKey, AddItem_2_TElement]:...


    # Skipped FirstGroupByKey due to it being static, abstract and generic.

    FirstGroupByKey : FirstGroupByKey_MethodGroup
    class FirstGroupByKey_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[FirstGroupByKey_2_T1], typing.Type[FirstGroupByKey_2_T2]]) -> FirstGroupByKey_2[FirstGroupByKey_2_T1, FirstGroupByKey_2_T2]: ...

        FirstGroupByKey_2_T1 = typing.TypeVar('FirstGroupByKey_2_T1')
        FirstGroupByKey_2_T2 = typing.TypeVar('FirstGroupByKey_2_T2')
        class FirstGroupByKey_2(typing.Generic[FirstGroupByKey_2_T1, FirstGroupByKey_2_T2]):
            FirstGroupByKey_2_TKey = ObservableGroupedCollectionExtensions.FirstGroupByKey_MethodGroup.FirstGroupByKey_2_T1
            FirstGroupByKey_2_TElement = ObservableGroupedCollectionExtensions.FirstGroupByKey_MethodGroup.FirstGroupByKey_2_T2
            def __call__(self, source: ObservableGroupedCollection_2[FirstGroupByKey_2_TKey, FirstGroupByKey_2_TElement], key: FirstGroupByKey_2_TKey) -> ObservableGroup_2[FirstGroupByKey_2_TKey, FirstGroupByKey_2_TElement]:...


    # Skipped FirstGroupByKeyOrDefault due to it being static, abstract and generic.

    FirstGroupByKeyOrDefault : FirstGroupByKeyOrDefault_MethodGroup
    class FirstGroupByKeyOrDefault_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[FirstGroupByKeyOrDefault_2_T1], typing.Type[FirstGroupByKeyOrDefault_2_T2]]) -> FirstGroupByKeyOrDefault_2[FirstGroupByKeyOrDefault_2_T1, FirstGroupByKeyOrDefault_2_T2]: ...

        FirstGroupByKeyOrDefault_2_T1 = typing.TypeVar('FirstGroupByKeyOrDefault_2_T1')
        FirstGroupByKeyOrDefault_2_T2 = typing.TypeVar('FirstGroupByKeyOrDefault_2_T2')
        class FirstGroupByKeyOrDefault_2(typing.Generic[FirstGroupByKeyOrDefault_2_T1, FirstGroupByKeyOrDefault_2_T2]):
            FirstGroupByKeyOrDefault_2_TKey = ObservableGroupedCollectionExtensions.FirstGroupByKeyOrDefault_MethodGroup.FirstGroupByKeyOrDefault_2_T1
            FirstGroupByKeyOrDefault_2_TElement = ObservableGroupedCollectionExtensions.FirstGroupByKeyOrDefault_MethodGroup.FirstGroupByKeyOrDefault_2_T2
            def __call__(self, source: ObservableGroupedCollection_2[FirstGroupByKeyOrDefault_2_TKey, FirstGroupByKeyOrDefault_2_TElement], key: FirstGroupByKeyOrDefault_2_TKey) -> ObservableGroup_2[FirstGroupByKeyOrDefault_2_TKey, FirstGroupByKeyOrDefault_2_TElement]:...


    # Skipped InsertGroup due to it being static, abstract and generic.

    InsertGroup : InsertGroup_MethodGroup
    class InsertGroup_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[InsertGroup_2_T1], typing.Type[InsertGroup_2_T2]]) -> InsertGroup_2[InsertGroup_2_T1, InsertGroup_2_T2]: ...

        InsertGroup_2_T1 = typing.TypeVar('InsertGroup_2_T1')
        InsertGroup_2_T2 = typing.TypeVar('InsertGroup_2_T2')
        class InsertGroup_2(typing.Generic[InsertGroup_2_T1, InsertGroup_2_T2]):
            InsertGroup_2_TKey = ObservableGroupedCollectionExtensions.InsertGroup_MethodGroup.InsertGroup_2_T1
            InsertGroup_2_TElement = ObservableGroupedCollectionExtensions.InsertGroup_MethodGroup.InsertGroup_2_T2
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertGroup_2_TKey, InsertGroup_2_TElement], grouping: IGrouping_2[InsertGroup_2_TKey, InsertGroup_2_TElement]) -> ObservableGroup_2[InsertGroup_2_TKey, InsertGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertGroup_2_TKey, InsertGroup_2_TElement], key: InsertGroup_2_TKey) -> ObservableGroup_2[InsertGroup_2_TKey, InsertGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertGroup_2_TKey, InsertGroup_2_TElement], grouping: IGrouping_2[InsertGroup_2_TKey, InsertGroup_2_TElement], comparer: IComparer_1[InsertGroup_2_TKey]) -> ObservableGroup_2[InsertGroup_2_TKey, InsertGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertGroup_2_TKey, InsertGroup_2_TElement], key: InsertGroup_2_TKey, collection: IEnumerable_1[InsertGroup_2_TElement]) -> ObservableGroup_2[InsertGroup_2_TKey, InsertGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertGroup_2_TKey, InsertGroup_2_TElement], key: InsertGroup_2_TKey, comparer: IComparer_1[InsertGroup_2_TKey]) -> ObservableGroup_2[InsertGroup_2_TKey, InsertGroup_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertGroup_2_TKey, InsertGroup_2_TElement], key: InsertGroup_2_TKey, comparer: IComparer_1[InsertGroup_2_TKey], collection: IEnumerable_1[InsertGroup_2_TElement]) -> ObservableGroup_2[InsertGroup_2_TKey, InsertGroup_2_TElement]:...


    # Skipped InsertItem due to it being static, abstract and generic.

    InsertItem : InsertItem_MethodGroup
    class InsertItem_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[InsertItem_2_T1], typing.Type[InsertItem_2_T2]]) -> InsertItem_2[InsertItem_2_T1, InsertItem_2_T2]: ...

        InsertItem_2_T1 = typing.TypeVar('InsertItem_2_T1')
        InsertItem_2_T2 = typing.TypeVar('InsertItem_2_T2')
        class InsertItem_2(typing.Generic[InsertItem_2_T1, InsertItem_2_T2]):
            InsertItem_2_TKey = ObservableGroupedCollectionExtensions.InsertItem_MethodGroup.InsertItem_2_T1
            InsertItem_2_TElement = ObservableGroupedCollectionExtensions.InsertItem_MethodGroup.InsertItem_2_T2
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertItem_2_TKey, InsertItem_2_TElement], key: InsertItem_2_TKey, item: InsertItem_2_TElement) -> ObservableGroup_2[InsertItem_2_TKey, InsertItem_2_TElement]:...
            @typing.overload
            def __call__(self, source: ObservableGroupedCollection_2[InsertItem_2_TKey, InsertItem_2_TElement], key: InsertItem_2_TKey, keyComparer: IComparer_1[InsertItem_2_TKey], item: InsertItem_2_TElement, itemComparer: IComparer_1[InsertItem_2_TElement]) -> ObservableGroup_2[InsertItem_2_TKey, InsertItem_2_TElement]:...


    # Skipped RemoveGroup due to it being static, abstract and generic.

    RemoveGroup : RemoveGroup_MethodGroup
    class RemoveGroup_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[RemoveGroup_2_T1], typing.Type[RemoveGroup_2_T2]]) -> RemoveGroup_2[RemoveGroup_2_T1, RemoveGroup_2_T2]: ...

        RemoveGroup_2_T1 = typing.TypeVar('RemoveGroup_2_T1')
        RemoveGroup_2_T2 = typing.TypeVar('RemoveGroup_2_T2')
        class RemoveGroup_2(typing.Generic[RemoveGroup_2_T1, RemoveGroup_2_T2]):
            RemoveGroup_2_TKey = ObservableGroupedCollectionExtensions.RemoveGroup_MethodGroup.RemoveGroup_2_T1
            RemoveGroup_2_TValue = ObservableGroupedCollectionExtensions.RemoveGroup_MethodGroup.RemoveGroup_2_T2
            def __call__(self, source: ObservableGroupedCollection_2[RemoveGroup_2_TKey, RemoveGroup_2_TValue], key: RemoveGroup_2_TKey) -> None:...


    # Skipped RemoveItem due to it being static, abstract and generic.

    RemoveItem : RemoveItem_MethodGroup
    class RemoveItem_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[RemoveItem_2_T1], typing.Type[RemoveItem_2_T2]]) -> RemoveItem_2[RemoveItem_2_T1, RemoveItem_2_T2]: ...

        RemoveItem_2_T1 = typing.TypeVar('RemoveItem_2_T1')
        RemoveItem_2_T2 = typing.TypeVar('RemoveItem_2_T2')
        class RemoveItem_2(typing.Generic[RemoveItem_2_T1, RemoveItem_2_T2]):
            RemoveItem_2_TKey = ObservableGroupedCollectionExtensions.RemoveItem_MethodGroup.RemoveItem_2_T1
            RemoveItem_2_TValue = ObservableGroupedCollectionExtensions.RemoveItem_MethodGroup.RemoveItem_2_T2
            def __call__(self, source: ObservableGroupedCollection_2[RemoveItem_2_TKey, RemoveItem_2_TValue], key: RemoveItem_2_TKey, item: RemoveItem_2_TValue, removeGroupIfEmpty: bool = ...) -> None:...




class ReadOnlyObservableGroup_GenericClasses(abc.ABCMeta):
    Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TKey = typing.TypeVar('Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TKey')
    Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TElement = typing.TypeVar('Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TElement')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TKey], typing.Type[Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TElement]]) -> typing.Type[ReadOnlyObservableGroup_2[Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TKey, Generic_ReadOnlyObservableGroup_GenericClasses_ReadOnlyObservableGroup_2_TElement]]: ...

ReadOnlyObservableGroup : ReadOnlyObservableGroup_GenericClasses

ReadOnlyObservableGroup_2_TKey = typing.TypeVar('ReadOnlyObservableGroup_2_TKey')
ReadOnlyObservableGroup_2_TElement = typing.TypeVar('ReadOnlyObservableGroup_2_TElement')
class ReadOnlyObservableGroup_2(typing.Generic[ReadOnlyObservableGroup_2_TKey, ReadOnlyObservableGroup_2_TElement], ReadOnlyObservableCollection_1[ReadOnlyObservableGroup_2_TElement], IReadOnlyObservableGroup_2[ReadOnlyObservableGroup_2_TKey, ReadOnlyObservableGroup_2_TElement]):
    @typing.overload
    def __init__(self, group: ObservableGroup_2[ReadOnlyObservableGroup_2_TKey, ReadOnlyObservableGroup_2_TElement]) -> None: ...
    @typing.overload
    def __init__(self, key: ReadOnlyObservableGroup_2_TKey, collection: ObservableCollection_1[ReadOnlyObservableGroup_2_TElement]) -> None: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ReadOnlyObservableGroup_2_TElement: ...
    @property
    def Key(self) -> ReadOnlyObservableGroup_2_TKey: ...


class ReadOnlyObservableGroupedCollection_GenericClasses(abc.ABCMeta):
    Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TKey = typing.TypeVar('Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TKey')
    Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TElement = typing.TypeVar('Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TElement')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TKey], typing.Type[Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TElement]]) -> typing.Type[ReadOnlyObservableGroupedCollection_2[Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TKey, Generic_ReadOnlyObservableGroupedCollection_GenericClasses_ReadOnlyObservableGroupedCollection_2_TElement]]: ...

ReadOnlyObservableGroupedCollection : ReadOnlyObservableGroupedCollection_GenericClasses

ReadOnlyObservableGroupedCollection_2_TKey = typing.TypeVar('ReadOnlyObservableGroupedCollection_2_TKey')
ReadOnlyObservableGroupedCollection_2_TElement = typing.TypeVar('ReadOnlyObservableGroupedCollection_2_TElement')
class ReadOnlyObservableGroupedCollection_2(typing.Generic[ReadOnlyObservableGroupedCollection_2_TKey, ReadOnlyObservableGroupedCollection_2_TElement], ReadOnlyObservableCollection_1[ReadOnlyObservableGroup_2[ReadOnlyObservableGroupedCollection_2_TKey, ReadOnlyObservableGroupedCollection_2_TElement]], ILookup_2[ReadOnlyObservableGroupedCollection_2_TKey, ReadOnlyObservableGroupedCollection_2_TElement]):
    @typing.overload
    def __init__(self, collection: ObservableCollection_1[ObservableGroup_2[ReadOnlyObservableGroupedCollection_2_TKey, ReadOnlyObservableGroupedCollection_2_TElement]]) -> None: ...
    @typing.overload
    def __init__(self, collection: ObservableCollection_1[ReadOnlyObservableGroup_2[ReadOnlyObservableGroupedCollection_2_TKey, ReadOnlyObservableGroupedCollection_2_TElement]]) -> None: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> ReadOnlyObservableGroup_2[ReadOnlyObservableGroupedCollection_2_TKey, ReadOnlyObservableGroupedCollection_2_TElement]: ...

