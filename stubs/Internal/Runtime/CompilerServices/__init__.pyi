import typing, clr, abc

class Unsafe(abc.ABC):
    @staticmethod
    def InitBlockUnaligned(startAddress: clr.Reference[int], value: int, byteCount: int) -> None: ...
    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __getitem__(self, t:typing.Type[Add_1_T1]) -> Add_1[Add_1_T1]: ...

        Add_1_T1 = typing.TypeVar('Add_1_T1')
        class Add_1(typing.Generic[Add_1_T1]):
            Add_1_T = Unsafe.Add_MethodGroup.Add_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[None], elementOffset: int) -> clr.Reference[None]:...
            @typing.overload
            def __call__(self, source: clr.Reference[Add_1_T], elementOffset: int) -> clr.Reference[Add_1_T]:...
            # Method Add(source : T&, elementOffset : IntPtr) was skipped since it collides with above method


    # Skipped AddByteOffset due to it being static, abstract and generic.

    AddByteOffset : AddByteOffset_MethodGroup
    class AddByteOffset_MethodGroup:
        def __getitem__(self, t:typing.Type[AddByteOffset_1_T1]) -> AddByteOffset_1[AddByteOffset_1_T1]: ...

        AddByteOffset_1_T1 = typing.TypeVar('AddByteOffset_1_T1')
        class AddByteOffset_1(typing.Generic[AddByteOffset_1_T1]):
            AddByteOffset_1_T = Unsafe.AddByteOffset_MethodGroup.AddByteOffset_1_T1
            def __call__(self, source: clr.Reference[AddByteOffset_1_T], byteOffset: int) -> clr.Reference[AddByteOffset_1_T]:...


    # Skipped AreSame due to it being static, abstract and generic.

    AreSame : AreSame_MethodGroup
    class AreSame_MethodGroup:
        def __getitem__(self, t:typing.Type[AreSame_1_T1]) -> AreSame_1[AreSame_1_T1]: ...

        AreSame_1_T1 = typing.TypeVar('AreSame_1_T1')
        class AreSame_1(typing.Generic[AreSame_1_T1]):
            AreSame_1_T = Unsafe.AreSame_MethodGroup.AreSame_1_T1
            def __call__(self, left: clr.Reference[AreSame_1_T], right: clr.Reference[AreSame_1_T]) -> bool:...


    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_TFrom = Unsafe.As_MethodGroup.As_2_T1
            As_2_TTo = Unsafe.As_MethodGroup.As_2_T2
            def __call__(self, source: clr.Reference[As_2_TFrom]) -> clr.Reference[As_2_TTo]:...

        @typing.overload
        def __getitem__(self, t:typing.Type[As_1_T1]) -> As_1[As_1_T1]: ...

        As_1_T1 = typing.TypeVar('As_1_T1')
        class As_1(typing.Generic[As_1_T1]):
            As_1_T = Unsafe.As_MethodGroup.As_1_T1
            def __call__(self, value: typing.Any) -> As_1_T:...


    # Skipped AsPointer due to it being static, abstract and generic.

    AsPointer : AsPointer_MethodGroup
    class AsPointer_MethodGroup:
        def __getitem__(self, t:typing.Type[AsPointer_1_T1]) -> AsPointer_1[AsPointer_1_T1]: ...

        AsPointer_1_T1 = typing.TypeVar('AsPointer_1_T1')
        class AsPointer_1(typing.Generic[AsPointer_1_T1]):
            AsPointer_1_T = Unsafe.AsPointer_MethodGroup.AsPointer_1_T1
            def __call__(self, value: clr.Reference[AsPointer_1_T]) -> clr.Reference[None]:...


    # Skipped AsRef due to it being static, abstract and generic.

    AsRef : AsRef_MethodGroup
    class AsRef_MethodGroup:
        def __getitem__(self, t:typing.Type[AsRef_1_T1]) -> AsRef_1[AsRef_1_T1]: ...

        AsRef_1_T1 = typing.TypeVar('AsRef_1_T1')
        class AsRef_1(typing.Generic[AsRef_1_T1]):
            AsRef_1_T = Unsafe.AsRef_MethodGroup.AsRef_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[None]) -> clr.Reference[AsRef_1_T]:...
            @typing.overload
            def __call__(self, source: clr.Reference[AsRef_1_T]) -> clr.Reference[AsRef_1_T]:...


    # Skipped ByteOffset due to it being static, abstract and generic.

    ByteOffset : ByteOffset_MethodGroup
    class ByteOffset_MethodGroup:
        def __getitem__(self, t:typing.Type[ByteOffset_1_T1]) -> ByteOffset_1[ByteOffset_1_T1]: ...

        ByteOffset_1_T1 = typing.TypeVar('ByteOffset_1_T1')
        class ByteOffset_1(typing.Generic[ByteOffset_1_T1]):
            ByteOffset_1_T = Unsafe.ByteOffset_MethodGroup.ByteOffset_1_T1
            def __call__(self, origin: clr.Reference[ByteOffset_1_T], target: clr.Reference[ByteOffset_1_T]) -> int:...


    # Skipped IsAddressGreaterThan due to it being static, abstract and generic.

    IsAddressGreaterThan : IsAddressGreaterThan_MethodGroup
    class IsAddressGreaterThan_MethodGroup:
        def __getitem__(self, t:typing.Type[IsAddressGreaterThan_1_T1]) -> IsAddressGreaterThan_1[IsAddressGreaterThan_1_T1]: ...

        IsAddressGreaterThan_1_T1 = typing.TypeVar('IsAddressGreaterThan_1_T1')
        class IsAddressGreaterThan_1(typing.Generic[IsAddressGreaterThan_1_T1]):
            IsAddressGreaterThan_1_T = Unsafe.IsAddressGreaterThan_MethodGroup.IsAddressGreaterThan_1_T1
            def __call__(self, left: clr.Reference[IsAddressGreaterThan_1_T], right: clr.Reference[IsAddressGreaterThan_1_T]) -> bool:...


    # Skipped IsAddressLessThan due to it being static, abstract and generic.

    IsAddressLessThan : IsAddressLessThan_MethodGroup
    class IsAddressLessThan_MethodGroup:
        def __getitem__(self, t:typing.Type[IsAddressLessThan_1_T1]) -> IsAddressLessThan_1[IsAddressLessThan_1_T1]: ...

        IsAddressLessThan_1_T1 = typing.TypeVar('IsAddressLessThan_1_T1')
        class IsAddressLessThan_1(typing.Generic[IsAddressLessThan_1_T1]):
            IsAddressLessThan_1_T = Unsafe.IsAddressLessThan_MethodGroup.IsAddressLessThan_1_T1
            def __call__(self, left: clr.Reference[IsAddressLessThan_1_T], right: clr.Reference[IsAddressLessThan_1_T]) -> bool:...


    # Skipped IsNullRef due to it being static, abstract and generic.

    IsNullRef : IsNullRef_MethodGroup
    class IsNullRef_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNullRef_1_T1]) -> IsNullRef_1[IsNullRef_1_T1]: ...

        IsNullRef_1_T1 = typing.TypeVar('IsNullRef_1_T1')
        class IsNullRef_1(typing.Generic[IsNullRef_1_T1]):
            IsNullRef_1_T = Unsafe.IsNullRef_MethodGroup.IsNullRef_1_T1
            def __call__(self, source: clr.Reference[IsNullRef_1_T]) -> bool:...


    # Skipped NullRef due to it being static, abstract and generic.

    NullRef : NullRef_MethodGroup
    class NullRef_MethodGroup:
        def __getitem__(self, t:typing.Type[NullRef_1_T1]) -> NullRef_1[NullRef_1_T1]: ...

        NullRef_1_T1 = typing.TypeVar('NullRef_1_T1')
        class NullRef_1(typing.Generic[NullRef_1_T1]):
            NullRef_1_T = Unsafe.NullRef_MethodGroup.NullRef_1_T1
            def __call__(self) -> clr.Reference[NullRef_1_T]:...


    # Skipped Read due to it being static, abstract and generic.

    Read : Read_MethodGroup
    class Read_MethodGroup:
        def __getitem__(self, t:typing.Type[Read_1_T1]) -> Read_1[Read_1_T1]: ...

        Read_1_T1 = typing.TypeVar('Read_1_T1')
        class Read_1(typing.Generic[Read_1_T1]):
            Read_1_T = Unsafe.Read_MethodGroup.Read_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[int]) -> Read_1_T:...
            @typing.overload
            def __call__(self, source: clr.Reference[None]) -> Read_1_T:...


    # Skipped ReadUnaligned due to it being static, abstract and generic.

    ReadUnaligned : ReadUnaligned_MethodGroup
    class ReadUnaligned_MethodGroup:
        def __getitem__(self, t:typing.Type[ReadUnaligned_1_T1]) -> ReadUnaligned_1[ReadUnaligned_1_T1]: ...

        ReadUnaligned_1_T1 = typing.TypeVar('ReadUnaligned_1_T1')
        class ReadUnaligned_1(typing.Generic[ReadUnaligned_1_T1]):
            ReadUnaligned_1_T = Unsafe.ReadUnaligned_MethodGroup.ReadUnaligned_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[int]) -> ReadUnaligned_1_T:...
            @typing.overload
            def __call__(self, source: clr.Reference[None]) -> ReadUnaligned_1_T:...


    # Skipped SizeOf due to it being static, abstract and generic.

    SizeOf : SizeOf_MethodGroup
    class SizeOf_MethodGroup:
        def __getitem__(self, t:typing.Type[SizeOf_1_T1]) -> SizeOf_1[SizeOf_1_T1]: ...

        SizeOf_1_T1 = typing.TypeVar('SizeOf_1_T1')
        class SizeOf_1(typing.Generic[SizeOf_1_T1]):
            SizeOf_1_T = Unsafe.SizeOf_MethodGroup.SizeOf_1_T1
            def __call__(self) -> int:...


    # Skipped SkipInit due to it being static, abstract and generic.

    SkipInit : SkipInit_MethodGroup
    class SkipInit_MethodGroup:
        def __getitem__(self, t:typing.Type[SkipInit_1_T1]) -> SkipInit_1[SkipInit_1_T1]: ...

        SkipInit_1_T1 = typing.TypeVar('SkipInit_1_T1')
        class SkipInit_1(typing.Generic[SkipInit_1_T1]):
            SkipInit_1_T = Unsafe.SkipInit_MethodGroup.SkipInit_1_T1
            def __call__(self, value: clr.Reference[SkipInit_1_T]) -> None:...


    # Skipped Write due to it being static, abstract and generic.

    Write : Write_MethodGroup
    class Write_MethodGroup:
        def __getitem__(self, t:typing.Type[Write_1_T1]) -> Write_1[Write_1_T1]: ...

        Write_1_T1 = typing.TypeVar('Write_1_T1')
        class Write_1(typing.Generic[Write_1_T1]):
            Write_1_T = Unsafe.Write_MethodGroup.Write_1_T1
            @typing.overload
            def __call__(self, destination: clr.Reference[int], value: Write_1_T) -> None:...
            @typing.overload
            def __call__(self, destination: clr.Reference[None], value: Write_1_T) -> None:...


    # Skipped WriteUnaligned due to it being static, abstract and generic.

    WriteUnaligned : WriteUnaligned_MethodGroup
    class WriteUnaligned_MethodGroup:
        def __getitem__(self, t:typing.Type[WriteUnaligned_1_T1]) -> WriteUnaligned_1[WriteUnaligned_1_T1]: ...

        WriteUnaligned_1_T1 = typing.TypeVar('WriteUnaligned_1_T1')
        class WriteUnaligned_1(typing.Generic[WriteUnaligned_1_T1]):
            WriteUnaligned_1_T = Unsafe.WriteUnaligned_MethodGroup.WriteUnaligned_1_T1
            @typing.overload
            def __call__(self, destination: clr.Reference[int], value: WriteUnaligned_1_T) -> None:...
            @typing.overload
            def __call__(self, destination: clr.Reference[None], value: WriteUnaligned_1_T) -> None:...



