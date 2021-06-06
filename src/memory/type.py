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

from enum import IntEnum, auto
import struct


class Type(IntEnum):
    """
    TODO: maybe add signed variants of these
    """
    UINT8 = 0
    UINT16 = auto()
    UINT32 = auto()
    UINT64 = auto()
    FLOAT = auto()
    DOUBLE = auto()

    @property
    def size(self):
        """
        :return: gets the size of a type in bytes
        """
        return self.get_format().size

    def get_format(self):
        """
        :return: the struct format for the given type
        """
        type_to_format = {Type.UINT8: "B", Type.UINT16: "H",
                          Type.UINT32: "I", Type.UINT64: "Q",
                          Type.FLOAT: "f", Type.DOUBLE: "d"}
        return struct.Struct(type_to_format[self])

    def parse_value(self, value_str: str, ishex=False):
        """
        parses a given value for the type

        TODO: make it parse floats when I decide to support it

        :param value_str: string for the value
        :param ishex: if the value is in hex
        :return: returns the correct value as a non string
        """
        # self.value is NOT a callable...
        # pylint: disable=comparison-with-callable
        if self.value < 4:
            return int(value_str, 16 if ishex else 10)
        elif self.value == Type.DOUBLE or self.value == Type.FLOAT:
            return float(value_str.replace(",","."))
        return None

    def __str__(self):
        if self.value == Type.FLOAT or self.value == Type.DOUBLE:
            return self.name.capitalize()
        return f"{self.size} Bytes"
