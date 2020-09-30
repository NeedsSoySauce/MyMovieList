class Genre:
    def __init__(self, genre_name: str) -> None:
        self.genre_name = genre_name

    @property
    def genre_name(self) -> str:
        return self._genre_name

    @genre_name.setter
    def genre_name(self, genre_name: str) -> None:
        if genre_name == "" or type(genre_name) is not str:
            self._genre_name = None
        else:
            self._genre_name = genre_name.strip()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._genre_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False
        return other._genre_name == self._genre_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Genre):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self._genre_name < other._genre_name

    def __hash__(self) -> int:
        return hash(self._genre_name)
