import generators

test = generators.WeatherGen()
for i in range(100):
    next(test)


# help(generators)

