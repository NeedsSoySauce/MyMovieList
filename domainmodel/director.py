class Director:

    def __init__(self, director_full_name: str) -> None:
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @director_full_name.setter
    def director_full_name(self, director_full_name: str) -> None:
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    def __repr__(self) -> str:
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return other.__director_full_name == self.__director_full_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Director):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self.__director_full_name < other.__director_full_name

    def __hash__(self) -> int:
        return hash(self.__director_full_name)
