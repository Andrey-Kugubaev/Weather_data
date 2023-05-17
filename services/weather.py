import logging
import requests
from schedule import every, run_pending
import time
import os

from pydantic import ValidationError
import sentry_sdk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constant import api_key, base_url, db_path, si_value, sentry_dsn
from db import Base, City, Weather
from schemas import WeatherDataCreate


sentry_sdk.init(
     dsn=sentry_dsn,
     traces_sample_rate=1,
)


class WeatherCol:
    def __init__(self):
        self.apy_key = api_key
        self.base_url = base_url
        self.engine = create_engine(db_path)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_weather_data(self, lat: float, lon: float) -> dict:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.apy_key,
            'units': si_value
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def save_weather_data(
            self,
            weather_data: WeatherDataCreate,
            city_id: int
    ):
        session = self.Session()
        weather = Weather(
            main_temperature=weather_data.main_temperature,
            feel_temperature=weather_data.feel_temperature,
            humidity=weather_data.humidity,
            city_id=city_id
        )
        session.add(weather)
        session.commit()
        session.close()

    def collect_weather(self):
        session = self.Session()
        cities = session.query(City).all()
        session.close()

        for city in cities:
            weather_data = self.get_weather_data(
                city.latitude, city.longitude
            )
            data = {
                'main_temperature': weather_data['main']['temp'],
                'feel_temperature': weather_data['main']['feels_like'],
                'humidity': weather_data['main']['humidity']
            }
            log_path = os.path.join("..", "valid_logs.log")
            logging.basicConfig(
                level=logging.INFO,
                filename=log_path,
                format='%(asctime)s %(levelname)s %(message)s'
            )
            try:
                validated_data = WeatherDataCreate(**data)
                self.save_weather_data(validated_data, city.id)
                logging.info(
                    f'The weather for the {city.name} '
                    f'was successfully recorded.'
                )
                sentry_sdk.capture_message(
                    f'The weather for the {city.name} '
                    f'was successfully recorded.'
                )
            except ValidationError:
                logging.info('Incorrect weather data')

    def schedule_task(self):
        every().hour.do(self.collect_weather)
        while True:
            run_pending()
            time.sleep(1)
