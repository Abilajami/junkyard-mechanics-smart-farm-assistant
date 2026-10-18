from __future__ import annotations

from typing import Any


class MainWindow:
    """Minimum viable UI wrapper for the desktop app.

    The real GUI implementation is intentionally simple and safe: it provides a
    navigation shell and does not automate any game actions.
    """

    def __init__(self, repo: Any):
        self.repo = repo
        self.title = 'Junkyard Mechanics — Smart Farm Assistant'
        self.width = 1280
        self.height = 800

    def resize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def show(self) -> None:
        return None
