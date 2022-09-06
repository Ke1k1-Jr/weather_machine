import random
import datetime
from collections import namedtuple


class WeatherObservation:
    def __init__(self, timestamp):
        self.WeatherObservation = namedtuple('WeatherObservation',
                                             'timestamp temperature dewpoint humidity barometric_pressure')
        self.temp = self.temperature_gen()
        self.curr_weather = self.WeatherObservation(timestamp, self.temp,
                                                    self.dewpoint_gen(), self.humidity_gen(), self.barometricp_gen())

    def temperature_gen(self):
        return random.randint(-8, 2)

    def dewpoint_gen(self):
        return round(self.temp - 2)

    def humidity_gen(self):
        return random.randrange(70, 110, 10)

    def barometricp_gen(self):
        return round(random.uniform(995.6, 1009.1), 1)


class Weather:
    total_snow = 0.0

    def __init__(self, user_weather_observation=False, user_precipitation_gen=False):
        self.get_start_date()
        self.interval_period = int(input("Interval period: "))
        self.user_WeatherObservation = user_weather_observation
        self.user_PrecipitationGen = user_precipitation_gen
        if self.user_WeatherObservation:
            self.weather = self.user_WeatherObservation(self.start_date)
        else:
            self.weather = WeatherObservation(self.start_date)
        self.__next__()
        self.date_after_duration = self.weather.curr_weather.timestamp + datetime.timedelta(minutes=self.interval_period)
        print(f"""\n\nDate: {self.date_after_duration.strftime('%Y, %B, %d %I:%M%p')}
                    Temperature: {self.weather.curr_weather.temperature}C
                    Dewpoint: {self.weather.curr_weather.dewpoint}
                    Humidity: {self.weather.curr_weather.humidity}%
                    Barometric pressure: {self.weather.curr_weather.barometric_pressure}
                    Total snow amount: {round(Weather.total_snow, 3)} meters""")
        WeatherMeasurement(self.weather, self.precipitation_gen)

    def __next__(self):
        if self.user_PrecipitationGen:
            self.precipitation_gen = self.user_PrecipitationGen(self.weather, self.interval_period)
        else:
            self.precipitation_gen = PrecipitationGen(self.weather, self.interval_period)

        if self.precipitation_gen.snow_or_rain() == "Snow":
            self.add_snow(self.precipitation_gen.precipitation_amount())
        if self.precipitation_gen.snow_or_rain() == "Rain":
            Weather.total_snow -= self.precipitation_gen.precipitation_amount()

        if self.weather.curr_weather.temperature > 0:
            self.snow_melt_temp()
        if Weather.total_snow < 0:
            Weather.total_snow = 0

    def get_start_date(self):
        self.year = int(input("Enter a target year (YYYY): "))
        self.month = int(input("Enter a target month (MM): "))
        self.day = int(input("Enter a target day (DD): "))
        self.hour = int(input("Enter a target hour (HH): "))
        self.min = int(input("Enter a target minute (MM): "))
        self.start_date = datetime.datetime(self.year, self.month, self.day, self.hour, self.min, 0)

    def add_snow(self, precipitation_amount):
        if -1 >= self.weather.curr_weather.temperature >= -3:
            Weather.total_snow += precipitation_amount * .05
        if -4 >= self.weather.curr_weather.temperature >= -6:
            Weather.total_snow += precipitation_amount * .2
        else:
            Weather.total_snow += precipitation_amount * .5

    def snow_melt_temp(self):
        if self.weather.curr_weather.temperature == 1:
            return 0.05
        elif self.weather.curr_weather.temperature == 2:
            return 0.1
        elif self.weather.curr_weather.temperature == 3:
            return 0.15
        else:
            return 0


class PrecipitationGen:
    def __init__(self, weather_observation, interval_period):
        self.humidity = weather_observation.curr_weather.humidity
        self.pressure = weather_observation.curr_weather.barometric_pressure
        self.temp = weather_observation.curr_weather.temperature
        self.duration = interval_period

    def precipitation_amount(self):
        if self.humidity == 100:
            if 1009.1 > self.pressure > 1005.8:
                return 1 * self.duration
            elif 1005.8 > self.pressure > 1002.4:
                return 2 * self.duration
            elif 1002.4 > self.pressure > 999.0:
                return 3 * self.duration
            elif 999.0 > self.pressure > 995.6:
                return 4 * self.duration
        elif self.humidity == 90:
            if 1005.8 > self.pressure > 1002.4:
                return 1 * self.duration
            elif 1002.4 > self.pressure > 999.0:
                return 2 * self.duration
            elif 999.0 > self.pressure > 995.6:
                return 3 * self.duration
        elif self.humidity == 80:
            if 1002.4 > self.pressure > 999.0:
                return 1 * self.duration
            elif 999.0 > self.pressure > 995.6:
                return 2 * self.duration
        elif self.humidity == 70:
            if 999.0 > self.pressure > 995.6:
                return 1 * self.duration
        return 0

    def snow_or_rain(self):
        if self.temp <= 0:
            return "Snow"
        else:
            return "Rain"

class WeatherMeasurement:
    collection_of_weather = []
    def __init__(self, weather_observation, precipitation):
        WeatherMeasurement.collection_of_weather.append((weather_observation, precipitation))