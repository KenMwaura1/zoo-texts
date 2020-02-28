from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONNECTION_STRING = "sqlite+pysqlite:///texts.db"
TABLE_NAME = "texts"

engine = create_engine('sqlite:///main.db')
engine.connect()
Session = sessionmaker(bind=engine)

Base = declarative_base()
