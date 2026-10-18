from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    tier = Column(String, nullable=True)
    category = Column(String, nullable=True)
    purchase_price = Column(Integer, nullable=True)
    resale_price = Column(Integer, nullable=True)
    repair_cost = Column(Integer, nullable=True)
    junkyard_location = Column(String, nullable=True)
    availability_status = Column(String, nullable=True)
    collection_status = Column(String, nullable=True)
    data_source = Column(Text, nullable=True)
    last_verified = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tier': self.tier or 'Unknown',
            'category': self.category or 'Unknown',
            'purchase_price': self.purchase_price or 'Unknown',
            'resale_price': self.resale_price or 'Unknown',
            'repair_cost': self.repair_cost or 'Unknown',
            'junkyard_location': self.junkyard_location or 'Unknown',
            'availability_status': self.availability_status or 'Unknown',
            'collection_status': self.collection_status or 'Unknown',
            'data_source': self.data_source or 'Unknown',
            'last_verified': self.last_verified.isoformat() if self.last_verified else 'Unknown',
            'notes': self.notes or ''
        }

class Junkyard(Base):
    __tablename__ = 'junkyards'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    unlocked = Column(Boolean, default=False)
    last_checked = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    availability_records = relationship('AvailabilityRecord', back_populates='junkyard')

class AvailabilityRecord(Base):
    __tablename__ = 'availability_records'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    junkyard_id = Column(Integer, ForeignKey('junkyards.id'))
    observed_price = Column(Integer, nullable=True)
    tier_observed = Column(String, nullable=True)
    observed_time = Column(DateTime, default=datetime.utcnow)
    observed_status = Column(String, nullable=True)
    purchased_flag = Column(Boolean, default=False)
    observer_notes = Column(Text, nullable=True)

    vehicle = relationship('Vehicle')
    junkyard = relationship('Junkyard', back_populates='availability_records')

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    start_cash = Column(Integer, nullable=True)
    end_cash = Column(Integer, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    cars_purchased = Column(JSON, nullable=True)
    cars_sold = Column(JSON, nullable=True)
    total_revenue = Column(Integer, nullable=True)
    total_expenses = Column(Integer, nullable=True)
    net_profit = Column(Integer, nullable=True)
    avg_earnings_per_minute = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PartNote(Base):
    __tablename__ = 'part_notes'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=True)
    junkyard_id = Column(Integer, ForeignKey('junkyards.id'), nullable=True)
    part_name = Column(String, nullable=False)
    observed_damage = Column(Text, nullable=True)
    quantity = Column(Integer, default=1)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = 'recommendations'
    id = Column(Integer, primary_key=True)
    user_context = Column(JSON, nullable=True)
    candidates = Column(JSON, nullable=True)
    chosen_strategy = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
