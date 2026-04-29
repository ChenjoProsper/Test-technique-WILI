from sqlalchemy import Column, Integer, String
from database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    signe_nom = Column(String, unique=True) # Lien par le nom du signe
    texte = Column(String)