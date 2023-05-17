from services.city import CityData
from services.weather import WeatherCol


if __name__ == '__main__':
    cities_list = CityData()
    cities_list.load_from_csv()

    col = WeatherCol()
    col.schedule_task()
