from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class AccessibilityCheck:
    vehicle_name: str
    junkyard_name: str
    status: str
    price: int | None
    accessible: bool
    purchased: bool = False


class AvailabilityService:
    """Manual availability validation service.

    This project intentionally does not query live Roblox state. Availability is
    based only on local records entered by the player.
    """

    @staticmethod
    def filter_accessible(records: Iterable[object]) -> List[object]:
        """Keep only entries recorded as available in an accessible junkyard."""
        accessible = []
        for record in records:
            status = getattr(record, 'observed_status', None)
            junkyard = getattr(record, 'junkyard', None)
            accessible_flag = getattr(junkyard, 'unlocked', False)
            if status == 'AvailableAndAccessible' and accessible_flag:
                accessible.append(record)
        return accessible

    @staticmethod
    def classify_status(record: object) -> str:
        status = getattr(record, 'observed_status', None)
        if status == 'AvailableAndAccessible':
            return 'Available and accessible'
        if status == 'NotCurrentlyObserved':
            return 'Not currently observed'
        if status == 'InaccessibleOrLocked':
            return 'Inaccessible or locked'
        return 'Unknown'

    @staticmethod
    def should_recommend(record: object) -> bool:
        if getattr(record, 'observed_status', None) != 'AvailableAndAccessible':
            return False
        junkyard = getattr(record, 'junkyard', None)
        if junkyard is not None and not getattr(junkyard, 'unlocked', False):
            return False
        return True
