from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_url='sqlite:///peoplepulse.db'
engine=create_engine(db_url)
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)