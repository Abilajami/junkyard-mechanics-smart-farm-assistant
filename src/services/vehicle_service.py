from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class VehicleDTO:
    id: Optional[int]
    name: str
    tier: Optional[str]
    category: Optional[str]
    purchase_price: Optional[int]
    resale_price: Optional[int]
    repair_cost: Optional[int]
    junkyard_location: Optional[str]
    availability_status: Optional[str]
    collection_status: Optional[str]
    data_source: Optional[str]
    last_verified: Optional[datetime]
    notes: Optional[str]


class VehicleService:
    def __init__(self, repo):
        self.repo = repo

    def create(self, dto: VehicleDTO):
        kwargs = dto.__dict__.copy()
        kwargs.pop('id', None)
        return self.repo.add_vehicle(**kwargs)

    def list(self):
        return self.repo.list_vehicles()

    def find_by_name(self, name: str):
        return self.repo.get_vehicle_by_name(name)
