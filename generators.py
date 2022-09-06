import random
import datetime
from collections import namedtuple


class WeatherObservation:
    """
    A class used to generate values for weather

    ...

    Attributes
    ----------
    WeatherObservation : namedtuple
        A named tuple that consists of timestamp, temperature, humidity, and barometric_pressure
    temp : int
        A value that represents temperature that is between -8C and 2
    curr_weather : WeatherObservation
        A WeatherObservation object that represents the current weather

    Methods
    -------
    temperature_gen:
        Returns an int from -8 to 2
    humidity_gen:
        Returns a random int from the range of 70 to 110 incrementing by 10
    barometricp_gen:
        Returns a random float from the range of 995.6 to 1009.1
    """

    def __init__(self, timestamp: datetime):
        """
        Parameters
        ----------
        timestamp : datetime
            The date of the start of the forecast
        """
        self.WeatherObservation = namedtuple('WeatherObservation',
                                             'timestamp temperature humidity barometric_pressure')
        self.temp = self.temperature_gen()
        self.curr_weather = self.WeatherObservation(timestamp, self.temp, self.humidity_gen(), self.barometricp_gen())

    def temperature_gen(self):
        """
        Returns a random integer from -8 to 2 that represents the
        current temperature in celcius
        """
        return random.randint(-8, 2)

    def humidity_gen(self):
        """
        Returns a random integer from the range of 70 to 110 incrementing by 10
        that represents the current humidity level
        """
        return random.randrange(70, 110, 10)

    def barometricp_gen(self):
        """
        Returns a random float from the range of 995.6 to 1009.1 that represents
        the current barometric pressure
        """
        return round(random.uniform(995.6, 1009.1), 1)


class Weather:
    """
    A class that uses the WeatherObservation, PrecipitationGen, and WeatherMeasurement
    classes to calculate the total amount of snow and store that data

    ...

    Attributes
    ----------
    year : int
        The year
    month : int
        The month
    day : int
        The day
    hour : int
        The hour
    minute : int
        The minute
    start_date : datetime
        The date the forecast starts from
    duration : int
        The duration of the forecast
    user_WeatherObservation : WeatherObservation
        The users WeatherObservation object (defaults to False)
    user_PrecipitationGen : PrecipitationGen
        The users PrecipitationGen object (defaults to False)
    weather : WeatherObservation
        The current WeatherObservation object
    date_after_duration : datetime
        The new date after the duration has been added to the start_date

    Methods
    -------
    get_start_date:
        Returns a datetime object which represent the first date of the forecast
    add_snow:
        Depending on the temperature adds new snow amount to total_snow
    snow_melt:
        Depending on the temperature subtract from total_snow
    """
    total_snow = 0.0

    def __init__(self, user_weather_observation=False, user_precipitation_gen=False):
        """
        Parameters
        ----------
        user_WeatherObservation : WeatherObservation, optional
            The users WeatherObservation object (defaults to False)
        user_PrecipitationGen : PrecipitationGen, optional
            The users PrecipitationGen object (defaults to False)
        """
        self.get_start_date()
        self.duration = int(input("Duration: "))
        self.user_WeatherObservation = user_weather_observation
        self.user_PrecipitationGen = user_precipitation_gen
        if self.user_WeatherObservation:
            self.weather = self.user_WeatherObservation(self.start_date)
        else:
            self.weather = WeatherObservation(self.start_date)
        self.__next__()
        self.date_after_duration = self.weather.curr_weather.timestamp + datetime.timedelta(minutes=self.duration)
        print(f"""\n\nDate: {self.date_after_duration.strftime('%Y, %B, %d %I:%M%p')}
                    Temperature: {self.weather.curr_weather.temperature}C
                    Humidity: {self.weather.curr_weather.humidity}%
                    Barometric pressure: {self.weather.curr_weather.barometric_pressure}
                    Total snow amount: {round(Weather.total_snow, 3)} meters""")
        WeatherMeasurement(self.weather, self.precipitation_gen)

    def __next__(self):
        if self.user_PrecipitationGen:
            self.precipitation_gen = self.user_PrecipitationGen(self.weather, self.duration)
        else:
            self.precipitation_gen = PrecipitationGen(self.weather, self.duration)

        if self.precipitation_gen.snow_or_rain() == "Snow":
            self.add_snow(self.precipitation_gen.precipitation_amount())
        if self.precipitation_gen.snow_or_rain() == "Rain":
            Weather.total_snow -= self.precipitation_gen.precipitation_amount()

        if self.weather.curr_weather.temperature > 0:
            self.snow_melt()
        if Weather.total_snow < 0:
            Weather.total_snow = 0.0

    def get_start_date(self):
        """
        Gets user input to create a datetime object that represents the first
        date of the forecast

        Raises
        ------
        ValueError
            If the user enters something else than an int or an int
            that does not fit a date
        """
        self.year = int(input("Enter a target year (YYYY): "))
        self.month = int(input("Enter a target month (MM): "))
        self.day = int(input("Enter a target day (DD): "))
        self.hour = int(input("Enter a target hour (HH): "))
        self.min = int(input("Enter a target minute (MM): "))
        self.start_date = datetime.datetime(self.year, self.month, self.day, self.hour, self.min, 0)

    def add_snow(self, precipitation_amount: float):
        """
        Adds the amount of snow accumulated using the precipitation amount and
        the temperature

        Parameters
        ----------
        precipitation_amount : int
            The amount of precipitation
        """
        if -1 >= self.weather.curr_weather.temperature >= -3:
            Weather.total_snow += precipitation_amount * .05
        if -4 >= self.weather.curr_weather.temperature >= -6:
            Weather.total_snow += precipitation_amount * .2
        else:
            Weather.total_snow += precipitation_amount * .5

    def snow_melt(self):
        """
        Returns the amount of snow that will be lost depending on the temperature
        """
        if self.weather.curr_weather.temperature == 1:
            return 0.05
        elif self.weather.curr_weather.temperature == 2:
            return 0.1
        elif self.weather.curr_weather.temperature == 3:
            return 0.15
        else:
            return 0


