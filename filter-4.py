import pandas as pd
import os
import re 

def limpiar_numero_telefono(numero):
    # Eliminar todos los caracteres no numéricos
    numero_limpio = re.sub(r'\D', '', numero)

    return numero_limpio

# Ruta de la carpeta que contiene los archivos de Excel
excel = 'Paraguay/datos_unicos_con_archivo.xlsx'

df = pd.read_excel(excel)

df[3] = df[3].apply(limpiar_numero_telefono)

df.to_excel('numeros_limpios.xlsx', index=False)

print(f'Se han eliminado los contactos duplicados. Puedes encontrar los datos únicos con el nombre del archivo en "datos_unicos_con_archivo.xlsx".')
