#      This file is part of ot-project.
#
#      ot-project is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      ot-project is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#

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
            size = value_type.size
            bytes_read = fd.read(size)

            return struct.unpack(decode_format, bytes_read)[0]

    def _write(self):
        raise NotImplementedError("write is not currently supported")
