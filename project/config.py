from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

DATABASE_URI = 'mysql+pymysql://shravan:kvshravan1@@localhost:3306/college'
engine = create_engine(DATABASE_URI,echo = True)
Base.metadata.create_all(engine)
