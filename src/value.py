import typing

from type import Type


class Value:
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

    def __init__(self, address: int, value: typing.Any, typeof: Type = Type.UINT32):
        self.address = address
        self.type = typeof
        self.value = value

    def read(self):
        raise NotImplementedError("read not implemented")

    def write(self, value):
        raise NotImplementedError("write not implemented")

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
