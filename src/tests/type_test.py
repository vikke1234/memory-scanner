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

import unittest

from memory.type import Type


class TypeTest(unittest.TestCase):
    def setUp(self) -> None:
        self._type: Type = Type.UINT32

    def test_parse_int_hex(self):
        self.assertEqual(self._type.parse_value("0x123", ishex=True), 0x123)

    def test_parse_int(self):
        self.assertEqual(self._type.parse_value("123"), 123)

    def test_get_format(self):
        self.assertEqual(self._type.get_format(), "I")
