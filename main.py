from app.services.city import CityData
from app.services.weather import WeatherCol


if __name__ == '__main__':
    cities_list = CityData()
    cities_list.load_from_csv()

    col = WeatherCol()
    col.collect_weather()
    col.schedule_task()
