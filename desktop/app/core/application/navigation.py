from typing import Protocol


class Navigation(Protocol):
    def show_login(self) -> None:
        ...

    def show_dashboard(self) -> None:
        ...