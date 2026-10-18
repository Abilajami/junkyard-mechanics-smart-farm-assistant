from typing import List, Dict, Any
from src.database.models import Vehicle

# Simple farm optimizer implementing the three strategies described


def filter_accessible(candidates: List[Vehicle]) -> List[Vehicle]:
    # Only include vehicles that have availability_status recorded as 'RecordedAvailable' and have a purchase price
    out = []
    for v in candidates:
        if v.availability_status == 'RecordedAvailable':
            out.append(v)
    return out


def strategy_highest_tier(candidates: List[Vehicle]) -> List[Vehicle]:
    # Rank by tier string (assumes tiers sortable). We'll fallback to purchase_price
    return sorted(candidates, key=lambda v: (v.tier or ''), reverse=True)


def strategy_highest_price(candidates: List[Vehicle], budget: int = None) -> List[Vehicle]:
    c = [v for v in candidates if v.purchase_price is not None]
    if budget is not None:
        c = [v for v in c if v.purchase_price <= budget]
    return sorted(c, key=lambda v: v.purchase_price or 0, reverse=True)


def estimate_profit(vehicle: Vehicle) -> Dict[str, Any]:
    missing = []
    if vehicle.resale_price is None:
        missing.append('resale_price')
    if vehicle.purchase_price is None:
        missing.append('purchase_price')
    if vehicle.repair_cost is None:
        missing.append('repair_cost')

    if missing:
        return {'vehicle': vehicle, 'estimate': None, 'missing': missing}

    profit = (vehicle.resale_price or 0) - (vehicle.purchase_price or 0) - (vehicle.repair_cost or 0)
    return {'vehicle': vehicle, 'estimate': profit, 'missing': []}


def strategy_best_estimated_profit(candidates: List[Vehicle]) -> List[Dict]:
    estimates = [estimate_profit(v) for v in candidates]
    # Sort: known estimates first by profit desc, then unknowns
    known = [e for e in estimates if e['estimate'] is not None]
    unknown = [e for e in estimates if e['estimate'] is None]
    known_sorted = sorted(known, key=lambda x: x['estimate'], reverse=True)
    return known_sorted + unknown
