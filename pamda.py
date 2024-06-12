import pandas as pd
from tabulate import tabulate

def mutasi():
    df = pd.read_csv('mutasi.csv')
    table = tabulate(df, headers='keys', tablefmt='pretty')
    print(table)

mutasi()
