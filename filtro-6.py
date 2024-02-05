
# este filtro se asegura que solo queden numeros paraguayos
# se puede cambiar la funcion para que filtre numeros de otra nacionalidad
#
# NOTA: Antes de procesar los datos castear a tipo string la columna de los telefonos

import phonenumbers
import pandas as pd

def es_numero_paraguayo(numero_telefono):
    try:
        # Parsear el número de teléfono
        numero_parsed = phonenumbers.parse(numero_telefono, "PY")

        # Verificar si el número es válido y si pertenece a Paraguay
        return phonenumbers.is_valid_number(numero_parsed) and phonenumbers.region_code_for_number(numero_parsed) == "PY"

    except phonenumbers.NumberParseException:
        # Manejar excepciones si el número no se puede analizar
        return False
    
excel = 'Paraguay/numeros_limpios.xlsx'

df = pd.read_excel(excel)

df[3] = df[3].astype(str)

df_nuevo = pd.DataFrame(columns=df.columns)

print(f' long dataset original {df.shape[0]}')

for indice, valor in enumerate(df[3]):
    if not es_numero_paraguayo(valor):
        df = df.drop(indice)

print(f' long dataset original {df.shape[0]}')

df.to_excel('solo_paraguay.xlsx', index=False)
