from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
DATABASE_URI = 'mysql+pymysql://shravan:kvshravan1@@localhost:3306/college'
engine = create_engine(DATABASE_URI,echo = True)
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

def create_engine_models():
    Base.metadata.create_all(engine)

from project.mod_student import models
from project.mod_faculty import models
create_engine_models()
from project.mod_student import controllers
