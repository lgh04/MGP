from db import Base, engine
from models.bill import Bill

Base.metadata.create_all(bind=engine)