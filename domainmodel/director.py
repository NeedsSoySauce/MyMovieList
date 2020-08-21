from .person import Person


class Director(Person):

    @property
    def director_full_name(self) -> str:
        return self._full_name

    @director_full_name.setter
    def director_full_name(self, director_full_name: str) -> None:
        if director_full_name == "" or type(director_full_name) is not str:
            self._full_name = None
        else:
            self._full_name = director_full_name.strip()

    def __repr__(self) -> str:
        return f"<Director {self._full_name}>"
