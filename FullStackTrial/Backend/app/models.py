from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    location = Column(Text, nullable=False)  # Changed profession to location to match the API

    # A doctor can take care of many animals
    animals = relationship('Animal', back_populates='doctor')

class Animal(Base):
    __tablename__ = 'animals'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    a_type = Column(Text, nullable=False)  # Changed a_type to type to match the API
    doctor_id = Column(Integer, ForeignKey('doctors.id'))  # Foreign key to Doctor
    
    # Relationship back to the doctor
    doctor = relationship('Doctor', back_populates='animals')
    
    # An animal can have one owner
    owner_id = Column(Integer, ForeignKey('owners.id'))  # Foreign key to Owner
    owner = relationship('Owner', back_populates='animals')

class Owner(Base):
    __tablename__ = 'owners'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    phone_number = Column(Integer, nullable=False, unique=True)
    location = Column(Text, nullable=False)
    
    # An owner can have many animals
    animals = relationship('Animal', back_populates='owner')
