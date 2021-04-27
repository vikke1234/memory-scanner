import unittest
from unittest import mock
from unittest.mock import Mock

import psutil

from memory import Memory
from value import Value


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

    @mock.patch.object(psutil.Process, "memory_maps", autospec=True)
    @mock.patch.object(Memory, "read", autospec=True)
    def test_scan(self, read_mock: Mock, mem_map_mock: Mock):
        read_mock.side_effect = [123, 123]
        mem_map_mock.return_value = [InternalMmap("0-8", 8, "r--w")]
        self.assertEqual(self.memory.scan("123"), [Value(0, 0, 123), Value(0, 4, 123)])

    @mock.patch.object(psutil.Process, "memory_maps", autospec=True)
    @mock.patch.object(Memory, "read", autospec=True)
    def test_scan_empty_search(self, read_mock: Mock, mem_map_mock: Mock):
        read_mock.side_effect = [123, 123]
        mem_map_mock.return_value = [InternalMmap("0-8", 8, "r--w")]
