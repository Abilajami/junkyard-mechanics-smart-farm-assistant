from __future__ import annotations

from typing import Any, List, Dict


def filter_accessible(candidates: List[Any]) -> List[Any]:
    """Return only vehicles whose availability status indicates accessible and available."""
    return [v for v in candidates if getattr(v, 'availability_status', None) == 'RecordedAvailable']


def estimate_profit(vehicle: Any) -> Dict[str, Any]:
    """Return a simple estimate based on verified data fields only."""
    missing = []
    for key in ('resale_price', 'purchase_price', 'repair_cost'):
        if getattr(vehicle, key, None) is None:
            missing.append(key)
    if missing:
        return {'vehicle': vehicle.name, 'estimate': None, 'missing': missing}

    estimate = (vehicle.resale_price or 0) - (vehicle.purchase_price or 0) - (vehicle.repair_cost or 0)
    return {'vehicle': vehicle.name, 'estimate': estimate, 'missing': []}
