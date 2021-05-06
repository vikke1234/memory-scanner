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
import typing
from abc import ABC

import psutil

from memory.binary_io import BinaryIO
from memory.type import Type
from memory.value import Value


def _get_pid(name: str) -> int:
    """
    Tries to find a process by a given name
    :param name: name of the process
    :return: pid of the process or None if not found
    """
    for proc in psutil.process_iter():
        if name in proc.name():
            return proc.pid
    return 0


class Memory(BinaryIO, ABC):
    """
    This class is for reading/writing to another process, optimally you'd probably map the pages
    you wanted to read/write to the current process but we'll see, initially I'll use
    /proc/{pid}/maps

    It's quite unlikely that this class will receive unit tests since it's very easy to manually
    test this but quite hard to make automatic tests for it. If it will, it will probably use mocks
    """

    def __init__(self):
        """
        NOTE: if you give the name it tries to find a process by that name but it may get it wrong

        :param pid: pid or name of process
        """
        super().__init__()
        self.pid: int = 0
        self.memory: typing.BinaryIO = None
        self.process: psutil.Process = None
        self.entries: typing.List[Value] = None

    def attach(self, pid: int):
        self.pid = pid
        self.memory = open(f"/proc/{pid}/mem", "r+b")
        self.process = psutil.Process(pid)

    def detach(self):
        """
        detaches itself from an attached process
        """
        if self.memory is not None:
            self.memory.close()
        self.memory = None
        self.process = None
        self.pid = 0

    def read(self, address: int, type_: Type) -> typing.Any:
        """
        read size bytes from the processes memory
        :param address: address to read from
        :param type_: the type to look for
        :param size: bytes to read
        :return: the bytes
        """
        self.memory.seek(int(address))
        buf = self.memory.read(type_.size)
        return struct.unpack(type_.get_format(), buf)[0]

    def write(self, address: int, data: typing.Any) -> None:
        """
        tries to write to a given memory address

        :param address: address of to write to
        :param data: data to write
        :return:
        """
        self.memory.seek(int(address))
        self.memory.write(data)

    def progress(self):
        """
        this will be for the eventual progress bar
        :return:
        """
        raise NotImplementedError("progress not implemented")

    def reset_scan(self):
        """
        resets the current search results
        :return: None
        """
        self.entries = None

    def scan(self, value: typing.Any, value_type: Type = Type.UINT32, aligned: bool = True):
        """
        scans the memory for a given number
        TODO: add more configuration of what to search, e.g. only look in stack, non executables etc
        also, threading

        NOTE: this could probably read a page at a time, I'll have to do performance tests though
        this should also be optimized a lot more, wastes quite a lot of memory currently as it
        creates a new list each time it filters the results though on "new" computers it would
        probably not be an issue

        :param value: value to compare to
        :param value_type: type of the value
        :param aligned: if search should be aligned or not, ignored if not initial scan
        :return:
        """
        if isinstance(value, str):
            if value == "":
                return self.entries
            value = value_type.parse_value(value)

        if self.entries is None:
            return self._scan_initial(value, value_type, aligned)

        return self._scan_cull(value)

    def _scan_initial(self, value: typing.Any, value_type: Type, aligned: bool = True):
        """
        initial scanning, creates the first list which then will be culled down
        :param value: value to look for
        :param value_type: the type of the value
        :param aligned: whether or not the search will be aligned or not
        :return: a list of entries found
        """
        offset = value_type.size if aligned else 1
        self.entries = []

        for mem_map in self.process.memory_maps(grouped=False):
            if mem_map.path in ("[vvar]", "[vsyscall]") or "r" not in mem_map.perms:
                # There seems to be some bug that you cannot read from vvar from an
                # outside process
                continue

            print("scanning range:", mem_map.addr)
            addr = int(mem_map.addr.split("-")[0], 16)
            map_size = int(mem_map.size)

            for i in range(0, map_size, offset):
                read_value = self.read(addr + i, value_type)

                if read_value == value:
                    self.entries.append(Value(self.pid, addr + i, read_value, value_type))

        return self.entries

    def _scan_cull(self, value: typing.Any):
        if self.entries is None:
            return []
        new_list: typing.List[Value] = []

        for entry in self.entries:
            # doesn't use it's own read function since it requires opening a new fd and since
            # we want it to be as fast as possible, we don't use it.
            new_value = self.read(entry.address, entry.type)

            if new_value == value:
                entry.previous_value = value
                new_list.append(entry)

        self.entries = new_list
        return self.entries
