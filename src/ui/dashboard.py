from __future__ import annotations

from typing import Any


class DashboardView:
    """Simple placeholder dashboard object for the app overview panel."""

    def __init__(self, repo: Any):
        self.repo = repo

    def render(self) -> str:
        return 'Overview Dashboard\n- Local records only\n- Manual tracking enabled'
