import pandas as pd

# Ruta de la carpeta que contiene los archivos de Excel
excel = 'Paraguay/numeros_limpios.xlsx'

df = pd.read_excel(excel)

df = df.drop_duplicates(subset=3, keep="first")

df.to_excel('sin_duplicados.xlsx', index=False)
