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
        return random.randint(-8, 3)

    def dewpoint_gen(self):
        return round(self.temp - 2)

    def humidity_gen(self):
        return random.randrange(40, 100, 10)

    def barometricp_gen(self):
        return round(random.uniform(995.6, 1009.1), 1)


class WeatherGen:
    total_snow = 0

    def __init__(self):
        self.get_target_date()
        self.weather = WeatherObservation(datetime.datetime.now())
        while self.weather.curr_weather.timestamp <= self.target_date:
            print(f"""\n\nDate: {self.weather.curr_weather.timestamp.strftime('%Y, %B, %d %I:%M%p')}
                        Temperature: {self.weather.curr_weather.temperature}C
                        Dewpoint: {self.weather.curr_weather.dewpoint}
                        Humidity: {self.weather.curr_weather.humidity}%
                        Barometric pressure: {self.weather.curr_weather.barometric_pressure}
                        Total snow amount: {round(WeatherGen.total_snow, 3)} meters""")
            self.__next__()
            print(f"""\n\nDate: {self.weather.curr_weather.timestamp.strftime('%Y, %B, %d %I:%M%p')}
                        Temperature: {self.weather.curr_weather.temperature}C
                        Dewpoint: {self.weather.curr_weather.dewpoint}
                        Humidity: {self.weather.curr_weather.humidity}%
                        Barometric pressure: {self.weather.curr_weather.barometric_pressure}
                        Total snow amount: {round(WeatherGen.total_snow, 3)} meters""")

    def __next__(self):

        precipitation_gen = PrecipitationGen(self.weather.curr_weather.humidity,
                                             self.weather.curr_weather.barometric_pressure,
                                             self.weather.curr_weather.temperature)
        if precipitation_gen.snow_or_rain() == "Snow":
            self.add_snow(precipitation_gen.precipitation_amount())
        if precipitation_gen.snow_or_rain() == "Rain":
            WeatherGen.total_snow -= precipitation_gen.precipitation_amount()
        if self.weather.curr_weather.temperature > 0:
            self.snow_melt_temp()
        if WeatherGen.total_snow < 0:
            WeatherGen.total_snow = 0
        self.weather = WeatherObservation(self.weather.curr_weather.timestamp + datetime.timedelta(minutes=5))

    def get_target_date(self):
        self.year = int(input("Enter a target year (YYYY): "))
        self.month = int(input("Enter a target month (MM): "))
        self.day = int(input("Enter a target day (DD): "))
        self.hour = int(input("Enter a target hour (HH): "))
        self.min = int(input("Enter a target minute (MM): "))
        self.target_date = datetime.datetime(self.year, self.month, self.day, self.hour, self.min, 0)

    def add_snow(self, precipitation_amount):
        if -1 >= self.weather.curr_weather.temperature >= -3:
            WeatherGen.total_snow += precipitation_amount * .05
        if -4 >= self.weather.curr_weather.temperature >= -6:
            WeatherGen.total_snow += precipitation_amount * .2
        else:
            WeatherGen.total_snow += precipitation_amount * .5

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
    def __init__(self, humidity, pressure, temperature):
        self.humidity = humidity
        self.pressure = pressure
        self.temp = temperature

    def precipitation_amount(self):
        if self.humidity == 100:
            if 1009.1 > self.pressure > 1005.8:
                return 1
            elif 1005.8 > self.pressure > 1002.4:
                return 2
            elif 1002.4 > self.pressure > 999.0:
                return 3
            elif 999.0 > self.pressure > 995.6:
                return 4
        elif self.humidity == 90:
            if 1005.8 > self.pressure > 1002.4:
                return 1
            elif 1002.4 > self.pressure > 999.0:
                return 2
            elif 999.0 > self.pressure > 995.6:
                return 3
        elif self.humidity == 80:
            if 1002.4 > self.pressure > 999.0:
                return 1
            elif 999.0 > self.pressure > 995.6:
                return 2
        elif self.humidity == 70:
            if 999.0 > self.pressure > 995.6:
                return 1
        return 0

    def snow_or_rain(self):
        if self.temp < 0:
            return "Snow"
        else:
            return "Rain"
