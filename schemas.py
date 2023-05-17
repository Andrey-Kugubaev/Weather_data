from pydantic import BaseModel, Field, PositiveInt


class CityListCreate(BaseModel):
    name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    population: PositiveInt = Field(None)


class WeatherDataCreate(BaseModel):
    main_temperature: float = Field(gt=-100, le=100)
    feel_temperature: float = Field(None, gt=-100, le=100)
    humidity: int = Field(None)
