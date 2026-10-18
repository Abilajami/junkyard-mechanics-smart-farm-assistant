from src.database import init_db, Repository
from datetime import datetime

def seed_data(repo: Repository):
    # Add a few manual seed vehicles. These are NOT verified live game data.
    repo.seed_sample()
    # Additional manual seeds
    try:
        repo.add_vehicle(
            name='Rusty Cruiser',
            tier='2',
            category='Coupe',
            purchase_price=500,
            resale_price=800,
            repair_cost=150,
            junkyard_location='Boneyard',
            availability_status='RecordedAvailable',
            collection_status='Wanted',
            data_source='Manual Seed',
            last_verified=datetime.utcnow(),
            notes='Seeded vehicle - replace with verified source when available.'
        )
    except Exception:
        pass
