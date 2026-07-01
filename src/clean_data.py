from sqlalchemy import create_engine

# Pandas connection string pointing to your local Postgres instance
engine = create_engine("postgresql://postgres:postgres@localhost:5432/bootcamp")