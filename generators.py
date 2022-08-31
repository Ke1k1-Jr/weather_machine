"""Weather Generator

This module allows the user to find the amount of water that will be created in a certain amount of time.

This file can also be imported as a module and contains the following classes:

    * WeatherGen - generates 'timestamp temperature dewpoint humidity barometric_pressure' values.
    * RainGen - using the WeatherGen attributes determines if rain will occur
"""

import random
import datetime
from collections import namedtuple


class WeatherGen:
    """
    A class used to generate values for weather

    ...

    Attributes
    ----------
    total_rain : int
        An int that represent total amount of rain
    WeatherObservation : namedtuple
        A namedtuple for 'timestamp temperature dewpoint humidity barometric_pressure'
    temp : float
        The temperature
    weather : namedtuple
        The current 'timestamp temperature dewpoint humidity barometric_pressure'

    Methods
    -------
    timestamp_gen()
        Adds five minutes to the current time and returns a datetime type

    temperature_gen()
        Returns a random float from the range of -3.8 to 1.6 which represents the current temperature


    dewpoint_gen()
        Returns an int that is 2 less than the current temperature

    humidity_gen()
        Returns a random int from the range of 40 to 100 incrementing by 10 that represents
        the current humidity percent

    barometricp_gen()
        Returns a random float from the range of 995.6 to 1009.1 which represent the barometric pressure
    """

    total_rain = 0

    def __init__(self):
        self.WeatherObservation = namedtuple('WeatherObservation',
                                             'timestamp temperature dewpoint humidity barometric_pressure')
        self.temp = self.temperature_gen()
        self.weather = self.WeatherObservation(datetime.datetime(2022, 1, 1, 0, 0, 0), self.temp,
                                               self.dewpoint_gen(), self.humidity_gen(), self.barometricp_gen())

    def __iter__(self):
        return self

    def __next__(self):
        """
        Checks if rain is possible and if so adds it to total_rain then prints the current
        weather then generates the next 5 minutes weather and saves it
        """
        rain_gen = RainGen(self.weather.humidity, self.weather.barometric_pressure)
        WeatherGen.total_rain += rain_gen.rain_amount()
        print(f"""Date: {self.weather.timestamp.strftime('%Y, %B, %A %I:%M%p')}
    Temperature: {self.weather.temperature}C
    Dewpoint: {self.weather.dewpoint}
    Humidity: {self.weather.humidity}%
    Barometric Pressure: {self.weather.barometric_pressure}
    Total Rain amount: {WeatherGen.total_rain}ml""", end='\n\n\n\n')
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
        returns a random float temperature between -3.8 and 1.6
        """
        return round(random.uniform(-3.8, 1.6), 1)

    def dewpoint_gen(self):
        """
        returns a float that is 2 less than the current temperature
        """
        return round(self.temp - 2)

    def humidity_gen(self):
        """
        returns an int from the range of 40 to 100 incremented by 10
        """
        return random.randrange(40, 100, 10)

    def barometricp_gen(self):
        """
        returns a random float from the range of 995.6 to 1009.1
        """
        return round(random.uniform(995.6, 1009.1), 1)


class RainGen:
    """
    A class used to determine if rain is possible

    ...

    Methods
    -------
    rain_amount()
        Returns the amount of rain depending on the current humidity and barometric pressure
    """

    def __init__(self, humidity, pressure):
        """
        Parameters
        ----------
        humidity : int
            The current humidity
        pressure : float
            The current barometric pressure
        """
        self.humidity = humidity
        self.pressure = pressure

    def rain_amount(self):
        """
        Returns the amount of rain depending on the current humidity and barometric pressure
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
