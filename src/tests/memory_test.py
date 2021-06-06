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
from unittest.mock import Mock, mock_open, patch

import psutil

from core.memory import Memory
from core.value import Value


class InternalMmap:
    def __init__(self, addr, size, perms):
        self.path = ""
        self.addr = addr
        self.size = size
        self.perms = perms


class MemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.memory = Memory()
        # just attach to own process, we're overriding the read values anyway
        self.memory.process = psutil.Process()

    @patch.object(psutil.Process, "memory_maps", autospec=True)
    @patch.object(Memory, "read", autospec=True)
    def test_scan(self, read_mock: Mock, mem_map_mock: Mock):
        read_mock.side_effect = [123, 123]
        mem_map_mock.return_value = [InternalMmap("0-8", 8, "r--w")]
        self.assertEqual(self.memory.scan("123"), [Value(0, 0, 123), Value(0, 4, 123)])

    @patch.object(psutil.Process, "memory_maps", autospec=True)
    @patch.object(Memory, "read", autospec=True)
    def test_scan_empty_search(self, read_mock: Mock, mem_map_mock: Mock):
        read_mock.side_effect = [123, 123]
        mem_map_mock.return_value = [InternalMmap("0-8", 8, "r--w")]

    def test_scan_cull_empty(self):
        self.assertEqual(self.memory._scan_cull(Value(0, 0, 123)), [])

    def test_scan_cull(self):
        maps = [InternalMmap("0-32", 32, "r--w")]
        # 15 because 32/4 = 8, since we need twice the scan area, we have a total of 16, then we
        # append a false value too to make sure the filtering works
        packed = [Value(0, 0, 123)] * 15
        packed.append(Value(0, 0, 12))

        with patch.object(Memory, "read", side_effect=packed), \
                patch("builtins.open", mock_open()), \
                patch("psutil.Process.__init__", return_value=None), \
                patch("psutil.Process.memory_maps", return_value=maps):
            self.memory.attach(123)
            self.assertEqual(len(self.memory.scan(123)), 8)
            self.assertEqual(len(self.memory.scan(123)), 7)

    def test_attach(self):
        with patch("builtins.open", mock_open()), patch("psutil.Process.__init__",
                                                        return_value=None):
            self.memory.attach(123)
            self.assertEqual(self.memory.pid, 123)

    def test_detach(self):
        with patch("builtins.open", mock_open()), patch("psutil.Process.__init__",
                                                        return_value=None):
            self.memory.attach(123)
            self.memory.detach()
            self.assertEqual(self.memory.pid, 0)
