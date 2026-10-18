from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Vehicle
from datetime import datetime


def init_db(db_path='data.db'):
    engine = create_engine(f'sqlite:///{db_path}', echo=False, future=True)
    Base.metadata.create_all(bind=engine)
    return engine


class Repository:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine, future=True)

    def add_vehicle(self, **kwargs):
        with self.Session() as s:
            v = Vehicle(**kwargs)
            s.add(v)
            s.commit()
            s.refresh(v)
            return v

    def get_vehicle_by_name(self, name: str):
        with self.Session() as s:
            return s.query(Vehicle).filter(Vehicle.name == name).one_or_none()

    def list_vehicles(self):
        with self.Session() as s:
            return s.query(Vehicle).all()

    def seed_sample(self):
        # Placeholder: add sample vehicle if DB empty
        with self.Session() as s:
            if s.query(Vehicle).count() == 0:
                v = Vehicle(
                    name='Sample Car',
                    tier='Tier 1',
                    category='Sedan',
                    purchase_price=1000,
                    resale_price=1500,
                    repair_cost=200,
                    junkyard_location='Boneyard',
                    availability_status='RecordedAvailable',
                    collection_status='Wanted',
                    data_source='Seed',
                    last_verified=datetime.utcnow(),
                    notes='This is a seeded sample vehicle.'
                )
                s.add(v)
                s.commit()
