from app.core.database import Base, engine
from app.models import product, user

# Create all tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
