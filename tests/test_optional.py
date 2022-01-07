import unittest

from optional_python import Optional

class OptionalTest(unittest.TestCase):

    def test_private_constructor(self):
        obj:str = "abcd"
        self.assertRaises(TypeError, lambda _: Optional(obj)) 

    def test_filled_optional(self):
        obj:str = "abcd"
        optional:Optional[str] = Optional.of(obj)
        self.assertTrue(optional.is_present(), "Optional should be present")
        self.assertEqual("abcd", optional.get())

    def test_empty_optional(self):
        optional:Optional[str] = Optional.empty()
        self.assertFalse(optional.is_present())
        self.assertRaises(TypeError, optional.get)

    def test_map(self):
        obj:str = "abcd"
        other_obj = Optional.of(obj).map(str.upper).or_else_throw()
        self.assertEqual("ABCD", other_obj)

    def test_map_empty(self):
        obj:str = None
        opt = Optional.of_nullable(obj).map(str.upper)
        self.assertTrue(opt.is_empty())