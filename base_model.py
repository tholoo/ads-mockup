class BaseAdvertising:
    def __init__(self, id: int, name: str) -> None:
        self._id = id
        self._name = name
        self._clicks = 0
        self._views = 0

    def __str__(self) -> str:
        return f"{self._name} has {self._clicks} clicks and {self._views} views"

    def describe_me(self) -> str:
        return "This is a base class for all advertising entities"

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_clicks(self) -> int:
        return self._clicks

    def get_views(self) -> int:
        return self._views

    def inc_clicks(self) -> None:
        self._clicks += 1

    def inc_views(self) -> None:
        self._views += 1