class PrecipitationGen:
    """
    A class used to generate values for weather

    ...

    Attributes
   ----------
   humidity : int
       Represents the current humidity level
   pressure : float
       Represents the current barometric pressure
   temp : int
       Represents the current temperature
   duration : int
       Represents the duration of the precipitation

   Methods
   -------
   precipitation_amount:
       Returns the precipitation amount depending on the humidity and pressure
   snow_or_rain:
       Returns "Snow" if the temperature is less than or equal to 0 otherwise returns "False"
   """

    def __init__(self, weather_observation, duration):
        self.humidity = weather_observation.curr_weather.humidity
        self.pressure = weather_observation.curr_weather.barometric_pressure
        self.temp = weather_observation.curr_weather.temperature
        self.duration = duration

    def precipitation_amount(self) -> float:
        if self.humidity == 100:
            if 1009.1 > self.pressure > 1005.8:
                return float(1 * self.duration)
            elif 1005.8 > self.pressure > 1002.4:
                return float(2 * self.duration)
            elif 1002.4 > self.pressure > 999.0:
                return float(3 * self.duration)
            elif 999.0 > self.pressure > 995.6:
                return float(4 * self.duration)
        elif self.humidity == 90:
            if 1005.8 > self.pressure > 1002.4:
                return float(1 * self.duration)
            elif 1002.4 > self.pressure > 999.0:
                return float(2 * self.duration)
            elif 999.0 > self.pressure > 995.6:
                return float(3 * self.duration)
        elif self.humidity == 80:
            if 1002.4 > self.pressure > 999.0:
                return float(1 * self.duration)
            elif 999.0 > self.pressure > 995.6:
                return float(2 * self.duration)
        elif self.humidity == 70:
            if 999.0 > self.pressure > 995.6:
                return float(1 * self.duration)
        return 0.0

    def snow_or_rain(self) -> str:
        if self.temp <= 0:
            return "Snow"
        else:
            return "Rain"


class WeatherMeasurement:
    """
    A class used to store WeatherObservation and PrecipitationGen objects

    ...

    Attributes
   ----------
   collection_of_weather: list
       A list of WeatherObservation and PrecipitationGen objects tuples
   """
    collection_of_weather = []

    def __init__(self, weather_observation, precipitation):
        WeatherMeasurement.collection_of_weather.append((weather_observation, precipitation))
