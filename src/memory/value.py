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

import os
import typing

from memory.binary_io import BinaryIO
from memory.type import Type


class Value(BinaryIO):
    """
    Represents a value in memory

    TODO: somehow add functionality to update it from this class, i.e. add some `.read` function
    problem for that though is that I've not figured out a good way to pass it down to each
    of the addresses, maybe I'll just add another argument to the __init__ function which is the
    file descriptor. Not sure problem with that implementation is that you can't really make Values
    outside of Memory reasonably then.

    We'll see though, I'll figure something out. For now it will simply be a way to conveniently
    store the address, type and value.

    Although since it will essentially read ~8 bytes max on average per say 100ms, it will be a
    pretty insignificant slowdown to open/close the file on read to update the value, a good idea
    would probably be to pass the pid of the process to this class each time.

    """

    def __init__(self, pid: int, address: int, value: typing.Any, typeof: Type = Type.UINT32):
        """

        :param pid: pid of the process the value belongs to
        :param address: address of the value
        :param value:
        :param typeof:
        """
        super().__init__(pid)
        self.address = address
        self.type = typeof
        self.value = value
        self.previous_value = value

    def read(self):
        """
        reads a memory address and updates the value
        :return: value read
        """
        if not os.path.isfile(f"/proc/{self.pid}/mem"):
            return self.value
        self.value = super()._read(self.address, self.type)
        return self.value

    def write(self, address):
        pass

    def __eq__(self, other):
        """
        compares two values
        :param other:
        :return: returns true if the type and address match
        """
        if isinstance(other, Value):
            return self.type == other.type and self.address == other.address
        return self.value == other

    def __str__(self):
        return str(self.value)
