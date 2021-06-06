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
import unittest
from unittest.mock import patch, mock_open

from core.binary_io import BinaryIO
from core.type import Type


class BinaryIOTest(unittest.TestCase):
    def setUp(self) -> None:
        self.io = BinaryIO()

    def test_read(self):
        read_data = struct.pack("I", 123)
        mocked_open = mock_open(read_data=read_data)

        with patch("builtins.open", mocked_open):
            self.assertEqual(self.io._read(0, Type.UINT32), 123)
