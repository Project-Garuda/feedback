from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
def create_engine_models():
    print('Hello')
    DATABASE_URI = 'mysql+pymysql://shravan:kvshravan1@@localhost:3306/college'
    engine = create_engine(DATABASE_URI,echo = True)
    Base.metadata.create_all(engine)
from project.mod_student import models
from project.mod_faculty import models
create_engine_models()
