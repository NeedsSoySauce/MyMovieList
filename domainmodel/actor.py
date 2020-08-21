from typing import Set


class Actor:
    def __init__(self, actor_full_name: str) -> None:
        if actor_full_name == "" or type(actor_full_name) is not str:
            self._actor_full_name = None
        else:
            self._actor_full_name = actor_full_name.strip()
        self._colleagues: Set[Actor] = set()

    @property
    def colleagues(self) -> Set['Actor']:
        return self._colleagues

    @property
    def actor_full_name(self) -> str:
        return self._actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, actor_full_name: str) -> None:
        if actor_full_name == "" or type(actor_full_name) is not str:
            self._actor_full_name = None
        else:
            self._actor_full_name = actor_full_name.strip()

    def __repr__(self) -> str:
        return f"<Actor {self._actor_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return other._actor_full_name == self._actor_full_name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Actor):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self._actor_full_name < other._actor_full_name

    def __hash__(self) -> int:
        return hash(self._actor_full_name)

    def add_actor_colleague(self, colleague: 'Actor') -> None:
        if not isinstance(colleague, Actor):
            raise TypeError(f"'colleague' must be of type '{type(self).__name__}' but was '{type(colleague).__name__}'")
        self._colleagues.add(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor') -> bool:
        if not isinstance(colleague, Actor):
            raise TypeError(f"'colleague' must be of type '{type(self).__name__}' but was '{type(colleague).__name__}'")
        return colleague in self._colleagues
