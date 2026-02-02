import pandas as pd

userAvgs = pd.read_csv("datasets/user_average_values.csv")

print(userAvgs.head())
print(userAvgs.info())

lifeExpectancy = pd.read_csv("datasets/life-expectancy.csv")

print(lifeExpectancy.head())
print(lifeExpectancy.info())

fintessHealth = pd.read_csv("datasets/health_fitness_dataset.csv")

print(fintessHealth.head())
print(fintessHealth.info())
