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
import operator
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

    def read(self, address: int, size: int) -> typing.Any:
        """
        read size bytes from the processes memory
        :param address: address to read from
        :param size: bytes to read
        :param format_: struct format string

        :return: the bytes
        """
        self.memory.seek(int(address))
        buf = self.memory.read(size)
        return buf

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

    def scan(self, value: typing.Any, value_type: Type = Type.UINT32,
             match_function: typing.Callable = operator.eq):
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
            return self._scan_initial(value, value_type, match_function)

        return self._scan_cull(value, match_function)

    def _scan_initial(self, value: typing.Any, value_type: Type, match_function: typing.Callable):
        """
        initial scanning, creates the first list which then will be culled down
        :param value: value to look for
        :param value_type: the type of the value
        :param aligned: whether or not the search will be aligned or not
        :return: a list of entries found
        """
        self.entries = []
        fmt = value_type.get_format()
        size = value_type.size
        for mem_map in self.process.memory_maps(grouped=False):
            if mem_map.path in ("[vvar]", "[vsyscall]") or "r" not in mem_map.perms:
                # There seems to be some bug that you cannot read from vvar from an
                # outside process
                continue

            print("scanning range:", mem_map.addr)
            addr = int(mem_map.addr.split("-")[0], 16)
            map_size = int(mem_map.size)
            read_bytes = self.read(addr, map_size)

            self.entries.extend([Value(self.pid, addr + i * size, read_value[0], value_type)
                                 for i, read_value
                                 in enumerate(fmt.iter_unpack(read_bytes)) if
                                 match_function(read_value[0], value)])
        return self.entries

    def _scan_cull(self, value: typing.Any, match_function: typing.Callable):
        if self.entries is None:
            return []
        new_list: typing.List[Value] = []
        # since the type can be assumed to be the same for all, since you can't change the type
        # after first scan, we'll simply check what the first one is, that way we will improve
        # performance, since python doens't know jack about how to optimize anything
        size = self.entries[0].type.size
        fmt = self.entries[0].type.get_format()

        for entry in self.entries:
            # doesn't use it's own read function since it requires opening a new fd and since
            # we want it to be as fast as possible, we don't use it.
            new_value = fmt.unpack(self.read(entry.address, size))[0]

            if match_function(new_value, value):
                entry.previous_value = new_value
                new_list.append(entry)

        self.entries = new_list
        return self.entries
