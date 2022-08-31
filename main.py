import generators

test = generators.WeatherGen()
for i in range(60):
    next(test)


help(generators)

