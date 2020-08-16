import os

from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
database = Database(DATABASE_URL)
