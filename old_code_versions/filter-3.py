import pandas as pd
import os
import re

def limpiar_numero_telefono(numero):
    # Eliminar todos los caracteres no numéricos
    numero_limpio = re.sub(r'\D', '', numero)
    print(numero_limpio)
    return numero_limpio

# Ruta de la carpeta que contiene los archivos de Excel
carpeta_excel = 'Paraguay/filtro-1'

# Lista para almacenar los datos únicos con el nombre del archivo
datos_unicos_con_archivo = []

# Iterar sobre cada archivo en la carpeta
for archivo in os.listdir(carpeta_excel):
    if archivo.endswith('.xlsx'):  # Asegúrate de que solo estás considerando archivos Excel
        # Leer el archivo Excel
        df = pd.read_excel(os.path.join(carpeta_excel, archivo))
        if (df.shape[0] > 1):
            # Añadir columna con el nombre del archivo
            df['NombreArchivo'] = archivo  
            datos_unicos_con_archivo.extend(df.astype(str).to_records(index=False))

# Crear un nuevo DataFrame con los datos únicos y el nombre del archivo
df_datos_unicos_con_archivo = pd.DataFrame.from_records(datos_unicos_con_archivo)

# Guardar el DataFrame con los datos únicos y el nombre del archivo en un nuevo archivo Excel
df_datos_unicos_con_archivo.to_excel(os.path.join(carpeta_excel, 'datos_unicos_con_archivo.xlsx'), index=False)

print(f'Se han eliminado los contactos duplicados. Puedes encontrar los datos únicos con el nombre del archivo en "datos_unicos_con_archivo.xlsx".')
