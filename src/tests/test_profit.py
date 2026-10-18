import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Vehicle
from src.services.availability_service import AvailabilityService
from src.services.purchase_service import PurchaseService
from src.services.profit_calculator import ProfitCalculator
from src.services.farm_optimizer import filter_accessible, estimate_profit


@pytest.fixture
def in_memory_repo():
    engine = create_engine('sqlite:///:memory:', future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    session = Session()

    v1 = Vehicle(
        name='Cheap Car',
        tier='1',
        purchase_price=100,
        resale_price=150,
        repair_cost=20,
        availability_status='RecordedAvailable',
    )
    v2 = Vehicle(
        name='Expensive Car',
        tier='3',
        purchase_price=2000,
        resale_price=2800,
        repair_cost=300,
        availability_status='RecordedAvailable',
    )
    v3 = Vehicle(
        name='Unknown Car',
        tier='2',
        purchase_price=None,
        resale_price=None,
        repair_cost=None,
        availability_status='RecordedUnAvailable',
    )
    session.add_all([v1, v2, v3])
    session.commit()
    yield session
    session.close()


def test_filter_accessible(in_memory_repo):
    vehicles = in_memory_repo.query(Vehicle).all()
    filtered = filter_accessible(vehicles)
    assert len(filtered) == 2


def test_estimate_profit(in_memory_repo):
    v = in_memory_repo.query(Vehicle).filter(Vehicle.name == 'Expensive Car').one()
    result = estimate_profit(v)
    assert result['estimate'] == 2800 - 2000 - 300


def test_availability_service_classify_status():
    class Dummy:
        observed_status = 'AvailableAndAccessible'
        junkyard = type('J', (), {'unlocked': True})()

    status = AvailabilityService.classify_status(Dummy())
    assert status == 'Available and accessible'


def test_purchase_affordability_and_shortfall(in_memory_repo):
    v = in_memory_repo.query(Vehicle).filter(Vehicle.name == 'Expensive Car').one()
    advice = PurchaseService.evaluate_purchase(v, current_cash=1500)
    assert advice.affordable is False
    assert advice.shortfall == 500


def test_purchase_affordability_when_cash_enough(in_memory_repo):
    v = in_memory_repo.query(Vehicle).filter(Vehicle.name == 'Cheap Car').one()
    advice = PurchaseService.evaluate_purchase(v, current_cash=200)
    assert advice.affordable is True
    assert advice.shortfall == 0
