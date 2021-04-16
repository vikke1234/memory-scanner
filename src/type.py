import enum


class Type(enum.IntEnum):
    """
    TODO: maybe add signed variants of these
    """
    UINT8 = 0
    UINT16 = 1
    UINT32 = 2
    UINT64 = 3

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
