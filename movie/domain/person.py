class Person:

    def __init__(self, full_name: str) -> None:
        self._full_name = full_name

    @property
    def _full_name(self):
        return self._person_full_name

    @_full_name.setter
    def _full_name(self, full_name: str) -> None:
        if full_name == "" or not isinstance(full_name, str):
            self._person_full_name = None
        else:
            self._person_full_name = full_name.strip()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._person_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False
        return other._person_full_name == self._person_full_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Person):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self._person_full_name < other._person_full_name

    def __hash__(self) -> int:
        return hash(self._person_full_name)
