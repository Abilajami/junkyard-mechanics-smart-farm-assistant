from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PurchaseAdvice:
    vehicle_name: str
    tier: str | None
    location: str | None
    asking_price: int | None
    current_cash: int | None
    shortfall: int | None
    affordable: bool
    reason: str


class PurchaseService:
    """Manual purchase planning service.

    This service does not automate buying in-game and only evaluates the local
    state entered by the player.
    """

    @staticmethod
    def evaluate_purchase(vehicle: Any, current_cash: int | None) -> PurchaseAdvice:
        if vehicle is None:
            return PurchaseAdvice(
                vehicle_name='Unknown',
                tier=None,
                location=None,
                asking_price=None,
                current_cash=current_cash,
                shortfall=None,
                affordable=False,
                reason='No vehicle selected.'
            )

        price = getattr(vehicle, 'purchase_price', None)
        if price is None:
            return PurchaseAdvice(
                vehicle_name=getattr(vehicle, 'name', 'Unknown'),
                tier=getattr(vehicle, 'tier', None),
                location=getattr(vehicle, 'junkyard_location', None),
                asking_price=None,
                current_cash=current_cash,
                shortfall=None,
                affordable=False,
                reason='No verified purchase price is available.'
            )

        if current_cash is None:
            return PurchaseAdvice(
                vehicle_name=getattr(vehicle, 'name', 'Unknown'),
                tier=getattr(vehicle, 'tier', None),
                location=getattr(vehicle, 'junkyard_location', None),
                asking_price=price,
                current_cash=None,
                shortfall=None,
                affordable=False,
                reason='Current cash is unknown. Enter your cash to evaluate affordability.'
            )

        shortfall = max(0, price - current_cash)
        affordable = current_cash >= price
        reason = 'Affordable' if affordable else 'Insufficient cash for this target.'
        return PurchaseAdvice(
            vehicle_name=getattr(vehicle, 'name', 'Unknown'),
            tier=getattr(vehicle, 'tier', None),
            location=getattr(vehicle, 'junkyard_location', None),
            asking_price=price,
            current_cash=current_cash,
            shortfall=shortfall,
            affordable=affordable,
            reason=reason,
        )
