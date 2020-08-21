class Person:

    def __init__(self, full_name: str) -> None:
        if full_name == "" or type(full_name) is not str:
            self._full_name = None
        else:
            self._full_name = full_name.strip()

    @property
    def full_name(self):
        return self._full_name

    def __repr__(self) -> str:
        return f"<Person {self._full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False
        return other._full_name == self._full_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Person):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self._full_name < other._full_name

    def __hash__(self) -> int:
        return hash(self._full_name)
