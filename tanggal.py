import pandas as pd
from tabulate import tabulate

def filter_transaksi_mei_2024():
    df = pd.read_csv('mutasi.csv')
    df['tanggal'] = pd.to_datetime(df['tanggal'])  # Konversi kolom 'tanggal' ke datetime
    
    # Filter untuk transaksi pada Mei 2024
    df_mei_2024 = df[(df['tanggal'].dt.year == 2024) & (df['tanggal'].dt.month == 5)]
    
    table = tabulate(df_mei_2024, headers='keys', tablefmt='pretty')
    print(table)

filter_transaksi_mei_2024()
