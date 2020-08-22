from .person import Person


class Director(Person):

    @property
    def director_full_name(self) -> str:
        return self._full_name

    @director_full_name.setter
    def director_full_name(self, director_full_name: str) -> None:
        self._full_name = director_full_name
