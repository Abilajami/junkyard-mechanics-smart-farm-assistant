from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class ProfitEstimate:
    vehicle_name: str
    estimate: int | None
    missing_fields: List[str]
    confidence: str
    reason: str


class ProfitCalculator:
    @staticmethod
    def calculate(vehicle: Any, other_costs: int = 0) -> ProfitEstimate:
        if vehicle is None:
            return ProfitEstimate('Unknown', None, ['vehicle'], 'Low', 'No vehicle was selected.')

        required = ['purchase_price', 'resale_price', 'repair_cost']
        missing = []
        for key in required:
            value = getattr(vehicle, key, None)
            if value is None:
                missing.append(key)

        if missing:
            return ProfitEstimate(
                vehicle_name=getattr(vehicle, 'name', 'Unknown'),
                estimate=None,
                missing_fields=missing,
                confidence='Low',
                reason='Insufficient verified data for a reliable estimate.'
            )

        estimate = (
            (getattr(vehicle, 'resale_price') or 0)
            - (getattr(vehicle, 'purchase_price') or 0)
            - (getattr(vehicle, 'repair_cost') or 0)
            - other_costs
        )
        return ProfitEstimate(
            vehicle_name=getattr(vehicle, 'name', 'Unknown'),
            estimate=estimate,
            missing_fields=[],
            confidence='High',
            reason='Estimated profit based on verified resale, purchase, and repair values.'
        )
