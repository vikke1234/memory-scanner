import struct
from abc import ABC, abstractmethod

from type import Type


class BinaryIO(ABC):
    def __init__(self, pid: int = 0):
        self.pid = pid

    def _read(self, address: int, value_type: Type):
        """
        reads from a given address
        :param address: address to read from
        :param value_type: expected type
        :return: returns what ever value it read after unpacking
        """
        with open(f"/proc/{self.pid}/mem", "rb") as fd:
            fd.seek(address)
            decode_format = value_type.get_format()
            size = value_type.size()
            bytes_read = fd.read(size)

            return struct.unpack(decode_format, bytes_read)[0]

    def _write(self):
        raise NotImplementedError("write is not currently supported")
