from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, declared_attr, relationship


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Weather(Base):
    main_temperature = Column(Float, nullable=False)
    feel_temperature = Column(Float)
    humidity = Column(Integer)
    time = Column(DateTime, nullable=False, default=datetime.now)
    city_id = Column(Integer, ForeignKey('city.id'))


class City(Base):
    name = Column(String(168), unique=True, nullable=False)
    latitude = Column(Float, unique=True, nullable=False)
    longitude = Column(Float, unique=True, nullable=False)
    population = Column(Integer, nullable=False)
    weather = relationship(Weather, cascade='delete')
