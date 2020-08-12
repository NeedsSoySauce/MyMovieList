
class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        pass

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __hash__(self):
        pass



import unittest

class TestDirectorMethods(unittest.TestCase):

    def test_init(self):
        director1 = Director("Taika Waititi")
        self.assertEqual(repr(director1), "<Director Taika Waititi>")
        director2 = Director("")
        self.assertIsNone(director2.director_full_name)
        director3 = Director(42)
        self.assertIsNone(director3.director_full_name)
