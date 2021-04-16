import unittest

from type import Type


class TypeTest(unittest.TestCase):
    def setUp(self) -> None:
        self._type: Type = Type.UINT32

    def test_parse_int_hex(self):
        self.assertEqual(self._type.parse_value("0x123", ishex=True), 0x123)

    def test_parse_int(self):
        self.assertEqual(self._type.parse_value("123"), 123)
