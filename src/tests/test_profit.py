import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Vehicle
from src.services.farm_optimizer import filter_accessible, estimate_profit


@pytest.fixture
def in_memory_repo():
    engine = create_engine('sqlite:///:memory:', future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    s = Session()
    v1 = Vehicle(name='Cheap Car', tier='1', purchase_price=100, resale_price=150, repair_cost=20, availability_status='RecordedAvailable')
    v2 = Vehicle(name='Expensive Car', tier='3', purchase_price=2000, resale_price=2800, repair_cost=300, availability_status='RecordedAvailable')
    v3 = Vehicle(name='Unknown Car', tier='2', purchase_price=None, resale_price=None, repair_cost=None, availability_status='RecordedUnAvailable')
    s.add_all([v1, v2, v3])
    s.commit()
    yield s
    s.close()


def test_filter_accessible(in_memory_repo):
    session = in_memory_repo
    vehicles = session.query(Vehicle).all()
    filtered = filter_accessible(vehicles)
    assert len(filtered) == 2


def test_estimate_profit(in_memory_repo):
    session = in_memory_repo
    v = session.query(Vehicle).filter(Vehicle.name=='Expensive Car').one()
    res = estimate_profit(v)
    assert res['estimate'] == 2800 - 2000 - 300
