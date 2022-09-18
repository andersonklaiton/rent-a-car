from sqlalchemy import Column, Integer, String

from app.configs.database import db

class States(db.Model):
    state_id:int
    name:str

    __tablename__ = 'tb_states'

    state_id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False, unique = True)