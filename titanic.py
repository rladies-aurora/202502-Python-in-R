import pandas as pd

def read_titanic(file):
    # read the CSV file
    titanic = pd.read_csv(file)
    # filter rows with non-null age and fare
    titanic = titanic[['age', 'fare', 'survived']].dropna()
    return titanic

