from Homevee.APIModule import APIModule
from Homevee.Item.Status import *
from Homevee.Manager.WeatherManager import WeatherManager

ACTION_KEY_GET_WEATHER = "getweather"
ACTION_KEY_GET_WEATHER_CITY_LIST = "getweathercitylist"
ACTION_KEY_SET_WEATHER_CITY_ID = "setweathercityid"

class WeatherAPIModule(APIModule):
    def __init__(self):
        super(WeatherAPIModule, self).__init__()
        self.weather_manager = WeatherManager()
        return

    def get_function_mappings(self):
        mappings = {
            ACTION_KEY_GET_WEATHER: self.get_weather,
            ACTION_KEY_GET_WEATHER_CITY_LIST: self.get_weather_city_list,
            ACTION_KEY_SET_WEATHER_CITY_ID: self.set_weather_city_id
        }

        return mappings

    def get_weather(self, user, request, db):
        data = self.weather_manager.get_weather(int(request['daycount']), db)
        return Status(type=STATUS_OK, data={'weather':data})

    def get_weather_city_list(self, user, request, db):
        data = self.weather_manager.get_weather_city_list(db)
        return Status(type=STATUS_OK, data=data)

    def set_weather_city_id(self, user, request, db):
        data = self.weather_manager.set_weather_city_id(user, request['id'], db)
        return Status(type=STATUS_OK, data=data)