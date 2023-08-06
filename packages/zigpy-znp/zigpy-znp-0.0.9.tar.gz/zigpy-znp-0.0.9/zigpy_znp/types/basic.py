import enum
import typing


class Bytes(bytes):
    def serialize(self) -> "Bytes":
        return self

    @classmethod
    def deserialize(cls, data: bytes) -> typing.Tuple["Bytes", bytes]:
        return cls(data), b""

    def __repr__(self) -> str:
        # Reading byte sequences like \x200\x21 is extremely annoying
        # compared to \x20\x30\x21
        escaped = "".join(f"\\x{b:02X}" for b in self)

        return f"b'{escaped}'"

    __str__ = __repr__


class TrailingBytes(Bytes):
    """
    Bytes must occur at the very end of a parameter list for easy parsing.
    """

    pass


def serialize_list(objects) -> Bytes:
    return Bytes(b"".join([o.serialize() for o in objects]))


class FixedIntType(int):
    _signed = None
    _size = None

    def _concrete_new(cls, value=0):
        instance = super().__new__(cls, value)
        instance.serialize()

        return instance

    def __new__(cls, value):
        raise TypeError(f"Instances of abstract type {cls} cannot be created")

    def __init_subclass__(cls, signed=None, size=None, **kwargs) -> None:
        if signed is not None:
            cls._signed = signed

        if size is not None:
            cls._size = size

        # XXX: The enum module uses the first class with `__new__` in its `__dict__`
        #      as the member type. We have to give each subclass its own `__new__`.
        if signed is not None or size is not None:
            cls.__new__ = cls._concrete_new

        super().__init_subclass__(**kwargs)

    def serialize(self) -> bytes:
        try:
            return self.to_bytes(self._size, "little", signed=self._signed)
        except OverflowError as e:
            # OverflowError is not a subclass of ValueError, making it annoying to catch
            raise ValueError(str(e)) from e

    @classmethod
    def deserialize(cls, data: bytes) -> typing.Tuple["int_t", bytes]:
        if len(data) < cls._size:
            raise ValueError(f"Data is too short to contain {cls._size} bytes")

        r = cls.from_bytes(data[: cls._size], "little", signed=cls._signed)
        data = data[cls._size :]
        return r, data


class uint_t(FixedIntType, signed=False):
    pass


class int_t(FixedIntType, signed=True):
    pass


class int8s(int_t, size=1):
    pass


class int16s(int_t, size=2):
    pass


class int24s(int_t, size=3):
    pass


class int32s(int_t, size=4):
    pass


class int40s(int_t, size=5):
    pass


class int48s(int_t, size=6):
    pass


class int56s(int_t, size=7):
    pass


class int64s(int_t, size=8):
    pass


class uint8_t(uint_t, size=1):
    pass


class uint16_t(uint_t, size=2):
    pass


class uint24_t(uint_t, size=3):
    pass


class uint32_t(uint_t, size=4):
    pass


class uint40_t(uint_t, size=5):
    pass


class uint48_t(uint_t, size=6):
    pass


class uint56_t(uint_t, size=7):
    pass


class uint64_t(uint_t, size=8):
    pass


class ShortBytes(Bytes):
    _header = uint8_t

    def serialize(self) -> "Bytes":
        return self._header(len(self)).serialize() + self

    @classmethod
    def deserialize(cls, data: bytes) -> typing.Tuple[Bytes, bytes]:
        length, data = cls._header.deserialize(data)
        if length > len(data):
            raise ValueError(f"Data is too short to contain {length} bytes of data")
        return cls(data[:length]), data[length:]


class LongBytes(ShortBytes):
    _header = uint16_t


class TypedListMeta(list):
    _item_type = None
    _length = None

    def serialize(self) -> bytes:
        if self._length is not None and len(self) != self._length:
            raise ValueError(
                f"Invalid length for {self!r}: expected {self._length}, got {len(self)}"
            )

        return b"".join([self._item_type(i).serialize() for i in self])

    @classmethod
    def deserialize(cls, data: bytes):
        raise NotImplementedError()  # pragma: no cover


class LVList(TypedListMeta):
    def __init_subclass__(cls, *, item_type, length_type) -> None:
        super().__init_subclass__()
        cls._item_type = item_type
        cls._header = length_type

    def serialize(self) -> bytes:
        assert self._item_type is not None
        return self._header(len(self)).serialize() + super().serialize()

    @classmethod
    def deserialize(cls, data: bytes):
        assert cls._item_type is not None
        length, data = cls._header.deserialize(data)
        r = cls()
        for i in range(length):
            item, data = cls._item_type.deserialize(data)
            r.append(item)
        return r, data


class FixedList(TypedListMeta):
    def __init_subclass__(cls, *, item_type, length) -> None:
        super().__init_subclass__()
        cls._item_type = item_type
        cls._length = length

    @classmethod
    def deserialize(cls, data):
        assert cls._item_type is not None
        r = cls()
        for i in range(cls._length):
            item, data = cls._item_type.deserialize(data)
            r.append(item)
        return r, data


class HexRepr:
    def __str__(self):
        return ("0x{:0" + str(self._size * 2) + "X}").format(self)

    __repr__ = __str__


class EnumIntFlagMixin:
    """
    Enum does not allow multiple base classes. We turn enum.IntFlag into a mixin, since
    it really doesn't depend on the base class specifically being `int`.
    """

    # Rebind classmethods to our own class
    _missing_ = classmethod(enum.IntFlag._missing_.__func__)
    _create_pseudo_member_ = classmethod(enum.IntFlag._create_pseudo_member_.__func__)

    __or__ = enum.IntFlag.__or__
    __and__ = enum.IntFlag.__and__
    __xor__ = enum.IntFlag.__xor__
    __ror__ = enum.IntFlag.__ror__
    __rand__ = enum.IntFlag.__rand__
    __rxor__ = enum.IntFlag.__rxor__
    __invert__ = enum.IntFlag.__invert__


class enum_uint8(uint8_t, enum.Enum):
    pass


class enum_uint16(uint16_t, enum.Enum):
    pass


class enum_uint24(uint24_t, enum.Enum):
    pass


class enum_uint32(uint32_t, enum.Enum):
    pass


class enum_uint40(uint40_t, enum.Enum):
    pass


class enum_uint48(uint48_t, enum.Enum):
    pass


class enum_uint56(uint56_t, enum.Enum):
    pass


class enum_uint64(uint64_t, enum.Enum):
    pass


class enum_flag_uint8(EnumIntFlagMixin, uint8_t, enum.Flag):
    pass


class enum_flag_uint16(EnumIntFlagMixin, uint16_t, enum.Flag):
    pass


class enum_flag_uint24(EnumIntFlagMixin, uint24_t, enum.Flag):
    pass


class enum_flag_uint32(EnumIntFlagMixin, uint32_t, enum.Flag):
    pass


class enum_flag_uint40(EnumIntFlagMixin, uint40_t, enum.Flag):
    pass


class enum_flag_uint48(EnumIntFlagMixin, uint48_t, enum.Flag):
    pass


class enum_flag_uint56(EnumIntFlagMixin, uint56_t, enum.Flag):
    pass


class enum_flag_uint64(EnumIntFlagMixin, uint64_t, enum.Flag):
    pass
