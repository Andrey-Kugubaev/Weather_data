import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constant import db_path, DATAFILE
from db import Base, City
from schemas import CityListCreate


class CityData:
    def __init__(self):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_cities(self, city: CityListCreate):
        session = self.Session()
        existing_city = session.query(City).filter_by(name=city.name).first()
        if existing_city:
            session.close()
            return

        city_data = City(
            name=city.name,
            latitude=city.latitude,
            longitude=city.longitude,
            population=city.population
        )
        session.add(city_data)
        session.commit()
        session.close()

    def load_from_csv(self):
        with open(DATAFILE, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city = CityListCreate(**row)
                self.add_cities(city)
