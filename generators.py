"""Weather Generator

This module allows the user to find the amount of snow that will be created on a certain date and time.

Contains the following classes:

    * WeatherGen - A class used to generate values for weather to determine how much snow is created
    * PrecipitationGen - using the WeatherGen attributes determines if precipitation will occur
"""

import random
import datetime
from collections import namedtuple


class WeatherGen:
    """
    A class used to generate values for weather to determine how much snow is created

    ...

    Attributes
    ----------
    total_snow : int
        An int that represent total amount of snow currently in meters
    WeatherObservation : namedtuple
        A namedtuple for 'timestamp temperature dewpoint humidity barometric_pressure'
    temp : int
        The temperature
    weather : namedtuple
        The current 'timestamp temperature dewpoint humidity barometric_pressure'

    Methods
    -------
    timestamp_gen()
        Adds five minutes to the current time and returns a datetime type

    temperature_gen()
        Returns a random int from the range of -8C to 3C which represents the current temperature


    dewpoint_gen()
        Returns an int that is 2 less than the current temperature

    humidity_gen()
        Returns a random int from the range of 40% to 100% incrementing by 10 that represents
        the current humidity percent

    barometricp_gen()
        Returns a random float from the range of 995.6 to 1009.1 which represent the barometric pressure

    add_snow(precipitation_amount)
        Returns the amount of water that would turn into snow and add it to the total_snow
    """

    total_snow = 0

    def __init__(self):
        self.WeatherObservation = namedtuple('WeatherObservation',
                                             'timestamp temperature dewpoint humidity barometric_pressure')
        self.temp = self.temperature_gen()
        self.weather = self.WeatherObservation(datetime.datetime(2022, 1, 1, 0, 0, 0), self.temp,
                                               self.dewpoint_gen(), self.humidity_gen(), self.barometricp_gen())

    def __next__(self):
        """
        Checks if precipitation is possible and if it is snow then it adds it to total_snow then prints the current
        weather then generates the next 5 minutes weather and saves it
        """
        precipitation_gen = PrecipitationGen(self.weather.humidity, self.weather.barometric_pressure, self.weather.temperature)
        if precipitation_gen.snow_or_rain() == "Snow":
            self.add_snow(precipitation_gen.precipitation_amount())
        print(f"""Date: {self.weather.timestamp.strftime('%Y, %B, %A %I:%M%p')}
    Temperature: {self.weather.temperature}C
    Dewpoint: {self.weather.dewpoint}
    Humidity: {self.weather.humidity}%
    Barometric pressure: {self.weather.barometric_pressure}
    Total snow amount: {round(WeatherGen.total_snow, 3)}meters""", end='\n\n\n\n')
        self.temp = self.temperature_gen()
        self.weather = self.WeatherObservation(self.timestamp_gen(), self.temp, self.dewpoint_gen(),
                                               self.humidity_gen(), self.barometricp_gen())

    def timestamp_gen(self):
        """
        adds 5 minutes to the current time and returns it as a datetime type
        """
        new_dt = self.weather.timestamp + datetime.timedelta(minutes=5)
        return new_dt

    def temperature_gen(self):
        """
        returns a random int temperature between -8C and 3C
        """
        return random.randint(-8, 3)

    def dewpoint_gen(self):
        """
        returns a float that is 2 less than the current temperature
        """
        return round(self.temp - 2)

    def humidity_gen(self):
        """
        returns an int from the range of 40% to 100% incremented by 10
        """
        return random.randrange(40, 100, 10)

    def barometricp_gen(self):
        """
        returns a random float from the range of 995.6 to 1009.1
        """
        return round(random.uniform(995.6, 1009.1), 1)

    def add_snow(self, precipitation_amount):
        """
        Depending on the temperature how much water turns into snow is multiplied by a certain number
        """
        if -1 >= self.temp >= -3:
            WeatherGen.total_snow += precipitation_amount * 0.01
        if -4 >= self.temp >= -6:
            WeatherGen.total_snow += precipitation_amount * 0.015
        else:
            WeatherGen.total_snow += precipitation_amount * 0.02

class PrecipitationGen:
    """
    A class used to determine if precipitation is possible and whether it is snow or rain
    ...

    Methods
    -------
    precipitation_amount()
        Returns the amount of precipitation depending on the current humidity and barometric pressure

    snow_or_rain()
        If the temperature is below 0C then the precipitation is snow otherwise it is rain
    """

    def __init__(self, humidity, pressure, temperature):
        """
        Parameters
        ----------
        humidity : int
            The current humidity
        pressure : float
            The current barometric pressure
        temp: int
            The current temperature
        """
        self.humidity = humidity
        self.pressure = pressure
        self.temp = temperature

    def precipitation_amount(self):
        """
        Returns the amount of precipitation depending on the current humidity and barometric pressure
        """
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
        """
        If the temperature is below 0C then the precipitation is snow otherwise it is rain
        """
        if self.temp < 0:
            return "Snow"
        else:
            return "Rain"