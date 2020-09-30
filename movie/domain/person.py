class Person:

    def __init__(self, full_name: str) -> None:
        self._full_name = full_name

    @property
    def _full_name(self):
        return self.__full_name

    @_full_name.setter
    def _full_name(self, full_name: str) -> None:
        if full_name == "" or not isinstance(full_name, str):
            self.__full_name = None
        else:
            self.__full_name = full_name.strip()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.__full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False
        return other.__full_name == self.__full_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Person):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self.__full_name < other.__full_name

    def __hash__(self) -> int:
        return hash(self.__full_name)
