from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleCreate(BaseModel):
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

class VehicleRead(VehicleCreate):
    id: int


class VehicleService:
    def __init__(self, repo):
        self.repo = repo

    def create_vehicle(self, data: VehicleCreate):
        kwargs = data.dict()
        if kwargs.get('last_verified') is None:
            kwargs['last_verified'] = None
        v = self.repo.add_vehicle(**kwargs)
        return v

    def find_by_name(self, name: str):
        return self.repo.get_vehicle_by_name(name)

    def list_all(self):
        return self.repo.list_vehicles()
