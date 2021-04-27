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

import enum


class Type(enum.IntEnum):
    """
    TODO: maybe add signed variants of these
    """
    UINT8 = 0
    UINT16 = 1
    UINT32 = 2
    UINT64 = 3

    @property
    def size(self):
        """
        :return: gets the size of a type in bytes
        """
        return 2**self.value

    def get_format(self):
        """
        :return: the struct format for the given type
        """
        type_to_format = {Type.UINT8: "B", Type.UINT16: "H",
                          Type.UINT32: "I", Type.UINT64: "Q"}
        return type_to_format[self]

    def parse_value(self, value_str: str, ishex=False):
        """
        parses a given value for the type

        TODO: make it parse floats when I decide to support it

        :param value_str: string for the value
        :param ishex: if the value is in hex
        :return: returns the correct value as a non string
        """
        if self.value < 4:
            return int(value_str, 16 if ishex else 10)
        return None
